// appscript.json, evaluationMailTemplate.html, Installation Properties.png
// dosyalari haric diger tum dosyalarda/modullerde yazilmis olan fonksiyonlar bu dosyanin icindedir.
// Yani yukaridaki adi verilen dosyalar ve bu Code.gs dosyasi kurulum icin yeterlidir.

function setupWhitelist() { // After installation of the project, DELETE setupWhiteList() function from the app script area!!!
  var scriptProperties = PropertiesService.getScriptProperties();

  // Whitelist'i ayarla
  scriptProperties.setProperty('DB_URL', '_YOUR_DATABASE_URL_');
  scriptProperties.setProperty('DB_USER', '_YOUR_DB_USER_');
  scriptProperties.setProperty('DB_PASSWORD', '_YOUR_DB_PASS_');
  scriptProperties.setProperty('CALENDAR_ID', '_YOUR_CALENDAR_ID_');
  scriptProperties.setProperty('CLIENT_ID', '_YOUR_CLIENT_ID_');
  scriptProperties.setProperty('CLIENT_SECRET', '_YOUR_CLIENT_SECRET_');
  scriptProperties.setProperty('VALID_TABLES',
  'form1_applicant, form1_application, form1_old_applicant, form1_old_application, appointments_current, appointments_old_or_deleted');
  scriptProperties.setProperty('VALID_COLUMNS', 'crm_ID, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province, crm_ApplicantID, crm_Period, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir, crm_FirstInterview, crm_SecondInterview, crm_WhenUpdated, crm_ID_in_applicantTable, crm_ID_in_applicationTable, crm_EventID, crm_InterviewDatetime, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_Summary, crm_Description, crm_Location, crm_OnlineMeetingLink, crm_ResponseStatus, crm_AttendeeEmails, crm_AttendeeID, crm_WhenDeleted, crm_ID_Deleted, crm_AttendeeName, crm_AttendeeSurname');
  // scriptProperties.setProperty('', '');
}

function getWhitelist() {
  var scriptProperties = PropertiesService.getScriptProperties();

  var validTables = scriptProperties.getProperty('VALID_TABLES').split(', ');
  var validColumns = scriptProperties.getProperty('VALID_COLUMNS').split(', ');

  return {
    validTables: validTables,
    validColumns: validColumns
  };
}

// .................. Configurtaion Area - Config Sinifi .................. //
class Config {
  constructor() {
    // JDBC bağlantı bilgileri
    var properties = PropertiesService.getScriptProperties();
    this.serverUrl = properties.getProperty('DB_URL');
    this.user = properties.getProperty('DB_USER');
    this.userPwd = properties.getProperty('DB_PASSWORD');
    this.client_id = properties.getProperty('CLIENT_ID');
    this.secret_key = properties.getProperty('CLIENT_SECRET');

    this.applicationTable = 'form1_application';
    this.applicationPeriodFieldName = 'crm_Period';
    this.firstInterviewFieldName = 'crm_FirstInterview';
    this.applicantIdFieldName = 'crm_ApplicantID';

    this.appointmentsTable = 'appointments_current';
    this.eventIdFieldName = 'crm_EventID';
    this.mentorNameFieldName = 'crm_MentorName';
    this.mentorSurnameFieldName = 'crm_MentorSurname';
    this.mentorMailFieldName = 'crm_MentorMail';

    this.attendeeIdFieldName = 'crm_AttendeeID';
    this.datetimeFieldNames = ['crm_Timestamp', 'crm_InterviewDatetime'];

    this.ownerOfTheCalendarMail = 'calendarownerORapplicationmanager@mail.com';
    // this.calendarId, etkinliklerin alınacağı takvimi belirtir.
    // 'primary', kullanıcının birincil takvimini ifade eder. Alternatif olarak, belirli bir takvimin kimliği (örneğin, bir takvim URL'si) kullanılabilir.
    this.calendarId = properties.getProperty('CALENDAR_ID'); // 'primary'; // OR ownerOfTheCalendarMail;

    this.evaluationLinkMailTemplate = 'evaluationLinkMailTemplate';
    //Diger genel kullanim degiskenleri buraya eklenecek..
  }

  openConn() {
    return Jdbc.getConnection(this.serverUrl, this.user, this.userPwd);
  }

  closeConn(conn) {
    return conn.close();   // Connection kapatılıyor
  }

  getServerUrl() {
    return this.serverUrl;
  }

  setServerUrl(value) {
    this.serverUrl = value;
  }

  getUser() {
    return this.user;
  }

  setUser(value) {
    this.user = value;
  }

  getUserPwd() {
    return this.userPwd;
  }

  setUserPwd(value) {
    this.userPwd = value;
  }

  getClientId() {
    return this.client_id;
  }

  getSecretKey() {
    return this.secret_key;
  }

  getApplicationTable() {
    return this.applicationTable;
  }

  setApplicationTable(value) {
    this.applicationTable = value;
  }

  getApplicationPeriodFieldName() {
    return this.applicationPeriodFieldName;
  }

  setApplicationPeriodFieldName(value) {
    this.applicationPeriodFieldName = value;
  }

