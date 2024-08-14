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

    this.applicationTable = 'form_application';
    this.applicationPeriodFieldName = 'Period';
    this.firstInterviewFieldName = 'FirstInterview';
    this.applicantIdFieldName = 'ApplicantID';

    this.appointmentsTable = 'appointments_current';
    this.eventIdFieldName = 'EventID';
    this.mentorNameFieldName = 'MentorName';
    this.mentorSurnameFieldName = 'MentorSurname';
    this.mentorMailFieldName = 'MentorMail';

    this.attendeeIdFieldName = 'AttendeeID';
    this.fields = ['Timestamp_', 'EventID', 'InterviewDatetime', 'MentorName', 'MentorSurname', 'MentorMail', 'Summary', 'Description', 'Location', 'OnlineMeetingLink', 'ResponseStatus']; // Kullanimdan kalkti. Gecici olarak tutuluyor!!! Kullanilmazsa sonra methodlariyla birlikte silinecek
    this.datetimeFieldNames = ['Timestamp_', 'InterviewDatetime'];

    this.ownerOfTheCalendarMail = 'calendarownerORapplicationmanager@mail.com';
    // this.calendarId, etkinliklerin alınacağı takvimi belirtir.
    // 'primary', kullanıcının birincil takvimini ifade eder. Alternatif olarak, belirli bir takvimin kimliği (örneğin, bir takvim URL'si) kullanılabilir.
    this.calendarId = properties.getProperty('CALENDAR_ID'); // 'primary'; // OR ownerOfTheCalendarMail;
    this.java_sql_Types = {
      INTEGER: 4,
      VARCHAR: 12,
      TIMESTAMP: 93,
      DATE: 91
      // Diğer türler gerektiğinde buraya eklenebilir
    };

    this.secretkey = null;
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
