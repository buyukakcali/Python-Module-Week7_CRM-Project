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
