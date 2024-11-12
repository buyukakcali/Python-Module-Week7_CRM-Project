function addEvaluation(formData) {
  var conn = null; // Database baglantisi icin degiskenimizi tanimliyoruz.

  try {
    var cnf = new Config();
    var formTable = cnf.getFormTableName();
    var timestampFieldName = cnf.getTimestampFieldName();

    var whitelist = getWhitelist(); // get whitelist
    var usedTablesInThisFunction = [formTable];
    var columns = Object.keys(formData);
    // Although this variable is in formData, it is still added again. Due to the danger of manual manipulation of the variable
    columns.push(timestampFieldName);

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
    // Logger.log(JSON.stringify(formData));

    var insertStmt = 'INSERT INTO ' + formTable + ' (';
    insertStmt += Object.keys(formData).join(', ') + ') VALUES (' + Object.keys(formData).map(() => '?').join(', ') + ')';
    conn = cnf.openConn();
    var stmtInsert = conn.prepareStatement(insertStmt, Jdbc.Statement.RETURN_GENERATED_KEYS);

    // Data is assigned to its place in the query text.
    for (var i = 0; i < Object.keys(formData).length; i++) {
      if (Object.keys(formData)[i] === timestampFieldName) {
        stmtInsert.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(formData)[i]));
      } else if (typeof(Object.values(formData)[i]) === 'string'){
        stmtInsert.setString(i + 1, Object.values(formData)[i]);
      } else if (typeof(Object.values(formData)[i]) === 'number'){
        stmtInsert.setInt(i + 1, Object.values(formData)[i]);
      } else {
        Logger.log('Trying to assign an unknown type of data!!!');
      }
    }

    var resultStmtInsert = null;
    try {
      resultStmtInsert = stmtInsert.executeUpdate();
      if (!resultStmtInsert) {
        Logger.log('Returned value is empty in addEvaluation!');
      } else {
        Logger.log('Evaluation added successfully.');
      }
    } catch(e) {
      console.error('Error :' + e.stack);
    } finally {
      stmtInsert.close();
      return resultStmtInsert;
    }
  } catch (e) {
    console.error('Error occurred in addEvaluation function: ' + e.stack);
  } finally {
    if (conn) {
      conn.close();
    }
  }
}
