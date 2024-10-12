function removeSubFolderSharingByDate() {
  try {
    var cnf = new Config();

    // configuration sheet'inin ID'si (buraya yeni sheet ID'sini ekleyin)
    var configSheetId = getSheetId(cnf.getConfigurationSheetFileName());  // Configuration dosyasinin adina gore sheet'in ID'si elde ediliyor.

    // configuration sheet'ine erişmek
    var sheet = SpreadsheetApp.openById(configSheetId);
    var sheetData = sheet.getDataRange().getValues();
    var headers = sheetData.shift(); // Başlık satırını ayırır

    // Parent Folder islemlerini tamamla
    var headerOfParentFolderColumnName = cnf.getHeaderOfParentFolderColumnName();
    var parentFolderColumnIndex = headers.indexOf(headerOfParentFolderColumnName);
    var parentFolderName = sheetData[0][parentFolderColumnIndex].toString().trim() || null;
    if (!parentFolderName) {
      Logger.log("'" + cnf.getConfigurationSheetFileName() + "' sheet dosyasinda olmasi gereken parent klasor ismi bulunmamaktadir! (Bos!!!)");
      return
    }
    var parentFolderId = getFolderIdByName(parentFolderName);
    if (!parentFolderId) {
      Logger.log("Google Drive'daki, proje klasorunde; '" + cnf.getConfigurationSheetFileName() + "' sheet dosyasinda yazili klasor adinda bir klasor bulunmamaktadir!");
      return
    }
    var parentFolder = DriveApp.getFolderById(parentFolderId);

    // deadline islemlerini tamamla
    var headerOfDeadlineColumnName = cnf.getHeaderOfDeadlineColumnName();
    var deadlineColumnIndex = headers.indexOf(headerOfDeadlineColumnName);
    var deadline = sheetData[0][deadlineColumnIndex].toString().trim();
    var removeSharingDateTime = new Date(deadline);

    var rightNow = new Date();
    if (rightNow >= removeSharingDateTime) {
      Logger.log('Removing sharing permissions for all subfolders under: ' + parentFolder.getName());

      // Call recursive function to process all folders
      removeFolderSharing(parentFolder);

      Logger.log('All sharing permissions removed for all subfolders.');
    } else {
      Logger.log('Today is before the specified removeSharingDate. No sharing permissions removed.');
    }
  } catch (e) {
    Logger.log('Error removing folder sharing: ' + e.toString());
    console.error('Error occurred in removeSubFolderSharingByDate function: ' + e.stack);
  }
}
