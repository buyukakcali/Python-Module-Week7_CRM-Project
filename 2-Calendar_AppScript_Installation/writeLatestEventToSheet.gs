function writeLatestEventToSheet() {
  var totalTimer = new Timer();
  var sectionTimer = new Timer();
  // Ekleme veya Guncelleme islemleri icin performans olcumu
  var add_updateTimer = new Timer();
  // Silme islemleri icin performans olcumu
  var deleteTimer = new Timer();
  var deletedCount = 0;
  
  var cnf = new Config();
  
  try {
    conn = Jdbc.getConnection(cnf.getServerUrl(), cnf.getUser(), cnf.getUserPwd());

    // SQL veri tabani baglantisi olusturmak icin gecen sure:
    Logger.log("Veritabanı bağlantısı kuruldu. Islem suresi:: " + sectionTimer.elapsed());
    sectionTimer.reset();

    // .................. Variables Area ................... //
    var fields = cnf.getFields(); 
    var ownerOfTheCalendarMail = cnf.getOwnerOfTheCalendarMail();
    // calendarId, etkinliklerin alınacağı takvimi belirtir.
    // 'primary', kullanıcının birincil takvimini ifade eder. Alternatif olarak, belirli bir takvimin kimliği (örneğin, bir takvim URL'si) kullanılabilir.
    var calendarId = cnf.getCalendarId(); // 'primary'; // OR ownerOfTheCalendarMail;
    // .................................................... //

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Son basvuru doneminin adini al
    var lastApplicationPeriod = getLastApplicationPeriod(cnf, conn);

    // SQL baglantisi ve gecen sure: getLastApplicationPeriod fonksiyonu
    Logger.log("Son başvuru dönemi adı alındı. Islem suresi::  " + sectionTimer.elapsed());
    sectionTimer.reset();

    // form_basvuru tablosundan en son BaşvuruDönemi içindeki ilk kaydın oluşturulduğu zamanı al
    var lastApplicationPeriodStartDate = null;
    if (lastApplicationPeriod) {
      lastApplicationPeriodStartDate = getLastApplicationPeriodStartDate(cnf, conn, lastApplicationPeriod);
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
    Logger.log("Takvim olayları alındı. Islem suresi:: " + sectionTimer.elapsed());
    sectionTimer.reset();

    var currentEventIds = new Set(events.items.map(event => event.id));
    var sheetData = sheet.getDataRange().getValues();
    var header = sheetData.shift(); // Başlık satırını ayır

    // SILME ISLEMI : Once silinecek etkinlik varsa onu sil
    deletedCount = deleteEvent(cnf, conn, sheet, currentEventIds, sheetData, lastApplicationPeriod, lastApplicationPeriodStartDate);
    
    // Silme islemi ile ilgili performans loglari::
    if (deletedCount !== 0) {
      // Her silme olayindan sonra gecen sure logu:
      Logger.log(deletedCount + " kayit silindi. Islem suresi: " + deleteTimer.elapsed());
      deleteTimer.reset();
    }
    
    // GUNCELLEME VEYA EKLEME ISLEMLERI:
    // Takvimdeki guncel verileri Google Sheet'teki verilerle karsilastirarak GUNCELLE veya sheet dosyasinda yoksa EKLE
    events.items.forEach((event, index) => {
      var eventId = event.id;
      // Tum gun surecek sekilde olusturulan etkinlikler icin saat kaydini 00:00:01 olarak ayarliyoruz.
      // 00:00:00 da olabilirdi ama uluslararasi calisan bir kurulus bu saatte de normal toplanti duzenleyebilir diye bir saniyelik fark olusturduk. 
      var startTime = event.start.dateTime ? convertToUTC(event.start.dateTime)['utcDatetime'] : convertToUTC(event.start.date + "T00:00:01")['utcDatetime'];
      // Takvimden gelen verilerden istenenler sozluge aliniyor.
      var eventData = {
        'ZamanDamgasi':convertToUTC(event.created)['utcDatetime'] || 'null',            // Zaman Damgası (event.created değeri)
        'EtkinlikID':eventId || 'null',                                                 // Etkinlik ID
        'MulakatZamani':startTime || 'null',                                            // Mulakat Zamanı
        // Buraya MentorAdi ve MentorSoyadi ekleniyor sonra...
        'MentorMail':event.creator.email || 'null',                                     // Mentor Mail
        'Summary':event.summary || 'null',                                              // summary
        'Description':event.description || 'null',                                      // description
        'Location':event.location || 'null',                                            // location
        'OnlineMeetingLink':event.hangoutLink || 'null',                                // hangoutLink
        'ResponseStatus':event.attendees ? event.attendees[1].responseStatus : 'null'   // responseStatus - burada farkli bir yaklasim gerekebilir ilerde
      };

      var rowIndex = sheetData.findIndex(row => row[1] === eventId); // eventId'nin 2. sütunda olduğunu varsayıyoruz
      var result = null; // sheetData[index][3]'de MentorAdi nin ve sheetData[index][4]'de de MentorSoyadi nin bulundugunu varsayiyoruz.
      
      // rowIndex degerine gore guncelleme veya ekleme islemine karar veriliyor
      if (rowIndex !== -1){
        if (sheetData[index][3] === 'not a Contact' || sheetData[index][4] === 'not a Contact'){
          // Mentorun Ad ve Soyadini guncellemek icin People API'ya baglanip veriyi guncellemeye calis!
          result = getPersonInfo(event.creator.email);
          eventData = insertMentorInfo(eventData, result['givenName'] || 'not a Contact', result['familyName'] || 'not a Contact');
        } else {
          // Eger mentor ad ve soyadi 'not a Contact' degilse, zaten dogru veri vardir! Aynisini koy! Burasinin baska bir Mentor tarafindan degistirilmesi en uzak olasilik (mumkun ama!) . Mentorlerin kendi olusturmadiklari etkinlikleri duzenleyip sahiplenmeyeceklerini varsaymak zorundayim!
          eventData = insertMentorInfo(eventData, sheetData[index][3], sheetData[index][4]);
        }
        updateEvent(cnf, conn, sheet, rowIndex, sheetData, eventData);
      } else {
        // Yeni kayit!!! Ekleme olacagi icin mutlaka API cagrisi yapilacak ve Mentorun Ad ve Soyadini almaya calisacagiz...
        result = getPersonInfo(event.creator.email);
        eventData = insertMentorInfo(eventData, result['givenName'] || 'not a Contact', result['familyName'] || 'not a Contact');
        addEvent(cnf, conn, eventData);
      }

      // Ekleme ve guncelleme islemleri ile ilgili performans loglari:
      Logger.log("Tekil islem suresi: ekleme/güncelleme tamalandi, gecen süre: " + sectionTimer.elapsed()); // Her bir tekil islem suresi
      sectionTimer.reset();
      // Her 5 islemde bir performans logu : Ekleme ve guncelleme icin sadece
      if (index % 5 === 0 && index > 0) {
        Logger.log(index + " olay işlendi!!!!!: " + add_updateTimer.elapsed());
        add_updateTimer.reset();
      }
    });
  } catch (e) {
    console.error('Error occurred in writeLatestEventToSheet function: ' + e);
  } finally {
    if (conn) {
      conn.close();  // Connection kapatılıyor
    }
    // Trigger calistiktan sonra toplam gecen sure logu:
    Logger.log("Tüm işlem tamamlandı. Toplam süre: " + totalTimer.elapsed());
  }
}