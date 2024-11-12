// After installation of the project, DELETE setupWhiteList() function from the app script area (from here)!!!
function setupWhitelist() {
  try {
    var scriptProperties = PropertiesService.getScriptProperties();

    // Whitelist'i ayarla
    scriptProperties.setProperty('DB_URL', '_YOUR_DATABASE_URL_');
    scriptProperties.setProperty('DB_USER', '_YOUR_DB_USER_');
    scriptProperties.setProperty('DB_PASSWORD', '_YOUR_DB_PASS_');

    scriptProperties.setProperty('VALID_TABLES', 'form1_data');
    scriptProperties.setProperty('VALID_COLUMNS', 'crm_ID, crm_RowID, crm_Timestamp, crm_Period, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province, crm_SuAnkiDurum, crm_EgitimDurum, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_UAFDurum, crm_BootcampOrOtherCourse, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_Sorular, crm_MotivasyonunNedir, crm_GelecekPlani, crm_SaatKarisikligiOnay');
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
    this.encryptionKey = properties.getProperty('YOUR_ENCRYPTION_KEY');

    // Alanları tanımla
    this.fields = ['crm_Timestamp', 'crm_Period', 'crm_Name', 'crm_Surname', 'crm_Email', 'crm_Phone', 'crm_PostCode', 'crm_Province', 'crm_SuAnkiDurum', 'crm_EgitimDurum', 'crm_EkonomikDurum', 'crm_DilKursunaDevam', 'crm_IngilizceSeviye', 'crm_HollandacaSeviye', 'crm_UAFDurum', 'crm_BootcampOrOtherCourse', 'crm_ITTecrube', 'crm_ProjeDahil', 'crm_CalismakIstedigi', 'crm_Sorular', 'crm_MotivasyonunNedir', 'crm_GelecekPlani', 'crm_SaatKarisikligiOnay'];  // Ayarlanacak alan!!!

    this.formTable = 'form1_data';
    this.rowIdFieldName = 'crm_RowID';
    this.applicationPeriodFieldName = 'crm_Period';
    this.timestampFieldName = 'crm_Timestamp';
    this.emailFieldName = ['crm_Email'];

    this.newApplicationAddedTemplate = 'newApplicationAddedTemplate';
    this.applicationUpdatedTemplate = 'applicationUpdatedTemplate';
    //Diger genel kullanim degiskenleri buraya eklenecek..



    // SQL Sorgulari:
    this.normalQueries = {
      "q1":"INSERT INTO form1_data (crm_RowID, crm_Timestamp, crm_Period, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    };

    this.cryptionQueries = {
      "q1": "INSERT INTO form1_data (crm_RowID, crm_Timestamp, crm_Period, " +
        "TO_BASE64(AES_ENCRYPT(crm_Name, '" + this.encryptionKey + "')), " +
        "TO_BASE64(AES_ENCRYPT(crm_Surname, '" + this.encryptionKey + "')), " +
        "TO_BASE64(AES_ENCRYPT(crm_Email, '" + this.encryptionKey + "')), " +
        "TO_BASE64(AES_ENCRYPT(crm_Phone, '" + this.encryptionKey + "')), " +
        "TO_BASE64(AES_ENCRYPT(crm_PostCode, '" + this.encryptionKey + "')), " +
        "TO_BASE64(AES_ENCRYPT(crm_Province, '" + this.encryptionKey + "')), crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, " +
        "crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, " +
        "crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, " +
        "crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
      "q2":"SELECT"
    }
  }

  openConn() {
    return Jdbc.getConnection(this.serverUrl, this.user, this.userPwd);
  }

  // getters and setters
  getFields() {
    return this.fields;
  }

  setFields(value) {
    this.fields = value;
  }

  getFormTable() {
    return this.formTable;
  }

  setFormTable(value) {
    this.formTable = value;
  }

  getRowIdFieldName() {
    return this.rowIdFieldName;
  }

  setRowIdFieldName(value) {
    this.rowIdFieldName = value;
  }

  getApplicationPeriodFieldName() {
    return this.applicationPeriodFieldName;
  }

  setApplicationPeriodFieldName(value) {
    this.applicationPeriodFieldName = value;
  }

  getTimestampFieldName() {
    return this.timestampFieldName;
  }

  setTimestampFieldName(value) {
    this.timestampFieldName = value;
  }

  getEmailFieldName() {
    return this.emailFieldName;
  }

  setEmailFieldName(value) {
    this.emailFieldName = value;
  }

  getNewApplicationAddedTemplate() {
    return this.newApplicationAddedTemplate;
  }

  setNewApplicationAddedTemplate(value) {
    this.newApplicationAddedTemplate = value;
  }

  getApplicationUpdatedTemplate() {
    return this.applicationUpdatedTemplate;
  }

  setApplicationUpdatedTemplate(value) {
    this.applicationUpdatedTemplate = value;
  }
}
