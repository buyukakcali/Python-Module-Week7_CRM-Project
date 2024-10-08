function readRowData(rowNumber) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet(); // Aktif çalışma sayfasını alın
    var range = sheet.getRange(rowNumber, 1, 1, sheet.getLastColumn()); // Belirtilen satır numarasındaki tüm hücreleri alın
    var rowData = range.getValues()[0]; // Hücrelerin değerlerini alın

    // Verileri bir diziye atayın
    var dataArray = [];
    for (var i = 0; i < rowData.length; i++) {
      dataArray.push(rowData[i]);
    }
    return dataArray;
  } catch (e) {
    console.error('Error occurred in readRowData function: ' + e.stack);
  }
}
