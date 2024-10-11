// After installation of the project, DELETE setupWhiteList() function from the app script area (from here)!!!
function setupWhitelist() {
  try{
    var scriptProperties = PropertiesService.getScriptProperties();

    // Whitelist'i ayarla
    scriptProperties.setProperty('DB_URL', '_YOUR_DATABASE_URL_');
    scriptProperties.setProperty('DB_USER', '_YOUR_DB_USER_');
    scriptProperties.setProperty('DB_PASSWORD', '_YOUR_DB_PASS_');
    scriptProperties.setProperty('CALENDAR_ID', '_YOUR_CALENDAR_ID_');
    scriptProperties.setProperty('CLIENT_ID', '_YOUR_CLIENT_ID_');
    scriptProperties.setProperty('CLIENT_SECRET', '_YOUR_CLIENT_SECRET_');
    scriptProperties.setProperty('VALID_TABLES',
    'form1_applicant, form1_application, form1_old_applicant, form1_old_application, appointments_current, appointments_old_or_deleted, form2_evaluations');
    scriptProperties.setProperty('VALID_COLUMNS', 'crm_ID, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province, crm_ApplicantID, crm_Period, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir, crm_FirstInterview, crm_WhenUpdated, crm_ID_in_applicantTable, crm_ID_in_applicationTable, crm_EventID, crm_InterviewDatetime, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_Summary, crm_Description, crm_Location, crm_OnlineMeetingLink, crm_ResponseStatus, crm_AttendeeEmails, crm_AttendeeID, crm_WhenDeleted, crm_ID_Deleted, crm_AttendeeName, crm_AttendeeSurname, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_ProjectReturnDatetime, crm_IsApplicantACandidate');
    // scriptProperties.setProperty('', '');
  } catch(e) {
    console.error('Error occurred in setupWhitelist function: ' + e.stack);
  }
}

