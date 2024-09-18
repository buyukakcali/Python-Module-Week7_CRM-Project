function addApplication(conn_, formTable_, formTableTimestampFieldName_, formData_) {
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

    // Actions ==>
    var queryAdd = 'INSERT INTO ' + formTable_ + ' (';
    queryAdd += Object.keys(formData_).join(', ') + ') VALUES (' + Object.keys(formData_).map(() => '?').join(', ') + ')';
    var stmtInsert = conn_.prepareStatement(queryAdd, Jdbc.Statement.RETURN_GENERATED_KEYS);

    // Veri sorgu metnindeki yerine atanir.
    for (var i = 0; i < Object.keys(formData_).length; i++) {
      if (Object.keys(formData_)[i].startsWith(formTableTimestampFieldName_)) {
        stmtInsert.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(formData_)[i]));
      } else if (typeof(Object.values(formData_)[i]) === 'string'){
        stmtInsert.setString(i + 1, Object.values(formData_)[i]);
      } else if (typeof(Object.values(formData_)[i]) === 'number'){
        stmtInsert.setInt(i + 1, Object.values(formData_)[i]);
      } else {
        Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
      }
    }
    // Logger.log('Query string: ' + queryAdd);

    var resultStmtInsert = null;
    try {
      resultStmtInsert = stmtInsert.executeUpdate();
      Logger.log('resultStmtInsert: ' + resultStmtInsert);
      if (resultStmtInsert) {
        Logger.log('Basvuru ekleme islemi basarili!');
      } else {
        Logger.log('addApplication fonksiyonunda hata! Donen deger: null');
      }
    } catch (e) {
      console.error('Error: ' + e.stack);
    } finally {
      stmtInsert.close();
      return resultStmtInsert;
    }
  } catch (e) {
    console.error('Error in addApplication function: ' + e.stack);
  }
}
