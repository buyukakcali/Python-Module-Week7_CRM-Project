function getLastApplicationPeriodStartDate(cnf_, conn_, lastApplicationPeriod_ ) {
  // .................. Variables Area ................... //
  var applicationTable = cnf_.getApplicationTable();
  var applicationPeriodFieldName = cnf_.getApplicationPeriodFieldName();  
  var datetimeFieldNames = cnf_.getDatetimeFieldNames();
  // ..................................................... //


  var lastApplicationPeriodStartDate_ = null;

  try {
    var whitelist = getWhitelist(); // Whitelist'i çek

    var usedTablesInThisFunction = [applicationTable];
    var columns = [applicationPeriodFieldName, datetimeFieldNames[0], datetimeFieldNames[1]];

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

    var resultLastApplicationPeriodStartDate = null;
    var queryLastApplicationPeriodStartDate = 'SELECT MIN('+ datetimeFieldNames[0] +') FROM '+applicationTable+' WHERE '+applicationPeriodFieldName+' = ? LIMIT 1';
    var stmtLastApplicationPeriodStartDate = conn_.prepareStatement(queryLastApplicationPeriodStartDate);
    // Veri sorgu metnindeki yerine atanir.
    stmtLastApplicationPeriodStartDate.setString(1, lastApplicationPeriod_);
    // Logger.log('Sorgu metni: ' + queryLastApplicationPeriodStartDate);

    try {
      resultLastApplicationPeriodStartDate = stmtLastApplicationPeriodStartDate.executeQuery();
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
