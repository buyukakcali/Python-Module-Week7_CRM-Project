function createAndShareFolder(attendeeMail) {
  try {
    var cnf = new Config();

    var periodFolder = prepareFolders();

    // Son Basvuru Donemi ve AttendeeMail'e göre yeni klasör adı oluşturuyoruz veya var olup olmadığını kontrol ediyoruz
    var lastPeriodName = getLastApplicationPeriod(cnf, cnf.openConn());

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
