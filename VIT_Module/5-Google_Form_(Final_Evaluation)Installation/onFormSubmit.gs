function onFormSubmit(e) {
  try {
    // Form yanıtının eklenmiş olduğu satır numarasını alın
    var row = e.range.getRow();

    // formResponses ve sheetResponses dizilerine veriler alindiktan sonra, her iki objedeki veriler trim fonksiyonu ile temizlenecek.
    var formResponses = e.values.map(trimData); // Formdan gelen yanitlar formResponses adinda bir diziye ekleniyor ve temizleniyor.
    var sheetResponses = readRowData(row).map(trimData); // Sheetten gelen veriler sheetResponses adinda bir diziye ekleniyor ve temizleniyor.

    var formStatus = 'add';
    for (var i = 1; i < formResponses.length; i++){
      // Logger.log('sheetResponses['+i+']: '+sheetResponses[i]+' ?= formResponses['+i+']: ' + formResponses[i]);
      if (sheetResponses[i].toString() !== formResponses[i].toString()){
        formStatus = 'edit';
      }
    }
    // Logger.log('formStatus: ' + formStatus);

    // Sheetten gelen verileri alan adlarıyla eşleştir
    var cnf = new Config();
    var fields = cnf.getFields();
    var emailFieldNames = cnf.getEmailFieldNames();
    var timestampFieldName = cnf.getTimestampFieldName();
    var formData = {};

    for (var i = 0; i < formResponses.length; i++) {
      if (fields[i].startsWith(timestampFieldName)) { // key degeri crm_Timestamp ise iceri gir.
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

    // Islem turune gore aksiyonlar:
    var mentorEmail = sheetResponses[2].toLowerCase();
    var candidateEmail = sheetResponses[3].toLowerCase();
    // Get candidate's details
    var candidateDetails = getCandidateInfo(candidateEmail);
    // Logger.log('candidateDetails: ' + candidateDetails[0] + ' ' + candidateDetails[1]);

    if (candidateDetails[0] !== undefined) {
      var rowId = {};
      rowId[cnf.getRowIdFieldName()] = row;
      if (formStatus === 'add'){
        // rowId and formData are merged for new adding
        var formData = Object.assign(rowId, formData);

        var resultAddEvaluation = addEvaluation(formData);
        // Logger.log('resultAddEvaluation: ' + resultAddEvaluation);

        if (resultAddEvaluation && isValidEmail(mentorEmail)) {
          var finalEvaluationIsRecordedTemplate = cnf.getFinalEvaluationIsRecordedTemplate();
          sendConfirmationEmail(mentorEmail, finalEvaluationIsRecordedTemplate, candidateDetails);
        } else {
          Logger.log('Final proje degerlendirmesi ile ilgili bilgi maili gonderiminde hata!');
        }
      } else {
        var applicationPeriod = {};
        applicationPeriod[cnf.getApplicationPeriodFieldName()] = sheetResponses[1];
        var resultUpdateEvaluation = updateEvaluation(rowId, applicationPeriod, formData);
        // Logger.log('resultUpdateEvaluation: ' + resultUpdateEvaluation);

        if (resultUpdateEvaluation && isValidEmail(mentorEmail)) {
          var finalEvaluationIsUpdatedTemplate = cnf.getFinalEvaluationIsUpdatedTemplate();
          sendConfirmationEmail(mentorEmail, finalEvaluationIsUpdatedTemplate, candidateDetails);
        } else {
          Logger.log('Degerlendirmenin guncellenmesiyle ilgili bilgi maili gonderiminde hata!');
        }
      }
    } else {
      var wrongCandiddateEmailTemplate = cnf.getWrongCandiddateEmailTemplate();
      sendConfirmationEmail(mentorEmail, wrongCandiddateEmailTemplate, candidateDetails);
      Logger.log('Hatalı girilen e-posta adresi ile ilgili olarak mentöre bilgilendirme maili atılıyor!');
    }
  } catch (e) {
    console.error('Error occurred in onFormSubmit function: ' + e.stack);
  }
}
