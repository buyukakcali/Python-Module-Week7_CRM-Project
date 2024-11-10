function prepareFolders() {
  var cnf = new Config();

  var parentFolderName = getConfigurationSheetValues()['parentFolderName'].toString().trim() || null;

  // Burada google drivedaki proje odevlerinin tutuldugu ana klasorunun varligi kontrol ediliyor, yoksa olusturuluyor.
  var file = SpreadsheetApp.getActiveSpreadsheet().getId(); // Aktif Google Sheet dosyasının ID'sini alıyoruz
  var parentFolder = DriveApp.getFileById(file).getParents().next();  // Aktif Google Sheet dosyasının da icinde bulundugu klasor

  var folders = parentFolder.getFoldersByName(parentFolderName);
  var projectHomeworksParentFolder;

  if (folders.hasNext()) {
    // Eğer klasör varsa mevcut olanı al
    projectHomeworksParentFolder = folders.next();
  } else {
    // Eğer klasör yoksa, oluştur
    projectHomeworksParentFolder = parentFolder.createFolder(parentFolderName);
  }
  // Burada da period klasorunun varligi kontrol ediliyor, yoksa olusturuluyor.
  var periodFolderName = getLastApplicationPeriod(cnf, cnf.openConn());
  var folders = projectHomeworksParentFolder.getFoldersByName(periodFolderName);
  var periodFolder;

  if (folders.hasNext()) {
    // Eğer klasör varsa mevcut olanı al
    periodFolder = folders.next();
  } else {
    // Eğer klasör yoksa, oluştur
    periodFolder = projectHomeworksParentFolder.createFolder(periodFolderName);
  }
  return periodFolder;
}
