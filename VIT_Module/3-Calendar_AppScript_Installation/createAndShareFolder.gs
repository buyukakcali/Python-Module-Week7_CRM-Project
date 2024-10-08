function createAndShareFolder(attendeeMail, targetFolderName) {
  try {
    // Aktif Google Sheet dosyasının ID'sini alıyoruz
    var file = SpreadsheetApp.getActiveSpreadsheet().getId();
    var parentFolder = DriveApp.getFileById(file).getParents().next();

    // Parametre olarak gelen "targetFolderName" adinda bir klasör olup olmadığını kontrol ediyoruz
    var folders = parentFolder.getFoldersByName(targetFolderName);
    var targetFolder;

    if (folders.hasNext()) {
      // Eğer klasör varsa mevcut olanı alıyoruz
      targetFolder = folders.next();
    } else {
      // Eğer klasör yoksa yeni klasörü oluşturuyoruz
      targetFolder = parentFolder.createFolder(targetFolderName);
    }

    // Son Basvuru Donemi ve AttendeeMail'e göre yeni klasör adı oluşturuyoruz veya var olup olmadığını kontrol ediyoruz
    var cnf = new Config();
    var dbsconn = cnf.openConn();  // Database connection
    var lastPeriodName = getLastApplicationPeriod(cnf, dbsconn);
    if (dbsconn) {
      cnf.closeConn(dbsconn);
    }

    var folderName = lastPeriodName + '_' + attendeeMail; // Klasor adini; son basvuru donemi, alt cizgi ve attendeeMail bilgisini birlestirerek belirliyoruz.
    var subFolders = targetFolder.getFoldersByName(folderName);
    var newFolder;

    if (subFolders.hasNext()) {
      // Eğer klasör varsa, mevcut olanı alıyoruz
      newFolder = subFolders.next();
      Logger.log('Folder already exists for ' + folderName);
    } else {
      // Eğer klasör yoksa, yeni klasör oluşturuyoruz
      newFolder = targetFolder.createFolder(folderName);
      Logger.log('New folder created for ' + folderName);
    }

    // Google hesabı olup olmadığını kontrol ediyoruz
    if (attendeeMail.indexOf('@gmail.com') !== -1 || attendeeMail.indexOf('@googlemail.com') !== -1) {
      // Google hesabıysa attendeeMail'e düzenleme yetkisi veriyoruz
      newFolder.addEditor(attendeeMail);
      return newFolder.getUrl(); // Google hesabı olan kullanıcılar için paylaşım linki döndürüyoruz
    } else {
      // Google hesabı olmayan kullanıcılar için paylaşım türünü "Bağlantıya sahip olan herkes düzenleyebilir" yapıyoruz
      newFolder.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
      Logger.log('Folder shared with public upload link.');
      return newFolder.getUrl(); // Klasör linki döndürüyoruz
    }
  } catch (e) {
    Logger.log('Error creating and sharing folder in createAndShareFolder function: ' + e.stack);
    return null;
  }
}
