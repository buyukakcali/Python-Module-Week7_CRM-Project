/*  appscript.json,
    Config-Timer.gs,
    html template dosyalari (wrongEventCreationMailTemplate.html, evaluationMailTemplate.html vd.) ile
    Installation Properties.png dosyalari haric diger tum dosyalarda/modullerde yazilmis olan fonksiyonlar bu dosyanin
    icindedir.
    Yani yukaridaki adi verilen dosyalar ve bu Code.gs dosyasi kurulum icin yeterlidir.
*/

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

    // // SQL veri tabani baglantisi olusturmak icin gecen sure:
    // Logger.log("Veritabanı bağlantısı kuruldu. Islem suresi:: " + sectionTimer.elapsed());
    // sectionTimer.reset();

    // .................. Variables Area ................... //
    var ownerOfTheCalendarMail = cnf.getOwnerOfTheCalendarMail();
    // calendarId, etkinliklerin alınacağı takvimi belirtir.
    // 'primary', kullanıcının birincil takvimini ifade eder. Alternatif olarak, belirli bir takvimin kimliği (örneğin, bir takvim URL'si) kullanılabilir.
    var calendarId = cnf.getCalendarId(); // 'primary'; // OR ownerOfTheCalendarMail;
    // .................................................... //

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Son basvuru doneminin adini al
    var lastApplicationPeriod = getLastApplicationPeriod(cnf, dbsconn);

    // // SQL baglantisi ve gecen sure: getLastApplicationPeriod fonksiyonu
    // Logger.log("Son başvuru dönemi adı alındı. Islem suresi::  " + sectionTimer.elapsed());
    // sectionTimer.reset();

    // form_application tablosundan en son BaşvuruDönemi içindeki ilk kaydın oluşturulduğu zamanı al
    var lastApplicationPeriodStartDate = null;
    if (lastApplicationPeriod) {
      lastApplicationPeriodStartDate = getLastApplicationPeriodStartDate(cnf, dbsconn, lastApplicationPeriod);
      //  Logger.log('lastApplicationPeriodStartDate: ' + lastApplicationPeriodStartDate);
    }

    // // SQL baglantisi ve gecen sure: getLastApplicationPeriodStartDate fonksiyonu
    // Logger.log("Son başvuru dönemi başlangıç tarihi alındı. Islem suresi:: " + sectionTimer.elapsed());
    // sectionTimer.reset();

    // Son basvuru donemi basladiktan sonraki tüm etkinlikleri al
    var events = Calendar.Events.list(calendarId, {
      timeMin: lastApplicationPeriodStartDate.toISOString(),
      orderBy: 'startTime',
      singleEvents: true,
      maxResults: 2500
    });

    // // Logger.log('events: '+events);
    // Logger.log("Takvim olayları alındı. Islem suresi:: " + sectionTimer.elapsed());
    // sectionTimer.reset();

    var currentEventIds = new Set(events.items.map(event => event.id));
    var sheetData = sheet.getDataRange().getValues();
    var header = sheetData.shift(); // Başlık satırını ayır

    // SILME ISLEMI : Once silinecek etkinlik varsa onu sil
    deletedCount = deleteEvent(cnf, dbsconn, currentEventIds, sheetData, lastApplicationPeriod, lastApplicationPeriodStartDate);

    // // Silme islemi ile ilgili performans loglari::
    // if (deletedCount !== 0) {
    //   if (deletedCount === 1) {
    //     // Her silme olayindan sonra gecen sure logu:
    //     Logger.log(deletedCount + " record is deleted. Processing time: " + deleteTimer.elapsed());
    //     deleteTimer.reset();
    //   } else {
    //     // Her silme olayindan sonra gecen sure logu:
    //     Logger.log(deletedCount + " records are deleted. Processing time: " + deleteTimer.elapsed());
    //     deleteTimer.reset();
    //   }
    // }

    // GUNCELLEME VEYA EKLEME ISLEMLERI:
    // Takvimdeki guncel verileri Google Sheet'teki verilerle karsilastirarak GUNCELLE veya sheet dosyasinda yoksa EKLE
    events.items.forEach((event) => {
      // Logger.log('DETAY BILGISI: ' + JSON.stringify(event));
      // Logger.log('event.attendees');
      // Logger.log(event.attendees[0]['responseStatus']);
      var eventId = event.id;
      // Tum gun surecek sekilde olusturulan etkinlikler icin saat kaydini 00:00:01 olarak ayarliyoruz.
      // 00:00:00 da olabilirdi ama uluslararasi calisan bir kurulus bu saatte de normal toplanti duzenleyebilir ve karisiklik olmasin/anlasilsin diye bir saniyelik fark olusturduk.
      var startTime = event.start.dateTime ? convertToUTC(event.start.dateTime)['utcDatetime'] : convertToUTC(event.start.date + "T00:00:01")['utcDatetime'];
      // Davetlilerin e-posta adreslerini bir diziye ekleme
      var attendeeEmails = null;  // Varsayılan olarak 'null' atıyoruz
      // Eğer davetliler sheet dosyasinda varsa onlari aynen yaziyoruz
      var rowIndex = sheetData.findIndex(row => row[1] === eventId); // eventId'nin 2. sütunda olduğunu varsayıyoruz

      if (sheetData[rowIndex] !== undefined){
        // Logger.log('sheetData[rowIndex][10]: ' + sheetData[rowIndex][10]);
        attendeeEmails = sheetData[rowIndex][10];
      }
      if (event.attendees && event.attendees.length > 0) {
        // Eğer davetliler varsa, onları virgülle ayrılmış bir dizeye dönüştür
        attendeeEmails = event.attendees.map(attendee => attendee.email.trim().toLowerCase()).join(', ');
      }

      // Davetlilerin katilim durumlarini bir diziye ekleme
      var responseStatus = 'null';  // Varsayılan olarak 'null' atıyoruz
      // Eğer eski responseStatus bilgileri sheet dosyasinda varsa onlari aynen aliyoruz. Aslinda alttaki if blogu olmadan da ugulama duzgun calisir. Sadece olaganustu bir cakismada mevcut veriyi yine de korumak istedigim icin koyuyorum..
      if (sheetData[rowIndex] !== undefined){
        // Logger.log('sheetData[rowIndex][11]: ' + sheetData[rowIndex][11]);
        responseStatus = sheetData[rowIndex][11];
      }
      // En guncel katilim durumlarini aliyoruz ve responseStatus degiskenine atiyoruz.
      if (event.attendees && event.attendees.length > 0) {
        // Eğer responseStatus varsa, onları virgülle ayrılmış bir dizeye dönüştür
        responseStatus = event.attendees.map(attendee => attendee.responseStatus).join(', ');
      }

      // Takvimden gelen verilerden istenenler sozluge aliniyor.
      var eventData = {
        'crm_Timestamp': convertToUTC(event.created)['utcDatetime'] || 'null',                           // Timestamp (event.created value)
        'crm_EventID': eventId || 'null',                                                                // Event ID
        'crm_InterviewDatetime': startTime || 'null',                                                    // Interview datetime
        'crm_MentorMail': (event.creator.email && event.creator.email.trim().toLowerCase()) || 'null',   // Mentor Mail
        'crm_Summary': (event.summary && event.summary.trim()) || 'null',                                // Trim only if event.summary exists
        // alttaki satirda html taglari temizleniyor. yalniz bu durum daha sonraki amacimiza hizmet etmeyebilir! degerlendirilmeli!!!
        // 'crm_Description': (event.description && event.description.replace(/<\/?[^>]+(>|$)/g, "").trim()) || 'null',  // Same for description
        'crm_Description': (event.description && event.description.trim()) || 'null',                    // Same for description
        'crm_Location': event.location || 'null',                                                        // location
        'crm_OnlineMeetingLink': event.hangoutLink || 'null',                                            // hangoutLink
        'crm_AttendeeEmails': attendeeEmails || 'null',                                                  // Attendee Emails
        'crm_ResponseStatus': responseStatus || ['null'],                                                // All attendee's responseStatus
      };


      // var rowIndex = sheetData.findIndex(row => row[1] === eventId); // eventId'nin 2. sütunda olduğunu varsayıyoruz
      var result = null;

      // rowIndex degerine gore guncelleme veya ekleme islemine karar veriliyor
      if (rowIndex !== -1){ // sheetData[rowIndex][3]'de MentorName nin ve sheetData[rowIndex][4]'de de MentorSurname nin bulundugunu varsayiyoruz.
        if (sheetData[rowIndex][3] === 'not a Contact' || sheetData[rowIndex][4] === 'not a Contact'){
          // Mentorun Ad ve Soyadini guncellemek icin People API'ya baglanip veriyi guncellemeye calis!
          result = getPersonInfo(sheetData[rowIndex][5]);  // Mentor Mail bilgisinin 6. sutunda oldugunu varsayiyoruz.
          if (result) {
            eventData = insertMentorInfo(eventData, result['givenName'] || 'not a Contact', result['familyName'] || 'not a Contact');
          } else {
            eventData = insertMentorInfo(eventData, 'not a Contact', 'not a Contact');
          }
          // eventData = insertMentorInfo(eventData, result['givenName'] || 'not a Contact', result['familyName'] || 'not a Contact');
        } else {
          // Eger mentor ad ve soyadi 'not a Contact' degilse, zaten dogru veri vardir! Aynisini koy! Burasinin baska bir Mentor tarafindan degistirilmesi en uzak olasilik (mumkun ama!). Mentorlerin kendi olusturmadiklari etkinlikleri duzenleyip sahiplenmeyeceklerini varsaymak zorundayim!
          eventData = insertMentorInfo(eventData, sheetData[rowIndex][3], sheetData[rowIndex][4]);
        }
        updateEvent(cnf, dbsconn, rowIndex, sheetData, eventData);
        // if (!(eventData['crm_Summary'].startsWith('1') || eventData['crm_Summary'].startsWith('2') || eventData['crm_Summary'].startsWith('3'))) {
        //   Logger.log('Hatali/Eksik/Uyumsuz Etkinlik Guncellemesi; ilgiliye bilgi veriliyor..');
        //   Logger.log('DETAY BILGISIupdate: ' + JSON.stringify(eventData));
        //   var wrongEventUpdateMailTemplate = cnf.getWrongEventUpdateMailTemplate();
        //   sendEmail(eventData[cnf.getMentorMailFieldName()], wrongEventUpdateMailTemplate, eventData);
        // }

      } else {
        // Yeni kayit!!! Ekleme olacagi icin mutlaka API cagrisi yapilacak ve Mentorun Ad ve Soyadini almaya calisacagiz...
        result = getPersonInfo(event.creator.email);
        if (result) {
          eventData = insertMentorInfo(eventData, result['givenName'] || 'not a Contact', result['familyName'] || 'not a Contact');
        } else {
          eventData = insertMentorInfo(eventData, 'not a Contact', 'not a Contact');
        }
        // eventData = insertMentorInfo(eventData, result['givenName'] || 'not a Contact', result['familyName'] || 'not a Contact');
        addEvent(cnf, dbsconn, eventData);
        if (!(eventData['crm_Summary'].startsWith('1') || eventData['crm_Summary'].startsWith('2') || eventData['crm_Summary'].startsWith('3'))) {
          Logger.log('Hatali/Eksik/Uyumsuz Etkinlik Olusturma; ilgiliye bilgi veriliyor..');
          var wrongEventCreationMailTemplate = cnf.getWrongEventCreationMailTemplate();
          sendEmail(eventData[cnf.getMentorMailFieldName()], wrongEventCreationMailTemplate, eventData);
        }
      }
    });
    // // Ekleme ve guncelleme islemleri ile ilgili performans loglari:
    // Logger.log("Ekleme/güncelleme islemleri tamalandi, gecen süre: " + sectionTimer.elapsed());
    // sectionTimer.reset();
  } catch (e) {
    console.error('Error occurred in writeLatestEventToSheet function: ' + e.stack);
  } finally {
    if (dbsconn) {
      cnf.closeConn(dbsconn);  // Connection kapatılıyor

      // Herhangi bir ekleme, guncelleme veya silme islemi gerceklesirse de bekleyen mentor atama islemleri gerceklestirilsin. Bunun icin ayrica zamanli triggerin(removeDuplicateEvents fonksiyonunu calistiran trigger) bir saat icinde calismasi beklenmesin!
      // addAttendeesToCalendarEvent();
    }
    // // Trigger calistiktan sonra toplam gecen sure logu:
    // Logger.log("Tüm işlem tamamlandı. Toplam süre: " + totalTimer.elapsed());
  }
}

