// Değerleri karşılaştırma fonksiyonu - (event guncellenmis mi diye kontrol etmek icin)
function hasChanges(oldRow, eventData, datetimeFieldNames) {
  try {
    for (var i = 0; i < Object.values(eventData).length; i++) {
      var oldValue = oldRow[i];
      var newValue = Object.values(eventData)[i];

      // Tarih/saat alanları için özel karşılaştırma
      if (datetimeFieldNames.includes(Object.keys(eventData)[i])) {
        oldValue = new Date(oldValue).getTime();
        newValue = new Date(newValue).getTime();
      }

      // Diğer alanlar için tip dönüşümü
      else {
        oldValue = String(oldValue);
        newValue = String(newValue);
      }

      if (oldValue !== newValue) {
        Logger.log('Changed data found, will return to main function!\nChanged Data: ' + Object.keys(eventData)[i] + ' is changed: ' + oldValue + ' => ' + newValue);
        return true;
      }
    }
    return false;
  } catch (e) {
    console.error('Error occurred in hasChanges function: ' + e.stack);
  }
}
