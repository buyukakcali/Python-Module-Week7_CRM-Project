function getApplicantInfo(applicantEmail) {
  var conn = null;

  try {
    var cnf = new Config();
    var applicantInfo = [];
    var resultApplicantInfo = null;

    conn = cnf.openConn();
    var stmtApplicantInfo = conn.prepareStatement(cnf.getQuery('queryGetApplicant'));
    stmtApplicantInfo.setString(1, applicantEmail);

    try {
      resultApplicantInfo = stmtApplicantInfo.executeQuery();

      while (resultApplicantInfo.next()) {
        // Sonuçlardan verileri alın
        var name = resultApplicantInfo.getString(cnf.getApplicantNameFieldName());
        var surname = resultApplicantInfo.getString(cnf.getApplicantSurnameFieldName());

        // Verileri bir diziye ekleyin
        applicantInfo = [name, surname];
        // Logger.log('applicantInfo: ' + name +' '+ surname);
      }

    } catch (e) {
      console.error('Error about result: ' + e.stack);
    } finally {
      resultApplicantInfo.close();  // ResultSet kapatılıyor
      stmtApplicantInfo.close();    // Statement kapatılıyor
      return applicantInfo;
    }
  } catch (e) {
    console.error('Error occurred in getApplicantInfo function: ' + e.stack);
  } finally {
    if (conn) {
      conn.close();
    }
  }
}
