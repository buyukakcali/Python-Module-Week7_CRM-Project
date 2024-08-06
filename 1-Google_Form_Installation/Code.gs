function onFormSubmit(e) {
  // Form yanıtlarının geldiği Sheet'i alın
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  // Form yanıtının eklenmiş olduğu satır numarasını alın
  var row = e.range.getRow();

  var formResponses = e.values; // Formdan gelen yanitlar formResponses adinda bir diziye ekleniyor.
  // Logger.log('e.values: ' + e.values);
  var sheetResponses = readRowData(row); // Worksheetten gelen veriler sheetResponses adinda bir diziye ekleniyor.

  /* ----- KURULUM ALANI (Asagi dogru) - Projeyi uyarlamak icin yalnizca buradaki verileri duzenleyin!!! Kodlar otomatik calisacaktir. ------ */
  /**/
  /**/
  /**/

  // Alanları tanımla
  var fields = ['ZamanDamgasi', 'BasvuruDonemi', 'Ad', 'Soyad', 'Email', 'Telefon', 'PostaKodu', 'YasadiginizEyalet', 'SuAnkiDurum', 'ITPHEgitimKatilmak', 'EkonomikDurum', 'DilKursunaDevam', 'IngilizceSeviye', 'HollandacaSeviye', 'BaskiGoruyor', 'BootcampBitirdi', 'OnlineITKursu', 'ITTecrube', 'ProjeDahil', 'CalismakIstedigi', 'NedenKatilmakIstiyor', 'MotivasyonunNedir'];  // Ayarlanacak alan!!!
  var values = {};

  // Email bilgisi:
  var email = sheetResponses[4];


  // JDBC bağlantı bilgileri
  var properties = PropertiesService.getScriptProperties();
  var serverUrl = properties.getProperty('DB_URL');
  var user = properties.getProperty('DB_USER');
  var userPwd = properties.getProperty('DB_PASSWORD');
  var conn;

  var formTable = 'form_data';
  var formTableRowIdFieldName = 'RowID';
  var formTableTimestampFieldName = 'ZamanDamgasi';
  var applicationPeriodFieldName = 'BasvuruDonemi';
  var postalCodeColumnIndex = 7; // Örneğin, posta kodları G sütunundaysa 7 olur

  var newApplicationAddedTemplate = 'yeniBasvuruEklendiTemplate';
  var applicationIsUpdatedTemplate = 'basvuruGuncellendiTemplate';

  /**/
  /**/
  /**/
  /* ---------------------------------- Buradan yukarisi KURULUM ALANI ------------------------------------- */


  try {
    conn = Jdbc.getConnection(serverUrl, user, userPwd);
    var formStatus = 'add';

    for (var i = 1; i < sheetResponses.length; i++){
      // Logger.log('sheetResponses['+i+']: '+sheetResponses[i]+' ?= formResponses['+i+']: ' + formResponses[i]);
      if (sheetResponses[i] !== formResponses[i]){
        formStatus = 'edit';
      }
    }

    // ONCE POSTA KODU ISTENEN FORMATTA KAYDEDILECEK
    // 1) Posta kodlarının bulunduğu sütunun indeksini belirtin
    // var postalCodeColumnIndex = 7; // Örneğin, posta kodları G sütunundaysa 7 olur [{(* !!! Konfigurasyon alanina tasindi! *)}]

    // 2) Yeni eklenen satırdaki posta kodunu alın ve temizleyin
    var postalCode = sheet.getRange(row, postalCodeColumnIndex).getValue().toString().toUpperCase().trim();
    var cleanedPostalCode = cleanPostalCode(postalCode);

    // 3) Temizlenmiş posta kodunu güncelleyin
    sheet.getRange(row, postalCodeColumnIndex).setValue(cleanedPostalCode);

    // 4) Database'e gondermeden once veriyi duzeltiyoruz.
    sheetResponses[postalCodeColumnIndex - 1] = cleanPostalCode(sheetResponses[postalCodeColumnIndex - 1]);


    // Worksheetten gelen verileri alan adlarıyla eşleştir
    for (var i = 0; i < sheetResponses.length; i++) {
      if (fields[i].startsWith(formTableTimestampFieldName)) { // key degeri ZamanDamgasi ise iceri gir.
        var timestamp = parseTimestamp(sheetResponses[i]);
        values[fields[i]] = timestamp;
      } else {
        values[fields[i]] = sheetResponses[i];
      }
      Logger.log('WorksheetValues['+fields[i]+']: ' + values[fields[i]]);
    }

    if (formStatus === 'add'){
      var resultAddBasvuru = addBasvuru(conn, formTable, formTableRowIdFieldName, formTableTimestampFieldName, row, values);
      if (resultAddBasvuru && isValidEmail(email)) {
        sendConfirmationEmail(email, row, newApplicationAddedTemplate)
      } else {
        Logger.log('Mail (yeni basvuru) gonderiminde hata!');
      }
    } else {
      var resultUpdateBasvuru = updateBasvuru(conn, formTable, formTableRowIdFieldName, formTableTimestampFieldName, applicationPeriodFieldName, row, values);

      if (resultUpdateBasvuru && isValidEmail(email)) {
        sendConfirmationEmail(email, row, applicationIsUpdatedTemplate);
      } else {
        Logger.log('Mail gonderiminde hata!')
      }
    }
  } catch (e) {
    Logger.log('Hata oluştu: ' + e.message);
  } finally {
    if (conn) {
      try {
        conn.close();
      } catch (e) {
        Logger.log('Bağlantı kapatma hatası: ' + e.message);
      }
    }
  }
}

