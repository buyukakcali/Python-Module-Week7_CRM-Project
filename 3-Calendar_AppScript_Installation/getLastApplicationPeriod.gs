function getLastApplicationPeriod(cnf_, conn_) {
  // .................. Variables Area ................... //
  var applicationTable = cnf_.getApplicationTable();
  var applicationPeriodFieldName = cnf_.getApplicationPeriodFieldName();
  // ..................................................... //

  try {
    var lastApplicationPeriod_ = null;
    var resultLastApplicationPeriod = null;
    var queryLastApplicationPeriod = 'SELECT ' + applicationPeriodFieldName + ' ' +'FROM ' + applicationTable + ' ' +'ORDER BY CAST(SUBSTRING(' + applicationPeriodFieldName + ', 4) AS UNSIGNED) DESC ' + 'LIMIT 1';
    var stmtLastApplicationPeriod = conn_.createStatement();
        
    try {
      resultLastApplicationPeriod = stmtLastApplicationPeriod.executeQuery(queryLastApplicationPeriod);
      if (resultLastApplicationPeriod.next()) {
        lastApplicationPeriod_ = resultLastApplicationPeriod.getString(applicationPeriodFieldName);
      }
    } finally {
      resultLastApplicationPeriod.close();  // ResultSet kapatılıyor
      stmtLastApplicationPeriod.close();    // Statement kapatılıyor
    }
    // Logger.log('Son basvuru donemi adi: ' + lastApplicationPeriod_);
  } catch (e) {
    console.error('Error occured in getLastApplicationPeriod function: ' + e);
  }
  finally {
    return lastApplicationPeriod_;
  }    
}
