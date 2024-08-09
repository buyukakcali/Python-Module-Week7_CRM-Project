function getLastApplicationPeriodStartDate(cnf_, conn_, lastApplicationPeriod_ ) {
  // .................. Variables Area ................... //
  var applicationTable = cnf_.getApplicationTable();
  var applicationPeriodFieldName = cnf_.getApplicationPeriodFieldName();  
  var datetimeFieldNames = cnf_.getDatetimeFieldNames();
  // ..................................................... //

  try {
    var resultLastApplicationPeriodStartDate = null;
    var lastApplicationPeriodStartDate_ = null;
    var queryLastApplicationPeriodStartDate = 'SELECT MIN('+datetimeFieldNames[0]+') FROM '+applicationTable+' WHERE '+applicationPeriodFieldName+' = \'' + lastApplicationPeriod_ + '\' LIMIT 1';
    var stmtLastApplicationPeriodStartDate = conn_.createStatement();    
    try {
      resultLastApplicationPeriodStartDate = stmtLastApplicationPeriodStartDate.executeQuery(queryLastApplicationPeriodStartDate);
      if (resultLastApplicationPeriodStartDate.next()) {
        lastApplicationPeriodStartDate_ = new Date(resultLastApplicationPeriodStartDate.getTimestamp(1).getTime());
      }
    } catch (e) {
      console.error('Error: ' + e);
    } finally {
      resultLastApplicationPeriodStartDate.close();  // ResultSet kapatılıyor
      stmtLastApplicationPeriodStartDate.close();    // Statement kapatılıyor
    }
    // Logger.log('Son basvuru donemi icin baslangic tarihi: ' + lastApplicationPeriodStartDate);
  } catch (e) {
    console.error('Error occured in getLastApplicationPeriodStartDate function: ' + e);
  }
  finally {
    return lastApplicationPeriodStartDate_;;
  }    
}
