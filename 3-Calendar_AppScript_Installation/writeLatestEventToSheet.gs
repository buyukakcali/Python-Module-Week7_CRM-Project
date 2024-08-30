function writeLatestEventToSheet() {
  var totalTimer = new Timer();
  var sectionTimer = new Timer();
  // Ekleme veya Guncelleme islemleri icin performans olcumu
  var add_updateTimer = new Timer();
  // Silme islemleri icin performans olcumu
  var deleteTimer = new Timer();
  var deletedCount = 0;
  
  var cnf = new Config();
  var dbsconn = null;

  try {
    dbsconn = cnf.openConn();  // Database connection

    // SQL veri tabani baglantisi olusturmak icin gecen sure:
    Logger.log("Veritabanı bağlantısı kuruldu. Islem suresi:: " + sectionTimer.elapsed());
    sectionTimer.reset();

    // .................. Variables Area ................... //
    var ownerOfTheCalendarMail = cnf.getOwnerOfTheCalendarMail();
    // calendarId, etkinliklerin alınacağı takvimi belirtir.
    // 'primary', kullanıcının birincil takvimini ifade eder. Alternatif olarak, belirli bir takvimin kimliği (örneğin, bir takvim URL'si) kullanılabilir.
    var calendarId = cnf.getCalendarId(); // 'primary'; // OR ownerOfTheCalendarMail;
    // .................................................... //

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Son basvuru doneminin adini al
    var lastApplicationPeriod = getLastApplicationPeriod(cnf, dbsconn);

    // SQL baglantisi ve gecen sure: getLastApplicationPeriod fonksiyonu
    Logger.log("Son başvuru dönemi adı alındı. Islem suresi::  " + sectionTimer.elapsed());
    sectionTimer.reset();

    // form_application tablosundan en son BaşvuruDönemi içindeki ilk kaydın oluşturulduğu zamanı al
    var lastApplicationPeriodStartDate = null;
    if (lastApplicationPeriod) {
      lastApplicationPeriodStartDate = getLastApplicationPeriodStartDate(cnf, dbsconn, lastApplicationPeriod);
      //  Logger.log('lastApplicationPeriodStartDate: ' + lastApplicationPeriodStartDate);
    }

    // SQL baglantisi ve gecen sure: getLastApplicationPeriodStartDate fonksiyonu
    Logger.log("Son başvuru dönemi başlangıç tarihi alındı. Islem suresi:: " + sectionTimer.elapsed());
    sectionTimer.reset();

    // Son basvuru donemi basladiktan sonraki tüm etkinlikleri al
    var events = Calendar.Events.list(calendarId, {
      timeMin: lastApplicationPeriodStartDate.toISOString(),
      orderBy: 'startTime',
      singleEvents: true,
      maxResults: 2500
    });

    // Logger.log('events: '+events);
    Logger.log("Takvim olayları alındı. Islem suresi:: " + sectionTimer.elapsed());
    sectionTimer.reset();

    var currentEventIds = new Set(events.items.map(event => event.id));
    var sheetData = sheet.getDataRange().getValues();
    var header = sheetData.shift(); // Başlık satırını ayır

    // SILME ISLEMI : Once silinecek etkinlik varsa onu sil
    deletedCount = deleteEvent(cnf, dbsconn, currentEventIds, sheetData, lastApplicationPeriod, lastApplicationPeriodStartDate);

    // Silme islemi ile ilgili performans loglari::
    if (deletedCount !== 0) {
      // Her silme olayindan sonra gecen sure logu:
      Logger.log(deletedCount + " kayit silindi. Islem suresi: " + deleteTimer.elapsed());
      deleteTimer.reset();
    }

    // GUNCELLEME VEYA EKLEME ISLEMLERI:
    // Takvimdeki guncel verileri Google Sheet'teki verilerle karsilastirarak GUNCELLE veya sheet dosyasinda yoksa EKLE
    events.items.forEach((event, index) => {
      // Logger.log('DETAY BILGISI: ' + JSON.stringify(event));
      // Logger.log('index: ' + index);
      // Logger.log('event.attendees');
      // Logger.log(event.attendees[0]['responseStatus']);
      var eventId = event.id;
      // Tum gun surecek sekilde olusturulan etkinlikler icin saat kaydini 00:00:01 olarak ayarliyoruz.
      // 00:00:00 da olabilirdi ama uluslararasi calisan bir kurulus bu saatte de normal toplanti duzenleyebilir ve karisiklik olmasin/anlasilsin diye bir saniyelik fark olusturduk.
      var startTime = event.start.dateTime ? convertToUTC(event.start.dateTime)['utcDatetime'] : convertToUTC(event.start.date + "T00:00:01")['utcDatetime'];
      // Davetlilerin e-posta adreslerini bir diziye ekleme
      var attendeeEmails = null;  // Varsayılan olarak 'null' atıyoruz
      // Eğer davetliler sheet dosyasinda varsa onlari aynen yaziyoruz
      if (sheetData[index] !== undefined){
        // Logger.log('sheetData[index][10]: ' + sheetData[index][10]);
        attendeeEmails = sheetData[index][10];
      }
      if (event.attendees && event.attendees.length > 0) {
        // Eğer davetliler varsa, onları virgülle ayrılmış bir dizeye dönüştür
        attendeeEmails = event.attendees.map(attendee => attendee.email).join(', ');
      }

      // Davetlilerin katilim durumlarini bir diziye ekleme
      var responseStatus = 'null';  // Varsayılan olarak 'null' atıyoruz
      // Eğer eski responseStatus bilgileri sheet dosyasinda varsa onlari aynen aliyoruz. Aslinda alttaki if blogu olmadan da ugulama duzgun calisir. Sadece olaganustu bir cakismada mevcut veriyi yine de korumak istedigim icin koyuyorum..
      if (sheetData[index] !== undefined){
        // Logger.log('sheetData[index][11]: ' + sheetData[index][11]);
        responseStatus = sheetData[index][11];
      }
      // En guncel katilim durumlarini aliyoruz ve responseStatus degiskenine atiyoruz.
      if (event.attendees && event.attendees.length > 0) {
        // Eğer responseStatus varsa, onları virgülle ayrılmış bir dizeye dönüştür
        responseStatus = event.attendees.map(attendee => attendee.responseStatus).join(', ');
      }

      // Takvimden gelen verilerden istenenler sozluge aliniyor.
      var eventData = {
        'crm_Timestamp':convertToUTC(event.created)['utcDatetime'] || 'null',               // Timestamp (event.created value)
        'crm_EventID':eventId || 'null',                                                    // Event ID
        'crm_InterviewDatetime':startTime || 'null',                                        // Interview datetime
        'crm_MentorMail':event.creator.email || 'null',                                     // Mentor Mail
        'crm_Summary':event.summary || 'null',                                              // summary
        'crm_Description':event.description || 'null',                                      // description
        'crm_Location':event.location || 'null',                                            // location
        'crm_OnlineMeetingLink':event.hangoutLink || 'null',                                // hangoutLink
        'crm_AttendeeEmails':attendeeEmails || 'null',                                      // Attendee Emails
        'crm_ResponseStatus':responseStatus || ['null'],                                    // All attendee's responseStatus
        // 'crm_AttendeeName':'null',                                                          // Attendee Name (Candidate)
        // 'crm_AttendeeSurname':'null'                                                        // Attendee Surname (Candidate)
      };

      var rowIndex = sheetData.findIndex(row => row[1] === eventId); // eventId'nin 2. sütunda olduğunu varsayıyoruz
      var result = null;

      // rowIndex degerine gore guncelleme veya ekleme islemine karar veriliyor
      if (rowIndex !== -1){ // sheetData[index][3]'de MentorName nin ve sheetData[index][4]'de de MentorSurname nin bulundugunu varsayiyoruz.
        if (sheetData[index][3] === 'not a Contact' || sheetData[index][4] === 'not a Contact'){
          // Mentorun Ad ve Soyadini guncellemek icin People API'ya baglanip veriyi guncellemeye calis!
          result = getPersonInfo(event.creator.email);
          eventData = insertMentorInfo(eventData, result['givenName'] || 'not a Contact', result['familyName'] || 'not a Contact');
        } else {
          // Eger mentor ad ve soyadi 'not a Contact' degilse, zaten dogru veri vardir! Aynisini koy! Burasinin baska bir Mentor tarafindan degistirilmesi en uzak olasilik (mumkun ama!). Mentorlerin kendi olusturmadiklari etkinlikleri duzenleyip sahiplenmeyeceklerini varsaymak zorundayim!
          eventData = insertMentorInfo(eventData, sheetData[index][3], sheetData[index][4]);
        }
        updateEvent(cnf, dbsconn, rowIndex, sheetData, eventData);
      } else {
        // Yeni kayit!!! Ekleme olacagi icin mutlaka API cagrisi yapilacak ve Mentorun Ad ve Soyadini almaya calisacagiz...
        result = getPersonInfo(event.creator.email);
        eventData = insertMentorInfo(eventData, result['givenName'] || 'not a Contact', result['familyName'] || 'not a Contact');
        addEvent(cnf, dbsconn, eventData);
      }

      // Ekleme ve guncelleme islemleri ile ilgili performans loglari:
      Logger.log("Tekil islem suresi: ekleme/güncelleme tamalandi, gecen süre: " + sectionTimer.elapsed()); // Her bir tekil islem suresi
      sectionTimer.reset();
      // Her 5 islemde bir performans logu: Ekleme ve guncelleme icin sadece
      if (index % 5 === 0 && index > 0) {
        Logger.log(index + " olay işlendi!!!!!: " + add_updateTimer.elapsed());
        add_updateTimer.reset();
      }
    });
  } catch (e) {
    console.error('Error occurred in writeLatestEventToSheet function: ' + e.stack);
  } finally {
    if (dbsconn) {
      cnf.closeConn(dbsconn);  // Connection kapatılıyor

      // Herhangi bir ekleme, guncelleme veya silme islemi gerceklesirse de bekleyen mentor atama islemleri gerceklestirilsin. Bunun icin ayrica zamanli triggerin(removeDuplicateEvents fonksiyonunu calistiran trigger) bir saat icinde calismasi beklenmesin!
      addAttendeesToCalendarEvent();
    }
    // Trigger calistiktan sonra toplam gecen sure logu:
    Logger.log("Tüm işlem tamamlandı. Toplam süre: " + totalTimer.elapsed());
  }
}