function addEvent(cnf_, conn_, eventData_) {
  // .................. Variables Area ................... //
  var appointmentsTable = cnf_.getAppointmentsTable();
  var eventIdFieldName = cnf_.getEventIdFieldName();
  var datetimeFieldNames = cnf_.getDatetimeFieldNames();
  // ..................................................... //

  try {
    var whitelist = getWhitelist(); // get whitelist

    var usedTablesInThisFunction = [appointmentsTable];
    var columns = Object.keys(eventData_);
    columns.push(eventIdFieldName);

    usedTablesInThisFunction.forEach(table => {
      if (whitelist.validTables.includes(table) == false) {
        throw new Error('Invalid table name: '+ table);
      }
    });

    columns.forEach(column => {
      if (!whitelist.validColumns.includes(column)) {
        throw new Error('Invalid column name: ' + column);
      }
    });

    // Sheet'e yeni satir ekle (yeni randevu-etkinlik)
    addUniqueEvent(eventData_);

    // Database'e yeni kayit ekle
    var queryInsertEvent = 'INSERT INTO ' + appointmentsTable + ' (';
    queryInsertEvent += Object.keys(eventData_).join(', ') + ') VALUES (' + Object.keys(eventData_).map(() => '?').join(', ') + ')';
    var stmtInsertEvent = conn_.prepareStatement(queryInsertEvent, Jdbc.Statement.RETURN_GENERATED_KEYS);
    // Logger.log('Query string: ' + queryInsertEvent);

    // Veri sorgu metnindeki yerine atanir.
    for (var i = 0; i < Object.values(eventData_).length; i++) {
      if (datetimeFieldNames.includes(Object.keys(eventData_)[i])) {
        stmtInsertEvent.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(eventData_)[i]));
      } else if (typeof(Object.values(eventData_)[i]) === 'string'){
        stmtInsertEvent.setString(i + 1, Object.values(eventData_)[i]);
      } else if (typeof(Object.values(eventData_)[i]) === 'number'){
        stmtInsertEvent.setInt(i + 1, Object.values(eventData_)[i]);
      } else if (typeof(Object.values(eventData_)[i]) === 'null'){
        stmtInsertEvent.setNull(i + 1, Jdbc.Types.INTEGER); // INTEGER yerine, tekrar null yapacaginiz sutunda ne tur veri olmasini planlamissaniz onu yazin!
      } else {
        Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
      }
    }

    var resultStmtInsertEvent = null;
    try {
      resultStmtInsertEvent = stmtInsertEvent.executeUpdate();
      if (resultStmtInsertEvent) {
        // Logger.log('resultStmtInsertEvent: ' + resultStmtInsertEvent);
        Logger.log('Google Sheet dosyasina ve Databse\'deki '+ appointmentsTable +' tablosuna yeni kayit(' + eventIdFieldName + '= ' + eventData_[eventIdFieldName] + ') EKLENDI.');
      }
    } catch (e) {
      console.error('Error: ' + e.stack);
    } finally {
      stmtInsertEvent.close();  // Statement kapatılıyor
      return resultStmtInsertEvent;
    }
  } catch (e) {
    console.error('Error occurred in addEvent function: ' + e.stack);
  }
}

