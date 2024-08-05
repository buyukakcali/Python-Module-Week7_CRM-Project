function writeLatestEventToSheet() {
  // JDBC bağlantı bilgileri
  var properties = PropertiesService.getScriptProperties();
  var serverUrl = properties.getProperty('DB_URL');
  var user = properties.getProperty('DB_USER');
  var userPwd = properties.getProperty('DB_PASSWORD');
  var conn;

  conn = Jdbc.getConnection(serverUrl, user, userPwd);

  // .................. Configurtaion Area Starts ................... //

  var applicationTable = 'form_basvuru';
  var applicationPeriodFieldName = 'BasvuruDonemi';
  var firstInterviewFieldName = 'IlkMulakat';
  var applicantIdFieldName = 'BasvuranID';

  var appointmentsTable = 'appointments';
  var eventIdFieldName = 'EtkinlikID';
  var menteeIdFiledName = 'MentiID';
  var fields = ['ZamanDamgasi', 'EtkinlikID', 'MulakatZamani', 'MentorAdi', 'MentorSoyadi', 'MentorMail', 'Summary', 'Description', 'Location', 'OnlineMeetingLink', 'ResponseStatus'];
  var datetimeFieldNames = ['ZamanDamgasi', 'MulakatZamani'];

  var ownerOfTheCalendarMail = 'calendarownerORapplicationmanager@mail.com';
  var usedCalendarId = 'YOUR_CALENDAR_ID_HERE';

  // .................. Configurtaion Area Ends  .................... //

  // calendarId, etkinliklerin alınacağı takvimi belirtir.
  // 'primary', kullanıcının birincil takvimini ifade eder. Alternatif olarak, belirli bir takvimin kimliği (örneğin, bir takvim URL'si) kullanılabilir.
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var calendarId = usedCalendarId; // 'primary'; // OR ownerOfTheCalendarMail;

  // Son basvuru doneminin adini al
  var queryLastApplicationPeriod = 'SELECT ' + applicationPeriodFieldName + ' ' +'FROM ' + applicationTable + ' ' +'ORDER BY CAST(SUBSTRING(' + applicationPeriodFieldName + ', 4) AS UNSIGNED) DESC ' + 'LIMIT 1';
  var stmtLastApplicationPeriod = conn.createStatement();
  var resultLastApplicationPeriod = stmtLastApplicationPeriod.executeQuery(queryLastApplicationPeriod);
  var lastApplicationPeriod = null;
  if (resultLastApplicationPeriod.next()) {
    lastApplicationPeriod = resultLastApplicationPeriod.getString(applicationPeriodFieldName);
  }


  // form_basvuru tablosundan en son BaşvuruDönemi içindeki ilk kaydın oluşturulduğu zamanı al
  var queryLastApplicationPeriodStartDate = ('SELECT MIN('+datetimeFieldNames[0]+') FROM '+applicationTable+' WHERE '+applicationPeriodFieldName+' = (SELECT '+applicationPeriodFieldName+' FROM '+applicationTable+' ORDER BY CAST(SUBSTRING('+applicationPeriodFieldName+', 4) AS UNSIGNED) DESC LIMIT 1)');
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

    var startTime = event.start.dateTime ? convertToTimestamp(event.start.dateTime) : convertToTimestamp(event.start.date + "T00:00:01");
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
      event.attendees ? event.attendees[1].responseStatus : ''          // responseStatus - burada farkli bir yaklasim gerekebilir ilerde
    ];

    var eventForSQL = {};
    for (var i = 0; i < fields.length; i++){
      eventForSQL[fields[i]] = eventData[i];
      // Logger.log('eventForSQL[' + fields[i] + ']:' + eventData[i]);
    }

    // Logger.log('Row Index: ' + rowIndex);
    if (rowIndex !== -1) {
      // Etkinlik zaten var, güncelle
      var existingRow = sheetData[rowIndex];
      // Logger.log('Existing data: ' + existingRow);
      // Logger.log('New data: ' + eventData);
      // Logger.log('hasChanges(existingRow, eventData, fields,datetimeFieldNames): ' + hasChanges(existingRow, eventData, fields,datetimeFieldNames));
      if (hasChanges(existingRow, eventData, fields,datetimeFieldNames)) {
        sheet.getRange(rowIndex + 2, 1, 1, eventData.length).setValues([eventData]);

        // Database'deki veriyi guncelle
        var updateStmtEvent = 'UPDATE ' + appointmentsTable + ' SET ';
        var updateFieldsEvent = [];
        var updateValuesEvent = [];

        // Sorguda kullanilacak parametreleri ve veriyi ayarla
        for (var field in eventForSQL) {
          // Logger.log('eventForSQL['+field+']: '+ eventForSQL[field]);
          if (field !== eventIdFieldName) {
            updateFieldsEvent.push(field + ' = ?');
            updateValuesEvent.push(eventForSQL[field]);
          }
        }
        updateStmtEvent += updateFieldsEvent.join(', ') + ' WHERE ' + eventIdFieldName + ' = ?';
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
        // Logger.log('updateValuesEvent[' + (updateValuesEvent.length+1) +']: '+ eventForSQL[eventIdFieldName]);
        stmtUpdateEvent.setString(updateValuesEvent.length + 1, eventForSQL[eventIdFieldName]);  // eventIdFieldName's value is added

        var resultStmtUpdateEvent = stmtUpdateEvent.executeUpdate();
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
      var resultStmtInsertEvent = stmtInsertEvent.executeUpdate();
      // Logger.log('resultStmtInsertEvent: ' + resultStmtInsertEvent);
      Logger.log('Google Sheet dosyasina ve Databse\'deki '+ appointmentsTable +' tablosuna yeni kayit EKLENDI.');
    }
  });

  // .................................SILME ISLEMLERI........................................... //


  // Silinen veya zamanı geçmiş etkinlikleri kontrol et ve kaldır
  for (var i = sheetData.length - 1; i >= 0; i--) {
    var sheetEventId = sheetData[i][1]; // eventId'nin 2. sütunda olduğunu varsayıyoruz
    if (currentEventIds.has(sheetEventId) === false) {
      // Logger.log('Sadece silinenler ile ilgili bolumde girmesi gerekiyor!')

      // lastApplicationPeriodStartDate degeri MulakatZamani'ndan buyukse, yani yeni bir basvuru donemi acilmissa MentorAtama islemi otomatik iptal edilmez. Bu kod yalnizca randevunun bir sekilde silinmis olmasi sebebiyle olusabilecek karisikligi engeller. Mesela mentor bir randevu tarihi olusturmustur. Bundan sonra CRM Uygulama kullanicisi/yoneticisi bir basvurani bu mentorun olusturdugu randevuya atamistir. Ne var ki mentor, yoneticiye bilgi vermeden randevuyu silerse, basvuranla ilgili mentor atama islemini otomatikman iptal etmis oluruz.
      // tek birtransaction icinde olmali
      // Buraya bir de mail atma islevi konularak Basvuran ve Yoneticinin bilgilendirilmesi saglanabilir.

      if (lastApplicationPeriodStartDate < sheetData[i][2]){ // Burasi son basvuru donemi devam ederken silinen randevular icin calisir!
        var queryIsAssignedAppointment = "SELECT " +menteeIdFiledName+ " from " + appointmentsTable + " WHERE " + eventIdFieldName + " = '" + sheetEventId + "'";
        var stmtIsAssignedAppointment = conn.createStatement();
        var resultIsAssignedAppointment = stmtIsAssignedAppointment.executeQuery(queryIsAssignedAppointment);

        var menteeId = null;
        if (resultIsAssignedAppointment.next()) {
          menteeId = resultIsAssignedAppointment.getInt(menteeIdFiledName);  // MentiID degeri burada olacak
        }

        if (menteeId !== 0 && menteeId !== null) {
          //  Logger.log('Mentor atanmis olanlari once bosaltip sonra silmek icin buraya girer!');
          // Empty the record from appointments table
          var queryUnassignAppointment = "UPDATE " + appointmentsTable + " SET " +menteeIdFiledName+ " = ? WHERE " + eventIdFieldName + " = '?'";
          var stmtUnassignAppointment = conn.prepareStatement(queryUnassignAppointment);
          stmtUnassignAppointment.setString(1, 'null');
          stmtUnassignAppointment.setString(2, sheetEventId);
          var resultUnassignAppointment = stmtUnassignAppointment.executeUpdate();

          // Empty the record from form_basvuru table too
          var queryUnassignApplicant = "UPDATE " + applicationTable + " SET " +firstInterviewFieldName+ " = '?' WHERE " +applicantIdFieldName+ " = '?' AND " + applicationPeriodFieldName + " = '?'";
          var stmtUnassignApplicant = conn.prepareStatement(queryUnassignApplicant);
          stmtUnassignApplicant.setInt(1, 0);
          stmtUnassignApplicant.setInt(2, menteeId);
          stmtUnassignApplicant.setString(3, lastApplicationPeriod);
          var resultUnassignApplicant = stmtUnassignApplicant.executeUpdate();

          // Logger.log('resultUnassignAppointment: ' + resultUnassignAppointment);
          // Logger.log('resultUnassignApplicant: ' + resultUnassignApplicant);
          if (resultUnassignAppointment && resultUnassignApplicant) {
            Logger.log('Mentor atama islemi geri alindi / iptal edildi!\nDetay:  '+ appointmentsTable +' ve ' + applicationTable + ' tablolarindaki atamalar null ve 0 olarak yeniden guncellendi.');
          }
        }
        sheet.deleteRow(i + 2); // +2 çünkü başlık satırı ve 0-tabanlı indeks
        Logger.log('Yeni bir basvuru donemi basladigi icin appointments_old+or_deleted tablosuna tasinan etkinlik: ' + sheetEventId);
        try {
          // Silme sorgusunu hazırlayın
          var stmtDeleteEvent = conn.prepareStatement('DELETE FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = ?');
          stmtDeleteEvent.setString(1, sheetEventId);

          // Sorguyu çalıştır
          var resultStmtDeleteEvent = stmtDeleteEvent.executeUpdate();

          if (resultStmtDeleteEvent > 0) {
            Logger.log(eventIdFieldName + ': ' + sheetEventId + ' olan kayıt tasindi.');
          } else {
            Logger.log(eventIdFieldName + ': ' + sheetEventId + ' olan kayıt bulunamadı.');
          }
        } catch (e) {
          Logger.log('Hata: ' + e);
        }
      } else {
        sheet.deleteRow(i + 2); // +2 çünkü başlık satırı ve 0-tabanlı indeks
        Logger.log('Yeni basvuru donemi basladigi icin silinerek old_or_deleted tablosuna tasinan etkinlik: ' + sheetEventId);
        try {
          // Silme sorgusunu hazırlayın
          var stmtDeleteEvent = conn.prepareStatement('DELETE FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = ?');
          stmtDeleteEvent.setString(1, sheetEventId);

          // Sorguyu çalıştır
          var resultStmtDeleteEvent = stmtDeleteEvent.executeUpdate();

          if (resultStmtDeleteEvent > 0) {
            Logger.log(eventIdFieldName + '=' + sheetEventId + ' olan kayıt silinerek old_or_deleted tablosuna tasindi.');
          } else {
            Logger.log(eventIdFieldName + '=' + sheetEventId + ' olan kayıt bulunamadı.');
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


// Değerleri karşılaştırma fonksiyonu - (event guncellenmis mi diye kontrol etmek icin)
function hasChanges(oldRow, newData, fields, datetimeFieldNames) {
  for (var i = 0; i < newData.length; i++) {
    var oldVal = oldRow[i];
    var newVal = newData[i];

    if (datetimeFieldNames.includes(fields[i])) {
      oldVal = convertToUTC(oldVal)['utcDatetime'];
      newVal = convertToUTC(newVal)['utcDatetime'];
    }

    if (oldVal !== newVal) {
      return true;
    }
  }
  return false;
}


function parseTimestamp(timestamp) {
  // Giriş değerini string'e çevir
  if (typeof timestamp !== 'string') {
    timestamp = timestamp.toString();
  }

  // ISO 8601 formatı
  if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(timestamp)) {
    return new Date(timestamp).toISOString();
  }

  // ABD formatı (M/D/YYYY H:MM:SS AM/PM)
  if (/^\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{2}:\d{2} (AM|PM)$/.test(timestamp)) {
    return new Date(timestamp).toISOString();
  }

  // Avrupa formatı (D.M.YYYY H:MM:SS)
  if (/^\d{1,2}\.\d{1,2}\.\d{4} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
    var parts = timestamp.split(' ');
    var dateParts = parts[0].split('.');
    var timeParts = parts[1].split(':');
    return new Date(Date.UTC(
      parseInt(dateParts[2], 10),
      parseInt(dateParts[1], 10) - 1,
      parseInt(dateParts[0], 10),
      parseInt(timeParts[0], 10),
      parseInt(timeParts[1], 10),
      parseInt(timeParts[2], 10)
    )).toISOString();
  }

  // Yıl, Ay, Gün formatı (YYYY/M/D H:MM:SS)
  if (/^\d{4}\/\d{1,2}\/\d{1,2} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
    var parts = timestamp.split(' ');
    var dateParts = parts[0].split('/');
    var timeParts = parts[1].split(':');
    return new Date(Date.UTC(
      parseInt(dateParts[0], 10),
      parseInt(dateParts[1], 10) - 1,
      parseInt(dateParts[2], 10),
      parseInt(timeParts[0], 10),
      parseInt(timeParts[1], 10),
      parseInt(timeParts[2], 10)
    )).toISOString();
  }

  // Gün/Ay/Yıl formatı (D/M/YYYY H:MM:SS)
  if (/^\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
    var parts = timestamp.split(' ');
    var dateParts = parts[0].split('/');
    var timeParts = parts[1].split(':');
    return new Date(Date.UTC(
      parseInt(dateParts[2], 10),
      parseInt(dateParts[1], 10) - 1,
      parseInt(dateParts[0], 10),
      parseInt(timeParts[0], 10),
      parseInt(timeParts[1], 10),
      parseInt(timeParts[2], 10)
    )).toISOString();
  }

  // Gün-Ay-Yıl formatı (D-M-YYYY H:MM:SS)
  if (/^\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
    var parts = timestamp.split(' ');
    var dateParts = parts[0].split('-');
    var timeParts = parts[1].split(':');
    return new Date(Date.UTC(
      parseInt(dateParts[2], 10),
      parseInt(dateParts[1], 10) - 1,
      parseInt(dateParts[0], 10),
      parseInt(timeParts[0], 10),
      parseInt(timeParts[1], 10),
      parseInt(timeParts[2], 10)
    )).toISOString();
  }

  // Yıl.Ay.Gün formatı (YYYY.M.D H:MM:SS)
  if (/^\d{4}\.\d{1,2}\.\d{1,2} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
    var parts = timestamp.split(' ');
    var dateParts = parts[0].split('.');
    var timeParts = parts[1].split(':');
    return new Date(Date.UTC(
      parseInt(dateParts[0], 10),
      parseInt(dateParts[1], 10) - 1,
      parseInt(dateParts[2], 10),
      parseInt(timeParts[0], 10),
      parseInt(timeParts[1], 10),
      parseInt(timeParts[2], 10)
    )).toISOString();
  }

  // YYYY-MM-DD formatı (YYYY-MM-DD H:MM:SS)
  if (/^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
    var parts = timestamp.split(' ');
    var dateParts = parts[0].split('-');
    var timeParts = parts[1].split(':');
    return new Date(Date.UTC(
      parseInt(dateParts[0], 10),
      parseInt(dateParts[1], 10) - 1,
      parseInt(dateParts[2], 10),
      parseInt(timeParts[0], 10),
      parseInt(timeParts[1], 10),
      parseInt(timeParts[2], 10)
    )).toISOString();
  }

  // YYYY-MM-DD formatı (sadece tarih)
  if (/^\d{4}-\d{2}-\d{2}$/.test(timestamp)) {
    return new Date(timestamp).toISOString();
  }

  // MM/DD/YYYY formatı
  if (/^\d{2}\/\d{2}\/\d{4}$/.test(timestamp)) {
    return new Date(timestamp).toISOString();
  }

  // YYYY/MM/DD formatı
  if (/^\d{4}\/\d{2}\/\d{2}$/.test(timestamp)) {
    var parts = timestamp.split('/');
    return new Date(Date.UTC(
      parseInt(parts[0], 10),
      parseInt(parts[1], 10) - 1,
      parseInt(parts[2], 10)
    )).toISOString();
  }

  // Kompakt format (YYYYMMDDTHHMMSS)
  if (/^\d{8}T\d{6}$/.test(timestamp)) {
    return new Date(
      timestamp.substr(0, 4),
      parseInt(timestamp.substr(4, 2), 10) - 1,
      timestamp.substr(6, 2),
      timestamp.substr(9, 2),
      timestamp.substr(11, 2),
      timestamp.substr(13, 2)
    ).toISOString();
  }

  // Standart JavaScript Date.toString() formatı
  if (/^[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2} GMT[+-]\d{4} \(.*\)$/.test(timestamp)) {
    return new Date(timestamp).toISOString();
  }

  // Eğer hiçbir format eşleşmezse
  throw new Error('Tanınmayan zaman damgası formatı: ' + timestamp);
}

/*

Açıklama:
ISO 8601 formatı: (^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$)
ABD formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{2}:\d{2} (AM|PM)$)
Avrupa formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}\.\d{1,2}\.\d{4} \d{2}:\d{2}:\d{2}$)
Yıl, Ay, Gün formatı: Tek haneli gün ve ayları da destekler (^\d{4}\/\d{1,2}\/\d{1,2} \d{2}:\d{2}:\d{2}$)
Gün/Ay/Yıl formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2}:\d{2}$)
Gün-Ay-Yıl formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}:\d{2}$)
Yıl.Ay.Gün formatı: Tek haneli gün ve ayları da destekler (^\d{4}\.\d{1,2}\.\d{1,2} \d{2}:\d{2}:\d{2}$)
YYYY-MM-DD formatı: Tek haneli gün ve ayları da destekler (^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}$)
Sadece tarih (YYYY-MM-DD): (^\d{4}-\d{2}-\d{2}$)
MM/DD/YYYY formatı: (^\d{2}\/\d{2}\/\d{4}$)
YYYY/MM/DD formatı: (^\d{4}\/\d{2}\/\d{2}$)
Kompakt format: (^\d{8}T\d{6}$)
Standart JavaScript Date.toString() formatı: (^[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2} GMT[+-]\d{4} \(.*\)$)

Not: Tüm formatlar, uygun olduğunda tek haneli gün ve ayları destekler.
Fonksiyon, giriş değerini otomatik olarak string'e çevirir.
Çıktı her zaman ISO 8601 formatında olacaktır.

*/

function convertToUTC(isoString) {
  // ISO string'i Date nesnesine çevir
  const date = new Date(isoString);

  // Geçerli bir tarih olup olmadığını kontrol et
  if (isNaN(date.getTime())) {
    throw new Error('Geçersiz tarih formatı: ' + isoString);
  }

  // UTC timestamp (milisaniye cinsinden)
  const utcTimestamp = date.getTime();

  // UTC datetime nesnesi
  const utcDatetime = new Date(utcTimestamp);

  return {
    utcTimestamp: utcTimestamp,
    utcDatetime: utcDatetime,
    formattedUTC: utcDatetime.toUTCString(),
    isoUTC: utcDatetime.toISOString()
  };
}

/*
Bu fonksiyon şunları yapar:

Verilen ISO 8601 formatındaki string'i bir JavaScript Date nesnesine çevirir.
Oluşturulan tarihin geçerli olup olmadığını kontrol eder.
UTC timestamp'ini (Unix zamanı, milisaniye cinsinden) hesaplar.
UTC datetime nesnesini oluşturur.
Bir nesne döndürür, bu nesne şunları içerir:

utcTimestamp: UTC zaman damgası (milisaniye cinsinden)
utcDatetime: UTC datetime nesnesi
formattedUTC: İnsan tarafından okunabilir UTC string formatı
isoUTC: ISO 8601 formatında UTC string


Bu fonksiyonu şu şekilde kullanabilirsiniz:

KOD BLOGU BASLAR:

// Önce parseTimestamp fonksiyonunu kullanarak bir tarih parse edelim
const parsedDate = parseTimestamp("2023-08-15 14:30:00");

// Şimdi bu tarihi UTC'ye dönüştürelim
const utcResult = convertToUTC(parsedDate);

console.log(utcResult.utcTimestamp); // Örnek: 1692108600000
console.log(utcResult.utcDatetime); // Örnek: 2023-08-15T14:30:00.000Z (Date nesnesi)
console.log(utcResult.formattedUTC); // Örnek: "Tue, 15 Aug 2023 14:30:00 GMT"
console.log(utcResult.isoUTC); // Örnek: "2023-08-15T14:30:00.000Z"

KOD BLOGU BITTI:

Bu fonksiyon, parseTimestamp fonksiyonunun döndürdüğü her türlü ISO 8601 formatındaki tarihi alabilir ve onu UTC zaman damgasına ve datetime nesnesine dönüştürür. Ayrıca, insan tarafından okunabilir bir format ve ISO 8601 UTC formatı da sağlar. Bu, farklı ihtiyaçlarınız için esneklik sağlar.

*/


// // Google People API'yi kullanmak için OAuth2 kütüphanesini ekleyin
// // Kütüphane Kimliği: 1B7FSrk5Zi6L1rSxxTDgDEUsPzlukDsi4KGuTMorsTQHhGBzBkMun4iDF
var CLIENT_ID = 'YOUR_CLIENT_ID_HERE';
var CLIENT_SECRET = 'YOUR_CLIENT_SECRET_HERE';
var SCOPE = 'https://www.googleapis.com/auth/contacts.readonly';
var TOKEN_PROPERTY_NAME = 'people_api_token';


// OAuth2 kurulumu ve kimlik doğrulama işlemi
function getOAuthService() {
  return OAuth2.createService('GooglePeopleAPI')
    .setAuthorizationBaseUrl('https://accounts.google.com/o/oauth2/auth')
    .setTokenUrl('https://accounts.google.com/o/oauth2/token')
    .setClientId(CLIENT_ID)
    .setClientSecret(CLIENT_SECRET)
    .setCallbackFunction('authCallback')
    .setPropertyStore(PropertiesService.getUserProperties())
    .setScope(SCOPE)
    .setParam('access_type', 'offline')
    .setParam('approval_prompt', 'force');
}

function authCallback(request) {
  var oauthService = getOAuthService();
  var authorized = oauthService.handleCallback(request);
  if (authorized) {
    return HtmlService.createHtmlOutput('Başarıyla yetkilendirildi.').setWidth(500).setHeight(150);
  } else {
    return HtmlService.createHtmlOutput('Yetkilendirme başarısız.').setWidth(500).setHeight(150);
  }
}

function getPersonInfo(email) {
  var oauthService = getOAuthService();
  if (!oauthService.hasAccess()) {
    var authorizationUrl = oauthService.getAuthorizationUrl();
    Logger.log('Aşağıdaki URL\'yi ziyaret edin ve yetkilendirme işlemini tamamlayın: %s', authorizationUrl);
    return HtmlService.createHtmlOutput('Aşağıdaki URL\'yi ziyaret edin ve yetkilendirme işlemini tamamlayın: <a href="' + authorizationUrl + '" target="_blank">' + authorizationUrl + '</a>');
  }

  try {
    var connections = [];
    var nextPageToken = '';
    do {
      var url = 'https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses';
      if (nextPageToken) {
        url += '&pageToken=' + nextPageToken;
      }

      var response = UrlFetchApp.fetch(url, {
        headers: {
          Authorization: 'Bearer ' + oauthService.getAccessToken()
        }
      });
      var data = JSON.parse(response.getContentText());
      if (data.connections) {
        connections = connections.concat(data.connections);
      }
      nextPageToken = data.nextPageToken;
    } while (nextPageToken);

    Logger.log('Total connections retrieved: ' + connections.length);

    var person = connections.find(function(connection) {
      return connection.emailAddresses &&
             connection.emailAddresses.some(function(emailObj) {
               return emailObj.value.toLowerCase() === email.toLowerCase();
             });
    });

    if (person) {
      var name = person.names ? person.names[0].displayName : "İsim bulunamadı";
      return {
        fullName: name,
        givenName: person.names ? person.names[0].givenName : "Ad bulunamadı",
        familyName: person.names ? person.names[0].familyName : "Soyad bulunamadı"
      };
    } else {
      return "Kişi bulunamadı veya kişi listenizde yok.";
    }
  } catch (e) {
    Logger.log('Hata: ' + e.toString());
    return "Hata: " + e.toString();
  }
}

// Fonksiyonu test et
function testGetPersonInfo() {
  var email = "test@mail.com"; // Test etmek istediğiniz e-posta adresi
  Logger.log(getPersonInfo(email));
}
