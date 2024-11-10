function setProjectReturnDatetime() {
  try {
    var result = getFoldersWithLatestFile();
    var controlDatetime = new Date();
    controlDatetime.setMinutes(controlDatetime.getMinutes() - 61);  // 61 dakika cikart

    Object.keys(result).forEach(key => {
      // Logger.log('result[key]: ' + result[key] + '\ncontrolDatetime: ' + controlDatetime);
      if (result[key] >= controlDatetime) {  // Dosyanin yuklenme tarihi, su andan 61 dk oncesinden daha yeniyse islem yap
                                             //(cunku her saat removeDuplicateEvents fonksiyonu calisarak varolanlari ekliyor)
      var conn = cnf.openConn();
        var queryForApplicantId = "SELECT " + idFieldName + " from " + applicantTable + " WHERE " + emailFieldName + " = ?";
        var stmtForApplicantId = conn.prepareStatement(queryForApplicantId);
        stmtForApplicantId.setString(1, key.split('_')[1].toString());

        var resultForApplicantId = null;
        var applicantId = null;
        try {
          resultForApplicantId = stmtForApplicantId.executeQuery();
          if (resultForApplicantId.next()) {
            applicantId = parseInt(resultForApplicantId.getInt(cnf.getIdFieldName()));
          }
        } catch (e) {
          console.error('Error: ' + e.stack);
        } finally {
          stmtForApplicantId.close();  // ResultSet kapatılıyor
          resultForApplicantId.close();    // Statement kapatılıyor
          conn.close();
        }

        if (applicantId) {
          var dt = new Date(result[key]);
          var queryUpdateProjectReturnDatetime = 'UPDATE ' + evaluationTable + ' SET ' + projectReturnDatetimeFieldName + '  = ? WHERE ' + applicantIdFieldName + ' = ?';
          var conn = cnf.openConn();
          var stmtUpdateProjectReturnDatetime = conn.prepareStatement(queryUpdateProjectReturnDatetime);
          stmtUpdateProjectReturnDatetime.setTimestamp(1, Jdbc.newTimestamp(dt));
          stmtUpdateProjectReturnDatetime.setInt(2, applicantId);

          var resultUpdateProjectReturnDatetime = null;
          try {
            resultUpdateProjectReturnDatetime = stmtUpdateProjectReturnDatetime.executeUpdate();
            if (resultUpdateProjectReturnDatetime){
              //Sheet dosyasini da ekle
              // 3-Application_Evaluations_Form_Answers sheet'inin ID'si (buraya yeni sheet ID'sini ekleyin)
              var evaluationSheetId = getSheetId(cnf.getEvaluationSheetFileName());  // sheet dosyasinin adina gore ID'si elde ediliyor.

              // 3-Application_Evaluations_Form_Answers sheet'ine erişmek
              var sheet = SpreadsheetApp.openById(evaluationSheetId);
              var sheetData = sheet.getDataRange().getValues();
              for (var row = 1; row < sheetData.length; row++) {
                if (sheetData[row][3].toString() === key.split('_')[1].toString()) {
                  sheet.getRange('I' + (row + 1)).setValue(dt);
                }
              }
              Logger.log(key.split('_')[1] + ' mail adresiyle kaydolan aday proje odevini yukledi.');
            }
          } catch (e) {
            console.error('Error: ' + e.stack);
          } finally {
            stmtUpdateProjectReturnDatetime.close();  // Statement kapatılıyor
            conn.close();
          }
        } else { Logger.log("We couldn't retrieve applicantId from database!");}
      }
    });
  } catch (e) {
    console.error('Error occurred in setProjectReturnDatetime function: ' + e.stack);
  }
}
