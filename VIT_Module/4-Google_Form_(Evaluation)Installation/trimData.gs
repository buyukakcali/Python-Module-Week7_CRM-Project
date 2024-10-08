function trimData(data) {
  try {
    // Verinin string olup olmadığını kontrol edin
    if (typeof data === 'string') {
      data = data.trim(); // Başındaki ve sonundaki boşlukları temizler
    }
  } catch (e) {
    console.error('Error occurred in trimData function: ' + e.stack);
  } finally {
    return data;
  }
}
