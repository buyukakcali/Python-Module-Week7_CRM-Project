function addEvent(eventData) {
  var cnf = new Config();

  // .................. Variables Area ................... //
  var appointmentsTable = cnf.getAppointmentsTable();
  var eventIdFieldName = cnf.getEventIdFieldName();
  var datetimeFieldNames = cnf.getDatetimeFieldNames();
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

    // Sheet'e yeni satir ekle (yeni randevu-etkinlik)
    addUniqueEvent(eventData);

    // Database'e yeni kayit ekle
    var queryInsertEvent = 'INSERT INTO ' + appointmentsTable + ' (';
    queryInsertEvent += Object.keys(eventData).join(', ') + ') VALUES (' + Object.keys(eventData).map(() => '?').join(', ') + ')';
    var conn = cnf.openConn();
    var stmtInsertEvent = conn.prepareStatement(queryInsertEvent, Jdbc.Statement.RETURN_GENERATED_KEYS);
    // Logger.log('Query string: ' + queryInsertEvent);

    // Veri sorgu metnindeki yerine atanir.
    for (var i = 0; i < Object.values(eventData).length; i++) {
      if (datetimeFieldNames.includes(Object.keys(eventData)[i])) {
        stmtInsertEvent.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(eventData)[i]));
      } else if (typeof(Object.values(eventData)[i]) === 'string'){
        stmtInsertEvent.setString(i + 1, Object.values(eventData)[i]);
      } else if (typeof(Object.values(eventData)[i]) === 'number'){
        stmtInsertEvent.setInt(i + 1, Object.values(eventData)[i]);
      } else if (typeof(Object.values(eventData)[i]) === 'null'){
        stmtInsertEvent.setNull(i + 1, Jdbc.Types.INTEGER); // INTEGER yerine, tekrar null yapacaginiz sutunda ne tur veri olmasini planlamissaniz onu yazin!
      } else {
        Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
      }
    }

    var resultStmtInsertEvent = null;
    try {
      resultStmtInsertEvent = stmtInsertEvent.executeUpdate();
      if (resultStmtInsertEvent) {
        // Logger.log('resultStmtInsertEvent: ' + resultStmtInsertEvent);
        Logger.log('Google Sheet dosyasina ve Databse\'deki '+ appointmentsTable +' tablosuna yeni kayit(' + eventIdFieldName + '= ' + eventData[eventIdFieldName] + ') EKLENDI.');
      }
    } catch (e) {
      console.error('Error: ' + e.stack);
    } finally {
      stmtInsertEvent.close();  // Statement kapatılıyor
      return resultStmtInsertEvent;
    }
  } catch (e) {
    console.error('Error occurred in addEvent function: ' + e.stack);
  } finally {
    if (conn) {
      conn.close();  // Connection kapatılıyor
    }
  }
}
