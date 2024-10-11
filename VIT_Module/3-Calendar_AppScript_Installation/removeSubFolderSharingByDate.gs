function removeSubFolderSharingByDate() {
  try {
    var cnf = new Config();

    // configuration sheet'inin ID'si (buraya yeni sheet ID'sini ekleyin)
    var configSheetId = getSheetId(cnf.getConfigurationSheetFileName());  // Configuration dosyasinin adina gore sheet'in ID'si elde ediliyor.

    // configuration sheet'ine erişmek
    var sheet = SpreadsheetApp.openById(configSheetId);
    var sheetData = sheet.getDataRange().getValues();
    var headers = sheetData.shift(); // Başlık satırını ayırır

    // Period Folder islemlerini tamamla
    var headerOfPeriodFolderColumnName = cnf.getHeaderOfPeriodFolderColumnName();
    var periodFolderColumnIndex = headers.indexOf(headerOfPeriodFolderColumnName);
    var periodFolderName = sheetData[0][periodFolderColumnIndex].toString().trim() || null;
    if (!periodFolderName) {
      Logger.log("'" + cnf.getConfigurationSheetFileName() + "' sheet dosyasinda olmasi gereken period klasor ismi bulunmamaktadir! (Bos!!!)");
      return
    }
    var periodFolderId = getFolderIdByName(periodFolderName);
    if (!periodFolderId) {
      Logger.log("Google Drive'daki, proje klasorunde; '" + cnf.getConfigurationSheetFileName() + "' sheet dosyasinda yazili klasor adinda bir klasor bulunmamaktadir!");
      return
    }
    var periodFolder = DriveApp.getFolderById(periodFolderId);

    // deadline islemlerini tamamla
    var headerOfDeadlineColumnName = cnf.getHeaderOfDeadlineColumnName();
    var deadlineColumnIndex = headers.indexOf(headerOfDeadlineColumnName);
    var deadline = sheetData[0][deadlineColumnIndex].toString().trim();
    var removeSharingDateTime = new Date(deadline);

    var rightNow = new Date();
    if (rightNow >= removeSharingDateTime) {
      Logger.log('Removing sharing permissions for subfolders under: ' + periodFolder.getName());

      var subFolders = periodFolder.getFolders();
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
