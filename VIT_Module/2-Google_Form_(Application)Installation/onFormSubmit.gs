function onFormSubmit(e) {
  var conn; // Database baglantisi icin degiskenimizi tanimliyoruz.
  try {
    // Form yanıtlarının geldiği Sheet'i alın
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Form yanıtının eklenmiş olduğu satır numarasını alın
    var row = e.range.getRow();
    // Logger.log('e.values: ' + e.values);

    // formResponses ve sheetResponses dizilerine veriler alindiktan sonra, her iki objedeki veriler trim fonksiyonu ile temizlenecek.
    var formResponses = e.values.map(trimData); // Formdan gelen yanitlar formResponses adinda bir diziye ekleniyor ve temizleniyor.
    var sheetResponses = readRowData(row).map(trimData); // Sheetten gelen veriler sheetResponses adinda bir diziye ekleniyor ve temizleniyor.

    /* ----- KURULUM ALANI (Asagi dogru) - Projeyi uyarlamak icin yalnizca buradaki verileri duzenleyin!!! Kodlar otomatik calisacaktir. ------ */
    /**/
    /**/
    /**/

    // Alanları tanımla
    var fields = ['crm_Timestamp', 'crm_Period', 'crm_Name', 'crm_Surname', 'crm_Email', 'crm_Phone', 'crm_PostCode', 'crm_Province', 'crm_SuAnkiDurum', 'crm_ITPHEgitimKatilmak', 'crm_EkonomikDurum', 'crm_DilKursunaDevam', 'crm_IngilizceSeviye', 'crm_HollandacaSeviye', 'crm_BaskiGoruyor', 'crm_BootcampBitirdi', 'crm_OnlineITKursu', 'crm_ITTecrube', 'crm_ProjeDahil', 'crm_CalismakIstedigi', 'crm_NedenKatilmakIstiyor', 'crm_MotivasyonunNedir'];  // Ayarlanacak alan!!!
    var formData = {};

    // Email bilgisi:
    var email = sheetResponses[4].toLowerCase();

    // JDBC bağlantı bilgileri
    var properties = PropertiesService.getScriptProperties();
    var serverUrl = properties.getProperty('DB_URL');
    var user = properties.getProperty('DB_USER');
    var userPwd = properties.getProperty('DB_PASSWORD');

    var formTable = 'form1_data';
    var formTableTimestampFieldName = 'crm_Timestamp';
    var emailFieldNames = ['crm_Email'];
    var postalCodeColumnIndex = 7; // Örneğin, posta kodları G sütunundaysa 7 olur

    var applicationPeriod = {};
    applicationPeriod['crm_Period'] = sheetResponses[1];

    var formTableRowId = {};
    formTableRowId['crm_RowID'] = row;

    var newApplicationAddedTemplate = 'newApplicationAddedTemplate';
    var applicationIsUpdatedTemplate = 'applicationUpdatedTemplate';

    /**/
    /**/
    /**/
    /* ---------------------------------- Buradan yukarisi KURULUM ALANI ------------------------------------- */


    conn = Jdbc.getConnection(serverUrl, user, userPwd);

    var formStatus = 'add';
    for (var i = 1; i < sheetResponses.length; i++){
      // Logger.log('sheetResponses['+i+']: '+sheetResponses[i]+' ?= formResponses['+i+']: ' + formResponses[i]);
      if (sheetResponses[i].toString() !== formResponses[i].toString()){
        formStatus = 'edit';
      }
    }

    // ONCE POSTA KODU ISTENEN FORMATTA DUZENLENECEK
    // 1) Posta kodlarının bulunduğu sütunun indeksini belirtin ==> [{(* !!! Konfigurasyon alanina tasindi! *)}]

    // 2) Yeni eklenen satırdaki posta kodunu alın ve temizleyin
    var postalCode = sheet.getRange(row, postalCodeColumnIndex).getValue().toString().toUpperCase().trim();
    var cleanedPostalCode = cleanPostalCode(postalCode);

    // 3) Temizlenmiş posta kodunu sheet dosyasinda güncelleyin
    sheet.getRange(row, postalCodeColumnIndex).setValue(cleanedPostalCode);

    // 4) Database'e gondermeden once veriyi duzeltiyoruz.
    sheetResponses[postalCodeColumnIndex - 1] = cleanPostalCode(sheetResponses[postalCodeColumnIndex - 1]);


    // Sheetten gelen verileri alan adlarıyla eşleştir
    for (var i = 0; i < sheetResponses.length; i++) {
      if (fields[i].startsWith(formTableTimestampFieldName)) { // key degeri crm_Timestamp ise iceri gir.
        var timestamp = convertToUTC(parseTimestamp(sheetResponses[i]))['utcDatetime'];
        formData[fields[i]] = timestamp;
      } else {
        if (emailFieldNames.includes(fields[i])) {
          sheetResponses[i] = sheetResponses[i].toLowerCase();
        }
        formData[fields[i]] = sheetResponses[i];
      }
      // Logger.log('SheetValues['+fields[i]+']: ' + formData[fields[i]]);
    }

    // Bilgi maillerinde iyi bir sunum yapmak icin degiskenler
    var dataList = {'transactionId':row, 'applicantName':formData[fields[2]], 'applicantSurname':formData[fields[3]]};

    // Islem turune gore aksiyonlar:
    if (formStatus === 'add'){
      // formTableRowId and formData are merged for new adding
      var formDataCopy = Object.assign(formTableRowId, formData);
      var resultAddApplication = addApplication(conn, formTable, formTableTimestampFieldName, formDataCopy);
      if (resultAddApplication && isValidEmail(email)) {
        sendConfirmationEmail(email, newApplicationAddedTemplate, dataList)
      } else {
        Logger.log('Mail (yeni basvuru) gonderiminde hata!');
      }
    } else {
      var resultUpdateApplication = updateApplication(conn, formTable, formTableRowId, formTableTimestampFieldName, applicationPeriod, formData);
      if (resultUpdateApplication && isValidEmail(email)) {
        sendConfirmationEmail(email, applicationIsUpdatedTemplate, dataList);
      } else {
        Logger.log('Mail (basvuru guncelleme) gonderiminde hata!')
      }
    }
  } catch (e) {
    console.error('Error: ' + e.stack);
  } finally {
    if (conn) {
      try {
        conn.close();
      } catch (e) {
        console.error('Connection closing error: ' + e.stack);
      }
    }
  }
}
