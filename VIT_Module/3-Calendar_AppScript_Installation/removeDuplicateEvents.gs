//DIKKAT: Fonksiyon gecerli Worksheetteki baslik satirlarinda yazan yaziya gore calisiyor. Bu yaziyi degistirirseniz asagidan da 'Event ID' degerini de degistirin

function removeDuplicateEvents() {
  var rowsToDelete = [];

  try {
    var cnf = new Config();
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet(); // Sheet'i al
    var sheetData = sheet.getDataRange().getValues(); // Tüm veriyi al
    var headers = sheetData.shift();  // Başlık satırını ayır

    // EventID sütununun indeksini bul
    var eventIdIndex = headers.indexOf('Event ID');
    // NOT: Shetteki header degeri su anda 'Event ID' seklinde. Eger onu degistirirseniz, buradaki degeri de aynisi olacak sekilde degistirin.

    if (eventIdIndex === -1) {
      Logger.log('Event ID column not found, you probably changed the header value in the sheet file!');
    }

    // Benzersiz EventID'leri ve ilgili satır numaralarını tut
    var uniqueEvents = {};

    // Verileri kontrol et
    for (var i = 0; i < sheetData.length; i++) {
      var eventId = sheetData[i][eventIdIndex];
      // Logger.log('sheetdata['+i+']: ' + sheetData[i]);

      if (eventId in uniqueEvents) {
        // Bu EventID daha önce görülmüş, bu satırı silmek için işaretle
        rowsToDelete.push(i + 2); // +2 çünkü başlık satırı ve 1-tabanlı indeksleme
      } else {
        // Yeni EventID, kaydet
        uniqueEvents[eventId] = true;
      }
    }

    // Tekrarlanan satırları sil (sondan başa doğru)
    for (var i = rowsToDelete.length - 1; i >= 0; i--) {
      sheet.deleteRow(rowsToDelete[i]);
    }

  } catch (e) {
    console.error('Error occurred in removeDuplicateEvents function: ' + e.stack);
  } finally {
    // Etkinliklere davetlileri ekle ve mail gonder...
    // chooseEventLevel();
    addAttendeesToCalendarEvent();
    getFoldersWithLatestFile(getLastApplicationPeriod(cnf, cnf.openConn()));

    // Tekrarlanan satirlar silindikten sonra (veri tekilligi saglandiktan sonra) Mentor Adi ve Soyadi people api tarafindan alinamayan kayitlari tekrar almaya calismak icin, writeLatestEventToSheet fonksiyonunu da calistir.
    writeLatestEventToSheet();
    if (rowsToDelete.length > 0) {
      Logger.log(rowsToDelete.length + ' duplicate rows were deleted and existing data was maintained.');
    } else {
      Logger.log('No duplicate rows! Only maintenance of existing data (if needed).');
    }
  }
}
