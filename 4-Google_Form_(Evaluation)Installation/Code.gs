function onFormSubmit(e) {
  var conn; // Database baglantisi icin degiskenimizi tanimliyoruz.
  try {
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
    var fields = ['crm_Timestamp', 'crm_Period', 'crm_MentorMail', 'crm_CandidateMail', 'crm_ITSkills', 'crm_Availability', 'crm_Recommendation', 'crm_Comment'];
    var formData = {};

    // Email bilgisi:
    var mentorEmail = sheetResponses[2].toLowerCase();
    var candidateEmail = sheetResponses[3].toLowerCase();

    // sheetResponses verileri guncelleniyor
    sheetResponses[2] = mentorEmail;
    sheetResponses[3] = candidateEmail;

    // JDBC bağlantı bilgileri
    var properties = PropertiesService.getScriptProperties();
    var serverUrl = properties.getProperty('DB_URL');
    var user = properties.getProperty('DB_USER');
    var userPwd = properties.getProperty('DB_PASSWORD');

    var formTableName = 'form2_data';
    var formTableTimestampFieldName = 'crm_Timestamp';
    var emailFieldNames = ['crm_MentorMail', 'crmCandidateMail'];

    var applicationPeriod = {};
    applicationPeriod['crm_Period'] = sheetResponses[1];

    var formTableRowId={};
    formTableRowId['crm_RowID'] = row;

    var queryGetCandidate = 'SELECT crm_Name, crm_Surname FROM form1_applicant WHERE crm_Email = ?';

    var evaluationIsRecordedTemplate = 'evaluationIsRecordedTemplate';
    var evaluationIsUpdatedTemplate = 'evaluationIsUpdatedTemplate';
    var wrongCandiddateEmailTemplate = 'wrongCandiddateEmailTemplate';

    /**/
    /**/
    /**/
    /* ---------------------------------- Buradan yukarisi KURULUM ALANI ------------------------------------- */


    var formStatus = 'add';

    for (var i = 1; i < sheetResponses.length; i++){
      // Logger.log('sheetResponses['+i+']: '+sheetResponses[i]+' ?= formResponses['+i+']: ' + formResponses[i]);
      if (sheetResponses[i].toString() !== formResponses[i].toString()){
        formStatus = 'edit';
      }
    }

    // Sheetten gelen verileri alan adlarıyla eşleştir
    for (var i = 0; i < sheetResponses.length; i++) {
      if (fields[i].includes(formTableTimestampFieldName)) { // key degeri Timestamp_ ise iceri gir.
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

    var candidateDetails = getCandidateInfo(conn, queryGetCandidate, candidateEmail);
    Logger.log('candidateDetails: ' + candidateDetails['crm_Name'] + ' ' + candidateDetails['crm_Surname']);

    // Islem turune gore aksiyonlar:
    if (candidateDetails['crm_Name'] !== undefined) {
      if (formStatus === 'add'){
        // formTableRowId and formData are merged for new adding
        var formDataCopy = Object.assign(formTableRowId, formData);

        var resultAddEvaluation = addEvaluation(conn, formTableName, formTableTimestampFieldName, formDataCopy);
          Logger.log('resultAddEvaluation: ' + resultAddEvaluation);

        if (resultAddEvaluation && isValidEmail(mentorEmail)) {
          sendConfirmationEmail(mentorEmail, evaluationIsRecordedTemplate, candidateDetails);
        } else {
          Logger.log('Ilk degerlendirme ile ilgili bilgi maili gonderiminde hata!');
        }
      } else {
        var resultUpdateEvaluation = updateEvaluation(conn, formTableName, formTableRowId, formTableTimestampFieldName, applicationPeriod, formData);
        Logger.log('resultUpdateEvaluation: ' + resultUpdateEvaluation);

        if (resultUpdateEvaluation && isValidEmail(mentorEmail)) {
          sendConfirmationEmail(mentorEmail, evaluationIsUpdatedTemplate, candidateDetails);
        } else {
          Logger.log('Degerlendirmenin guncellenmesiyle ilgili bilgi maili gonderiminde hata!')
        }
      }
    } else {
      sendConfirmationEmail(mentorEmail, wrongCandiddateEmailTemplate, candidateDetails)
    }
  } catch (e) {
    console.error('Error occured in onFormSubmit function: ' + e.stack);
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

function readRowData(rowNumber) {
  try {
    // Aktif çalışma sayfasını alın
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Belirtilen satır numarasındaki tüm hücreleri alın
    var range = sheet.getRange(rowNumber, 1, 1, sheet.getLastColumn());

    // Hücrelerin değerlerini alın
    var rowData = range.getValues()[0];

    // Verileri bir diziye atayın
    var dataArray = [];
    for (var i = 0; i < rowData.length; i++) {
      dataArray.push(rowData[i]);
    }
    // Sonuçları konsola yazdırın (isteğe bağlı)
    // Logger.log('readRow fonksiyonu calisti');
    return dataArray;
  } catch (e) {
    console.error('Error: ' + e.stack);
    return null;
  }
}

function trimData(data) {
  var result = data;
  try {
    // Verinin string olup olmadığını kontrol edin
    if (typeof data === 'string') {
      result = data.trim(); // Başındaki ve sonundaki boşlukları temizler
    }
  } catch (e) {
    console.error('Error: ' + e.stack);
  } finally {
    return result;
  }
}


function isValidEmail(email) {
  var result = null;
  try {
    // E-posta adresinin geçerliliğini kontrol eden regex deseni
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // Logger.log('Mail Gecerlilik Durumu:' +regex.test(email));
    result = regex.test(email);
  } catch (e) {
    console.error('Error: ' + e.stack);
  } finally {
    return result;
  }
}


function addEvaluation(conn_, formTable_, formTableTimestampFieldName_, formData_) {
  try {
    var whitelist = getWhitelist(); // Whitelist'i çek
    var usedTablesInThisFunction = [formTable_];
    var columns = Object.keys(formData_);
    // Although this variable is in formData, it is still added again. Due to the danger of manual manipulation of the variable
    columns.push(formTableTimestampFieldName_);

    usedTablesInThisFunction.forEach(table => {
      if (whitelist.validTables.includes(table) == false) {
        throw new Error('Invalid table name: '+ table);
      }
    });

    columns.forEach(column => {
      if (!whitelist.validColumns.includes(column)) {
        throw new Error('Invalid column name: ' + column);
      }
    });

    for (var i = 0; i < formData_.length; i++) {
      Logger.log(Object.keys(formData_)[i] +' = ' + Object.values(formData_)[i]);
    }

    var insertStmt = 'INSERT INTO ' + formTable_ + ' (';
    insertStmt += Object.keys(formData_).join(', ') + ') VALUES (' + Object.keys(formData_).map(() => '?').join(', ') + ')';
    var stmtInsert = conn_.prepareStatement(insertStmt, Jdbc.Statement.RETURN_GENERATED_KEYS);

    // Veri sorgu metnindeki yerine atanir.
    for (var i = 0; i < Object.keys(formData_).length; i++) {
      if (Object.keys(formData_)[i] === formTableTimestampFieldName_) {
        stmtInsert.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(formData_)[i]));
      } else if (typeof(Object.values(formData_)[i]) === 'string'){
        stmtInsert.setString(i + 1, Object.values(formData_)[i]);
      } else if (typeof(Object.values(formData_)[i]) === 'number'){
        stmtInsert.setInt(i + 1, Object.values(formData_)[i]);
      } else {
        Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
      }
    }

    var resultStmtInsert = null;
    try {
      resultStmtInsert = stmtInsert.executeUpdate();
      if (!resultStmtInsert) {
        Logger.log('addEvaluation fonksiyonunda hata! Donen deger: null veya bosluk');
      }
    } catch(e) {
      console.error('Error :' + e.stack);
    } finally {
      stmtInsert.close();
      return resultStmtInsert;
    }
  } catch (e) {
    console.error('Error occured in addEvaluation function: ' + e.stack);
  }
}


function updateEvaluation(conn_, formTable_, formTableRowId_, formTableTimestampFieldName_, applicationPeriod_, formData_) {
  try {
    var whitelist = getWhitelist(); // Whitelist'i çek
    var usedTablesInThisFunction = [formTable_];
    var columns = Object.keys(formData_);
    // Although these variables are in formData, they are still added again. Due to the danger of manual manipulation of the variable
    columns.push(formTableTimestampFieldName_);
    columns.push(String(Object.keys(formTableRowId_)));

    usedTablesInThisFunction.forEach(table => {
      if (whitelist.validTables.includes(table) == false) {
        throw new Error('Invalid table name: '+ table);
      }
    });

    columns.forEach(column => {
      if (!whitelist.validColumns.includes(column)) {
        throw new Error('Invalid column name: ' + column);
      }
    });

    var queryUpdate = 'UPDATE ' + formTable_ + ' SET ';

    queryUpdate += Object.keys(formData_).join(' = ?, ') + '= ? WHERE ' + Object.keys(formTableRowId_) + ' = ? AND ' + Object.keys(applicationPeriod_) +' = ?';
    var stmtUpdate = conn_.prepareStatement(queryUpdate);

    // Veri sorgu metnindeki yerine atanir.
    for (var i = 0; i < Object.keys(formData_).length; i++) {
      if (Object.keys(formData_)[i].includes(formTableTimestampFieldName_)) {
        Logger.log('Eklenen veri: ' + Object.values(formData_)[i]);
        stmtUpdate.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(formData_)[i]));
      } else if (typeof(Object.values(formData_)[i]) === 'string'){
        stmtUpdate.setString(i + 1, Object.values(formData_)[i]);
      } else if (typeof(Object.values(formData_)[i]) === 'number'){
        stmtUpdate.setInt(i + 1, Object.values(formData_)[i]);
      } else {
        Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
      }
      Logger.log('Object.keys(formData_)['+i+']: ' + Object.keys(formData_)[i]);
      Logger.log('Object.values(formData_)['+i+']: ' + Object.values(formData_)[i]);
    }
    Logger.log('Sorgu metni: ' + queryUpdate);

    Logger.log('Object.values(formData_)[' + (Object.values(formData_).length+1) +']: '+ Object.values(formTableRowId_));
    Logger.log('Object.values(formData_)[' + (Object.values(formData_).length+2) +']: '+ Object.values(applicationPeriod_));
    stmtUpdate.setInt(Object.keys(formData_).length + 1, Object.values(formTableRowId_));  // crm_RowID
    stmtUpdate.setString(Object.keys(formData_).length + 2, Object.values(applicationPeriod_));  // crm_Period

    var resultStmtUpdate = null;
    try {
      resultStmtUpdate = stmtUpdate.executeUpdate();
      Logger.log('resultStmtUpdate===>: ' + resultStmtUpdate);
      if (resultStmtUpdate === 0){
        Logger.log('Degerlendirme formunda hicbir sey degistirilmedigi icin guncelleme yapilmadi.');
        resultStmtUpdate = null;
      } else if (resultStmtUpdate) {
        Logger.log('Degerlendirme basariyla guncellendi.');
      } else {
        Logger.log('Degerlendirme guncellenemedi! Bir hata var! Donen deger: ' + resultStmtUpdate);
      }
    } catch(e) {
      console.error('Error :' + e.stack);
    } finally {
      stmtUpdate.close();
      return resultStmtUpdate;
    }
  } catch (e) {
    console.error('Error occured in updateEvaluation function: ' + e.stack);
  }
}


