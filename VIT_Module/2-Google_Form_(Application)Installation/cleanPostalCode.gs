// Posta kodunu temizleyen ve tüm boşluk karakterlerini yok eden fonksiyon
function cleanPostalCode(postalCode) {
  var result = null;
  try {
    // Tüm boşluk karakterlerini kaldır ve büyük harfe çevir
    result = postalCode.replace(/\s+/g, '').toUpperCase();
  } catch (e) {
    console.error('Error occurred in cleanPostalCode function: ' + e.stack);
  } finally {
    return result;
  }
}