function updateEvent(cnf_, conn_, rowIndex_, sheetData_, eventData_) {
  // .................. Variables Area ................... //
  var appointmentsTable = cnf_.getAppointmentsTable();
  var eventIdFieldName = cnf_.getEventIdFieldName();
  var datetimeFieldNames = cnf_.getDatetimeFieldNames();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  // ..................................................... //

  try {
    var whitelist = getWhitelist(); // get whitelist

    var usedTablesInThisFunction = [appointmentsTable];
    var columns = Object.keys(eventData_);
    columns.push(eventIdFieldName);

    usedTablesInThisFunction.forEach(table => {
      if (whitelist.validTables.includes(table) == false) {
        throw new Error('Invalid table name: '+ table);
      }
    });

    columns.forEach(column => {
      if (!whitelist.validColumns.includes(column)) {
        throw new Error('Invalid column name: ' + column);
      }
    });

    // Etkinlik zaten var, verilerde bir degisim var mi kontrol et, varsa güncelle!
    var existingRow = sheetData_[rowIndex_];
    // Logger.log('Existing data: ' + existingRow);
    // Logger.log('New_____ data: ' + eventData_);
    // Logger.log('hasChanges(existingRow, eventData_, datetimeFieldNames): ' + hasChanges(existingRow, eventData_, datetimeFieldNames));

    // Bu fonksiyonla, ilgili etkinlikte herhangi bir degisiklik olup olmadigi kontrol ediliyor. Eger degisim varsa guncelleniyor, yoksa siradakine geciliyor. Boylece islemci gucu tasarruf ediliyor ve zaman kazaniliyor. Gereksiz yeniden yazma islemi yapilmiyor.
    if (hasChanges(existingRow, eventData_, datetimeFieldNames)) {
      // Sheet'deki satiri guncelle
      sheet.getRange(rowIndex_ + 2, 1, 1, Object.values(eventData_).length).setValues([Object.values(eventData_)]);

      // Database'deki veriyi guncelle:
      var queryUpdateEvent = 'UPDATE ' + appointmentsTable + ' SET ';
      queryUpdateEvent += Object.keys(eventData_).join(' = ?, ') + '= ? WHERE ' + eventIdFieldName + ' = ?';
      var stmtUpdateEvent = conn_.prepareStatement(queryUpdateEvent);
      // Logger.log('Query string: ' + queryUpdateEvent);

      // Veri sorgu metnindeki yerine atanir.
      for (var i = 0; i < Object.keys(eventData_).length; i++) {
        if (datetimeFieldNames.includes(Object.keys(eventData_)[i].split(' ')[0])) {
          stmtUpdateEvent.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(eventData_)[i]));
        } else if (typeof(Object.values(eventData_)[i]) === 'string'){
          stmtUpdateEvent.setString(i + 1, Object.values(eventData_)[i]);
        } else if (typeof(Object.values(eventData_)[i]) === 'number'){
          stmtUpdateEvent.setInt(i + 1, Object.values(eventData_)[i]);
        } else if (typeof(Object.values(eventData_)[i]) === 'null'){
          stmtUpdateEvent.setNull(i + 1, Jdbc.Types.INTEGER); // INTEGER yerine, tekrar null yapacaginiz sutunda ne tur veri olmasini planlamissaniz onu yazin!
        } else {
          Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
        }
        // Logger.log('Object.keys(eventData_)['+i+']: ' + Object.values(eventData_)[i]);
      }
      stmtUpdateEvent.setString(Object.values(eventData_).length + 1, eventData_[eventIdFieldName]);  // eventIdFieldName's value is added

      var resultStmtUpdateEvent = null;
      try {
        resultStmtUpdateEvent = stmtUpdateEvent.executeUpdate();
        if (resultStmtUpdateEvent){
          // Logger.log('resultStmtUpdateEvent===>: ' + resultStmtUpdateEvent);
          Logger.log('Google Sheet dosyasindaki ve Databse\'deki '+ appointmentsTable +' tablosundaki kayit(' + eventIdFieldName + '= ' + eventData_[eventIdFieldName] + ') GUNCELLENDI.');
        }
      } catch (e) {
        console.error('Error: ' + e.stack);
      } finally {
        stmtUpdateEvent.close();      // Statement kapatılıyor
        return resultStmtUpdateEvent;
      }
    }
  } catch (e) {
    console.error('Error occurred in updateEvent function: ' + e.stack);
  }
}

// This function is SQL INJECTION DANGER free function.
// But in other functions, I tried another type of method (using WhiteLists for table and column names).