function sendConfirmationEmail(emailAddress, mailType, dataList) {
  try {
    // Logger.log('Hedef e-mail: ' + emailAddress);

    // HTML şablonunu yükleyin ve içeriğini alın
    var htmlTemplate = HtmlService.createTemplateFromFile(mailType);

    // HTML içeriğini işleyin
    // HTML şablonuna işlem ID'sini geçirin
    htmlTemplate.candidateName = dataList['crm_Name'];
    htmlTemplate.candidateSurname = dataList['crm_Surname'];
    var htmlMessage = htmlTemplate.evaluate().getContent();

    // Gönderilecek e-posta içeriğini belirleyin
    if (mailType === 'evaluationIsRecordedTemplate'){
      var subject = "Değerlendirmeniz Alındı";
    } else if(mailType === 'evaluationIsUpdatedTemplate'){
      var subject = "Değerlendirmeniz Güncellendi";
    }  else if(mailType === 'wrongCandiddateEmailTemplate'){
      var subject = "Degerlendirmeniz alinMADI/guncellenMEDI";
    } else if(mailType === 'baskaBirTemplate'){
      var subject = "Baska birkonu";
    } else {
      var subject = "Bilgi maili gondermeyle ilgili sorun var!";
    }

    // E-posta gönderim işlemi
    emailSent = false;
    if (isValidEmail(emailAddress)){
      try {
        MailApp.sendEmail({
          to: emailAddress,
          subject: subject,
          htmlBody: htmlMessage
        });
        emailSent = true; // Eğer e-posta gönderimi başarılıysa değişkeni true yap
      } catch (e) {
        console.error('E-posta gönderiminde hata: ' + e.stack);
      }
    }

    // E-posta gönderim durumuna göre log yazdır
    if (emailSent) {
      Logger.log('E-posta başarıyla gönderildi: ' + emailAddress);
    } else {
      Logger.log('E-posta gönderilemedi: ' + emailAddress);
    }
  } catch (e) {
    console.error('Error: ' + e.stack);
  }
}


