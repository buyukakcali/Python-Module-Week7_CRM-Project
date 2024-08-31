function updateEvent(cnf_, conn_, rowIndex_, sheetData_, eventData_) {
  // .................. Variables Area ................... //
  var appointmentsTable = cnf_.getAppointmentsTable();
  var eventIdFieldName = cnf_.getEventIdFieldName();
  var datetimeFieldNames = cnf_.getDatetimeFieldNames();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  // ..................................................... //

  try {
    var whitelist = getWhitelist(); // get whitelist

    var usedTablesInThisFunction = [appointmentsTable];
    var columns = Object.keys(eventData_);
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
    var existingRow = sheetData_[rowIndex_];
    // Logger.log('Existing data: ' + existingRow);
    // Logger.log('New_____ data: ' + eventData_);
    // Logger.log('hasChanges(existingRow, eventData_, datetimeFieldNames): ' + hasChanges(existingRow, eventData_, datetimeFieldNames));

    // Bu fonksiyonla, ilgili etkinlikte herhangi bir degisiklik olup olmadigi kontrol ediliyor. Eger degisim varsa guncelleniyor, yoksa siradakine geciliyor. Boylece islemci gucu tasarruf ediliyor ve zaman kazaniliyor. Gereksiz yeniden yazma islemi yapilmiyor.
    if (hasChanges(existingRow, eventData_, datetimeFieldNames)) {
      // Sheet'deki satiri guncelle
      sheet.getRange(rowIndex_ + 2, 1, 1, Object.values(eventData_).length).setValues([Object.values(eventData_)]);

      // Database'deki veriyi guncelle:
      var queryUpdateEvent = 'UPDATE ' + appointmentsTable + ' SET ';
      queryUpdateEvent += Object.keys(eventData_).join(' = ?, ') + '= ? WHERE ' + eventIdFieldName + ' = ?';
      var stmtUpdateEvent = conn_.prepareStatement(queryUpdateEvent);
      // Logger.log('Query string: ' + queryUpdateEvent);

      // Veri sorgu metnindeki yerine atanir.
      for (var i = 0; i < Object.keys(eventData_).length; i++) {
        if (datetimeFieldNames.includes(Object.keys(eventData_)[i].split(' ')[0])) {
          stmtUpdateEvent.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(eventData_)[i]));
        } else if (typeof(Object.values(eventData_)[i]) === 'string'){
          stmtUpdateEvent.setString(i + 1, Object.values(eventData_)[i]);
        } else if (typeof(Object.values(eventData_)[i]) === 'number'){
          stmtUpdateEvent.setInt(i + 1, Object.values(eventData_)[i]);
        } else if (typeof(Object.values(eventData_)[i]) === 'null'){
          stmtUpdateEvent.setNull(i + 1, Jdbc.Types.INTEGER); // INTEGER yerine, tekrar null yapacaginiz sutunda ne tur veri olmasini planlamissaniz onu yazin!
        } else {
          Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
        }
        // Logger.log('Object.keys(eventData_)['+i+']: ' + Object.values(eventData_)[i]);
      }
      stmtUpdateEvent.setString(Object.values(eventData_).length + 1, eventData_[eventIdFieldName]);  // eventIdFieldName's value is added

      var resultStmtUpdateEvent = null;
      try {
        resultStmtUpdateEvent = stmtUpdateEvent.executeUpdate();
        if (resultStmtUpdateEvent){
          // Logger.log('resultStmtUpdateEvent===>: ' + resultStmtUpdateEvent);
          Logger.log('Google Sheet dosyasindaki ve Databse\'deki '+ appointmentsTable +' tablosundaki kayit(' + eventIdFieldName + '= ' + eventData_[eventIdFieldName] + ') GUNCELLENDI.');
        }
      } catch (e) {
        console.error('Error: ' + e.stack);
      } finally {
        stmtUpdateEvent.close();      // Statement kapatılıyor
        return resultStmtUpdateEvent;
      }
    }
  } catch (e) {
    console.error('Error occured in updateEvent function: ' + e.stack);
  }
}
