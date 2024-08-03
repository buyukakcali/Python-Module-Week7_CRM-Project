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

  var form_table = 'form_data';
  var form_table_id_name = 'RowID';
  var form_table_timestamp_column_name = 'ZamanDamgasi';
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
    var postalCodeColumnIndex = 7; // Örneğin, posta kodları G sütunundaysa 7 olur

    // 2) Yeni eklenen satırdaki posta kodunu alın ve temizleyin
    var postalCode = sheet.getRange(row, postalCodeColumnIndex).getValue().toString().toUpperCase().trim();
    var cleanedPostalCode = cleanPostalCode(postalCode);
    
    // 3) Temizlenmiş posta kodunu güncelleyin
    sheet.getRange(row, postalCodeColumnIndex).setValue(cleanedPostalCode);

    // 4) Database'e gondermeden once veriyi duzeltiyoruz.
    sheetResponses[postalCodeColumnIndex - 1] = cleanPostalCode(sheetResponses[postalCodeColumnIndex - 1]);

    // Worksheetten gelen verileri alan adlarıyla eşleştir
    for (var i = 0; i < sheetResponses.length; i++) {
      values[fields[i]] = sheetResponses[i];
      // Logger.log('Worlsheet> values['+fields[i]+']: ' + values[fields[i]]);      
    }

    if (formStatus === 'add'){
      var resultAddBasvuru = addBasvuru(conn, form_table, form_table_id_name, form_table_timestamp_column_name, row, values);
      if (resultAddBasvuru && isValidEmail(email)) {
        sendConfirmationEmail(email, row, newApplicationAddedTemplate)
      } else {
        Logger.log('Mail (yeni basvuru) gonderiminde hata!');
      }
    } else {
      var resultUpdateBasvuru = updateBasvuru(conn, form_table, form_table_id_name, form_table_timestamp_column_name, row, values);

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

  // Verileri döndürün
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


function convertToTimestamp(dateString) {
  var formats = [
    { regex: /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?(?:Z|[+-]\d{2}:\d{2})?$/, parser: parseISO },
    { regex: /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/, parser: parseYYYYMMDD_HHMMSS },
    { regex: /^\d{4}-\d{2}-\d{2}$/, parser: parseYYYYMMDD },
    { regex: /^\d{2}\/\d{2}\/\d{4}$/, parser: parseMMDDYYYY },
    { regex: /^\d{2}-\d{2}-\d{4}$/, parser: parseDDMMYYYY },
    { regex: /^\d{4}\/\d{2}\/\d{2}$/, parser: parseYYYYMMDD_Slash },
    { regex: /^\d{8}T\d{6}$/, parser: parseCompact },
    { regex: /^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}$/, parser: parseDDMMYYYY_HHMMSS },
    { regex: /^\d{1,2}\.\d{1,2}\.\d{4} \d{2}:\d{2}:\d{2}$/, parser: parseDMMYYYY_HHMMSS },
    { regex: /^\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2}:\d{2}$/, parser: parseMDYYYY_HHMMSS },
    { regex: /^\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}:\d{2}$/, parser: parseDMYYYY_HHMMSS },
    { regex: /^\d{1,2}\.\d{1,2}\.\d{4} \d{2}:\d{2}:\d{2}$/, parser: parseMDYYYY_HHMMSS },
    { regex: /^[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2} GMT[+-]\d{4} \(.*\)$/, parser: parseDateString }
  ];

  for (var i = 0; i < formats.length; i++) {
    var format = formats[i];
    if (format.regex.test(dateString)) {
      return format.parser(dateString);
    }
  }

  // Default parser for other date formats, including all time zones and country formats
  return parseDefault(dateString);
}

function parseISO(dateString) {
  return new Date(dateString);
}

function parseYYYYMMDD_HHMMSS(dateString) {
  var parts = dateString.split(/[- :]/);
  return new Date(parts[0], parts[1] - 1, parts[2], parts[3], parts[4], parts[5]);
}

function parseYYYYMMDD(dateString) {
  var parts = dateString.split('-');
  return new Date(parts[0], parts[1] - 1, parts[2]);
}

function parseMMDDYYYY(dateString) {
  var parts = dateString.split('/');
  return new Date(parts[2], parts[0] - 1, parts[1]);
}

function parseDDMMYYYY(dateString) {
  var parts = dateString.split('-');
  return new Date(parts[2], parts[1] - 1, parts[0]);
}

function parseYYYYMMDD_Slash(dateString) {
  var parts = dateString.split('/');
  return new Date(parts[0], parts[1] - 1, parts[2]);
}