function deleteEvent(cnf_, conn_, currentEventIds_, sheetData_, lastApplicationPeriod_, lastApplicationPeriodStartDate_) {
  // .................................DELETION PROCEDURES ........................................... //
  var deletedCount_ = 0;

  // .................. Variables Area ................... //
  // var applicationTable = cnf_.getApplicationTable();
  // var applicationPeriodFieldName = cnf_.getApplicationPeriodFieldName();
  // var firstInterviewFieldName = cnf_.getFirstInterviewFieldName();
  // var applicantIdFieldName = cnf_.getApplicantIdFieldName();

  // var appointmentsTable = cnf_.getAppointmentsTable();
  // var eventIdFieldName = cnf_.getEventIdFieldName();
  var attendeeIdFiledName = cnf_.getAttendeeIdFieldName();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  // ..................................................... //

  try {
    // Check and remove deleted or expired events
    for (var i = sheetData_.length - 1; i >= 0; i--) {
      var sheetEventId = sheetData_[i][1]; // We assume eventId is in column 2
      var summaryFromSheet = sheetData_[i][6].toString(); // We assume summary is in column 7
      // Logger.log('summaryFromSheet: ' + summaryFromSheet);
      if (currentEventIds_.has(sheetEventId) === false) {
        // Logger.log('Only the section about deleted items needs to be filled in!')

        // NOT: If the lastApplicationPeriodStartDate value is greater than InterviewDatetime, that is, if a new application period is opened, the MentorApplication process is not automatically canceled. This code only prevents any confusion that may occur if the appointment has been deleted in some way. For example, the mentor has created an appointment date. After that, the CRM Application user/manager assigned an applicant to the appointment created by this mentor. However, if the mentor deletes the appointment without informing the manager, we will automatically cancel the mentor appointment process for the applicant.
        // Buraya bir de mail atma islevi konularak Basvuran ve Yoneticinin bilgilendirilmesi saglanabilir.

        Logger.log(lastApplicationPeriodStartDate_ + '<?' + sheetData_[i][2]);
        if (lastApplicationPeriodStartDate_ < sheetData_[i][2]){ // This works for appointments that are deleted while the final application period is in progress!
          var queryIsAssignedAppointment = `SELECT crm_AttendeeID FROM appointments_current WHERE crm_EventID = ?`;
          var stmtIsAssignedAppointment = conn_.prepareStatement(queryIsAssignedAppointment);
          stmtIsAssignedAppointment.setString(1, sheetEventId);

          var attendeeId = null;
          var resultIsAssignedAppointment = null;

          try {
            resultIsAssignedAppointment = stmtIsAssignedAppointment.executeQuery();
            if (resultIsAssignedAppointment.next()) {
              attendeeId = resultIsAssignedAppointment.getInt(attendeeIdFiledName);  // AttendeeID value will be here
            }
          } catch (e) {
            console.error('Error: ' + e.stack);
          } finally {
            stmtIsAssignedAppointment.close();    // Statement is closing
            resultIsAssignedAppointment.close();  // ResultSet is closing
          }

          if (attendeeId !== 0 && attendeeId !== null) {
            //  Logger.log('It is entered here to empty the appointment values of the applicants who have been assigned a mentor in the relevant tables and then delete them!');
            // Empty the record from appointments table
            var queryUnassignAppointment = 'UPDATE appointments_current SET crm_AttendeeID = ? WHERE crm_EventID = ?';
            var stmtUnassignAppointment = conn_.prepareStatement(queryUnassignAppointment);
            stmtUnassignAppointment.setNull(1, Jdbc.Types.INTEGER);
            stmtUnassignAppointment.setString(2, sheetEventId);
            // Logger.log('Query string: ' + queryUnassignAppointment);
            var resultUnassignAppointment = null;

            if (summaryFromSheet && summaryFromSheet.trim()[0].startsWith('1')) {
              // First Interview Appointment
              // Empty the record from form_application table too
              var queryUnassignApplicant = 'UPDATE form1_application SET crm_FirstInterview = ? WHERE crm_ApplicantID = ? AND crm_Period = ?';
              var stmtUnassignApplicant = conn_.prepareStatement(queryUnassignApplicant);
              stmtUnassignApplicant.setInt(1, 0);
              stmtUnassignApplicant.setInt(2, attendeeId);
              stmtUnassignApplicant.setString(3, lastApplicationPeriod_);
              // Logger.log('Query string: ' + queryUnassignApplicant)
              var resultUnassignApplicant = null;

              try {
                resultUnassignAppointment = stmtUnassignAppointment.executeUpdate();
                resultUnassignApplicant = stmtUnassignApplicant.executeUpdate();

                // Logger.log('resultUnassignAppointment: ' + resultUnassignAppointment);
                // Logger.log('resultUnassignApplicant: ' + resultUnassignApplicant);
                if (resultUnassignAppointment && resultUnassignApplicant) {
                  Logger.log('Mentor appointment has been withdrawn/cancelled!\nDetails: The assignments in tables \'appointments\'  and \'application\' have been updated to null and 0');
                }
              } catch (e) {
                console.error('Error: ' + e.stack);
              } finally {
                stmtUnassignAppointment.close();    // 1. statement is closing
                stmtUnassignApplicant.close();      // 2. statement is closing
              }

            } else if (summaryFromSheet && summaryFromSheet.trim()[0].startsWith('2')) {
                // Project Interview Appointment
                // Empty the record from form_application table too
              var queryUnassignCandidate = 'UPDATE form2_evaluations SET crm_IsApplicantACandidate = ? WHERE crm_ApplicantID = ? AND crm_Period = ?';
              var stmtUnassignCandidate = conn_.prepareStatement(queryUnassignCandidate);
              stmtUnassignCandidate.setInt(1, 1);
              stmtUnassignCandidate.setInt(2, attendeeId);
              stmtUnassignCandidate.setString(3, lastApplicationPeriod_);
              // Logger.log('Query string: ' + queryUnassignCandidate)
              var resultUnassignCandidate = null;

              try {
                resultUnassignAppointment = stmtUnassignAppointment.executeUpdate();
                resultUnassignCandidate = stmtUnassignCandidate.executeUpdate();

                // Logger.log('resultUnassignAppointment: ' + resultUnassignAppointment);
                // Logger.log('resultUnassignCandidate: ' + resultUnassignCandidate);
                if (resultUnassignAppointment && resultUnassignCandidate) {
                  Logger.log('Mentor appointment has been withdrawn/cancelled!\nDetails: The assignments in tables \'appointments\'  and \'evaluations\' have been updated to null and 1');
                }
              } catch (e) {
                console.error('Error: ' + e.stack);
              } finally {
                stmtUnassignAppointment.close();    // 1. statement is closing
                stmtUnassignCandidate.close();      // 2. statement is closing
              }
            } else {
              Logger.log('For any other thing');
              Logger.log('Summary: ' + summaryFromSheet);
            }
          }

          sheet.deleteRow(i + 2); // +2 because header row and 0-based index
          // Prepare the delete query
          var queryDeleteEvent = 'DELETE FROM appointments_current WHERE crm_EventID = ?';
          var stmtDeleteEvent = conn_.prepareStatement(queryDeleteEvent);
          stmtDeleteEvent.setString(1, sheetEventId);

          var resultStmtDeleteEvent = null;
          try {
            resultStmtDeleteEvent = stmtDeleteEvent.executeUpdate();
            if (resultStmtDeleteEvent > 0) {
              Logger.log('Appointment record(Event Id= ' + sheetEventId + ') canceled during the application period was deleted and moved to the appointments_old_or_deleted table.');
            } else {
              Logger.log('No record (Event Id= ' + sheetEventId + ') was found.');
            }
          } catch (e) {
            console.error('Error: ' + e.stack);
          }
          finally {
            stmtDeleteEvent.close();    // Statement is closing
          }
        } else {
          // Buraya mevcut sheet dosyasinin bir kopyasini arsivleyen bir kod yazabiliriz. Databasedekinden ziyade yedek olarak kalir. Sormak lazim once, zira bence gereksiz...
          sheet.deleteRow(i + 2); // +2 because header row and 0-based index
          // Prepare the delete query
          var queryDeleteEventLast = 'DELETE FROM appointments_current WHERE crm_EventID = ?';
          var stmtDeleteEventLast = conn_.prepareStatement(queryDeleteEventLast);
          stmtDeleteEventLast.setString(1, sheetEventId);

          var resultStmtDeleteEventLast = null;
          try {
            resultStmtDeleteEventLast = stmtDeleteEventLast.executeUpdate();
            if (resultStmtDeleteEventLast > 0) {
              Logger.log('Due to the start of the new application period, the appointment record(Event Id= ' + sheetEventId + ') has been deleted and moved to the appointments_old_or_deleted table.');
            } else {
              Logger.log('No record (Event Id= ' + sheetEventId + ') was found.');
            }
          } catch (e) {
            console.error('Error: ' + e.stack);
          }
          finally {
            stmtDeleteEventLast.close();    // Statement is closing
          }
        }
        deletedCount_++;
      }
    }
  } catch (e) {
    console.error('Error occurred in deleteEvent function: ' + e.stack);
  } finally {
    return deletedCount_;
  }
}

function getWhitelist() {
  try {
    var scriptProperties = PropertiesService.getScriptProperties();

    var validTables = scriptProperties.getProperty('VALID_TABLES').split(', ');
    var validColumns = scriptProperties.getProperty('VALID_COLUMNS').split(', ');

    return {
      validTables: validTables,
      validColumns: validColumns
    };
  } catch (e) {
    console.error('Error occurred in getWhitelist function: ' + e.stack);
  }
}

function getLastApplicationPeriod(cnf_, conn_) {
  // .................. Variables Area ................... //
  var applicationTable = cnf_.getApplicationTable();
  var applicationPeriodFieldName = cnf_.getApplicationPeriodFieldName();
  // ..................................................... //

  try {
    var whitelist = getWhitelist(); // get whitelist

    var usedTablesInThisFunction = [applicationTable];
    var columns = [applicationPeriodFieldName];

    usedTablesInThisFunction.forEach(table => {
      if (whitelist.validTables.includes(table) == false) {
        throw new Error('Invalid table name: '+ table);
      }
    });

    columns.forEach(column => {
      if (!whitelist.validColumns.includes(column)) {
        throw new Error('Invalid column name: ' + column);
      }
    });


    var queryLastApplicationPeriod = 'SELECT ' + applicationPeriodFieldName + ' FROM ' + applicationTable + ' ORDER BY CAST(SUBSTRING(' + applicationPeriodFieldName + ', 4) AS UNSIGNED) DESC LIMIT 1';
    var stmtLastApplicationPeriod = conn_.createStatement();

    var resultLastApplicationPeriod = null;
    var lastApplicationPeriod_ = null;
    try {
      resultLastApplicationPeriod = stmtLastApplicationPeriod.executeQuery(queryLastApplicationPeriod);
      if (resultLastApplicationPeriod.next()) {
        lastApplicationPeriod_ = resultLastApplicationPeriod.getString(applicationPeriodFieldName);
      }
    } finally {
      resultLastApplicationPeriod.close();  // ResultSet kapatılıyor
      stmtLastApplicationPeriod.close();    // Statement kapatılıyor
    }
    // Logger.log('Last application period name: ' + lastApplicationPeriod_);
  } catch (e) {
    console.error('Error occurred in getLastApplicationPeriod function: ' + e.stack);
  }
  finally {
    return lastApplicationPeriod_;
  }
}

