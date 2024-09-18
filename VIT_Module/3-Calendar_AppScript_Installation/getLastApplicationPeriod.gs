function getLastApplicationPeriod(cnf_, conn_) {
  // .................. Variables Area ................... //
  var applicationTable = cnf_.getApplicationTable();
  var applicationPeriodFieldName = cnf_.getApplicationPeriodFieldName();
  // ..................................................... //


  try {
    var whitelist = getWhitelist(); // get whitelist

    var usedTablesInThisFunction = [applicationTable];
    var columns = [applicationPeriodFieldName];

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


    var queryLastApplicationPeriod = 'SELECT ' + applicationPeriodFieldName + ' FROM ' + applicationTable + ' ORDER BY CAST(SUBSTRING(' + applicationPeriodFieldName + ', 4) AS UNSIGNED) DESC LIMIT 1';
    var stmtLastApplicationPeriod = conn_.createStatement();

    var resultLastApplicationPeriod = null;
    var lastApplicationPeriod_ = null;
    try {
      resultLastApplicationPeriod = stmtLastApplicationPeriod.executeQuery(queryLastApplicationPeriod);
      if (resultLastApplicationPeriod.next()) {
        lastApplicationPeriod_ = resultLastApplicationPeriod.getString(applicationPeriodFieldName);
      }
    } finally {
      resultLastApplicationPeriod.close();  // ResultSet kapatılıyor
      stmtLastApplicationPeriod.close();    // Statement kapatılıyor
    }
    // Logger.log('Last application period name: ' + lastApplicationPeriod_);
  } catch (e) {
    console.error('Error occured in getLastApplicationPeriod function: ' + e.stack);
  }
  finally {
    return lastApplicationPeriod_;
  }    
}