function readRowData(rowNumber) {
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
}


// Posta kodunu temizleyen ve tüm boşluk karakterlerini yok eden fonksiyon
function cleanPostalCode(postalCode) {
  // Tüm boşluk karakterlerini kaldır ve büyük harfe çevir
  return postalCode.replace(/\s+/g, '').toUpperCase();
}


function isValidEmail(email) {
  // E-posta adresinin geçerliliğini kontrol eden regex deseni
  var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  // Logger.log('Mail Gecerlilik Durumu:' +regex.test(email));
  return regex.test(email);
}

// Kullanım örnekleri
// console.log(isValidEmail("example@example.com")); // true
// console.log(isValidEmail("example.com")); // false
// console.log(isValidEmail("example@.com")); // false
// console.log(isValidEmail("example@com")); // false
// console.log(isValidEmail("example@example..com")); // false
// console.log(isValidEmail("example@sub.example.com")); // true


function addBasvuru(conn, table, form_table_id_name, form_table_timestamp_column_name, row, values) {
  // Sadece dolu alanları al ve yeni kursiyer ekle
  var insertStmtBasvuru = 'INSERT INTO ' + table + ' ('
  var insertFieldsBasvuru = [form_table_id_name];
  var insertValuesBasvuru = [row];
  for (var field in values) {
    if (values[field]) {
      insertFieldsBasvuru.push(field);
      insertValuesBasvuru.push(values[field]);
    }
  }

  insertStmtBasvuru += insertFieldsBasvuru.join(', ') + ') VALUES (' + insertFieldsBasvuru.map(() => '?').join(', ') + ')';
  var stmtInsertBasvuru = conn.prepareStatement(insertStmtBasvuru, Jdbc.Statement.RETURN_GENERATED_KEYS);

  for (var i = 0; i < insertFieldsBasvuru.length; i++) {
    if (insertFieldsBasvuru[i] === form_table_id_name){
      stmtInsertBasvuru.setInt(i + 1, insertValuesBasvuru[i]);
    } else if (insertFieldsBasvuru[i] === form_table_timestamp_column_name) {
      // Logger.log('convertToUTC(insertValuesBasvuru['+i+'])[utcDatetime]: ' + convertToUTC(insertValuesBasvuru[i])['utcDatetime']);
      stmtInsertBasvuru.setTimestamp(i + 1, Jdbc.newTimestamp(convertToUTC(insertValuesBasvuru[i])['utcDatetime']));
    } else {
      stmtInsertBasvuru.setString(i + 1, insertValuesBasvuru[i]);
    }
  }
  var resultStmtInsertBasvuru = null;

  try {
    resultStmtInsertBasvuru = stmtInsertBasvuru.executeUpdate();
    if (resultStmtInsertBasvuru) {
      return resultStmtInsertBasvuru;
      // return resultStmtInsertBasvuru.getInt(1);
    } else {
      Logger.log('addBasvuru fonksiyonunda hata! Donen deger: null veya bosluk');
      return null;
    }
  } catch (e) {
    Logger.log('Hata: ' + e);
  } finally {
    stmtInsertBasvuru.close();
  }
}