function getLastApplicationPeriodStartDate(cnf_, conn_, lastApplicationPeriod_ ) {
  // .................. Variables Area ................... //
  var applicationTable = cnf_.getApplicationTable();
  var applicationPeriodFieldName = cnf_.getApplicationPeriodFieldName();
  var datetimeFieldNames = cnf_.getDatetimeFieldNames();
  // ..................................................... //

  try {
    var whitelist = getWhitelist(); // get whitelist

    var usedTablesInThisFunction = [applicationTable];
    var columns = [applicationPeriodFieldName, datetimeFieldNames[0], datetimeFieldNames[1]];

    usedTablesInThisFunction.forEach(table => {
      if (whitelist.validTables.includes(table) == false) {
        throw new Error('Invalid table name: '+ table);
      }
    });

    columns.forEach(column => {
      if (!whitelist.validColumns.includes(column)) {
        throw new Error('Invalid column name: ' + column);
      }
    });


    var queryLastApplicationPeriodStartDate = 'SELECT MIN('+ datetimeFieldNames[0] +') FROM '+applicationTable+' WHERE '+applicationPeriodFieldName+' = ? LIMIT 1';
    var stmtLastApplicationPeriodStartDate = conn_.prepareStatement(queryLastApplicationPeriodStartDate);
    // Veri sorgu metnindeki yerine atanir.
    stmtLastApplicationPeriodStartDate.setString(1, lastApplicationPeriod_);
    // Logger.log('Sorgu metni: ' + queryLastApplicationPeriodStartDate);

    var resultLastApplicationPeriodStartDate = null;
    var lastApplicationPeriodStartDate_ = null;
    try {
      resultLastApplicationPeriodStartDate = stmtLastApplicationPeriodStartDate.executeQuery();
      if (resultLastApplicationPeriodStartDate.next()) {
        lastApplicationPeriodStartDate_ = new Date(resultLastApplicationPeriodStartDate.getTimestamp(1).getTime());
      }
    } catch (e) {
      console.error('Error: ' + e.stack);
    } finally {
      resultLastApplicationPeriodStartDate.close();  // ResultSet kapatılıyor
      stmtLastApplicationPeriodStartDate.close();    // Statement kapatılıyor
    }
    // Logger.log('Son basvuru donemi icin baslangic tarihi: ' + lastApplicationPeriodStartDate);
  } catch (e) {
    console.error('Error occurred in getLastApplicationPeriodStartDate function: ' + e.stack);
  }
  finally {
    return lastApplicationPeriodStartDate_;;
  }
}

// // Google People API'yi kullanmak için OAuth2 kütüphanesini ekleyin
// // Kütüphane Kimliği: 1B7FSrk5Zi6L1rSxxTDgDEUsPzlukDsi4KGuTMorsTQHhGBzBkMun4iDF
var SCOPE = 'https://www.googleapis.com/auth/contacts.readonly';
var TOKEN_PROPERTY_NAME = 'people_api_token';


// OAuth2 kurulumu ve kimlik doğrulama işlemi
function getOAuthService() {
  try {
    var cnf = new Config();
    var CLIENT_ID = cnf.getClientId();
    var CLIENT_SECRET = cnf.getSecretKey();

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
  } catch (e) {
    console.error('Error occurred in getOAuthService function: ' + e.stack);
  }
}

function authCallback(request) {
  try {
    var oauthService = getOAuthService();
    var authorized = oauthService.handleCallback(request);
    if (authorized) {
      return HtmlService.createHtmlOutput('Başarıyla yetkilendirildi.').setWidth(500).setHeight(150);
    } else {
      return HtmlService.createHtmlOutput('Yetkilendirme başarısız.').setWidth(500).setHeight(150);
    }
  } catch (e) {
    console.error('Error occurred in authCallback function: ' + e.stack);
  }
}

function getPersonInfo(email) {
  try {
    var oauthService = getOAuthService();
    if (!oauthService.hasAccess()) {
      var authorizationUrl = oauthService.getAuthorizationUrl();
      Logger.log('Aşağıdaki URL\'yi ziyaret edin ve yetkilendirme işlemini tamamlayın: %s', authorizationUrl);
      return HtmlService.createHtmlOutput('Aşağıdaki URL\'yi ziyaret edin ve yetkilendirme işlemini tamamlayın: <a href="' + authorizationUrl + '" target="_blank">' + authorizationUrl + '</a>');
    }

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

    // Logger.log('Total connections retrieved: ' + connections.length);

    var person = connections.find(function(connection) {
      return connection.emailAddresses &&
             connection.emailAddresses.some(function(emailObj) {
               return emailObj.value.toLowerCase() === email.toLowerCase();
             });
    });

    if (person) {
      var name = person.names ? person.names[0].displayName : "Name not found";
      return {
        fullName: name,
        givenName: person.names ? person.names[0].givenName : "Name not found",
        familyName: person.names ? person.names[0].familyName : "Surname not found"
      };
    } else {
      return "The contact was not found or is not in your contact list.";
    }
  } catch (e) {
    console.error('Error occurred in getPersonInfo function: ' + e.stack);
  }
}

function insertMentorInfo(eventData_, newGivenName, newFamilyName) {
  try {
    // Logger.log('DETAY BILGISIinsertmentorinfo: ' + JSON.stringify(eventData_));
    var cnf = new Config(); // Config sınıfının bir örneğini oluşturun
    var updatedEventData = {};

    // 'MentorName' ve 'MentorSurname' eklenmeden önceki anahtar-değer çiftlerini ekle
    for (var key in eventData_) {
      if (key === cnf.getMentorMailFieldName()) {
        // 'MentorMail' anahtarından önce 'MentorName' ve 'MentorSurname' ekleniyor
        updatedEventData[cnf.getMentorNameFieldName()] = newGivenName || 'not a Contact';
        updatedEventData[cnf.getMentorSurnameFieldName()] = newFamilyName || 'not a Contact';
      }
      // Diğer anahtar-değer çiftlerini ekle
      updatedEventData[key] = eventData_[key];
    }
    return updatedEventData;
  } catch (e) {
    console.error('Error occurred in addUniqueEvent function: ' + e.stack);
  }
}

// Benzersiz EventID kontrol ve ekleme fonksiyonu
function addUniqueEvent(eventData) {
  try {
    var cnf = new Config(); // Config sınıfının bir örneğini oluşturun
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var lastRow = sheet.getLastRow();

    // EventID sütununun indeksini belirleyin (örneğin: A sütunu = 1, B sütunu = 2, vb.)
    var eventIdColumnIndex = 2; // Bu örnekte B sütunu, 2. sütun

    // Eğer lastRow 1 ise, yani sadece başlık satırı varsa, direkt olarak yeni satırı ekleyebiliriz
    if (lastRow === 1) {
      sheet.appendRow(Object.values(eventData));
      return;
    }

    // EventID değerlerini al
    var eventIdValues = sheet.getRange(2, eventIdColumnIndex, lastRow - 1, 1).getValues();

    // Yeni etkinlik ID'si
    var newEventId = eventData[cnf.getEventIdFieldName()];

    // EventID değerlerini kontrol et
    for (var i = 0; i < eventIdValues.length; i++) {
      if (eventIdValues[i][0] == newEventId) {
        Logger.log("Duplicate Event ID found: " + newEventId);
        return; // Aynı ID bulunursa, fonksiyondan çık
      }
    }

    // Yeni satırı ekle
    sheet.appendRow(Object.values(eventData));
  } catch(e) {
    console.error('Error occurred in addUniqueEvent function: ' + e.stack);
  }
}

//DIKKAT: Fonksiyon gecerli Worksheetteki baslik satirlarinda yazan yaziya gore calisiyor. Bu yaziyi degistirirseniz asagidan da 'Event ID' degerini de degistirin

function removeDuplicateEvents() {
  var rowsToDelete = [];

  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet(); // Sheet'i al
    var sheetData = sheet.getDataRange().getValues(); // Tüm veriyi al
    var headers = sheetData.shift();  // Başlık satırını ayır

    // EventID sütununun indeksini bul
    var eventIdIndex = headers.indexOf('Event ID');
    // NOT: Shetteki header degeri su anda 'Event ID' seklinde. Eger onu degistirirseniz, buradaki degeri de aynisi olacak sekilde degistirin.

    if (eventIdIndex === -1) {
      Logger.log('Event ID column not found, you probably changed the header value in the sheet file!');
    }

    // Benzersiz EventID'leri ve ilgili satır numaralarını tut
    var uniqueEvents = {};

    // Verileri kontrol et
    for (var i = 0; i < sheetData.length; i++) {
      var eventId = sheetData[i][eventIdIndex];
      // Logger.log('sheetdata['+i+']: ' + sheetData[i]);

      if (eventId in uniqueEvents) {
        // Bu EventID daha önce görülmüş, bu satırı silmek için işaretle
        rowsToDelete.push(i + 2); // +2 çünkü başlık satırı ve 1-tabanlı indeksleme
      } else {
        // Yeni EventID, kaydet
        uniqueEvents[eventId] = true;
      }
    }

    // Tekrarlanan satırları sil (sondan başa doğru)
    for (var i = rowsToDelete.length - 1; i >= 0; i--) {
      sheet.deleteRow(rowsToDelete[i]);
    }

  } catch (e) {
    console.error('Error occurred in removeDuplicateEvents function: ' + e.stack);
  } finally {
    // Etkinliklere davetlileri ekle ve mail gonder...
    // chooseEventLevel();
    addAttendeesToCalendarEvent();

    // Tekrarlanan satirlar silindikten sonra (veri tekilligi saglandiktan sonra) Mentor Adi ve Soyadi people api tarafindan alinamayan kayitlari tekrar almaya calismak icin, writeLatestEventToSheet fonksiyonunu da calistir.
    writeLatestEventToSheet();
    if (rowsToDelete.length > 0) {
      Logger.log(rowsToDelete.length + ' duplicate rows were deleted and existing data was maintained.');
    } else {
      Logger.log('No duplicate rows! Only maintenance of existing data (if needed).');
    }
  }
}