function parseTimestamp(timestamp) {
  try {
    // Giriş değerini string'e çevir
    if (typeof timestamp !== 'string') {
      timestamp = timestamp.toString();
    }

    // ISO 8601 formatı
    if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(timestamp)) {
      return new Date(timestamp).toISOString();
    }

    // ABD formatı (M/D/YYYY H:MM:SS AM/PM)
    if (/^\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{2}:\d{2} (AM|PM)$/.test(timestamp)) {
      return new Date(timestamp).toISOString();
    }

    // Avrupa formatı (D.M.YYYY H:MM:SS)
    if (/^\d{1,2}\.\d{1,2}\.\d{4} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('.');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[2], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[0], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // Yıl, Ay, Gün formatı (YYYY/M/D H:MM:SS)
    if (/^\d{4}\/\d{1,2}\/\d{1,2} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('/');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[0], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[2], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // Gün/Ay/Yıl formatı (D/M/YYYY H:MM:SS)
    if (/^\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('/');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[2], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[0], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // Gün-Ay-Yıl formatı (D-M-YYYY H:MM:SS)
    if (/^\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('-');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[2], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[0], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // Yıl.Ay.Gün formatı (YYYY.M.D H:MM:SS)
    if (/^\d{4}\.\d{1,2}\.\d{1,2} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('.');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[0], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[2], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // YYYY-MM-DD formatı (YYYY-MM-DD H:MM:SS)
    if (/^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('-');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[0], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[2], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // YYYY-MM-DD formatı (sadece tarih)
    if (/^\d{4}-\d{2}-\d{2}$/.test(timestamp)) {
      return new Date(timestamp).toISOString();
    }

    // MM/DD/YYYY formatı
    if (/^\d{2}\/\d{2}\/\d{4}$/.test(timestamp)) {
      return new Date(timestamp).toISOString();
    }

    // YYYY/MM/DD formatı
    if (/^\d{4}\/\d{2}\/\d{2}$/.test(timestamp)) {
      var parts = timestamp.split('/');
      return new Date(Date.UTC(
        parseInt(parts[0], 10),
        parseInt(parts[1], 10) - 1,
        parseInt(parts[2], 10)
      )).toISOString();
    }

    // Kompakt format (YYYYMMDDTHHMMSS)
    if (/^\d{8}T\d{6}$/.test(timestamp)) {
      return new Date(
        timestamp.substr(0, 4),
        parseInt(timestamp.substr(4, 2), 10) - 1,
        timestamp.substr(6, 2),
        timestamp.substr(9, 2),
        timestamp.substr(11, 2),
        timestamp.substr(13, 2)
      ).toISOString();
    }

    // Standart JavaScript Date.toString() formatı
    if (/^[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2} GMT[+-]\d{4} \(.*\)$/.test(timestamp)) {
      return new Date(timestamp).toISOString();
    }

    // Eğer hiçbir format eşleşmezse
    throw new Error('Tanınmayan zaman damgası formatı: ' + timestamp);

  } catch (e) {
    console.error('Error: ' + e.stack);
  }
}

/*

Açıklama:
ISO 8601 formatı: (^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$)
ABD formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{2}:\d{2} (AM|PM)$)
Avrupa formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}\.\d{1,2}\.\d{4} \d{2}:\d{2}:\d{2}$)
Yıl, Ay, Gün formatı: Tek haneli gün ve ayları da destekler (^\d{4}\/\d{1,2}\/\d{1,2} \d{2}:\d{2}:\d{2}$)
Gün/Ay/Yıl formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2}:\d{2}$)
Gün-Ay-Yıl formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}:\d{2}$)
Yıl.Ay.Gün formatı: Tek haneli gün ve ayları da destekler (^\d{4}\.\d{1,2}\.\d{1,2} \d{2}:\d{2}:\d{2}$)
YYYY-MM-DD formatı: Tek haneli gün ve ayları da destekler (^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}$)
Sadece tarih (YYYY-MM-DD): (^\d{4}-\d{2}-\d{2}$)
MM/DD/YYYY formatı: (^\d{2}\/\d{2}\/\d{4}$)
YYYY/MM/DD formatı: (^\d{4}\/\d{2}\/\d{2}$)
Kompakt format: (^\d{8}T\d{6}$)
Standart JavaScript Date.toString() formatı: (^[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2} GMT[+-]\d{4} \(.*\)$)

Not: Tüm formatlar, uygun olduğunda tek haneli gün ve ayları destekler.
Fonksiyon, giriş değerini otomatik olarak string'e çevirir.
Çıktı her zaman ISO 8601 formatında olacaktır.

*/

function convertToUTC(isoString) {
  try {
    // ISO string'i Date nesnesine çevir
    const date = new Date(isoString);

    // Geçerli bir tarih olup olmadığını kontrol et
    if (isNaN(date.getTime())) {
      throw new Error('Geçersiz tarih formatı: ' + isoString);
    }

    // UTC timestamp (milisaniye cinsinden)
    const utcTimestamp = date.getTime();

    // UTC datetime nesnesi
    const utcDatetime = new Date(utcTimestamp);

    return {
      utcTimestamp: utcTimestamp,
      utcDatetime: utcDatetime,
      formattedUTC: utcDatetime.toUTCString(),
      isoUTC: utcDatetime.toISOString()
    };
  } catch (e) {
    console.error('Error: ' + e.stack);
    return {
      'utcTimestamp': null,
      'utcDatetime': null,
      'formattedUTC': null,
      'isoUTC': null
    };
  }
}

/*
Bu fonksiyon şunları yapar:

Verilen ISO 8601 formatındaki string'i bir JavaScript Date nesnesine çevirir.
Oluşturulan tarihin geçerli olup olmadığını kontrol eder.
UTC timestamp'ini (Unix zamanı, milisaniye cinsinden) hesaplar.
UTC datetime nesnesini oluşturur.
Bir nesne döndürür, bu nesne şunları içerir:

utcTimestamp: UTC zaman damgası (milisaniye cinsinden)
utcDatetime: UTC datetime nesnesi
formattedUTC: İnsan tarafından okunabilir UTC string formatı
isoUTC: ISO 8601 formatında UTC string


Bu fonksiyonu şu şekilde kullanabilirsiniz:

KOD BLOGU BASLAR:

// Önce parseTimestamp fonksiyonunu kullanarak bir tarih parse edelim
const parsedDate = parseTimestamp("2023-08-15 14:30:00");

// Şimdi bu tarihi UTC'ye dönüştürelim
const utcResult = convertToUTC(parsedDate);

console.log(utcResult.utcTimestamp); // Örnek: 1692108600000
console.log(utcResult.utcDatetime); // Örnek: 2023-08-15T14:30:00.000Z (Date nesnesi)
console.log(utcResult.formattedUTC); // Örnek: "Tue, 15 Aug 2023 14:30:00 GMT"
console.log(utcResult.isoUTC); // Örnek: "2023-08-15T14:30:00.000Z"

KOD BLOGU BITTI:

Bu fonksiyon, parseTimestamp fonksiyonunun döndürdüğü her türlü ISO 8601 formatındaki tarihi alabilir ve onu UTC zaman damgasına ve datetime nesnesine dönüştürür. Ayrıca, insan tarafından okunabilir bir format ve ISO 8601 UTC formatı da sağlar. Bu, farklı ihtiyaçlarınız için esneklik sağlar.

*/