function removeDuplicateEvents() {
  // Sheet'i al
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Tüm veriyi al
  var data = sheet.getDataRange().getValues();
  
  // Başlık satırını ayır
  var headers = data.shift();
  
  // EtkinlikID sütununun indeksini bul
  var etkinlikIdIndex = headers.indexOf('Event ID');
  
  if (etkinlikIdIndex === -1) {
    Logger.log('EtkinlikID sütunu bulunamadı');
    return;
  }
  
  // Benzersiz EtkinlikID'leri ve ilgili satır numaralarını tut
  var uniqueEvents = {};
  var rowsToDelete = [];
  
  // Verileri kontrol et
  for (var i = 0; i < data.length; i++) {
    var etkinlikId = data[i][etkinlikIdIndex];
    
    if (etkinlikId in uniqueEvents) {
      // Bu EtkinlikID daha önce görülmüş, bu satırı silmek için işaretle
      rowsToDelete.push(i + 2); // +2 çünkü başlık satırı ve 1-tabanlı indeksleme
    } else {
      // Yeni EtkinlikID, kaydet
      uniqueEvents[etkinlikId] = true;
    }
  }
  
  // Tekrarlanan satırları sil (sondan başa doğru)
  for (var i = rowsToDelete.length - 1; i >= 0; i--) {
    sheet.deleteRow(rowsToDelete[i]);
  }
  
  writeLatestEventToSheet();
  Logger.log(rowsToDelete.length + ' adet tekrarlanan satır silindi ve mevcut verilere bakim yapildi.');
}