function addAttendeesToCalendarEvent() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var sheetData = sheet.getDataRange().getValues();
  var headers = sheetData.shift(); // Başlık satırını ayır

  try {
    var cnf = new Config();
    var calendarId = cnf.getCalendarId();
    var calendar = CalendarApp.getCalendarById(calendarId);

    var eventIdColumnIndex = 1; // 2. kolon
    var summaryColumnIndex = 6; // 7. kolon (0'dan başlayarak)
    var attendeeMailColumnIndex = 10; // 11. kolon (0'dan başlayarak)
    var attendeeResponseStatusColumnIndex = 11; // 12. kolon
    var folderShareLink = null;

    // 'Project Homework Deadline' sütununun indeksini bul

    var headerOfParentFolderColumnName = cnf.getHeaderOfParentFolderColumnName();
    var headerOfDeadlineColumnName = cnf.getHeaderOfDeadlineColumnName();

    // Yeni sheet'in ID'si (buraya yeni sheet ID'sini ekleyin)
    var configurationSheetName = cnf.getConfigurationSheetFileName();
    var configSheetId = getConfigurationSheetId(configurationSheetName);  // Configuration dosyasinin adina gore sheet'in ID'si elde ediliyor.

    // Yeni sheet'e erişmek
    var sheetConfig = SpreadsheetApp.openById(configSheetId);
    var sheetConfigData = sheetConfig.getDataRange().getValues();
    var headers = sheetConfigData.shift(); // Başlık satırını ayırır

    // headerOfDeadlineColumnName değişkeninde yer alan değerin bulunduğu sütunun indeksini bul
    var parentFolderColumnIndex = headers.indexOf(headerOfParentFolderColumnName);
    var parentFolderName = sheetConfigData[0][parentFolderColumnIndex].toString().trim() || null;

    if (!parentFolderName) {
      Logger.log(configurationSheetName + ' sheetinde bulunmasi gereken klasor ismi su anda bos. Lutfen bu dosyayi ve verilerini kontrol edin! Elle veya python uygulamasi (CRM) ile ilgili verileri guncelleyin!!!');
      var fatalErrorAboutConfigurationSheetTemplate = cnf.getFatalErrorAboutConfigurationSheetTemplate();
      sendEmail(cnf.getOwnerOfTheCalendarMail(), fatalErrorAboutConfigurationSheetTemplate, {});
      Logger.log(configurationSheetName + ' sheet dosyasini kontrol etmesi icin sistem yoneticisine uyari/bilgi maili gonderildi. Ayrica katilimcilarin ilgili eventlere eklenme islemleri de iptal edilmis oldu. Duzelteme yapildiktan sonra otomatikman islem devam edecektir...');
      return
    }
    var parentFolder = DriveApp.getFolderById(parentFolderId);

    // deadlineColumnName değişkeninde yer alan değerin bulunduğu sütunun indeksini bul
    var deadlineColumnIndex = headers.indexOf(headerOfDeadlineColumnName);
    var deadline = sheetConfigData[0][deadlineColumnIndex].toString().trim();
    // var removeSharingDateTime = new Date(deadline);
    var deadline = new Date(deadline);

    // Logger.log('deadline: ' + deadline);
    // Logger.log('typeof(deadline): ' + typeof(deadline));

    for (var i = 1; i < sheetData.length; i++) {                // Starts from 1, because first row is for headers
      var attendeeMail = sheetData[i][attendeeMailColumnIndex];
      var eventId = sheetData[i][eventIdColumnIndex];
      var attendeeResponseStatus = sheetData[i][attendeeResponseStatusColumnIndex];
      var summaryFromSheet = sheetData[i][summaryColumnIndex].toString();

      if (attendeeMail && attendeeMail.trim() !== "" &&
          (attendeeResponseStatus === null || attendeeResponseStatus === "null")) {
        if (eventId && eventId.trim() !== "") {
          try {
            var event = calendar.getEventById(eventId);
            // Logger.log('event.id  ??== eventId \n' + event.getId() + ' ??== ' + eventId);
            if (event) {
              // Logger.log();
              // Logger.log('DETAY BILGISI: ' + JSON.stringify(event));
              var eventStartTime = event.getStartTime();
              var eventEndTime = event.getEndTime();

              // Etkinlik detaylarını al ve davetli ekle
              var eventDetails = {
                guests: event.getGuestList().map(guest => guest.getEmail()).concat(attendeeMail),
                sendInvites: true
              };
              Logger.log('eventDetails.guests: ' + eventDetails.guests);

              // creatorEmail verisini de eventDetails.guests listesine ekleyelim
              var creatorEmail = event.getCreators().length > 0 ? event.getCreators()[0] : null;
              if (creatorEmail) {
                eventDetails.guests.push(creatorEmail);
              }
              // Logger.log('after adding creatoremail eventDetails.guests: ' + eventDetails.guests);

              // Event'i güncellemek ve e-posta göndermek için API kullanımı
              event.setGuestsCanModify(false);
              var calendarId = calendar.getId();
              var calendarApi = Calendar.Events;

              // Google Calendar API'sini kullanarak etkinliği güncelle ve sendUpdates parametresini ayarla
              var updateRequest = {
                summary: event.getTitle(),
                // Adaylara gonderilecek mailde sunum yazisini burada(description) guncelleyebiliriz. Mentorun etkinligi olustururken ne yazdigi veya bos biraktigini onemsemeden, otomatik olarak burada bir sunum yazariz. Mesela Sayin katilimci, detaylardaki gibi olan toplantida zamaninda hazir bulunmanizi beklemekteyiz... gibi vs. degiskenlerle bizzat sahsin ismiyle hitap da edebiliriz... event.setDescription methoduyla... Ayni sekilde summary icinde resmi bir baslik ayarlayabiliriz.... Ozetle, musteriye/basvurana sunum yapacagimiz sekle burada getiririz!
                description: event.getDescription(),
                start: { dateTime: eventStartTime.toISOString() },
                end: { dateTime: eventEndTime.toISOString() },
                attendees: eventDetails.guests.map(email => ({ email: email })),
                sendUpdates: 'all' // Burada sendUpdates parametresini ayarlıyoruz
              };

              // Adding extra text to the event description
              var note = '<p>Onemli Not: Eger Microsoft\'a ait bir mail adresi kullaniyorsaniz, Microsoft\'un, Google Takvim davetiyelerini islemesiyle ilgili bir sorundan dolayi etkinlik davetini gelen mailden kabul etseniz bile(RSVP seklinde gelen bolumden), bu cevap bizlere ulasamayabilir.<br><br>Bunun icin, daha asagida yer alan bolumde yer alan cevap secenegini (Yes, No, Maybe, More Options) kullanabilir veya etkinligin detaylarini goruntuleyerek, Google\'a ait bir sayfadan etkinlik davetini kabul edebilirsiniz.<br><br>Sabriniz icin tesekkur ederiz.</p><br><p>WeRHere Organization</p>';
              updateRequest.description = (updateRequest.description || '') + note;


              // updateRequest.attendees.forEach(email=> {
              //   Logger.log('attendee: ' + email.email);
              // });

              calendarApi.patch(updateRequest, calendarId, eventId, {sendUpdates: 'all'});
              Logger.log('Attendee ' + attendeeMail + ' added to event ' + eventId);

              // Send emails:
              var dataList = {};

              if (summaryFromSheet && summaryFromSheet.trim()[0].startsWith('1')) {
                // First Interview Appointment: Send the evaluation form link to the mentor
                dataList = {'crm_MentorName':sheetData[i][3], 'crm_MentorSurname':sheetData[i][4], 'crm_AttendeeName':sheetData[i][12], 'crm_AttendeeSurname':sheetData[i][13], 'crm_AttendeeEmails':sheetData[i][attendeeMailColumnIndex], 'sharedFolder':'', 'deadline':''};
                var evaluationMailTemplate = cnf.getEvaluationMailTemplate();
                sendEmail(creatorEmail, evaluationMailTemplate, dataList);
                Logger.log('Degerlendirme formu linki ve aday bilgileri, mentore gonderildi.');

              } else if (summaryFromSheet && summaryFromSheet.trim()[0].startsWith('2')) {
                // Project Interview Appointment: A Google Drive folder will be created and shared for the applicant and the link will be returned.
                if (attendeeMail !== 'null') {
                  // Katilimcinin mail adresi ile olusturulacak klasorun icinde bulunacagi klasorun adi, parametre olarak gonderiliyor.
                  folderShareLink = createAndShareFolder(attendeeMail, parentFolder.getName());
                }
                // Send the shared folder link to the attendee
                dataList = {'crm_MentorName':sheetData[i][3], 'crm_MentorSurname':sheetData[i][4], 'crm_AttendeeName':sheetData[i][12], 'crm_AttendeeSurname':sheetData[i][13], 'crm_AttendeeEmails':sheetData[i][attendeeMailColumnIndex], 'sharedFolder':folderShareLink, 'deadline':deadline};
                var projectHomeworkMailTemplate = cnf.getProjectHomeworkMailTemplate();
                sendEmail(attendeeMail, projectHomeworkMailTemplate, dataList);
                var projectHomeworkEvaluationFormMailTemplate = cnf.getProjectHomeworkEvaluationFormMailTemplate();
                sendEmail(creatorEmail, projectHomeworkEvaluationFormMailTemplate, dataList);
                Logger.log('Google Drive linki adaya ve Proje Odevi Degerlendirme Formu linki de mentore gonderildi.');

              } else {
                Logger.log('Calendar operations for any other thing');
                Logger.log('Summary: ' + summaryFromSheet);
              }
            } else {
              Logger.log('Event not found with ID: ' + eventId);
            }
          } catch (error) {
            Logger.log('Error adding attendee to event: ' + error);
          }
        } else {
          Logger.log('Empty or invalid Event ID for row ' + (i + 1));
        }
      } else { // Burayi devredisi biraktim. Cinku bu log dosyasini yazma isi islemci gucunu kullaniyor, toplam islem suresi uzuyor.
        Logger.log('Skipped row ' + (i + 1) + ': Invalid Attendee Mail or Response Status is not null');
      }
    }

  } catch (e) {
    console.error('Error occurred in addAttendeesToCalendarEvent function: ' + e);
  }
}

