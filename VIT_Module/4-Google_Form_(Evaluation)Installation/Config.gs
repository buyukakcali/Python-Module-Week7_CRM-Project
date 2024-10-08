// After installation of the project, DELETE setupWhiteList() function from the app script area (from here)!!!
function setupWhitelist() {
  try {
    var scriptProperties = PropertiesService.getScriptProperties();

    // Whitelist'i ayarla
    scriptProperties.setProperty('DB_URL', '_YOUR_DATABASE_URL_');
    scriptProperties.setProperty('DB_USER', '_YOUR_DB_USER_');
    scriptProperties.setProperty('DB_PASSWORD', '_YOUR_DB_PASS_');

    scriptProperties.setProperty('VALID_TABLES', 'form1_applicant, form2_data');
    scriptProperties.setProperty('VALID_COLUMNS', 'crm_Timestamp, crm_Period, crm_MentorMail, crm_ApplicantMail, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_RowID, crm_ID');
    // scriptProperties.setProperty('', '');
  } catch (e) {
    console.error('Error occurred in setupWhitelist function: ' + e.stack);
  }
}

// .................. Configurtaion Area - Config Sinifi .................. //
class Config {
  constructor() {
    // JDBC bağlantı bilgileri
    var properties = PropertiesService.getScriptProperties();
    this.serverUrl = properties.getProperty('DB_URL');
    this.user = properties.getProperty('DB_USER');
    this.userPwd = properties.getProperty('DB_PASSWORD');

    // SQ QUERIES:
    this.normalQeries = {
      "queryGetApplicant": "SELECT crm_Name, crm_Surname FROM form1_applicant WHERE crm_Email = ?"
    }

    // Mail Templates:
    this.evaluationIsRecordedTemplate = 'evaluationIsRecordedTemplate';
    this.evaluationIsUpdatedTemplate = 'evaluationIsUpdatedTemplate';
    this.wrongApplicantEmailTemplate = 'wrongApplicantEmailTemplate';
  }

  openConn() {
    return Jdbc.getConnection(this.serverUrl, this.user, this.userPwd);
  }

  closeConn(conn) {
    return conn.close();   // Connection kapatılıyor
  }

  getEvaluationIsRecordedTemplate () {
    return this.evaluationIsRecordedTemplate;
  }

  setEvaluationIsRecordedTemplate (value) {
    this.evaluationIsRecordedTemplate = value;
  }

  getEvaluationIsUpdatedTemplate () {
    return this.evaluationIsUpdatedTemplate;
  }

  setEvaluationIsUpdatedTemplate (value) {
    this.evaluationIsUpdatedTemplate = value;
  }

  getWrongApplicantEmailTemplate () {
    return this.wrongApplicantEmailTemplate;
  }

  setWrongApplicantEmailTemplate (value) {
    this.wrongApplicantEmailTemplate = value;
  }

  getQuery(queryName) {
    Logger.log(this.normalQeries[queryName]);
    return this.normalQeries[queryName];
  }
}
