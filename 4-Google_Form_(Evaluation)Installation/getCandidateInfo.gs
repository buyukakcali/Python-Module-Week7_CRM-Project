function getCandidateInfo(conn_, queryGetCandidate_, candidateEmail_) {
  try {
    var candidateInfo = [];
    var resultCandidateInfo = null;

    var stmtCandidateInfo = conn_.prepareStatement(queryGetCandidate_);
    stmtCandidateInfo.setString(1, candidateEmail_);

    try {
      resultCandidateInfo = stmtCandidateInfo.executeQuery();

      while (resultCandidateInfo.next()) {
        // Sonuçlardan verileri alın
        var name = resultCandidateInfo.getString('crm_Name');
        var surname = resultCandidateInfo.getString('crm_Surname');

        // Verileri bir diziye ekleyin
        candidateInfo = [name, surname];
        // Logger.log('candidateInfo: ' + name +' '+ surname);
      }

    } catch (e) {
      console.error('Error about result: ' + e.stack);
    } finally {
      resultCandidateInfo.close();  // ResultSet kapatılıyor
      stmtCandidateInfo.close();    // Statement kapatılıyor
      return candidateInfo;
    }
  } catch (e) {
    console.error('Error occured in getCandidateInfo function: ' + e.stack);
  }
}
