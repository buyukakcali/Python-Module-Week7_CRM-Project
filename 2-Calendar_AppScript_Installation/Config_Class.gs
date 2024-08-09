// .................. Configurtaion Area - Config Sinifi .................. //
class Config {
  constructor() {
    // JDBC bağlantı bilgileri
    var properties = PropertiesService.getScriptProperties();
    this.serverUrl = properties.getProperty('DB_URL');
    this.user = properties.getProperty('DB_USER');
    this.userPwd = properties.getProperty('DB_PASSWORD');

    this.applicationTable = 'form_basvuru';
    this.applicationPeriodFieldName = 'BasvuruDonemi';
    this.firstInterviewFieldName = 'IlkMulakat';
    this.applicantIdFieldName = 'BasvuranID';

    this.appointmentsTable = 'appointments';
    this.eventIdFieldName = 'EtkinlikID';
    this.mentorNameFieldName = 'MentorAdi';
    this.mentorSurnameFieldName = 'MentorSoyadi';
    this.mentorMailFieldName = 'MentorMail';

    this.menteeIdFiledName = 'MentiID';
    this.fields = ['ZamanDamgasi', 'EtkinlikID', 'MulakatZamani', 'MentorAdi', 'MentorSoyadi', 'MentorMail', 'Summary', 'Description', 'Location', 'OnlineMeetingLink', 'ResponseStatus']; // Kullanimdan kalkti. Gecici olarak tutuluyor!!! Kullanilmazsa sonra methodlariyla birlikte silinecek
    this.datetimeFieldNames = ['ZamanDamgasi', 'MulakatZamani'];

    this.ownerOfTheCalendarMail = 'calendarownerORapplicationmanager@mail.com';
    // this.calendarId, etkinliklerin alınacağı takvimi belirtir.
    // 'primary', kullanıcının birincil takvimini ifade eder. Alternatif olarak, belirli bir takvimin kimliği (örneğin, bir takvim URL'si) kullanılabilir.
    this.calendarId = '0b5ce8a3a81798b9e6edc1a72a566d8693f0e904b483f0fccae3e77130b88480@group.calendar.google.com'; // 'primary'; // OR ownerOfTheCalendarMail;
    this.java_sql_Types = {
      INTEGER: 4,
      VARCHAR: 12,
      TIMESTAMP: 93,
      DATE: 91
      // Diğer türler gerektiğinde buraya eklenebilir
    };

    this.secretkey = null;
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
  
  getMenteeIdFieldName() {
    return this.menteeIdFiledName;
  }

  setMenteeIdFieldName(value) {
    this.menteeIdFiledName = value;
  }

  getFields() {
    return this.fields;
  }

  setFields(value) {
    this.fields = value;
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

  getJava_sql_Types() {
    return this.java_sql_Types;
  }

  setJava_sql_Types(value) {
    this.java_sql_Types = value;
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