// .................. Configurtaion Area .................. //
// Config Sinifi
class Config {
  constructor() {
    // JDBC bağlantı bilgileri
    var properties = PropertiesService.getScriptProperties();
    this.serverUrl = properties.getProperty('DB_URL');
    this.user = properties.getProperty('DB_USER');
    this.userPwd = properties.getProperty('DB_PASSWORD');
    this.client_id = properties.getProperty('CLIENT_ID');
    this.secret_key = properties.getProperty('CLIENT_SECRET');

    this.applicantTable = 'form1_applicant';
    this.applicationTable = 'form1_application';
    this.appointmentsTable = 'appointments_current';
    this.evaluationTableName = 'form2_evaluations';

    this.idFieldName = 'crm_ID';
    this.periodFieldName = 'crm_Period';
    this.emailFiledName = 'crm_Email';
    this.applicantIdFieldName = 'crm_ApplicantID';
    this.firstInterviewFieldName = 'crm_FirstInterview';
    this.eventIdFieldName = 'crm_EventID';
    this.mentorNameFieldName = 'crm_MentorName';
    this.mentorSurnameFieldName = 'crm_MentorSurname';
    this.mentorMailFieldName = 'crm_MentorMail';
    this.attendeeIdFieldName = 'crm_AttendeeID';
    this.projectReturnDatetimeFieldName = 'crm_ProjectReturnDatetime';

    this.datetimeFieldNames = ['crm_Timestamp', 'crm_InterviewDatetime'];

    this.ownerOfTheCalendarMail = 'calendarownerORapplicationmanager@mail.com';
    // this.calendarId, etkinliklerin alınacağı takvimi belirtir.
    // 'primary', kullanıcının birincil takvimini ifade eder. Alternatif olarak, belirli bir takvimin kimliği (örneğin, bir takvim URL'si) kullanılabilir.
    this.calendarId = properties.getProperty('CALENDAR_ID'); // 'primary'; // OR ownerOfTheCalendarMail;

    // Mail Templates:
    this.wrongEventCreationMailTemplate = 'wrongEventCreationMailTemplate';
    this.wrongEventUpdateMailTemplate = 'wrongEventUpdateMailTemplate';
    this.evaluationMailTemplate = 'evaluationMailTemplate';
    this.projectHomeworkMailTemplate = 'projectHomeworkMailTemplate';
    this.projectHomeworkEvaluationFormMailTemplate = 'projectHomeworkEvaluationFormMailTemplate';
    this.fatalErrorAboutConfigurationSheetTemplate = 'fatalErrorAboutConfigurationSheetTemplate';

    // Maillerdeki Sunumlar icin ekstra metin duzenlemeleri:
    // -----------------------------------------------------

    // Adaylara gonderilecek mailde sunum yazisini burada(description) guncelleyebiliriz. Mentorun etkinligi olustururken ne yazdigi veya bos biraktigini onemsemeden, otomatik olarak burada bir sunum yazariz. Mesela Sayin katilimci, detaylardaki gibi olan toplantida zamaninda hazir bulunmanizi beklemekteyiz... gibi vs. degiskenlerle bizzat sahsin ismiyle hitap da edebiliriz... event.setDescription methoduyla... Ayni sekilde summary icinde resmi bir baslik ayarlayabiliriz.... Ozetle, musteriye/basvurana sunum yapacagimiz sekle burada getiririz!
    this.personalDescription = null;  // "Sunum yazisi buraya... HTML kullanmanizi tavsiye ederim.. Eger null olarak birakirsaniz, etkinlik olusturuldugunda ne yaziyorsa o eklenir."
    this.note1 = '<p>Onemli Not: Eger Microsoft\'a ait bir mail adresi kullaniyorsaniz, Microsoft\'un, Google Takvim davetiyelerini islemesiyle ilgili bir sorundan dolayi etkinlik davetini gelen mailden kabul etseniz bile(RSVP seklinde gelen bolumden), bu cevap bizlere ulasamayabilir.<br><br>Bunun icin, daha asagida yer alan bolumde yer alan cevap secenegini (Yes, No, Maybe, More Options) kullanabilir veya etkinligin detaylarini goruntuleyerek, Google\'a ait bir sayfadan etkinlik davetini kabul edebilirsiniz.<br><br>Sabriniz icin tesekkur ederiz.</p>';
    this.organizationSignature = '<br><p>WeRHere Organization</p>'

    // Mostly in Python module, for management.py and subfunctions. Additionally in addAttendeesToCalendar and some other functions
    this.evaluationSheetFileName = '3-Application_Evaluations_Form_Answers';
    this.projectHomeworksParentFolderName = "Candidate_Project_Homeworks";
    this.configurationSheetFileName = "configuration";
    this.headerOfPeriodFolderColumnName = "Project Homework Period Folder Name";
    this.headerOfDeadlineColumnName= "Project Homework Deadline";

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

  getApplicantTable() {
    return this.applicantTable;
  }

  setApplicantTable(value) {
    this.applicantTable = value;
  }

  getApplicationTable() {
    return this.applicationTable;
  }

  setApplicationTable(value) {
    this.applicationTable = value;
  }

  getIdFieldName() {
    return this.idFieldName;
  }

  setIdFieldName(value) {
    this.idFieldName = value;
  }

  getPeriodFieldName() {
    return this.periodFieldName;
  }

  setPeriodFieldName(value) {
    this.periodFieldName = value;
  }

  getEmailFiledName() {
    return this.emailFiledName;
  }

  setEmailFiledName(value) {
    this.emailFiledName = value;
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

  getEvaluationTableName() {
    return this.evaluationTableName;
  }

  setEvaluationTableName(value) {
    this.evaluationTableName = value;
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

  getProjectReturnDatetimeFieldName() {
    return this.projectReturnDatetimeFieldName;
  }

  setProjectReturnDatetimeFieldName(value) {
    this.projectReturnDatetimeFieldName = value;
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

  getWrongEventCreationMailTemplate() {
    return this.wrongEventCreationMailTemplate;
  }

  setWrongEventCreationMailTemplate(value) {
    this.wrongEventCreationMailTemplate = value;
  }

  getWrongEventUpdateMailTemplate() {
    return this.wrongEventUpdateMailTemplate;
  }

  setWrongEventUpdateMailTemplate(value) {
    this.wrongEventUpdateMailTemplate = value;
  }

  getEvaluationMailTemplate() {
    return this.evaluationMailTemplate;
  }

  setEvaluationMailTemplate(value) {
    this.evaluationMailTemplate = value;
  }

  getProjectHomeworkMailTemplate() {
    return this.projectHomeworkMailTemplate;
  }

  setProjectHomeworkMailTemplate(value) {
    this.projectHomeworkMailTemplate = value;
  }

  getProjectHomeworkEvaluationFormMailTemplate() {
    return this.projectHomeworkEvaluationFormMailTemplate;
  }

  setProjectHomeworkEvaluationFormMailTemplate(value) {
    this.projectHomeworkEvaluationFormMailTemplate = value;
  }

  getFatalErrorAboutConfigurationSheetTemplate() {
    return this.fatalErrorAboutConfigurationSheetTemplate;
  }

  setFatalErrorAboutConfigurationSheetTemplate(value) {
    this.fatalErrorAboutConfigurationSheetTemplate = value;
  }

  getPersonalDescription() {
    return this.personalDescription;
  }

  setPersonalDescription(value) {
    this.personalDescription = value;
  }

  getNote1() {
    return this.note1;
  }

  setNote1(value) {
    this.note1 = value;
  }

  getOrganizationSignature() {
    return this.organizationSignature;
  }

  setOrganizationSignature(value) {
    this.organizationSignature = value;
  }

  getEvaluationSheetFileName(){
    return this.evaluationSheetFileName;
  }

  setEvaluationSheetFileName(value) {
    this.evaluationSheetFileName = value;
  }

  getProjectHomeworksParentFolderName() {
    return this.projectHomeworksParentFolderName;
  }

  setProjectHomeworksParentFolderName(value) {
    this.projectHomeworksParentFolderName = value;
  }

  getConfigurationSheetFileName() {
    return this.configurationSheetFileName;
  }

  setConfigurationSheetFileName(value) {
    this.configurationSheetFileName = value;
  }

  getHeaderOfPeriodFolderColumnName() {
    return this.headerOfPeriodFolderColumnName;
  }

  setHeaderOfPeriodFolderColumnName(value) {
    this.headerOfPeriodFolderColumnName = value;
  }

  getHeaderOfDeadlineColumnName() {
    return this.headerOfDeadlineColumnName;
  }

  setHeaderOfDeadlineColumnName(value) {
    this.headerOfDeadlineColumnName = value;
  }
}


// Timer sınıfı
class Timer {
  constructor() {
    this.startTime = new Date().getTime();
  }

  elapsed() {
    return (new Date().getTime() - this.startTime) + " ms";
  }

  reset() {
    this.startTime = new Date().getTime();
  }
}
