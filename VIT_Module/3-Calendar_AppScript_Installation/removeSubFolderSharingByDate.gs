function removeSubFolderSharingByDate() {
  try {
    var cnf = new Config();
    var headerOfParentFolderColumnName = cnf.getHeaderOfParentFolderColumnName();
    var headerOfDeadlineColumnName = cnf.getHeaderOfDeadlineColumnName();

    // Yeni sheet'in ID'si (buraya yeni sheet ID'sini ekleyin)
    var configSheetId = getConfigurationSheetId(cnf.getConfigurationSheetFileName());  // Configuration dosyasinin adina gore sheet'in ID'si elde ediliyor.

    // Yeni sheet'e erişmek
    var sheet = SpreadsheetApp.openById(configSheetId);
    var sheetData = sheet.getDataRange().getValues();
    var headers = sheetData.shift(); // Başlık satırını ayırır

    // headerOfDeadlineColumnName değişkeninde yer alan değerin bulunduğu sütunun indeksini bul
    var parentFolderColumnIndex = headers.indexOf(headerOfParentFolderColumnName);
    var parentFolderName = sheetData[0][parentFolderColumnIndex].toString().trim() || null;
    if (!parentFolderName) {
      return
    }
    var parentFolderId = getFolderIdByName(parentFolderName);
    if (!parentFolderId) {
      Logger.log("Google Drive'daki, proje klasorunde; '" + cnf.getConfigurationSheetFileName() + "' sheet dosyasinda yazili klasor adinda bir klasor bulunmamaktadir!");
      return
    }
    var parentFolder = DriveApp.getFolderById(parentFolderId);

    // deadlineColumnName değişkeninde yer alan değerin bulunduğu sütunun indeksini bul
    var deadlineColumnIndex = headers.indexOf(headerOfDeadlineColumnName);
    var deadline = sheetData[0][deadlineColumnIndex].toString().trim();
    var removeSharingDateTime = new Date(deadline);

    var subFolders = parentFolder.getFolders();
    var rightNow = new Date();

    if (rightNow >= removeSharingDateTime) {
      Logger.log('Removing sharing permissions for subfolders under: ' + parentFolder.getName());

      while (subFolders.hasNext()) {
        var subFolder = subFolders.next();
        Logger.log('Processing folder: ' + subFolder.getName());

        var editors = subFolder.getEditors();
        var viewers = subFolder.getViewers();

        if (subFolder.getSharingAccess() === DriveApp.Access.ANYONE_WITH_LINK) {
          subFolder.setSharing(DriveApp.Access.PRIVATE, DriveApp.Permission.NONE);
          Logger.log('Sharing with anyone with the link removed for folder: ' + subFolder.getName());
        }

        for (var i = 0; i < editors.length; i++) {
          subFolder.removeEditor(editors[i]);
          Logger.log('Editor removed from folder: ' + subFolder.getName() + ', Editor: ' + editors[i].getEmail());
        }

        for (var j = 0; j < viewers.length; j++) {
          subFolder.removeViewer(viewers[j]);
          Logger.log('Viewer removed from folder: ' + subFolder.getName() + ', Viewer: ' + viewers[j].getEmail());
        }
      }
      Logger.log('All sharing permissions removed for subfolders.');
    } else {
      Logger.log('Today is before the specified removeSharingDate. No sharing permissions removed.');
    }
  } catch (e) {
    Logger.log('Error removing folder sharing: ' + e.toString());
    console.error('Error occurred in removeSubFolderSharingByDate function: ' + e.stack);
  }
}
