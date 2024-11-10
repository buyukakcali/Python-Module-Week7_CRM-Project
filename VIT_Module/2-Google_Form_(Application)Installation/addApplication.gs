function addApplication(formData) {
  var conn = null; // Database baglantisi icin degiskenimizi tanimliyoruz.

  try {
    var cnf = new Config();
    var formTable = cnf.getFormTable();
    var timestampFieldName = cnf.getTimestampFieldName();

    var whitelist = getWhitelist(); // get whitelist
    var usedTablesInThisFunction = [formTable];
    var columns = Object.keys(formData);

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
    var queryAdd = 'INSERT INTO ' + formTable + ' (';
    queryAdd += Object.keys(formData).join(', ') + ') VALUES (' + Object.keys(formData).map(() => '?').join(', ') + ')';
    conn = cnf.openConn();
    var stmtInsert = conn.prepareStatement(queryAdd, Jdbc.Statement.RETURN_GENERATED_KEYS);

    // Veri sorgu metnindeki yerine atanir.
    for (var i = 0; i < Object.keys(formData).length; i++) {
      if (Object.keys(formData)[i].startsWith(timestampFieldName)) {
        stmtInsert.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(formData)[i]));
      } else if (typeof(Object.values(formData)[i]) === 'string'){
        stmtInsert.setString(i + 1, Object.values(formData)[i]);
      } else if (typeof(Object.values(formData)[i]) === 'number'){
        stmtInsert.setInt(i + 1, Object.values(formData)[i]);
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
      console.error('Error while application adding: ' + e.stack);
    } finally {
      stmtInsert.close();
      return resultStmtInsert;
    }
  } catch (e) {
    console.error('Error occurred in addApplication function: ' + e.stack);
  } finally {
    if (conn) {
      try {
        conn.close();
      } catch (e) {
        console.error('Connection closing error: ' + e.stack);
      }
    }
  }
}
