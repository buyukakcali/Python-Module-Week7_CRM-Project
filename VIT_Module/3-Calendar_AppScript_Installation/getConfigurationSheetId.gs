function getConfigurationSheetId(configurationSheetFileNameHere) {
  try {
    // Bu dosyanın bulunduğu klasörü al
    var currentFileId = SpreadsheetApp.getActiveSpreadsheet().getId();
    var currentFile = DriveApp.getFileById(currentFileId);
    var parentFolder = currentFile.getParents().next(); // Bu dosyanın üst klasörü

    // Aynı klasördeki tüm dosyaları tara
    var files = parentFolder.getFiles();
    while (files.hasNext()) {
      var file = files.next();

      // Eğer dosya adı "configuration" ise
      if (file.getName() === configurationSheetFileNameHere) {
        var fileId = file.getId();
        Logger.log("Configuration dosya ID: " + fileId);

        // Dosyanın sheet'ine erişmek için dosya ID'sini döndür
        var configSpreadsheet = SpreadsheetApp.openById(fileId);
        return configSpreadsheet.getId();  // Gerekirse daha spesifik sheet'leri buradan seçebilirsiniz
      }
    }
    Logger.log("Configuration dosyası bulunamadı.");
    return null;
  } catch (e) {
    console.error('Error occurred in getConfigurationSheetId function: ' + e.stack);;
  }
}
