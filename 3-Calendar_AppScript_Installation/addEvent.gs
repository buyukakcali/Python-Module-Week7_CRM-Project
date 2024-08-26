function addEvent(cnf_, conn_, eventData_) {
  // .................. Variables Area ................... //
  var appointmentsTable = cnf_.getAppointmentsTable();
  var eventIdFieldName = cnf_.getEventIdFieldName();
  var datetimeFieldNames = cnf_.getDatetimeFieldNames();
  // ..................................................... //

  try {
    // Logger.log('Eski ve yeni datada değişiklik yok, yeni kayit eklenecek: ' + eventId);
    // Worksheet'e yeni satir ekle (yeni randevu-etkinlik)
    addUniqueEvent(eventData_);
    // sheet_.appendRow(Object.values(eventData_)); // Eski yapi: "sheet_" parametresi fonksiyondan kaldirildi. Kullanmak gerekecek olursa eklensin!

    // Sutun isimleri ve verilerini ayarla
    var { AttendeeName, AttendeeSurname, ...newEventData } = eventData_;

    // Database'e yeni kayit ekle
    var queryInsertEvent = 'INSERT INTO ' + appointmentsTable + ' (';

    queryInsertEvent += Object.keys(newEventData).join(', ') + ') VALUES (' + Object.keys(newEventData).map(() => '?').join(', ') + ')';
    Logger.log('Sorgu metni: ' + queryInsertEvent);

    var stmtInsertEvent = conn_.prepareStatement(queryInsertEvent, Jdbc.Statement.RETURN_GENERATED_KEYS);

    // Veri sorgu metnindeki yerine atanir.
    for (var i = 0; i < Object.values(newEventData).length; i++) {
      if (datetimeFieldNames.includes(Object.keys(newEventData)[i])) {
        stmtInsertEvent.setTimestamp(i + 1, Jdbc.newTimestamp(Object.values(newEventData)[i]));
      } else if (typeof(Object.keys(newEventData)[i]) === 'string'){
        stmtInsertEvent.setString(i + 1, Object.values(newEventData)[i]);
      } else if (typeof(Object.keys(newEventData)[i]) === 'number'){
        stmtInsertEvent.setInt(i + 1, Object.values(newEventData)[i]);
      } else if (typeof(Object.keys(newEventData)[i]) === 'null'){
        stmtInsertEvent.setNull(i + 1, java_sql_Types.INTEGER); // INTEGER yerine, tekrar null yapacaginiz sutunda ne tur veri olmasini planlamissaniz onu yazin!
      } else {
        Logger.log('Bilinmeyen bir tur veri atanmaya calisiliyor!!!');
      }
    }
    var resultStmtInsertEvent = null;

    try {
      resultStmtInsertEvent = stmtInsertEvent.executeUpdate();
      if (resultStmtInsertEvent) {
        // Logger.log('resultStmtInsertEvent: ' + resultStmtInsertEvent);
        Logger.log('Google Sheet dosyasina ve Databse\'deki '+ appointmentsTable +' tablosuna yeni kayit(' + eventIdFieldName + '= ' + newEventData[eventIdFieldName] + ') EKLENDI.');
      }
    } catch (e) {
      console.error('Error: ' + e);
    } finally {
      stmtInsertEvent.close();  // Statement kapatılıyor
    }
  } catch (e) {
    console.error('Error occured in addEvent function: ' + e);
  } finally {
    return resultStmtInsertEvent;
  }
}
