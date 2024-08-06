function writeLatestEventToSheet() {
  // JDBC bağlantı bilgileri
  var properties = PropertiesService.getScriptProperties();
  var serverUrl = properties.getProperty('DB_URL');
  var user = properties.getProperty('DB_USER');
  var userPwd = properties.getProperty('DB_PASSWORD');
  var conn;

  try {
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
    // calendarId, etkinliklerin alınacağı takvimi belirtir.
    // 'primary', kullanıcının birincil takvimini ifade eder. Alternatif olarak, belirli bir takvimin kimliği (örneğin, bir takvim URL'si) kullanılabilir.
    var calendarId = 'YOUR_CALENDAR_ID_HERE'; // 'primary'; // OR ownerOfTheCalendarMail;

    var java_sql_Types = {
      INTEGER: 4,
      VARCHAR: 12,
      TIMESTAMP: 93,
      DATE: 91
      // Diğer türler gerektiğinde buraya eklenebilir
    };

    // .................. Configurtaion Area Ends  .................... //

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Son basvuru doneminin adini al
    var queryLastApplicationPeriod = 'SELECT ' + applicationPeriodFieldName + ' ' +'FROM ' + applicationTable + ' ' +'ORDER BY CAST(SUBSTRING(' + applicationPeriodFieldName + ', 4) AS UNSIGNED) DESC ' + 'LIMIT 1';
    var stmtLastApplicationPeriod = conn.createStatement();
    var resultLastApplicationPeriod = null;
    var lastApplicationPeriod = null;
    try {
      resultLastApplicationPeriod = stmtLastApplicationPeriod.executeQuery(queryLastApplicationPeriod);
      if (resultLastApplicationPeriod.next()) {
        lastApplicationPeriod = resultLastApplicationPeriod.getString(applicationPeriodFieldName);
      }
    } finally {
      resultLastApplicationPeriod.close();  // ResultSet kapatılıyor
      stmtLastApplicationPeriod.close();    // Statement kapatılıyor
    }
    // Logger.log('Son basvuru donemi adi: ' + lastApplicationPeriod);

    // form_basvuru tablosundan en son BaşvuruDönemi içindeki ilk kaydın oluşturulduğu zamanı al
    var queryLastApplicationPeriodStartDate = ('SELECT MIN('+datetimeFieldNames[0]+') FROM '+applicationTable+' WHERE '+applicationPeriodFieldName+' = (SELECT '+applicationPeriodFieldName+' FROM '+applicationTable+' ORDER BY CAST(SUBSTRING('+applicationPeriodFieldName+', 4) AS UNSIGNED) DESC LIMIT 1)');
    var stmtLastApplicationPeriodStartDate = conn.createStatement();
    var resultLastApplicationPeriodStartDate = null;
    var lastApplicationPeriodStartDate = null;
    try {
      resultLastApplicationPeriodStartDate = stmtLastApplicationPeriodStartDate.executeQuery(queryLastApplicationPeriodStartDate);
      if (resultLastApplicationPeriodStartDate.next()) {
        lastApplicationPeriodStartDate = new Date(resultLastApplicationPeriodStartDate.getTimestamp(1).getTime());
      }
    } finally {
      resultLastApplicationPeriodStartDate.close();  // ResultSet kapatılıyor
      stmtLastApplicationPeriodStartDate.close();    // Statement kapatılıyor
    }
    // Logger.log('Son basvuru donemi icin baslangic tarihi: ' + lastApplicationPeriodStartDate);

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

      // Tum gun surecek sekilde olusturulan etkinlikler icin saat kaydini 00:00:01 olarak ayarliyoruz.
      // 00:00:00 da olabilirdi ama uluslararasi calisan bir kurulus bu saatte de normal toplanti duzenleyebilir diye bir saniyelik fark olusturduk.
      var startTime = event.start.dateTime ? convertToUTC(event.start.dateTime)['utcDatetime'] : convertToUTC(event.start.date + "T00:00:01")['utcDatetime'];

      // Takvimden gelen verilerden istenenler aliniyor.
      var eventData = [
        convertToUTC(event.created)['utcDatetime'],                                       // Zaman Damgası (event.created değeri)
        eventId,                                                                          // Etkinlik ID
        startTime,                                                                        // Mulakat Zamanı
        result['givenName'] || 'not a Contact',                                           // Mentor Adı
        result['familyName'] || 'not a Contact',                                          // Mentor Soyadı
        event.creator.email,                                                              // Mentor Mail
        event.summary || 'No title',                                                      // summary
        event.description || 'No description',                                            // description
        event.location || 'No location',                                                  // location
        event.hangoutLink|| 'No Link',                                                    // hangoutLink
        // event.attendees ? event.attendees[1].responseStatus : ''          // responseStatus - burada farkli bir yaklasim gerekebilir ilerde
      ];

      var eventForSQL = {}; // Sutun adlariyla, bunlara ait verileri tek bir yapida saklamak icin sozluk kullanildi ve atamalar yapiliyor.
      for (var i = 0; i < fields.length; i++){
        eventForSQL[fields[i]] = eventData[i];
        // Logger.log('eventForSQL[' + fields[i] + ']:' + eventData[i]);
      }

      // Islemin turunu belirlemek icin buradan itibaren basliyoruz. Islem turu: add or update
      if (rowIndex !== -1) {
        // Etkinlik zaten var, güncelle
        var existingRow = sheetData[rowIndex];
        Logger.log('Existing data: ' + existingRow);
        Logger.log('New data: ' + eventData);
        Logger.log('hasChanges(existingRow, eventData, fields,datetimeFieldNames): ' + hasChanges(existingRow, eventData, fields,datetimeFieldNames));

        // Bu fonksiyon ile ilgili etkinlikte herhangi bir degisiklik olup olmadigi kontrol ediliyor. Eger degisim varsa guncelleniyor, yoksa siradakine geciliyor. Boylece islemci gucu tasarruf ediliyor ve zaman kazaniliyor. Gereksiz yeniden yazma islemi yapilmiyor.
        if (hasChanges(existingRow, eventData, fields, datetimeFieldNames)) {
          sheet.getRange(rowIndex + 2, 1, 1, eventData.length).setValues([eventData]);

          // Database'deki veriyi guncelle
          var queryUpdateEvent = 'UPDATE ' + appointmentsTable + ' SET ';
          var updateEventFields = [];
          var updateEventValues = [];

          // Sorguda kullanilacak parametreleri ve veriyi ata
          for (var field in eventForSQL) {
            // Logger.log('eventForSQL['+field+']: '+ eventForSQL[field]);
            if (field !== eventIdFieldName) {
              updateEventFields.push(field + ' = ?');
              updateEventValues.push(eventForSQL[field]);
            }
          }
          queryUpdateEvent += updateEventFields.join(', ') + ' WHERE ' + eventIdFieldName + ' = ?';
          var stmtUpdateEvent = conn.prepareStatement(queryUpdateEvent);
          Logger.log('Sorgu metni: ' + queryUpdateEvent);

          // Veri sorgu metnindeki yerine atanir.
          for (var i = 0; i < updateEventValues.length; i++) {
            if (datetimeFieldNames.includes(updateEventFields[i].split(' ')[0])) {
              stmtUpdateEvent.setTimestamp(i + 1, Jdbc.newTimestamp(updateEventValues[i]));
            } else {
              stmtUpdateEvent.setString(i + 1, updateEventValues[i]);
            }
            // Logger.log('updateFieldsEvent['+i+']: ' + updateValuesEvent[i]);
          }
          stmtUpdateEvent.setString(updateEventValues.length + 1, eventForSQL[eventIdFieldName]);  // eventIdFieldName's value is added
          // Logger.log('Sorgu metni: ' + queryUpdateEvent);
          var resultStmtUpdateEvent = null;
          try {
            resultStmtUpdateEvent = stmtUpdateEvent.executeUpdate();
            if (resultStmtUpdateEvent){
              // Logger.log('resultStmtUpdateEvent===>: ' + resultStmtUpdateEvent);
              Logger.log('Google Sheet dosyasindaki ve Databse\'deki '+ appointmentsTable +' tablosundaki kayit(' + eventIdFieldName + '= ' + eventForSQL[eventIdFieldName] + ') GUNCELLENDI.');
            }
          } finally {
            stmtUpdateEvent.close();      // Statement kapatılıyor
          }
        }
      } else {
        // Yeni etkinlik, yeni satır ekle
        sheet.appendRow(eventData);

        // Database'e yeni kayit ekle
        var queryInsertEvent = 'INSERT INTO ' + appointmentsTable + ' (';
        var insertEventFields = [];
        var insertEventValues = [];

        // Sorguda kullanilacak parametreleri ve veriyi ata
        for (var field in eventForSQL) {
          // Logger.log('eventForSQL['+field+']: '+ eventForSQL[field]);
          if (eventForSQL[field]) {
            insertEventFields.push(field);
            insertEventValues.push(eventForSQL[field]);
          }
        }
        queryInsertEvent += insertEventFields.join(', ') + ') VALUES (' + insertEventFields.map(() => '?').join(', ') + ')';
        Logger.log('Sorgu metni: ' + queryInsertEvent);

        var stmtInsertEvent = conn.prepareStatement(queryInsertEvent, Jdbc.Statement.RETURN_GENERATED_KEYS);

        // Veri sorgu metnindeki yerine atanir.
        for (var i = 0; i < insertEventFields.length; i++) {
          if (datetimeFieldNames.includes(insertEventFields[i])) {
            stmtInsertEvent.setTimestamp(i + 1, Jdbc.newTimestamp(insertEventValues[i]));
          } else {
            stmtInsertEvent.setString(i + 1, insertEventValues[i]);
          }
        }
        var resultStmtInsertEvent = null;

        try {
          resultStmtInsertEvent = stmtInsertEvent.executeUpdate();
          if (resultStmtInsertEvent) {
            // Logger.log('resultStmtInsertEvent: ' + resultStmtInsertEvent);
            Logger.log('Google Sheet dosyasina ve Databse\'deki '+ appointmentsTable +' tablosuna yeni kayit(' + eventIdFieldName + '= ' + eventForSQL[eventIdFieldName] + ') EKLENDI.');
          }
        } finally {
          stmtInsertEvent.close();  // Statement kapatılıyor
        }
      }
    });

    // .................................SILME ISLEMLERI........................................... //

    // Silinen veya zamanı geçmiş etkinlikleri kontrol et ve kaldır
    for (var i = sheetData.length - 1; i >= 0; i--) {
      var sheetEventId = sheetData[i][1]; // eventId'nin 2. sütunda olduğunu varsayıyoruz
      if (currentEventIds.has(sheetEventId) === false) {
        // Logger.log('Sadece silinenler ile ilgili bolumde girmesi gerekiyor!')

        // NOT: lastApplicationPeriodStartDate degeri MulakatZamani'ndan buyukse, yani yeni bir basvuru donemi acilmissa MentorAtama islemi otomatik iptal edilmez. Bu kod yalnizca randevunun bir sekilde silinmis olmasi sebebiyle olusabilecek karisikligi engeller. Mesela mentor bir randevu tarihi olusturmustur. Bundan sonra CRM Uygulama kullanicisi/yoneticisi bir basvurani bu mentorun olusturdugu randevuya atamistir. Ne var ki mentor, yoneticiye bilgi vermeden randevuyu silerse, basvuranla ilgili mentor atama islemini otomatikman iptal etmis oluruz.
        // tek birtransaction icinde olmali
        // Buraya bir de mail atma islevi konularak Basvuran ve Yoneticinin bilgilendirilmesi saglanabilir.

        if (lastApplicationPeriodStartDate < sheetData[i][2]){ // Burasi son basvuru donemi devam ederken silinen randevular icin calisir!
          var queryIsAssignedAppointment = 'SELECT ' +menteeIdFiledName+ ' FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = \'' + sheetEventId + '\'';
          var stmtIsAssignedAppointment = conn.createStatement();
          var menteeId = null;
          var resultIsAssignedAppointment = null;

          try {
            resultIsAssignedAppointment = stmtIsAssignedAppointment.executeQuery(queryIsAssignedAppointment);
            if (resultIsAssignedAppointment.next()) {
              menteeId = resultIsAssignedAppointment.getInt(menteeIdFiledName);  // MentiID degeri burada olacak
            }
          } finally {
            stmtIsAssignedAppointment.close();    // Statement kapatılıyor
            resultIsAssignedAppointment.close();  // ResultSet kapatiliyor
          }

          if (menteeId !== 0 && menteeId !== null) {
            //  Logger.log('Mentor atanmis olanlari once bosaltip sonra silmek icin buraya girer!');
            // Empty the record from appointments table
            var queryUnassignAppointment = 'UPDATE ' + appointmentsTable + ' SET ' +menteeIdFiledName+ ' = ? WHERE ' + eventIdFieldName + ' = ?';
            var stmtUnassignAppointment = conn.prepareStatement(queryUnassignAppointment);
            stmtUnassignAppointment.setNull(1, java_sql_Types.INTEGER);
            stmtUnassignAppointment.setString(2, sheetEventId);
            // Logger.log('Sorgu Metni: ' + queryUnassignAppointment);
            var resultUnassignAppointment = null;

            // Empty the record from form_basvuru table too
            var queryUnassignApplicant = 'UPDATE ' + applicationTable + ' SET ' +firstInterviewFieldName+ ' = ? WHERE ' +applicantIdFieldName+ ' = ? AND ' + applicationPeriodFieldName + ' = ?';
            var stmtUnassignApplicant = conn.prepareStatement(queryUnassignApplicant);
            stmtUnassignApplicant.setInt(1, 0);
            stmtUnassignApplicant.setInt(2, menteeId);
            stmtUnassignApplicant.setString(3, lastApplicationPeriod);
            // Logger.log('Sorgu Metni: ' + queryUnassignApplicant)
            var resultUnassignApplicant = null;

            try {
              resultUnassignAppointment = stmtUnassignAppointment.executeUpdate();
              resultUnassignApplicant = stmtUnassignApplicant.executeUpdate();

              // Logger.log('resultUnassignAppointment: ' + resultUnassignAppointment);
              // Logger.log('resultUnassignApplicant: ' + resultUnassignApplicant);
              if (resultUnassignAppointment && resultUnassignApplicant) {
                Logger.log('Mentor atama islemi geri alindi / iptal edildi!\nDetay:  '+ appointmentsTable +' ve ' + applicationTable + ' tablolarindaki atamalar null ve 0 olarak yeniden guncellendi.');
              }
            } finally {
              stmtUnassignAppointment.close();    // 1. statement kapatılıyor
              stmtUnassignApplicant.close();      // 2. statement kapatılıyor
            }
          }

          sheet.deleteRow(i + 2); // +2 çünkü başlık satırı ve 0-tabanlı indeks
          // Silme sorgusunu hazırlayın
          var queryDeleteEvent = 'DELETE FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = ?';
          var stmtDeleteEvent = conn.prepareStatement(queryDeleteEvent);
          stmtDeleteEvent.setString(1, sheetEventId);
          var resultStmtDeleteEvent = null;

          try {
            resultStmtDeleteEvent = stmtDeleteEvent.executeUpdate();
            if (resultStmtDeleteEvent > 0) {
              Logger.log('Basvuru donemi icinde iptal edilen randevu kaydi(' +eventIdFieldName + '= ' + sheetEventId + ') silinerek appointments_old_or_deleted tablosuna tasindi.');
            } else {
              Logger.log(eventIdFieldName + ': ' + sheetEventId + ' olan kayıt bulunamadı.');
            }
          } catch (e) {
            Logger.log('Hata: ' + e);
          }
          finally {
            stmtDeleteEvent.close();    // Statement kapatılıyor
          }
        } else {
          sheet.deleteRow(i + 2); // +2 çünkü başlık satırı ve 0-tabanlı indeks
          // Silme sorgusunu hazırlayın
          var queryDeleteEventLast = 'DELETE FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = ?';
          var stmtDeleteEventLast = conn.prepareStatement(queryDeleteEventLast);
          stmtDeleteEventLast.setString(1, sheetEventId);
          var resultStmtDeleteEventLast = null;

          try {
            resultStmtDeleteEventLast = stmtDeleteEventLast.executeUpdate();
            if (resultStmtDeleteEventLast > 0) {
              Logger.log('Yeni bir basvuru donemi basladigi icin olan kayit(' + eventIdFieldName + '= ' + sheetEventId + ') silinerek old_or_deleted tablosuna tasindi.');
            } else {
              Logger.log(eventIdFieldName + '= ' + sheetEventId + ' olan kayit bulunamadi.');
            }
          } catch (e) {
            Logger.log('Hata: ' + e);
          }
          finally {
            stmtDeleteEventLast.close();    // Statement kapatılıyor
          }
        }
      }
    }
  } catch (e) {
    console.error('Error occurred: ' + e);
  } finally {
    if (conn) {
      conn.close();  // Connection kapatılıyor
    }
  }
}



// Değerleri karşılaştırma fonksiyonu - (event guncellenmis mi diye kontrol etmek icin)
function hasChanges(oldRow, newData, fields, datetimeFieldNames) {
  for (var i = 0; i < newData.length; i++) {
    if (datetimeFieldNames.includes(fields[i])) {
      oldRow[i] = convertToUTC(oldRow[i])['utcDatetime'];
      newData[i] = convertToUTC(newData[i])['utcDatetime'];
    }

    if (oldRow[i] !== newData[i]) {
      // Logger.log(i + ': ' + oldRow[i] + ' =? ' + newData[i]);
      return true;
    }
  }
  return false;
}


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
