function getLastApplicationPeriodStartDate(lastApplicationPeriod) {
  // .................. Variables Area ................... //
  var cnf = new Config();
  var conn = null;
  var applicationTable = cnf.getApplicationTable();
  var periodFieldName = cnf.getPeriodFieldName();
  var datetimeFieldNames = cnf.getDatetimeFieldNames();
  // ..................................................... //

  try {
    var whitelist = getWhitelist(); // get whitelist

    var usedTablesInThisFunction = [applicationTable];
    var columns = [periodFieldName, datetimeFieldNames[0], datetimeFieldNames[1]];

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


    var queryLastApplicationPeriodStartDate = 'SELECT MIN('+ datetimeFieldNames[0] +') FROM '+applicationTable+' WHERE '+periodFieldName+' = ? LIMIT 1';
    conn = cnf.openConn();
    var stmtLastApplicationPeriodStartDate = conn.prepareStatement(queryLastApplicationPeriodStartDate);
    // Veri sorgu metnindeki yerine atanir.
    stmtLastApplicationPeriodStartDate.setString(1, lastApplicationPeriod);
    // Logger.log('Sorgu metni: ' + queryLastApplicationPeriodStartDate);

    var resultLastApplicationPeriodStartDate = null;
    var lastApplicationPeriodStartDate = null;
    try {
      resultLastApplicationPeriodStartDate = stmtLastApplicationPeriodStartDate.executeQuery();
      if (resultLastApplicationPeriodStartDate.next()) {
        lastApplicationPeriodStartDate = new Date(resultLastApplicationPeriodStartDate.getTimestamp(1).getTime());
      }
    } catch (e) {
      console.error('Error: ' + e.stack);
    } finally {
      resultLastApplicationPeriodStartDate.close();  // ResultSet kapatılıyor
      stmtLastApplicationPeriodStartDate.close();    // Statement kapatılıyor
    }
    // Logger.log('Son basvuru donemi icin baslangic tarihi: ' + lastApplicationPeriodStartDate);
  } catch (e) {
    console.error('Error occurred in getLastApplicationPeriodStartDate function: ' + e.stack);
  }
  finally {
    if (conn) {
      conn.close();  // Connection kapatılıyor
    }
    return lastApplicationPeriodStartDate;;
  }    
}
