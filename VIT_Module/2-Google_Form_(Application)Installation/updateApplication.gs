function updateApplication(conn_, formTable_, formTableRowId_, formTableTimestampFieldName_, applicationPeriod_, formData_) {
  try {
    var whitelist = getWhitelist(); // Whitelist'i çek
    var usedTablesInThisFunction = [formTable_];
    var columns = Object.keys(formData_);
    // Although these variables are in formData, they are still added again. Due to the danger of manual manipulation of the variable
    columns.push(formTableTimestampFieldName_);
    columns.push(String(Object.keys(formTableRowId_)));

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
    var queryUpdate = 'UPDATE ' + formTable_ + ' SET ';

    queryUpdate += Object.keys(formData_).join(' = ?, ') + '= ? WHERE ' + Object.keys(formTableRowId_) + ' = ? AND ' + Object.keys(applicationPeriod_) +' = ?';
    var stmtUpdate = conn_.prepareStatement(queryUpdate);

    // Veri sorgu metnindeki yerine atanir.
    for (var i = 0; i < Object.keys(formData_).length; i++) {
      if (Object.keys(formData_)[i].includes(formTableTimestampFieldName_)) {
        stmtUpdate.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(formData_)[i]));
      } else if (typeof(Object.values(formData_)[i]) === 'string'){
        stmtUpdate.setString(i + 1, Object.values(formData_)[i]);
      } else if (typeof(Object.values(formData_)[i]) === 'number'){
        stmtUpdate.setInt(i + 1, Object.values(formData_)[i]);
      } else {
        Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
      }
      // Logger.log('Object.keys(formData_)['+i+']: ' + Object.keys(formData_)[i]);
      // Logger.log('Object.values(formData_)['+i+']: ' + Object.values(formData_)[i]);
    }
    // Logger.log('Query string: ' + queryUpdate);

    stmtUpdate.setInt(Object.keys(formData_).length + 1, Object.values(formTableRowId_));  // crm_RowID
    stmtUpdate.setString(Object.keys(formData_).length + 2, Object.values(applicationPeriod_));  // crm_Period

    var resultStmtUpdate = null;
    try {
      resultStmtUpdate = stmtUpdate.executeUpdate();
      // Logger.log('resultStmtUpdate===>: ' + resultStmtUpdate);
      if (resultStmtUpdate === 0){
        Logger.log('Formda hicbir sey degistirilmedigi icin guncelleme yapilmadi. Donen deger: ' + resultStmtUpdate);
        resultStmtUpdate = null;
      } else if (resultStmtUpdate) {
        Logger.log('Basvuru guncelleme islemi basarili!');
      } else {
        Logger.log('updateApplication fonksiyonunda hata! Donen deger: null');
      }
    } catch (e) {
      console.error('Error: ' + e.stack);
    } finally {
      stmtUpdate.close();
      return resultStmtUpdate;
    }
  } catch (e) {
    console.error('Error occurred in updateApplication function: ' + e.stack);
  }
}
