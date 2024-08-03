// Zaman damgası dönüşümü için yardımcı fonksiyon
function convertToComparableTimestamp(value) {
  if (value instanceof Date) {
    return value.getTime();
  } else if (typeof value === 'string') {
    return new Date(value).getTime();
  }
  return value;
}

// Değerleri karşılaştırma fonksiyonu
function hasChanges(oldRow, newData, fields, datetimeFieldNames) {
  for (var i = 0; i < newData.length; i++) {
    var oldVal = oldRow[i];
    var newVal = newData[i];

    if (datetimeFieldNames.includes(fields[i])) {
      oldVal = convertToComparableTimestamp(oldVal);
      newVal = convertToComparableTimestamp(newVal);
    }

    if (oldVal !== newVal) {
      return true;
    }
  }
  return false;
}

function writeLatestEventToSheet() {
  // JDBC bağlantı bilgileri
  var properties = PropertiesService.getScriptProperties();
  var serverUrl = properties.getProperty('DB_URL');
  var user = properties.getProperty('DB_USER');
  var userPwd = properties.getProperty('DB_PASSWORD');
  var conn;

  conn = Jdbc.getConnection(serverUrl, user, userPwd);

  // .................. Configurtaion Area Starts ................... //

  var appointmentsTable = 'appointments';
  var basvuruTable = 'form_basvuru';
  var applicationPeriodFieldName = 'BasvuruDonemi';
  // Alanları tanımla
  var fields = ['ZamanDamgasi', 'EtkinlikID', 'MulakatZamani', 'MentorAdi', 'MentorSoyadi', 'MentorMail', 'Summary', 'Description', 'Location', 'OnlineMeetingLink', 'ResponseStatus'];
  var unique_key = 'EtkinlikID';
  var datetimeFieldNames = ['ZamanDamgasi', 'MulakatZamani'];
  var ownerOfTheCalendarMail = 'creator@mail.com';
  var usedCalendarId = 'YOUR_CALENDAR_ID_HERE';

  // .................. Configurtaion Area Ends  .................... //

  // calendarId, etkinliklerin alınacağı takvimi belirtir.
  // 'primary', kullanıcının birincil takvimini ifade eder. Alternatif olarak, belirli bir takvimin kimliği (örneğin, bir takvim URL'si) kullanılabilir.
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var calendarId = usedCalendarId; // 'primary'; // OR ownerOfTheCalendarMail;
  var now = new Date();

  // Son basvuru doneminin adini al
  var queryLastApplicationPeriod = 'SELECT ' + applicationPeriodFieldName + ' ' +'FROM ' + basvuruTable + ' ' +'ORDER BY CAST(SUBSTRING(' + applicationPeriodFieldName + ', 4) AS UNSIGNED) DESC ' + 'LIMIT 1';
  var stmtLastApplicationPeriod = conn.createStatement();
  var resultLastApplicationPeriod = stmtLastApplicationPeriod.executeQuery(queryLastApplicationPeriod);
  var lastApplicationPeriod = null;
  if (resultLastApplicationPeriod.next()) {
    lastApplicationPeriod = resultLastApplicationPeriod.getString(applicationPeriodFieldName);
  }
  
  
  // form_basvuru tablosundan en son BaşvuruDönemi içindeki ilk kaydın oluşturulduğu zamanı al
  var queryLastApplicationPeriodStartDate = ('SELECT MIN('+datetimeFieldNames[0]+') FROM '+basvuruTable+' WHERE '+applicationPeriodFieldName+' = (SELECT '+applicationPeriodFieldName+' FROM '+basvuruTable+' ORDER BY CAST(SUBSTRING('+applicationPeriodFieldName+', 4) AS UNSIGNED) DESC LIMIT 1)');
  var stmtLastApplicationPeriodStartDate = conn.createStatement();
  var resultLastApplicationPeriodStartDate = stmtLastApplicationPeriodStartDate.executeQuery(queryLastApplicationPeriodStartDate);
  var lastApplicationPeriodStartDate = null;
  
  if (resultLastApplicationPeriodStartDate.next()) {
    lastApplicationPeriodStartDate = new Date(resultLastApplicationPeriodStartDate.getTimestamp(1).getTime());
  }
  Logger.log('Son başvuru dönemi için başlangıç tarihi: ' + lastApplicationPeriodStartDate);
  
  // Son basvuru donemi basladiktan sonraki tüm etkinlikleri al
  var events = Calendar.Events.list(calendarId, {
    timeMin: lastApplicationPeriodStartDate.toISOString(),
    orderBy: 'startTime',
    singleEvents: true,
    maxResults: 2500
  });
  
  var currentEventIds = new Set(events.items.map(event => event.id));
  var sheetData = sheet.getDataRange().getValues();
  var header = sheetData.shift(); // Başlık satırını ayır
  
  // Sheet'teki verileri güncelle veya ekle
  events.items.forEach(event => {
    var eventId = event.id;
    var rowIndex = sheetData.findIndex(row => row[1] === eventId); // eventId'nin 2. sütunda olduğunu varsayıyoruz
    // Mentorun Ad ve Soyadini getir.
    var result = getPersonInfo(event.creator.email);
    // Logger.log(result);
    
    var startTime = event.start.dateTime ? convertToTimestamp(event.start.dateTime) : convertToTimestamp(event.start.date + "T00:59:59");
    var eventData = [
      convertToTimestamp(event.created),                                                // Zaman Damgası (event.created değeri)
      eventId,                                                                          // Etkinlik ID
      startTime,                                                                        // Mulakat Zamanı
      result['givenName'] || 'not a Contact',                                           // Mentor Adı
      result['familyName'] || 'not a Contact',                                          // Mentor Soyadı
      event.creator.email,                                                              // Mentor Mail
      event.summary || 'No title',                                                      // summary
      event.description || 'No description',                                            // description
      event.location || '',                                                             // location
      event.hangoutLink|| '',                                                           // hangoutLink
      event.attendees ? event.attendees[1].responseStatus : ''                          // responseStatus
    ];

    var eventForSQL = {};
    for (var i = 0; i < fields.length; i++){
      eventForSQL[fields[i]] = eventData[i];
      Logger.log('eventForSQL[' + fields[i] + ']:' + eventData[i]);
    }
    
    Logger.log('Row Index: ' + rowIndex);
    if (rowIndex !== -1) {
      // Etkinlik zaten var, güncelle
      var existingRow = sheetData[rowIndex];
      Logger.log('Existing data: ' + existingRow);
      Logger.log('New data: ' + eventData);
      if (hasChanges(existingRow, eventData, fields,datetimeFieldNames)) {
        sheet.getRange(rowIndex + 2, 1, 1, eventData.length).setValues([eventData]);

        // Database'deki veriyi guncelle
        var updateStmtEvent = 'UPDATE ' + appointmentsTable + ' SET ';
        var updateFieldsEvent = [];
        var updateValuesEvent = [];

        // Sorguda kullanilacak parametreleri ve veriyi ayarla
        for (var field in eventForSQL) {        
          // Logger.log('eventForSQL['+field+']: '+ eventForSQL[field]);
          if (field !== unique_key) {
            updateFieldsEvent.push(field + ' = ?');
            updateValuesEvent.push(eventForSQL[field]);
          }                 
        }
        updateStmtEvent += updateFieldsEvent.join(', ') + ' WHERE ' + unique_key + ' = ?';
        var stmtUpdateEvent = conn.prepareStatement(updateStmtEvent);
        // Logger.log('Sorgu metni: ' + updateStmtEvent);

        // Veri sorgu metni ile eslestirilir.
        for (var i = 0; i < updateValuesEvent.length; i++) {
          if (datetimeFieldNames.includes(updateFieldsEvent[i].split(' ')[0])) {
            stmtUpdateEvent.setTimestamp(i + 1, Jdbc.newTimestamp(updateValuesEvent[i]));
          } else {
            stmtUpdateEvent.setString(i + 1, updateValuesEvent[i]);
          }
          // Logger.log('updateFieldsEvent['+i+']: ' + updateValuesEvent[i]);
        }
        // Logger.log('updateValuesEvent[' + (updateValuesEvent.length+1) +']: '+ eventForSQL[unique_key]);
        stmtUpdateEvent.setString(updateValuesEvent.length + 1, eventForSQL[unique_key]);  // unique_key

        var resultStmtUpdateEvent = stmtUpdateEvent.executeUpdate();  // stmtUpdateEvent.execute();
        // Logger.log('resultStmtUpdateEvent===>: ' + resultStmtUpdateEvent);
        Logger.log('Google Sheet dosyasindaki ve Databse\'deki '+ appointmentsTable +' tablosundaki kayit GUNCELLENDI.');
      }
    } else {
      // Yeni etkinlik, yeni satır ekle
      sheet.appendRow(eventData);

      // Database'e veri yeni kayit ekle
      var insertStmtEvent = 'INSERT INTO ' + appointmentsTable + ' (';      
      var insertFieldsEvent = [];
      var insertValuesEvent = [];

      // Sorguda kullanilacak parametreleri ve veriyi ayarla
      for (var field in eventForSQL) {        
        // Logger.log('eventForSQL['+field+']: '+ eventForSQL[field]);
        if (eventForSQL[field]) {
          insertFieldsEvent.push(field);
          insertValuesEvent.push(eventForSQL[field]);
        }                 
      }
      insertStmtEvent += insertFieldsEvent.join(', ') + ') VALUES (' + insertFieldsEvent.map(() => '?').join(', ') + ')';
      // Logger.log('Sorgu metni: ' + insertStmtEvent);
      
      var stmtInsertEvent = conn.prepareStatement(insertStmtEvent, Jdbc.Statement.RETURN_GENERATED_KEYS);
      
      for (var i = 0; i < insertFieldsEvent.length; i++) {
        if (datetimeFieldNames.includes(insertFieldsEvent[i])) {
          stmtInsertEvent.setTimestamp(i + 1, Jdbc.newTimestamp(insertValuesEvent[i]));
        } else {
          stmtInsertEvent.setString(i + 1, insertValuesEvent[i]);
        }
      }
      var resultStmtInsertEvent = stmtInsertEvent.executeUpdate();  // stmtInsertEvent.execute();
      // Logger.log('resultStmtInsertEvent: ' + resultStmtInsertEvent);
      Logger.log('Google Sheet dosyasina ve Databse\'deki '+ appointmentsTable +' tablosuna yeni kayit EKLENDI.');
    }
  });
  
// .................................SILME ISLEMLERI........................................... //


  // Silinen veya zamanı geçmiş etkinlikleri kontrol et ve kaldır
  for (var i = sheetData.length - 1; i >= 0; i--) {
    var sheetEventId = sheetData[i][1]; // eventId'nin 2. sütunda olduğunu varsayıyoruz
    if (!currentEventIds.has(sheetEventId)) {
      // Logger.log('lastApplicationPeriodStartDate: ' + lastApplicationPeriodStartDate);
      // Logger.log('Mulakat Zamani: ' + sheetData[i][2]);
      
      // lastApplicationPeriodStartDate degeri MulakatZamani'ndan buyukse, yani yeni bir basvuru donemi acilmissa Mentor Atama islemi otomatik iptal edilmez. Bu kod yalnizca randevunun bir sekilde silinmis olmasi sebebiyle olusabilecek karisikligi engeller. Mesela mentor bir randevu tarihi olusturmustur. Bundan sonra CRM Uygulama kullanicisi/yoneticisi bir basvurani bu mentorun olusturdugu randevuya atamistir. Ne var ki mentor, yoneticiye bilgi vermeden randevuyu silerse, basvuranin mentor atama islemini otomatikman iptal etmis oluruz. 
      // tek birtransaction icinde olmali
      // Buraya bir de mail atma islevi konularak Basvuran ve Yoneticinin bilgilendirilmesi saglanabilir.
      
      if (lastApplicationPeriodStartDate < sheetData[i][2]){
        var queryIsAssignedAppointment = "SELECT MentiID from " + appointmentsTable + " WHERE " + unique_key + " = '" + sheetEventId + "'";
        var stmtIsAssignedAppointment = conn.createStatement();
        var resultIsAssignedAppointment = stmtIsAssignedAppointment.executeQuery(queryIsAssignedAppointment);
        var isAssignedAppointment = null;
        
        if (resultIsAssignedAppointment.next()) {
          isAssignedAppointment = resultIsAssignedAppointment.getInt("MentiID");  // MentiID degeri burada olacak
          Logger.log('isaassigned type: '+ typeof(isAssignedAppointment));
          
          // Empty the record from appointments table
          var queryUnassignAppointment = "UPDATE " + appointmentsTable + " SET MentiID = null WHERE " + unique_key + " = '" + sheetEventId + "'";
          var stmtUnassignAppointment = conn.prepareStatement(queryUnassignAppointment);
          // stmtDeleteEvent.setString(1, sheetEventId);
          var resultUnassignAppointment = stmtUnassignAppointment.executeUpdate();
          
          // Empty the record from form_basvuru table too
          var queryUnassignApplicant = "UPDATE " + basvuruTable + " SET IlkMulakat = 0 WHERE BasvuranID = " + isAssignedAppointment + " AND " + applicationPeriodFieldName + " = '" + lastApplicationPeriod + "'";
          var stmtUnassignApplicant = conn.prepareStatement(queryUnassignApplicant);
          var resultUnassignApplicant = stmtUnassignApplicant.executeUpdate();

          Logger.log('resultUnassignAppointment: ' + resultUnassignAppointment);
          Logger.log('resultUnassignApplicant: ' + resultUnassignApplicant);
          if (resultUnassignAppointment && resultUnassignApplicant) {
            Logger.log('Mentor atama islemi geri alindi / iptal edildi!\nDetay:  '+ appointmentsTable +' ve ' + basvuruTable + ' tablolarindaki atamalar null ve 0 olarak yeniden guncellendi.');
            sheet.deleteRow(i + 2); // +2 çünkü başlık satırı ve 0-tabanlı indeks
            Logger.log('Son basvuru donemiyle ilgili olup silinen etkinlik: ' + sheetEventId);
            try {
              // Silme sorgusunu hazırlayın
              var stmtDeleteEvent = conn.prepareStatement('DELETE FROM ' + appointmentsTable + ' WHERE ' + unique_key + ' = ?');
              stmtDeleteEvent.setString(1, sheetEventId);

              // Sorguyu çalıştır
              var resultStmtDeleteEvent = stmtDeleteEvent.executeUpdate();

              if (resultStmtDeleteEvent > 0) {
                Logger.log(unique_key + '=' + sheetEventId + ' olan kayıt silindi.');
              } else {
                Logger.log(unique_key + '=' + sheetEventId + ' olan kayıt bulunamadı.');
              }
            } catch (e) {
              Logger.log('Hata: ' + e);
            }
          }
        }
      } else {
        sheet.deleteRow(i + 2); // +2 çünkü başlık satırı ve 0-tabanlı indeks
        Logger.log('Yeni basvuru donemi basladigi icin silinerek old_or_deleted tablosuna tasinan etkinlik: ' + sheetEventId);
        try {
          // Silme sorgusunu hazırlayın
          var stmtDeleteEvent = conn.prepareStatement('DELETE FROM ' + appointmentsTable + ' WHERE ' + unique_key + ' = ?');
          stmtDeleteEvent.setString(1, sheetEventId);

          // Sorguyu çalıştır
          var resultStmtDeleteEvent = stmtDeleteEvent.executeUpdate();

          if (resultStmtDeleteEvent > 0) {
            Logger.log(unique_key + '=' + sheetEventId + ' olan kayıt silinerek old_or_deleted tablosuna tasindi.');
          } else {
            Logger.log(unique_key + '=' + sheetEventId + ' olan kayıt bulunamadı.');
          }
        } catch (e) {
          Logger.log('Hata: ' + e);
        }
      }
    }
  }
  // Veritabanı bağlantısını kapat
  conn.close();
}