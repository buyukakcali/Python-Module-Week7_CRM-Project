//DIKKAT: Fonksiyon gecerli Worksheetteki baslik satirlarinda yazan yaziya gore calisiyor. Bu yaziyi degistirirseniz asagidan da 'Event ID' degerini de degistirin

function removeDuplicateEvents() {
  // Sheet'i al
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  // Tüm veriyi al
  var sheetData = sheet.getDataRange().getValues();

  // Başlık satırını ayır
  var headers = sheetData.shift();

  // EventID sütununun indeksini bul
  var eventIdIndex = headers.indexOf('Event ID');

  if (eventIdIndex === -1) {
    Logger.log('Event ID sütunu bulunamadı');
    return;
  }

  // Benzersiz EventID'leri ve ilgili satır numaralarını tut
  var uniqueEvents = {};
  var rowsToDelete = [];

  // Verileri kontrol et
  for (var i = 0; i < sheetData.length; i++) {
    var eventId = sheetData[i][eventIdIndex];

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

  // Tekrarlanan satirlar silindikten sonra (veri tekilligi saglandiktan sonra) Mentor Adi ve Soyadi people api tarafindan alinamayan kayitlari tekrar almaya calismak icin, writeLatestEventToSheet fonksiyonunu da calistir.
  writeLatestEventToSheet();
  if (rowsToDelete.length > 0) {
    Logger.log(rowsToDelete.length + ' adet tekrarlanan satır silindi ve mevcut verilere bakim yapildi.');
  } else {
    Logger.log(' Tekrarlanan satır yok! Sadece (ihtiyac varsa) mevcut verilere bakim yapildi.');
  }
}