function createAndShareFolder(attendeeMail, targetFolderName) {
  try {
    // Aktif Google Sheet dosyasının ID'sini alıyoruz
    var file = SpreadsheetApp.getActiveSpreadsheet().getId();
    var parentFolder = DriveApp.getFileById(file).getParents().next();

    // Parametre olarak gelen "targetFolderName" adinda bir klasör olup olmadığını kontrol ediyoruz
    var folders = parentFolder.getFoldersByName(targetFolderName);
    var targetFolder;

    if (folders.hasNext()) {
      // Eğer klasör varsa mevcut olanı alıyoruz
      targetFolder = folders.next();
    } else {
      // Eğer klasör yoksa yeni klasörü oluşturuyoruz
      targetFolder = parentFolder.createFolder(targetFolderName);
    }

    // Son Basvuru Donemi ve AttendeeMail'e göre yeni klasör adı oluşturuyoruz veya var olup olmadığını kontrol ediyoruz
    var cnf = new Config();
    var dbsconn = cnf.openConn();  // Database connection
    var lastPeriodName = getLastApplicationPeriod(cnf, dbsconn);
    if (dbsconn) {
      cnf.closeConn(dbsconn);
    }

    var folderName = lastPeriodName + '_' + attendeeMail; // Klasor adini; son basvuru donemi, alt cizgi ve attendeeMail bilgisini birlestirerek belirliyoruz.
    var subFolders = targetFolder.getFoldersByName(folderName);
    var newFolder;

    if (subFolders.hasNext()) {
      // Eğer klasör varsa, mevcut olanı alıyoruz
      newFolder = subFolders.next();
      Logger.log('Folder already exists for ' + folderName);
    } else {
      // Eğer klasör yoksa, yeni klasör oluşturuyoruz
      newFolder = targetFolder.createFolder(folderName);
      Logger.log('New folder created for ' + folderName);
    }

    // Google hesabı olup olmadığını kontrol ediyoruz
    if (attendeeMail.indexOf('@gmail.com') !== -1 || attendeeMail.indexOf('@googlemail.com') !== -1) {
      // Google hesabıysa attendeeMail'e düzenleme yetkisi veriyoruz
      newFolder.addEditor(attendeeMail);
      return newFolder.getUrl(); // Google hesabı olan kullanıcılar için paylaşım linki döndürüyoruz
    } else {
      // Google hesabı olmayan kullanıcılar için paylaşım türünü "Bağlantıya sahip olan herkes düzenleyebilir" yapıyoruz
      newFolder.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
      Logger.log('Folder shared with public upload link.');
      return newFolder.getUrl(); // Klasör linki döndürüyoruz
    }
  } catch (e) {
    Logger.log('Error creating and sharing folder in createAndShareFolder function: ' + e.stack);
    return null;
  }
}

function sendEmail(emailAddress, mailType, dataList_) {
  try {
    // Logger.log('Target email: ' + emailAddress);

    // HTML şablonunu yükleyin ve içeriğini alın
    var htmlTemplate = HtmlService.createTemplateFromFile(mailType);
    var cnf = new Config();

    // HTML içeriğini işleyin
    // HTML şablonuna işlem ID'sini geçirin
    htmlTemplate.mentorName = dataList_['crm_MentorName'] || null;
    htmlTemplate.mentorSurname = dataList_['crm_MentorSurname'] || null;
    htmlTemplate.attendeeName = dataList_['crm_AttendeeName'] || null;
    htmlTemplate.attendeeSurname = dataList_['crm_AttendeeSurname'] || null;
    htmlTemplate.attendeeMail = dataList_['crm_AttendeeEmails'] || null;
    htmlTemplate.interviewDateTime = dataList_['crm_InterviewDatetime'] || null;
    htmlTemplate.sharedFolder = dataList_['sharedFolder'] || null;
    htmlTemplate.deadline = dataList_['deadline'] || null;
    htmlTemplate.ownerMail = cnf.getOwnerOfTheCalendarMail();
    htmlTemplate.configurationSheetName = cnf.getConfigurationSheetFileName();

    var htmlMessage = htmlTemplate.evaluate().getContent();

    // Gönderilecek e-posta içeriğini belirleyin
    if (mailType === 'evaluationMailTemplate'){;
      var subject = "WeRHere VIT Projesi Basvuru Degerlendirme Formu Linki";
    } else if(mailType === 'wrongEventCreationMailTemplate'){
      var subject = "Hatali/Eksik/Uyumsuz Etkinlik Olusturma";
    } else if(mailType === 'wrongEventUpdateMailTemplate'){
      var subject = "Hatali/Eksik/Uyumsuz Etkinlik Guncellemesi";
    } else if(mailType === 'projectHomeworkMailTemplate'){
      var subject = "Proje Odevi Yukleme Linki";
    } else if(mailType === 'projectHomeworkEvaluationFormMailTemplate'){
      var subject = "WeRHere VIT Projesi Aday Degerlendirme Formu Linki (Proje Odevi Toplantisi icin)";
    } else if(mailType === 'fatalErrorAboutConfigurationSheetTemplate'){
      var subject = "CRM PRojesi Kritik Sistem Hatasi";
    } else if(mailType === 'anyOtherTemplate'){
      var subject = "Any other subject";
    } else {
      var subject = "Problematic email regarding adding event attendee!";
    }

    // E-posta gönderim işlemiE-posta gönderilemedi:
    emailSent = false;
    if (isValidEmail(emailAddress)){
      try {
        MailApp.sendEmail({
          to: emailAddress,
          subject: subject,
          htmlBody: htmlMessage
        });
        emailSent = true; // Eğer e-posta gönderimi başarılıysa değişkeni true yap
      } catch (e) {
        console.error('Error sending email: ' + e.stack);
      }
    }

    // E-posta gönderim durumuna göre log yazdır
    if (emailSent) {
      Logger.log('Email sent successfully: ' + emailAddress);
    } else {
      Logger.log('Email could not be sent: ' + emailAddress);
    }
  } catch (e) {
    console.error('Error occurred in sendMail function: ' + e.stack);
  }
}

