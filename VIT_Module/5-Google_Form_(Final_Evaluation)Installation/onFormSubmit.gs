function onFormSubmit(e) {
  var conn; // Database baglantisi icin degiskenimizi tanimliyoruz.
  try {
    var cnf = new Config();
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
    var fields = ['crm_Timestamp', 'crm_Period', 'crm_MentorMail', 'crm_CandidateMail', 'crm_CodingSkills', 'crm_AssistantEvaluation1', 'crm_AssistantEvaluation2', 'crm_AssistantEvaluation3', 'crm_MentorEvaluation'];
    var formData = {};

    // Email bilgisi:
    var mentorEmail = sheetResponses[2].toLowerCase();
    var candidateEmail = sheetResponses[3].toLowerCase();

    // JDBC bağlantı bilgileri
    var properties = PropertiesService.getScriptProperties();
    var serverUrl = properties.getProperty('DB_URL');
    var user = properties.getProperty('DB_USER');
    var userPwd = properties.getProperty('DB_PASSWORD');

    var formTableName = 'form3_data';
    var formTableTimestampFieldName = 'crm_Timestamp';
    var emailFieldNames = ['crm_MentorMail', 'crm_CandidateMail'];

    var applicationPeriod = {};
    applicationPeriod['crm_Period'] = sheetResponses[1];

    var formTableRowId={};
    formTableRowId['crm_RowID'] = row;

    /**/
    /**/
    /**/
    /* ---------------------------------- Buradan yukarisi KURULUM ALANI ------------------------------------- */


    var formStatus = 'add';

    Logger.log(sheetResponses[4].toString());

    for (var i = 1; i < formResponses.length; i++){
      // Logger.log('sheetResponses['+i+']: '+sheetResponses[i]+' ?= formResponses['+i+']: ' + formResponses[i]);
      if (sheetResponses[i].toString() !== formResponses[i].toString()){
        formStatus = 'edit';
      }
    }

    // Sheetten gelen verileri alan adlarıyla eşleştir
    for (var i = 0; i < formResponses.length; i++) {
      if (fields[i].startsWith(formTableTimestampFieldName)) { // key degeri crm_Timestamp ise iceri gir.
        var timestamp = convertToUTC(parseTimestamp(sheetResponses[i]))['utcDatetime'];
        formData[fields[i]] = timestamp;
      } else {
        if (emailFieldNames.includes(fields[i])) {
          sheetResponses[i] = sheetResponses[i].toLowerCase();
        }
        formData[fields[i]] = sheetResponses[i];
      }
      // Logger.log('SheetValues['+fields[i]+']: |' + formData[fields[i]] + '|');
    }
    Logger.log('formStatus: ' + formStatus);




    // for (var i = 0; i < Object.values(formData).length; i++) {
    //   Logger.log(Object.keys(formData)[i] + ' = ' + Object.values(formData)[i]);
    // }

    //Database baglantisini kur ve devam et
    conn = Jdbc.getConnection(serverUrl, user, userPwd);

    var candidateDetails = getCandidateInfo(conn, candidateEmail);
    Logger.log('candidateDetails: ' + candidateDetails[0] + ' ' + candidateDetails[1]);

    // Islem turune gore aksiyonlar:
    if (candidateDetails[0] !== undefined) {
      if (formStatus === 'add'){
        // formTableRowId and formData are merged for new adding
        var formDataCopy = Object.assign(formTableRowId, formData);

        var resultAddEvaluation = addEvaluation(conn, formTableName, formTableTimestampFieldName, formDataCopy);
          Logger.log('resultAddEvaluation: ' + resultAddEvaluation);

        if (resultAddEvaluation && isValidEmail(mentorEmail)) {
          var finalEvaluationIsRecordedTemplate = cnf.getFinalEvaluationIsRecordedTemplate();
          sendConfirmationEmail(mentorEmail, finalEvaluationIsRecordedTemplate, candidateDetails);
        } else {
          Logger.log('Ilk degerlendirme ile ilgili bilgi maili gonderiminde hata!');
        }
      } else {
        var resultUpdateEvaluation = updateEvaluation(conn, formTableName, formTableRowId, formTableTimestampFieldName, applicationPeriod, formData);
        // Logger.log('resultUpdateEvaluation: ' + resultUpdateEvaluation);

        if (resultUpdateEvaluation && isValidEmail(mentorEmail)) {
          var finalEvaluationIsUpdatedTemplate = cnf.getFinalEvaluationIsUpdatedTemplate();
          sendConfirmationEmail(mentorEmail, finalEvaluationIsUpdatedTemplate, candidateDetails);
        } else {
          Logger.log('Degerlendirmenin guncellenmesiyle ilgili bilgi maili gonderiminde hata!')
        }
      }
    } else {
      var wrongCandiddateEmailTemplate = cnf.getWrongCandiddateEmailTemplate();
      sendConfirmationEmail(mentorEmail, wrongCandiddateEmailTemplate, candidateDetails)
    }
  } catch (e) {
    console.error('Error occurred in onFormSubmit function: ' + e.stack);
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
