/*
removeSubFolderSharingByDate fonksiyonu icinde cagrilan yardimci fonksiyondur. Klasorun adini parametre olarak alir ve Drive'da bu klasoru bularak Id'sini dondurur.
*/
function getFolderIdByName(folderName) {
  try {
    // Verilen isimde bir klasör arayın
    var folders = DriveApp.getFoldersByName(folderName);

    // Eğer klasör bulunursa, ID'sini döndür
    if (folders.hasNext()) {
      var folder = folders.next();
      // Logger.log('Folder ID: ' + folder.getId()); // Klasör ID'sini konsola yazdır
      return folder.getId();
    } else {
      Logger.log('Folder not found with the name: ' + folderName);
      return null;
    }
  } catch (e) {
    console.error('Error occurred in getFolderIdByName function: ' + e.stack);
    return null;
  }
}