function isValidEmail(email) {
  try {
    // E-posta adresinin geçerliliğini kontrol eden regex deseni
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // Logger.log('Mail Gecerlilik Durumu:' +regex.test(email));
    return regex.test(email);
  } catch (e) {
    console.error('Error occurred in isValidEmail function: ' + e.stack);
  }
}

function removeSubFolderSharingByDate() {
  try {
    var cnf = new Config();
    var headerOfParentFolderColumnName = cnf.getHeaderOfParentFolderColumnName();
    var headerOfDeadlineColumnName = cnf.getHeaderOfDeadlineColumnName();

    // Yeni sheet'in ID'si (buraya yeni sheet ID'sini ekleyin)
    var configSheetId = getConfigurationSheetId(cnf.getConfigurationSheetFileName());  // Configuration dosyasinin adina gore sheet'in ID'si elde ediliyor.

    // Yeni sheet'e erişmek
    var sheet = SpreadsheetApp.openById(configSheetId);
    var sheetData = sheet.getDataRange().getValues();
    var headers = sheetData.shift(); // Başlık satırını ayırır

    // headerOfDeadlineColumnName değişkeninde yer alan değerin bulunduğu sütunun indeksini bul
    var parentFolderColumnIndex = headers.indexOf(headerOfParentFolderColumnName);
    var parentFolderName = sheetData[0][parentFolderColumnIndex].toString().trim() || null;
    if (!parentFolderName) {
      return
    }
    var parentFolderId = getFolderIdByName(parentFolderName);
    if (!parentFolderId) {
      Logger.log("Google Drive'daki, proje klasorunde; '" + cnf.getConfigurationSheetFileName() + "' sheet dosyasinda yazili klasor adinda bir klasor bulunmamaktadir!");
      return
    }
    var parentFolder = DriveApp.getFolderById(parentFolderId);

    // deadlineColumnName değişkeninde yer alan değerin bulunduğu sütunun indeksini bul
    var deadlineColumnIndex = headers.indexOf(headerOfDeadlineColumnName);
    var deadline = sheetData[0][deadlineColumnIndex].toString().trim();
    var removeSharingDateTime = new Date(deadline);

    var subFolders = parentFolder.getFolders();
    var rightNow = new Date();

    if (rightNow >= removeSharingDateTime) {
      Logger.log('Removing sharing permissions for subfolders under: ' + parentFolder.getName());

      while (subFolders.hasNext()) {
        var subFolder = subFolders.next();
        Logger.log('Processing folder: ' + subFolder.getName());

        var editors = subFolder.getEditors();
        var viewers = subFolder.getViewers();

        if (subFolder.getSharingAccess() === DriveApp.Access.ANYONE_WITH_LINK) {
          subFolder.setSharing(DriveApp.Access.PRIVATE, DriveApp.Permission.NONE);
          Logger.log('Sharing with anyone with the link removed for folder: ' + subFolder.getName());
        }

        for (var i = 0; i < editors.length; i++) {
          subFolder.removeEditor(editors[i]);
          Logger.log('Editor removed from folder: ' + subFolder.getName() + ', Editor: ' + editors[i].getEmail());
        }

        for (var j = 0; j < viewers.length; j++) {
          subFolder.removeViewer(viewers[j]);
          Logger.log('Viewer removed from folder: ' + subFolder.getName() + ', Viewer: ' + viewers[j].getEmail());
        }
      }
      Logger.log('All sharing permissions removed for subfolders.');
    } else {
      Logger.log('Today is before the specified removeSharingDate. No sharing permissions removed.');
    }
  } catch (e) {
    Logger.log('Error removing folder sharing: ' + e.toString());
    console.error('Error occurred in removeSubFolderSharingByDate function: ' + e.stack);
  }
}

function getConfigurationSheetId(configurationSheetFileNameHere) {
  try {
    // Bu dosyanın bulunduğu klasörü al
    var currentFileId = SpreadsheetApp.getActiveSpreadsheet().getId();
    var currentFile = DriveApp.getFileById(currentFileId);
    var parentFolder = currentFile.getParents().next(); // Bu dosyanın üst klasörü

    // Aynı klasördeki tüm dosyaları tara
    var files = parentFolder.getFiles();
    while (files.hasNext()) {
      var file = files.next();

      // Eğer dosya adı "configuration" ise
      if (file.getName() === configurationSheetFileNameHere) {
        var fileId = file.getId();
        Logger.log("Configuration dosya ID: " + fileId);

        // Dosyanın sheet'ine erişmek için dosya ID'sini döndür
        var configSpreadsheet = SpreadsheetApp.openById(fileId);
        return configSpreadsheet.getId();  // Gerekirse daha spesifik sheet'leri buradan seçebilirsiniz
      }
    }
    Logger.log("Configuration dosyası bulunamadı.");
    return null;
  } catch (e) {
    console.error('Error occurred in getConfigurationSheetId function: ' + e.stack);;
  }
}

/*
removeSubFolderSharingByDate fonksiyonu icinde cagrilan yardimci fonksiyondur. Klasorun adini parametre olarak alir ve Drive'da bu klasoru bularak Id'sini dondurur.
*/
function getFolderIdByName(folderName) {
  try {
    // Verilen isimde bir klasör arayın
    var folders = DriveApp.getFoldersByName(folderName);

    // Eğer klasör bulunursa, ID'sini döndür
    if (folders.hasNext()) {
      var folder = folders.next();
      // Logger.log('Folder ID: ' + folder.getId()); // Klasör ID'sini konsola yazdır
      return folder.getId();
    } else {
      Logger.log('Folder not found with the name: ' + folderName);
      return null;
    }
  } catch (e) {
    Logger.log('Error in getting folder ID: ' + e.toString());
    console.error('Error occurred in getFolderIdByName function: ' + e.stack);
    return null;
  }
}

// Değerleri karşılaştırma fonksiyonu - (event guncellenmis mi diye kontrol etmek icin)
function hasChanges(oldRow, eventData, datetimeFieldNames) {
  try {
    for (var i = 0; i < Object.values(eventData).length; i++) {
      var oldValue = oldRow[i];
      var newValue = Object.values(eventData)[i];

      // Tarih/saat alanları için özel karşılaştırma
      if (datetimeFieldNames.includes(Object.keys(eventData)[i])) {
        oldValue = new Date(oldValue).getTime();
        newValue = new Date(newValue).getTime();
      }

      // Diğer alanlar için tip dönüşümü
      else {
        oldValue = String(oldValue);
        newValue = String(newValue);
      }

      if (oldValue !== newValue) {
        Logger.log('Changed data found, will return to main function!\nChanged Data: ' + Object.keys(eventData)[i] + ' is changed: ' + oldValue + ' => ' + newValue);
        return true;
      }
    }
    return false;
  } catch (e) {
    console.error('Error occurred in hasChanges function: ' + e.stack);
  }
}

function convertToUTC(isoString) {
  try {
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
  } catch (e) {
    console.error('Error occurred in convertToUTC function: ' + e.stack);
    return {
      'utcTimestamp': null,
      'utcDatetime': null,
      'formattedUTC': null,
      'isoUTC': null
    };
  }
}
