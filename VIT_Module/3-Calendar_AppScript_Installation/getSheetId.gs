function getSheetId(sheetFileNameHere) {
  try {
    // Bu dosyanın bulunduğu klasörü al
    var currentFileId = SpreadsheetApp.getActiveSpreadsheet().getId();
    var currentFile = DriveApp.getFileById(currentFileId);
    var parentFolder = currentFile.getParents().next(); // Bu dosyanın üst klasörü

    // Aynı klasördeki tüm dosyaları tara
    var files = parentFolder.getFiles();
    while (files.hasNext()) {
      var file = files.next();

      // Eğer dosya adı "sheetFileNameHere" parametresindeki deger ise
      if (file.getName() === sheetFileNameHere) {
        var fileId = file.getId();
        Logger.log(sheetFileNameHere + " dosyasi ID: " + fileId);

        // Dosyanın sheet'ine erişmek için dosya ID'sini döndür
        var thisSpreadsheet = SpreadsheetApp.openById(fileId);
        return thisSpreadsheet.getId();  // Gerekirse daha spesifik sheet'leri buradan seçebilirsiniz
      }
    }
    Logger.log(sheetFileNameHere + " dosyası bulunamadı.");
    return null;
  } catch (e) {
    console.error('Error occurred in getSheetId function: ' + e.stack);;
  }
}
