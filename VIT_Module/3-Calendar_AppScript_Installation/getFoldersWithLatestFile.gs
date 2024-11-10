function getFoldersWithLatestFile() {
  try {
    var cnf = new Config();

    var applicantTable = cnf.getApplicantTable();
    var evaluationTable = cnf.getEvaluationTableName();
    var idFieldName = cnf.getIdFieldName();
    var emailFieldName = cnf.getEmailFiledName();
    var projectReturnDatetimeFieldName = cnf.getProjectReturnDatetimeFieldName();
    var applicantIdFieldName = cnf.getApplicantIdFieldName();

    var whitelist = getWhitelist(); // get whitelist
    var usedTablesInThisFunction = [applicantTable, evaluationTable];
    var columns = [idFieldName, emailFieldName, projectReturnDatetimeFieldName, applicantIdFieldName];

    usedTablesInThisFunction.forEach(table => {
      if (whitelist.validTables.includes(table) == false) {
        throw new Error('Invalid table name: '+ table);
      }
    });

    columns.forEach(column => {
      if (!whitelist.validColumns.includes(column)) {
        throw new Error('Invalid column name: ' + column);
      }
    });

    var periodFolderName = prepareFolders();
    var periodFolderId = getFolderIdByName(periodFolderName);

    if (!periodFolderId) {
      Logger.log(periodFolderName + ' isimli klasor Proje klasorunun altinda mevcut degil! Silinmis veya adi degistirilmis olabilir...\n Geri kalan islemlere devam edilmedi!');
      return
    }
    var mainFolder = DriveApp.getFolderById(periodFolderId);

    // Ana klasör altındaki tüm alt klasörleri al
    var subFolders = mainFolder.getFolders();
    var result = {}; // Sonuçları saklayacağımız sözlük

    // Alt klasörleri tarayalım
    while (subFolders.hasNext()) {
      var folder = subFolders.next();
      var periodFolderName = folder.getName();

      // Klasördeki dosyaları al
      var files = folder.getFiles();
      var latestFileTimestamp = 0;

      // Dosyaları tarayalım ve en yeni dosyanın yüklenme zamanını bulalım
      while (files.hasNext()) {
        var file = files.next();
        var lastUploaded = file.getDateCreated().getTime(); // Dosyanın Drive'a yüklenme zamanı

        // Eğer bu dosya en yeni dosya ise zaman damgasını güncelle
        if (lastUploaded > latestFileTimestamp) {
          latestFileTimestamp = lastUploaded;
        }
      }

      // Eğer klasörde en yeni dosya varsa, klasör adını ve zaman damgasını sözlüğe ekle
      if (latestFileTimestamp > 0) {
        result[periodFolderName] = new Date(latestFileTimestamp);
      }
    }
    return result;

  } catch (e) {
    console.error('Error occurred in getFoldersWithLatestFile function: ' + e.stack);
  }
}
