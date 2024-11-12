function updateEvent(rowIndex, sheetData, eventData) {
  var cnf = new Config();

  // .................. Variables Area ................... //
  var appointmentsTable = cnf.getAppointmentsTable();
  var eventIdFieldName = cnf.getEventIdFieldName();
  var datetimeFieldNames = cnf.getDatetimeFieldNames();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  // ..................................................... //

  try {
    var whitelist = getWhitelist(); // get whitelist

    var usedTablesInThisFunction = [appointmentsTable];
    var columns = Object.keys(eventData);
    columns.push(eventIdFieldName);

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

    // Etkinlik zaten var, verilerde bir degisim var mi kontrol et, varsa güncelle!
    var existingRow = sheetData[rowIndex];
    // Logger.log('Existing data: ' + existingRow);
    // Logger.log('New_____ data: ' + eventData_);
    // Logger.log('hasChanges(existingRow, eventData_, datetimeFieldNames): ' + hasChanges(existingRow, eventData_, datetimeFieldNames));

    // Bu fonksiyonla, ilgili etkinlikte herhangi bir degisiklik olup olmadigi kontrol ediliyor. Eger degisim varsa guncelleniyor, yoksa siradakine geciliyor. Boylece islemci gucu tasarruf ediliyor ve zaman kazaniliyor. Gereksiz yeniden yazma islemi yapilmiyor.
    if (hasChanges(existingRow, eventData, datetimeFieldNames)) {
      // Sheet'deki satiri guncelle
      sheet.getRange(rowIndex + 2, 1, 1, Object.values(eventData).length).setValues([Object.values(eventData)]);

      // Database'deki veriyi guncelle:
      var queryUpdateEvent = 'UPDATE ' + appointmentsTable + ' SET ';
      queryUpdateEvent += Object.keys(eventData).join(' = ?, ') + '= ? WHERE ' + eventIdFieldName + ' = ?';
      var conn = cnf.openConn();
      var stmtUpdateEvent = conn.prepareStatement(queryUpdateEvent);
      // Logger.log('Query string: ' + queryUpdateEvent);

      // Veri sorgu metnindeki yerine atanir.
      for (var i = 0; i < Object.keys(eventData).length; i++) {
        if (datetimeFieldNames.includes(Object.keys(eventData)[i].split(' ')[0])) {
          stmtUpdateEvent.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(eventData)[i]));
        } else if (typeof(Object.values(eventData)[i]) === 'string'){
          stmtUpdateEvent.setString(i + 1, Object.values(eventData)[i]);
        } else if (typeof(Object.values(eventData)[i]) === 'number'){
          stmtUpdateEvent.setInt(i + 1, Object.values(eventData)[i]);
        } else if (typeof(Object.values(eventData)[i]) === 'null'){
          stmtUpdateEvent.setNull(i + 1, Jdbc.Types.INTEGER); // INTEGER yerine, tekrar null yapacaginiz sutunda ne tur veri olmasini planlamissaniz onu yazin!
        } else {
          Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
        }
        // Logger.log('Object.keys(eventData_)['+i+']: ' + Object.values(eventData_)[i]);
      }
      stmtUpdateEvent.setString(Object.values(eventData).length + 1, eventData[eventIdFieldName]);  // eventIdFieldName's value is added

      var resultStmtUpdateEvent = null;
      try {
        resultStmtUpdateEvent = stmtUpdateEvent.executeUpdate();
        if (resultStmtUpdateEvent){
          // Logger.log('resultStmtUpdateEvent===>: ' + resultStmtUpdateEvent);
          Logger.log('Google Sheet dosyasindaki ve Databse\'deki '+ appointmentsTable +' tablosundaki kayit(' + eventIdFieldName + '= ' + eventData[eventIdFieldName] + ') GUNCELLENDI.');
        }
      } catch (e) {
        console.error('Error: ' + e.stack);
      } finally {
        stmtUpdateEvent.close();      // Statement kapatılıyor
        return resultStmtUpdateEvent;
      }
    }
  } catch (e) {
    console.error('Error occurred in updateEvent function: ' + e.stack);
  } finally {
    if (conn) {
      conn.close();  // Connection kapatılıyor
    }
  }
}
