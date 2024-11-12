function getCandidateInfo(candidateEmail) {
  var conn = null;

  try {
    var cnf = new Config();
    var candidateInfo = [];
    var resultCandidateInfo = null;

    conn = cnf.openConn();
    var stmtCandidateInfo = conn.prepareStatement(cnf.getNormalQuery('queryGetCandidate'));
    stmtCandidateInfo.setString(1, candidateEmail);

    try {
      resultCandidateInfo = stmtCandidateInfo.executeQuery();

      while (resultCandidateInfo.next()) {
        // Sonuçlardan verileri alın
        var name = resultCandidateInfo.getString(cnf.getCandidateNameFieldName());
        var surname = resultCandidateInfo.getString(cnf.getCandidateSurnameFieldName());

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
    console.error('Error occurred in getCandidateInfo function: ' + e.stack);
  } finally {
    if (conn) {
      conn.close();
    }
  }
}
