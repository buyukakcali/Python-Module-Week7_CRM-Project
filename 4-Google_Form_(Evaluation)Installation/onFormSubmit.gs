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
    Logger.log('candidateDetails: ' + candidateDetails[0] + ' ' + candidateDetails[1]);

    // Islem turune gore aksiyonlar:
    if (candidateDetails[0] !== undefined) {
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
        // Logger.log('resultUpdateEvaluation: ' + resultUpdateEvaluation);

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
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet(); // Aktif çalışma sayfasını alın
    var range = sheet.getRange(rowNumber, 1, 1, sheet.getLastColumn()); // Belirtilen satır numarasındaki tüm hücreleri alın
    var rowData = range.getValues()[0]; // Hücrelerin değerlerini alın

    // Verileri bir diziye atayın
    var dataArray = [];
    for (var i = 0; i < rowData.length; i++) {
      dataArray.push(rowData[i]);
    }
    return dataArray;
  } catch (e) {
    console.error('Error: ' + e.stack);
  }
}

function trimData(data) {
  try {
    // Verinin string olup olmadığını kontrol edin
    if (typeof data === 'string') {
      data = data.trim(); // Başındaki ve sonundaki boşlukları temizler
    }
  } catch (e) {
    console.error('Error oocured in trimData function: ' + e.stack);
  } finally {
    return data;
  }
}

function isValidEmail(email) {
  try {
    // E-posta adresinin geçerliliğini kontrol eden regex deseni
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // Logger.log('Mail Gecerlilik Durumu:' +regex.test(email));
    return regex.test(email);
  } catch (e) {
    console.error('Error occured in isValidEmail function: ' + e.stack);
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
    console.error('Error  occured in parseTimestamp function: ' + e.stack);
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
    console.error('Error occured in convertToUTC function: ' + e.stack);
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
