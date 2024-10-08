function getApplicantInfo(conn_, applicantEmail_) {
  try {
    var cnf = new Config();
    var applicantInfo = [];
    var resultApplicantInfo = null;

    var stmtApplicantInfo = conn_.prepareStatement(cnf.getQuery('queryGetApplicant'));
    stmtApplicantInfo.setString(1, applicantEmail_);

    try {
      resultApplicantInfo = stmtApplicantInfo.executeQuery();

      while (resultApplicantInfo.next()) {
        // Sonuçlardan verileri alın
        var name = resultApplicantInfo.getString('crm_Name');
        var surname = resultApplicantInfo.getString('crm_Surname');

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
  }
}
