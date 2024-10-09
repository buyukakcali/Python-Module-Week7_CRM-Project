function createAndShareFolder(attendeeMail, periodFolderName) {
  try {
    var cnf = new Config();

    // Burada google drivedaki proje odevlerinin tutuldugu ana klasorunun varligi kontrol ediliyor, yoksa olusturuluyor.
    var file = SpreadsheetApp.getActiveSpreadsheet().getId(); // Aktif Google Sheet dosyasının ID'sini alıyoruz
    var parentFolder = DriveApp.getFileById(file).getParents().next();  // Aktif Google Sheet dosyasının da icinde bulundugu klasor

    var folders = parentFolder.getFoldersByName(cnf.getProjectHomeworksParentFolderName());
    var projectHomeworksParentFolder;

    if (folders.hasNext()) {
      // Eğer klasör varsa mevcut olanı al
      projectHomeworksParentFolder = folders.next();
    } else {
      // Eğer klasör yoksa, oluştur
      projectHomeworksParentFolder = parentFolder.createFolder(cnf.getProjectHomeworksParentFolderName());
    }
    // Burada da period klasorunun varligi kontrol ediliyor, yoksa olusturuluyor.
    var folders = projectHomeworksParentFolder.getFoldersByName(periodFolderName);
    var periodFolder;

    if (folders.hasNext()) {
      // Eğer klasör varsa mevcut olanı al
      periodFolder = folders.next();
    } else {
      // Eğer klasör yoksa, oluştur
      periodFolder = projectHomeworksParentFolder.createFolder(periodFolderName);
    }

    // Son Basvuru Donemi ve AttendeeMail'e göre yeni klasör adı oluşturuyoruz veya var olup olmadığını kontrol ediyoruz
    var dbsconn = cnf.openConn();  // Database connection
    var lastPeriodName = getLastApplicationPeriod(cnf, dbsconn);
    if (dbsconn) {
      cnf.closeConn(dbsconn);
    }

    var candidateFolderName = lastPeriodName + '_' + attendeeMail; // Klasor adini; son basvuru donemi, alt cizgi ve attendeeMail bilgisini birlestirerek belirliyoruz.
    var subFolders = periodFolder.getFoldersByName(candidateFolderName);
    var candidateFolder;

    if (subFolders.hasNext()) {
      // Eğer klasör varsa mevcut olanı al
      candidateFolder = subFolders.next();
      Logger.log('Folder already exists for ' + candidateFolderName);
    } else {
      // Eğer klasör yoksa, oluştur
      candidateFolder = periodFolder.createFolder(candidateFolderName);
      Logger.log('New folder created for ' + candidateFolderName);
    }

    // attendeeMail'in Google hesabı olup olmadığını kontrol et
    if (attendeeMail.indexOf('@gmail.com') !== -1 || attendeeMail.indexOf('@googlemail.com') !== -1) {
      // Google hesabıysa attendeeMail'e düzenleme yetkisi ver
      candidateFolder.addEditor(attendeeMail);
      Logger.log('Folder shared with personal upload link.');
      return candidateFolder.getUrl(); // Google hesabı olan kullanıcılar için kisiel paylaşım linki döndür
    } else {
      // Google hesabı olmayan kullanıcılar için paylaşım türünü "Bağlantıya sahip olan herkes düzenleyebilir" yap
      candidateFolder.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.EDIT);
      Logger.log('Folder shared with public upload link.');
      return candidateFolder.getUrl(); // Klasör linkini döndür
    }
  } catch (e) {
    Logger.log('Error creating and sharing folder in createAndShareFolder function: ' + e.stack);
    return null;
  }
}