function parseCompact(dateString) {
  var year = parseInt(dateString.substring(0, 4), 10);
  var month = parseInt(dateString.substring(4, 6), 10) - 1;
  var day = parseInt(dateString.substring(6, 8), 10);
  var hour = parseInt(dateString.substring(9, 11), 10);
  var minute = parseInt(dateString.substring(11, 13), 10);
  var second = parseInt(dateString.substring(13, 15), 10);
  return new Date(year, month, day, hour, minute, second);
}

function parseDDMMYYYY_HHMMSS(dateString) {
  var parts = dateString.split(/[. :]/);
  var day = parts[0];
  var month = parts[1];
  var year = parts[2];
  var hour = parts[3];
  var minute = parts[4];
  var second = parts[5];
  
  return new Date(year, month - 1, day, hour, minute, second);
}

function parseDMMYYYY_HHMMSS(dateString) {
  var parts = dateString.split(/[. :]/);
  var day = parts[0];
  var month = parts[1];
  var year = parts[2];
  var hour = parts[3];
  var minute = parts[4];
  var second = parts[5];

  return new Date(year, month - 1, day, hour, minute, second);
}

function parseMDYYYY_HHMMSS(dateString) {
  var parts = dateString.split(/[\/. :]/);
  var month = parts[0];
  var day = parts[1];
  var year = parts[2];
  var hour = parts[3];
  var minute = parts[4];
  var second = parts[5];

  return new Date(year, month - 1, day, hour, minute, second);
}

function parseDMYYYY_HHMMSS(dateString) {
  var parts = dateString.split(/[- :]/);
  var day = parts[0];
  var month = parts[1];
  var year = parts[2];
  var hour = parts[3];
  var minute = parts[4];
  var second = parts[5];

  return new Date(year, month - 1, day, hour, minute, second);
}

function parseDateString(dateString) {
  return new Date(dateString);
}

function parseDefault(dateString) {
  return new Date(dateString);
}

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
      stmtInsertBasvuru.setTimestamp(i + 1, Jdbc.newTimestamp(convertToTimestamp(insertValuesBasvuru[i])));
    } else {
      stmtInsertBasvuru.setString(i + 1, insertValuesBasvuru[i]);
    }
  }
  var resultStmtInsertBasvuru = stmtInsertBasvuru.executeUpdate();

  // var resultStmtInsertBasvuru = stmtInsertBasvuru.getGeneratedKeys();
  // if (resultStmtInsertBasvuru.next()) {
     if (resultStmtInsertBasvuru) {
    return resultStmtInsertBasvuru;
    // return resultStmtInsertBasvuru.getInt(1);
  } else {
    Logger.log('addBasvuru fonksiyonunda hata! Donen deger: null veya bosluk');
    return null;
  }
}


function updateBasvuru(conn, table, form_table_id_name, form_table_timestamp_column_name, row, values) {
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

  updateStmtBasvuru += updateFieldsBasvuru.join(', ') + ' WHERE ' + form_table_id_name + ' = ? AND BasvuruDonemi = ?';
  var stmtUpdateBasvuru = conn.prepareStatement(updateStmtBasvuru);

  for (var i = 0; i < updateValuesBasvuru.length; i++) {
    // Logger.log('updateFieldsBasvuru['+i+']: ' + updateValuesBasvuru[i]); 
    if (updateFieldsBasvuru[i].startsWith(form_table_timestamp_column_name)) {
      stmtUpdateBasvuru.setTimestamp(i + 1, Jdbc.newTimestamp(convertToTimestamp(updateValuesBasvuru[i])));
    } else {
      stmtUpdateBasvuru.setString(i + 1, updateValuesBasvuru[i]);
      // Logger.log('updateFieldsBasvuru['+i+']: ' + updateValuesBasvuru[i]);
    }
    // Logger.log('updateFieldsBasvuru['+i+']: '+updateFieldsBasvuru[i]);
    // Logger.log('updateValuesBasvuru['+i+']: '+updateValuesBasvuru[i]);
  }
  // Logger.log('updateValuesBasvuru[' + (updateValuesBasvuru.length+1) +']: '+ row);
  stmtUpdateBasvuru.setInt(updateValuesBasvuru.length + 1, row);  // RowID
  stmtUpdateBasvuru.setString(updateValuesBasvuru.length + 2, values['BasvuruDonemi']);  // BasvuruDonemi
  // Logger.log('updateStmtBasvuru Sorgu Metni: ' + updateStmtBasvuru);

  var resultStmtUpdateBasvuru = stmtUpdateBasvuru.executeUpdate();
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
