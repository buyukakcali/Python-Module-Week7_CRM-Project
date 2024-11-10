function onFormSubmit(e) {
  try {
    // Form yanıtlarının geldiği Sheet'i alın
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Form yanıtının eklenmiş olduğu satır numarasını alın
    var row = e.range.getRow();
    // Logger.log('e.values: ' + e.values);

    // formResponses ve sheetResponses dizilerine veriler alindiktan sonra, her iki objedeki veriler trimData fonksiyonu ile temizlenecek.
    var formResponses = e.values.map(trimData); // Formdan gelen yanitlar formResponses adinda bir diziye ekleniyor ve temizleniyor.
    var sheetResponses = readRowData(row).map(trimData); // Sheetten gelen veriler sheetResponses adinda bir diziye ekleniyor ve temizleniyor.

    // Determine the type of action
    var formStatus = 'add';
    for (var i = 1; i < sheetResponses.length; i++){
      // Logger.log('sheetResponses['+i+']: '+sheetResponses[i]+' ?= formResponses['+i+']: ' + formResponses[i]);
      if (sheetResponses[i].toString() !== formResponses[i].toString()){
        formStatus = 'edit';
      }
    }

    // ONCE POSTA KODU ISTENEN FORMATTA DUZENLENECEK
    var postalCodeColumnIndex = 7; // Örneğin, posta kodları G sütunundaysa 7 olur

    // 1) Posta kodlarının bulunduğu sütunun indeksini belirtin ==> [{(* !!! Konfigurasyon alanina tasindi! *)}]

    // 2) Yeni eklenen satırdaki posta kodunu alın ve temizleyin
    var postalCode = sheet.getRange(row, postalCodeColumnIndex).getValue().toString().toUpperCase().trim();
    var cleanedPostalCode = cleanPostalCode(postalCode);

    // 3) Temizlenmiş posta kodunu sheet dosyasinda güncelleyin
    sheet.getRange(row, postalCodeColumnIndex).setValue(cleanedPostalCode);

    // 4) Database'e gondermeden once veriyi duzeltiyoruz.
    sheetResponses[postalCodeColumnIndex - 1] = cleanPostalCode(sheetResponses[postalCodeColumnIndex - 1]);


    // Sheetten gelen verileri alan adlarıyla eşleştir
    var cnf = new Config();
    var fields = cnf.getFields();
    var emailFieldName = cnf.getEmailFieldName();
    var formTableTimestampFieldName = cnf.getTimestampFieldName();
    var formData = {};
    for (var i = 0; i < sheetResponses.length; i++) {
      if (fields[i].startsWith(formTableTimestampFieldName)) { // key degeri crm_Timestamp ise iceri gir.
        var timestamp = convertToUTC(parseTimestamp(sheetResponses[i]))['utcDatetime'];
        formData[fields[i]] = timestamp;
      } else {
        if (emailFieldName.includes(fields[i])) {
          sheetResponses[i] = sheetResponses[i].toLowerCase();
        }
        formData[fields[i]] = sheetResponses[i];
      }
      // Logger.log('SheetValues['+fields[i]+']: ' + formData[fields[i]]);
    }

    // Bilgi maillerinde iyi bir sunum yapmak icin degiskenler
    var dataList = {'transactionId':row, 'applicantName':formData[fields[2]], 'applicantSurname':formData[fields[3]]};

    // Islem turune gore aksiyonlar:
    var email = sheetResponses[4].toLowerCase();
    var formTableRowId = {};
    formTableRowId[cnf.getRowIdFieldName()] = row;

    if (formStatus === 'add'){
      var formData = Object.assign(formTableRowId, formData);
      var resultAddApplication = addApplication(formData);
      if (resultAddApplication && isValidEmail(email)) {
        sendConfirmationEmail(email, cnf.getNewApplicationAddedTemplate(), dataList)
      } else {
        Logger.log('Mail (yeni basvuru) gonderiminde hata!');
      }
    } else {
      var applicationPeriod = {};
      applicationPeriod[cnf.getApplicationPeriodFieldName()] = sheetResponses[1];
      var resultUpdateApplication = updateApplication(formTableRowId, applicationPeriod, formData);
      if (resultUpdateApplication && isValidEmail(email)) {
        sendConfirmationEmail(email, cnf.getApplicationUpdatedTemplate(), dataList);
      } else {
        Logger.log('Mail (basvuru guncelleme) gonderiminde hata!')
      }
    }
  } catch (e) {
    console.error('Error occurred in onFormSubmit function: ' + e.stack);
  }
}