  getFirstInterviewFieldName() {
    return this.firstInterviewFieldName;
  }

  setFirstInterviewFieldName(value) {
    this.firstInterviewFieldName = value;
  }

  getApplicantIdFieldName() {
    return this.applicantIdFieldName;
  }

  setApplicantIdFieldName(value) {
    this.applicantIdFieldName = value;
  }

  getAppointmentsTable() {
    return this.appointmentsTable;
  }

  setAppointmentsTable(value) {
    this.appointmentsTable = value;
  }

  getEventIdFieldName() {
    return this.eventIdFieldName;
  }

  setEventIdFieldName(value) {
    this.eventIdFieldName = value;
  }

  getMentorNameFieldName() {
    return this.mentorNameFieldName;
  }

  setMentorNameFieldName(value) {
    this.mentorNameFieldName = value;
  }

  getMentorSurnameFieldName() {
    return this.mentorSurnameFieldName;
  }

  setMentorSurnameFieldName(value) {
    this.mentorSurnameFieldName = value;
  }

  getMentorMailFieldName() {
    return this.mentorMailFieldName;
  }

  setMentorMailFieldName(value) {
    this.mentorMailFieldName = value;
  }

  getAttendeeIdFieldName() {
    return this.attendeeIdFieldName;
  }

  setAttendeeIdFieldName(value) {
    this.attendeeIdFieldName = value;
  }

  getDatetimeFieldNames() {
    return this.datetimeFieldNames;
  }

  setDatetimeFieldNames(value) {
    this.datetimeFieldNames = value;
  }

  getOwnerOfTheCalendarMail() {
    return this.ownerOfTheCalendarMail;
  }

  setOwnerOfTheCalendarMail(value) {
    this.ownerOfTheCalendarMail = value;
  }

  getCalendarId() {
    return this.calendarId;
  }

  setCalendarId(value) {
    this.calendarId = value;
  }

  getEvaluationLinkMailTemplate() {
    return this.evaluationLinkMailTemplate;
  }

  setEvaluationLinkMailTemplate(value) {
    this.evaluationLinkMailTemplate = value;
  }
}

// Timer sınıfı
function Timer() {
  this.startTime = new Date().getTime();

  this.elapsed = function() {
    return (new Date().getTime() - this.startTime) + " ms";
  };

  this.reset = function() {
    this.startTime = new Date().getTime();
  };
}

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
      if (deletedCount === 1) {
        // Her silme olayindan sonra gecen sure logu:
        Logger.log(deletedCount + " record is deleted. Processing time: " + deleteTimer.elapsed());
        deleteTimer.reset();
      } else {
        // Her silme olayindan sonra gecen sure logu:
        Logger.log(deletedCount + " records are deleted. Processing time: " + deleteTimer.elapsed());
        deleteTimer.reset();
      }
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
    console.error('Error occured in getLastApplicationPeriod function: ' + e.stack);
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
    console.error('Error occured in getLastApplicationPeriodStartDate function: ' + e.stack);
  }
  finally {
    return lastApplicationPeriodStartDate_;;
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
    console.error('Error occured in addEvent function: ' + e.stack);
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
    console.error('Error occured in updateEvent function: ' + e.stack);
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
      if (currentEventIds_.has(sheetEventId) === false) {
        // Logger.log('Only the section about deleted items needs to be filled in!')

        // NOT: If the lastApplicationPeriodStartDate value is greater than InterviewDatetime, that is, if a new application period is opened, the MentorApplication process is not automatically canceled. This code only prevents any confusion that may occur if the appointment has been deleted in some way. For example, the mentor has created an appointment date. After that, the CRM Application user/manager assigned an applicant to the appointment created by this mentor. However, if the mentor deletes the appointment without informing the manager, we will automatically cancel the mentor appointment process for the applicant.
        // Buraya bir de mail atma islevi konularak Basvuran ve Yoneticinin bilgilendirilmesi saglanabilir.

        // Logger.log(lastApplicationPeriodStartDate_ + '<?' + sheetData_[i][2]);
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
                Logger.log('Mentor appointment has been withdrawn/cancelled!\nDetails: The assignments in tables \'appointments\'  and \'applicant\' have been updated to null and 0.');
              }
            } catch (e) {
              console.error('Error: ' + e.stack);
            } finally {
              stmtUnassignAppointment.close();    // 1. statement is closing
              stmtUnassignApplicant.close();      // 2. statement is closing
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
    console.error('Error occured in deleteEvent function: ' + e.stack);
  } finally {
    return deletedCount_;
  }
}

function insertMentorInfo(eventData_, newGivenName, newFamilyName) {
  try {
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
    console.error('Error: ' + e.stack);
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
    console.error('Error: ' + e.stack);
  }
}

