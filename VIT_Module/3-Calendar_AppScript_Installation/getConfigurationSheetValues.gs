function getConfigurationSheetValues() {
  try {
    var cnf = new Config();

    // configuration sheet'inin ID'sini elde et
    var configurationSheetName = cnf.getConfigurationSheetFileName();
    var configSheetId = getSheetId(configurationSheetName);  // Configuration dosyasinin adina gore sheet'in ID'si elde ediliyor.

    // configuration sheet'ine erişmek
    var sheetConfig = SpreadsheetApp.openById(configSheetId);
    var sheetConfigData = sheetConfig.getDataRange().getValues();
    var headers = sheetConfigData.shift(); // Başlık satırını ayırır

    // headerOfParentFolderColumnName değişkeninde yer alan değere gore configuration sheetindeki parent klasunun adini getir
    var headerOfParentFolderColumnName = cnf.getHeaderOfParentFolderColumnName();
    var parentFolderColumnIndex = headers.indexOf(headerOfParentFolderColumnName);
    var parentFolderName = sheetConfigData[0][parentFolderColumnIndex].toString().trim() || null;

    // headerOfDeadlineColumnName değişkeninde yer alan değere gore deadline hesapla
    var headerOfDeadlineColumnName = cnf.getHeaderOfDeadlineColumnName();
    var deadlineColumnIndex = headers.indexOf(headerOfDeadlineColumnName);
    var deadline = sheetConfigData[0][deadlineColumnIndex].toString().trim();
    var deadline = new Date(deadline);

    // headerOfPreparingForFirstInterviewLinkColumnName değişkeninde yer alan değere gore configuration sheetindeki parent klasunun adini getir
    var headerOfPreparingForFirstInterviewLinkColumnName = cnf.getHeaderOfPreparingForFirstInterviewLinkColumnName();
    var googlePreparingForFirstInterviewLinkColumnIndex = headers.indexOf(headerOfPreparingForFirstInterviewLinkColumnName);
    var preparingForFirstInterviewLink = sheetConfigData[0][googlePreparingForFirstInterviewLinkColumnIndex].toString().trim() || null;

    // headerOfGoogleEvaluation1FormLinkColumnName değişkeninde yer alan değere gore configuration sheetindeki parent klasunun adini getir
    var headerOfGoogleEvaluation1FormLinkColumnName = cnf.getHeaderOfGoogleEvaluation1FormLinkColumnName();
    var googleEvaluation1FormLinkColumnIndex = headers.indexOf(headerOfGoogleEvaluation1FormLinkColumnName);
    var googleEvaluation1FormLink = sheetConfigData[0][googleEvaluation1FormLinkColumnIndex].toString().trim() || null;

    // headerOfProjectHomeworkLinkColumnName değişkeninde yer alan değere gore configuration sheetindeki parent klasunun adini getir
    var headerOfProjectHomeworkLinkColumnName = cnf.getHeaderOfProjectHomeworkLinkColumnName();
    var googleProjectHomeworkLinkColumnIndex = headers.indexOf(headerOfProjectHomeworkLinkColumnName);
    var projectHomeworkLink = sheetConfigData[0][googleProjectHomeworkLinkColumnIndex].toString().trim() || null;

    // headerOfGoogleEvaluation2FormLinkColumnName değişkeninde yer alan değere gore configuration sheetindeki parent klasunun adini getir
    var headerOfGoogleEvaluation2FormLinkColumnName = cnf.getHeaderOfGoogleEvaluation2FormLinkColumnName();
    var googleEvaluation2FormLinkColumnIndex = headers.indexOf(headerOfGoogleEvaluation2FormLinkColumnName);
    var googleEvaluation2FormLink = sheetConfigData[0][googleEvaluation2FormLinkColumnIndex].toString().trim() || null;

    // Logger.log('parentFolderName: ' + parentFolderName);
    // Logger.log('deadline: ' + deadline);

    var result = {};
    result['parentFolderName'] = parentFolderName;
    result['deadline'] = deadline;
    result['preparingForFirstInterviewLink'] = preparingForFirstInterviewLink;
    result['googleEvaluation1FormLink'] = googleEvaluation1FormLink;
    result['projectHomeworkLink'] = projectHomeworkLink;
    result['googleEvaluation2FormLink'] = googleEvaluation2FormLink;

    return result;

  } catch (e) {
    console.error('Error occurred in getConfigurationSheetValues function: ' + e.stack);
  }
}
