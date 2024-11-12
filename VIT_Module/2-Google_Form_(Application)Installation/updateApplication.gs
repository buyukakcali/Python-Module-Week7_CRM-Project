function updateApplication(rowId, applicationPeriod, formData) {
  var conn = null; // Database baglantisi icin degiskenimizi tanimliyoruz.

  try {
    var cnf = new Config();
    var formTable = cnf.getFormTable();
    var timestampFieldName = cnf.getTimestampFieldName();

    var whitelist = getWhitelist(); // Whitelist'i çek
    var usedTablesInThisFunction = [formTable];
    var columns = Object.keys(formData);
    // Although these variables are in formData, they are still added again. Due to the danger of manual manipulation of the variable
    columns.push(String(Object.keys(rowId)));
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

    // Actions ==>
    var queryUpdate = 'UPDATE ' + formTable + ' SET ';

    queryUpdate += Object.keys(formData).join(' = ?, ') + '= ? WHERE ' + Object.keys(rowId) + ' = ? AND ' + Object.keys(applicationPeriod) +' = ?';
    conn = cnf.openConn();
    var stmtUpdate = conn.prepareStatement(queryUpdate);

    // Veri sorgu metnindeki yerine atanir.
    for (var i = 0; i < Object.keys(formData).length; i++) {
      if (Object.keys(formData)[i].includes(timestampFieldName)) {
        stmtUpdate.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(formData)[i]));
      } else if (typeof(Object.values(formData)[i]) === 'string'){
        stmtUpdate.setString(i + 1, Object.values(formData)[i]);
      } else if (typeof(Object.values(formData)[i]) === 'number'){
        stmtUpdate.setInt(i + 1, Object.values(formData)[i]);
      } else {
        Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
      }
      // Logger.log('Object.keys(formData_)['+i+']: ' + Object.keys(formData_)[i]);
      // Logger.log('Object.values(formData_)['+i+']: ' + Object.values(formData_)[i]);
    }
    // Logger.log('Query string: ' + queryUpdate);

    stmtUpdate.setInt(Object.keys(formData).length + 1, Object.values(rowId));  // crm_RowID
    stmtUpdate.setString(Object.keys(formData).length + 2, Object.values(applicationPeriod));  // crm_Period

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
      console.error('Error while application updating: ' + e.stack);
    } finally {
      stmtUpdate.close();
      return resultStmtUpdate;
    }
  } catch (e) {
    console.error('Error occurred in updateApplication function: ' + e.stack);
  } finally {
    if (conn) {
      conn.close();
    }
  }
}
