function getLastApplicationPeriod() {
  // .................. Variables Area ................... //
  var cnf = new Config();
  var conn = null;
  var applicationTable = cnf.getApplicationTable();
  var periodFieldName = cnf.getPeriodFieldName();
  // ..................................................... //

  try {
    var whitelist = getWhitelist(); // get whitelist

    var usedTablesInThisFunction = [applicationTable];
    var columns = [periodFieldName];

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


    var queryLastApplicationPeriod = 'SELECT ' + periodFieldName + ' FROM ' + applicationTable + ' ORDER BY CAST(SUBSTRING(' + periodFieldName + ', 4) AS UNSIGNED) DESC LIMIT 1';
    conn = cnf.openConn();
    var stmtLastApplicationPeriod = conn.createStatement();

    var resultLastApplicationPeriod = null;
    var lastApplicationPeriod = null;
    try {
      resultLastApplicationPeriod = stmtLastApplicationPeriod.executeQuery(queryLastApplicationPeriod);
      if (resultLastApplicationPeriod.next()) {
        lastApplicationPeriod = resultLastApplicationPeriod.getString(periodFieldName);
      }
    } finally {
      resultLastApplicationPeriod.close();  // ResultSet kapatılıyor
      stmtLastApplicationPeriod.close();    // Statement kapatılıyor
    }
    // Logger.log('Last application period name: ' + lastApplicationPeriod);
  } catch (e) {
    console.error('Error occurred in getLastApplicationPeriod function: ' + e.stack);
  }
  finally {
    if (conn) {
      conn.close();  // Connection kapatılıyor
    }
    return lastApplicationPeriod;
  }    
}
