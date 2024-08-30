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

