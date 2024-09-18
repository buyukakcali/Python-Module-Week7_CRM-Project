function setupWhitelist() { // After installation of the project, DELETE setupWhiteList() function from the app script area!!!
  var scriptProperties = PropertiesService.getScriptProperties();

  // Whitelist'i ayarla
  scriptProperties.setProperty('DB_URL', '_YOUR_DATABASE_URL_');
  scriptProperties.setProperty('DB_USER', '_YOUR_DB_USER_');
  scriptProperties.setProperty('DB_PASSWORD', '_YOUR_DB_PASS_');

  scriptProperties.setProperty('VALID_TABLES', 'form1_applicant, form2_data');
  scriptProperties.setProperty('VALID_COLUMNS', 'crm_Timestamp, crm_Period, crm_MentorMail, crm_ApplicantMail, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_RowID, crm_ID');
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