function updateBasvuru(conn, table, form_table_id_name, form_table_timestamp_column_name, appPeriodFieldName, row, values) {
  // Sadece dolu alanları sorguya ekle
  var updateStmtBasvuru = 'UPDATE ' + table + ' SET ';
  var updateFieldsBasvuru = [];
  var updateValuesBasvuru = [];

  for (var field in values) {
    if (values[field]) {
      updateFieldsBasvuru.push(field + ' = ?');
      updateValuesBasvuru.push(values[field]);
    }
  }

  updateStmtBasvuru += updateFieldsBasvuru.join(', ') + ' WHERE ' + form_table_id_name + ' = ? AND ' + appPeriodFieldName +' = ?';
  var stmtUpdateBasvuru = conn.prepareStatement(updateStmtBasvuru);

  for (var i = 0; i < updateValuesBasvuru.length; i++) {
    // Logger.log('updateFieldsBasvuru['+i+']: ' + updateValuesBasvuru[i]);
    if (updateFieldsBasvuru[i].startsWith(form_table_timestamp_column_name)) {
      stmtUpdateBasvuru.setTimestamp(i + 1, Jdbc.newTimestamp(convertToUTC(updateValuesBasvuru[i])['utcDatetime']));
    } else {
      stmtUpdateBasvuru.setString(i + 1, updateValuesBasvuru[i]);
      // Logger.log('updateFieldsBasvuru['+i+']: ' + updateValuesBasvuru[i]);
    }
    // Logger.log('updateFieldsBasvuru['+i+']: '+updateFieldsBasvuru[i]);
    // Logger.log('updateValuesBasvuru['+i+']: '+updateValuesBasvuru[i]);
  }
  // Logger.log('updateValuesBasvuru[' + (updateValuesBasvuru.length+1) +']: '+ row);
  stmtUpdateBasvuru.setInt(updateValuesBasvuru.length + 1, row);  // RowID
  stmtUpdateBasvuru.setString(updateValuesBasvuru.length + 2, values[appPeriodFieldName]);  // BasvuruDonemi
  var resultStmtUpdateBasvuru = null;
  // Logger.log('updateStmtBasvuru Sorgu Metni: ' + updateStmtBasvuru);

  try {
    resultStmtUpdateBasvuru = stmtUpdateBasvuru.executeUpdate();
    // Logger.log('resultStmtUpdateBasvuru===>: ' + resultStmtUpdateBasvuru);
    if (resultStmtUpdateBasvuru === 0){
      Logger.log('Basvuru formunda hicbir sey degistirilmedigi icin basvuru guncelleme yapilmadi.');
      return 'emptydata';
    } else if (resultStmtUpdateBasvuru) {
      Logger.log('Basvuru basariyla guncellendi.');
      return resultStmtUpdateBasvuru;
    } else {
      Logger.log('Basvuru guncellenemedi! Bir hata var! Donen deger: ' + resultStmtUpdateBasvuru);
      return null;
    }
  } catch (e) {
    Logger.log('Hata: ' + e);
  } finally {
    stmtUpdateBasvuru.close();
  }
}


function sendConfirmationEmail(emailAddress, transactionId, mailType) {
  // Form yanıtlarının geldiği Sheet'in adını alın
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  // Logger.log('Hedef e-mail: ' + emailAddress);

  // HTML şablonunu yükleyin ve içeriğini alın
  var htmlTemplate = HtmlService.createTemplateFromFile(mailType);

  // HTML içeriğini işleyin
  htmlTemplate.transactionId = transactionId; // HTML şablonuna işlem ID'sini geçirin
  var htmlMessage = htmlTemplate.evaluate().getContent();

  // Gönderilecek e-posta içeriğini belirleyin
  if (mailType === 'yeniBasvuruEklendiTemplate'){
    var subject = "Başvurunuz Alındı";
  } else if(mailType === 'basvuruGuncellenemediTemplate'){
    var subject = "Basvurunuz Guncellenemedi";
  } else if(mailType === 'basvuruGuncellemedeHataTemplate'){
    var subject = "Basvurunuz Guncellemede Kritik*(Uygulama) Hata";
  } else {
    var subject = "Başvurunuz Guncellendi";
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
    } catch (error) {
      Logger.log('E-posta gönderiminde hata: ' + error.message);
    }
  }

  // E-posta gönderim durumuna göre log yazdır
  if (emailSent) {
    Logger.log('E-posta başarıyla gönderildi: ' + emailAddress);
  } else {
    Logger.log('E-posta gönderilemedi: ' + emailAddress);
  }
}


function parseTimestamp(timestamp) {
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