function addAttendeesToCalendarEvent() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var sheetData = sheet.getDataRange().getValues();
  var evaluationLinkMail = 'evaluationMailTemplate';

  try {
    var cnf = new Config();
    var calendarId = cnf.getCalendarId();
    var calendar = CalendarApp.getCalendarById(calendarId);

    var attendeeMailColumnIndex = 10; // 11. kolon (0'dan başlayarak)
    var eventIdColumnIndex = 1; // 2. kolon
    var attendeeResponseStatusColumnIndex = 11; // 12. kolon

    for (var i = 1; i < sheetData.length; i++) {                // Starts from 1, because first row is for headers
      var attendeeMail = sheetData[i][attendeeMailColumnIndex];
      var eventId = sheetData[i][eventIdColumnIndex];
      var attendeeResponseStatus = sheetData[i][attendeeResponseStatusColumnIndex];

      if (attendeeMail && attendeeMail.trim() !== "" &&
          (attendeeResponseStatus === null || attendeeResponseStatus === "null")) {
        if (eventId && eventId.trim() !== "") {
          try {
            var event = calendar.getEventById(eventId);
            if (event) {
              var eventStartTime = event.getStartTime();
              var eventEndTime = event.getEndTime();

              // Etkinlik detaylarını al ve davetli ekle
              var eventDetails = {
                guests: event.getGuestList().map(guest => guest.getEmail()).concat(attendeeMail),
                sendInvites: true
              };

              // creatorEmail verisini de eventDetails.guests listesine ekleyelim
              var creatorEmail = event.getCreators().length > 0 ? event.getCreators()[0] : null;
              if (creatorEmail) {
                eventDetails.guests.push(creatorEmail);
              }

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

              updateRequest.attendees.forEach(email=> {
                Logger.log('attendee: ' + email.email);
              });

              calendarApi.patch(updateRequest, calendarId, eventId, {sendUpdates: 'all'});
              Logger.log('Attendee ' + attendeeMail + ' added to event ' + eventId);

              // Send evaluation form link to mentor
              var dataList = {'mentorName':sheetData[i][3], 'mentorSurname':sheetData[i][4], 'attendeeName':sheetData[i][12], 'attendeeSurname':sheetData[i][13], 'attendeeMail':sheetData[i][attendeeMailColumnIndex]};
              sendEmail(creatorEmail, evaluationLinkMail, dataList);
              Logger.log('Degerlendirme formu linki ve aday bilgileri, mentore gonderildi.');
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
    console.error('Error occured in removeDuplicateEvents function: ' + e.stack);
  } finally {
    // Etkinliklere davetlileri ekle ve mail gonder...
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

function sendEmail(emailAddress, mailType, dataList_) {
  try {
    // Logger.log('Target email: ' + emailAddress);

    // HTML şablonunu yükleyin ve içeriğini alın
    var htmlTemplate = HtmlService.createTemplateFromFile(mailType);

    // HTML içeriğini işleyin
    // HTML şablonuna işlem ID'sini geçirin
    htmlTemplate.mentorName = dataList_['mentorName'];
    htmlTemplate.mentorSurname = dataList_['mentorSurname'];
    htmlTemplate.attendeeName = dataList_['attendeeName'];
    htmlTemplate.attendeeSurname = dataList_['attendeeSurname'];
    htmlTemplate.attendeeMail = dataList_['attendeeMail'];
    var htmlMessage = htmlTemplate.evaluate().getContent();

    // Gönderilecek e-posta içeriğini belirleyin
    if (mailType === 'evaluationMailTemplate'){
      var subject = "WeRHere VIT Projesi Aday Degerlendirme Formu Linki";
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
    console.error('Error occured in sendMail function: ' + e.stack);
  }
}

function isValidEmail(email) {
  try {
    // E-posta adresinin geçerliliğini kontrol eden regex deseni
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // Logger.log('Mail Gecerlilik Durumu:' +regex.test(email));
    return regex.test(email);
  } catch (e) {
    console.error('Error occured in isValidEmail function: ' + e.stack);
  }
}

// Kullanım örnekleri
// console.log(isValidEmail("example@example.com")); // true
// console.log(isValidEmail("example.com")); // false
// console.log(isValidEmail("example@.com")); // false
// console.log(isValidEmail("example@com")); // false
// console.log(isValidEmail("example@example..com")); // false
// console.log(isValidEmail("example@sub.example.com")); // true

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
    console.error('Error in hasChanges function: ' + e.stack);
  }
}


function convertToUTC(isoString) {
  try {
    // ISO string'i Date nesnesine çevir
    const date = new Date(isoString);

    // Geçerli bir tarih olup olmadığını kontrol et
    if (isNaN(date.getTime())) {
      throw new Error('Invalid date format: ' + isoString);
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
    console.error('Error: ' + e.stack);
    return {
      'utcTimestamp': null,
      'utcDatetime': null,
      'formattedUTC': null,
      'isoUTC': null
    };
  }
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
    console.error('Error in getOAuthService function: ' + e.stack);
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
    console.error('Error in authCallback function: ' + e.stack);
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
    console.error('Error in getPersonInfo function: ' + e.stack);
  }
}

// Fonksiyonu test et
function testGetPersonInfo() {
  try {
    var email = "test@mail.com"; // Test etmek istediğiniz e-posta adresi
    Logger.log(getPersonInfo(email));
  } catch (e) {
    console.error('Error in testGetPersonInfo function: ' + e.stack);
  }
}
