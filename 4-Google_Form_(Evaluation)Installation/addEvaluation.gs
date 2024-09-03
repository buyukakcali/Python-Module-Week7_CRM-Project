function addEvaluation(conn_, formTable_, formTableTimestampFieldName_, formData_) {
  try {
    var whitelist = getWhitelist(); // get whitelist
    var usedTablesInThisFunction = [formTable_];
    var columns = Object.keys(formData_);
    // Although this variable is in formData, it is still added again. Due to the danger of manual manipulation of the variable
    columns.push(formTableTimestampFieldName_);

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

    for (var i = 0; i < formData_.length; i++) {
      Logger.log(Object.keys(formData_)[i] +' = ' + Object.values(formData_)[i]);
    }

    var insertStmt = 'INSERT INTO ' + formTable_ + ' (';
    insertStmt += Object.keys(formData_).join(', ') + ') VALUES (' + Object.keys(formData_).map(() => '?').join(', ') + ')';
    var stmtInsert = conn_.prepareStatement(insertStmt, Jdbc.Statement.RETURN_GENERATED_KEYS);

    // Data is assigned to its place in the query text.
    for (var i = 0; i < Object.keys(formData_).length; i++) {
      if (Object.keys(formData_)[i] === formTableTimestampFieldName_) {
        stmtInsert.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(formData_)[i]));
      } else if (typeof(Object.values(formData_)[i]) === 'string'){
        stmtInsert.setString(i + 1, Object.values(formData_)[i]);
      } else if (typeof(Object.values(formData_)[i]) === 'number'){
        stmtInsert.setInt(i + 1, Object.values(formData_)[i]);
      } else {
        Logger.log('Trying to assign an unknown type of data!!!');
      }
    }

    var resultStmtInsert = null;
    try {
      resultStmtInsert = stmtInsert.executeUpdate();
      if (!resultStmtInsert) {
        Logger.log('Returned value is empty in addEvaluation!');
      }
    } catch(e) {
      console.error('Error :' + e.stack);
    } finally {
      stmtInsert.close();
      return resultStmtInsert;
    }
  } catch (e) {
    console.error('Error occured in addEvaluation function: ' + e.stack);
  }
}
