function insertMentorInfo(eventData_, newGivenName, newFamilyName) {
  var cnf = new Config(); // Config sınıfının bir örneğini oluşturun

  var updatedEventData = {};

  // 'MentorAdi' ve 'MentorSoyadi' eklenmeden önceki anahtar-değer çiftlerini ekle
  for (var key in eventData_) {
    if (key === cnf.getMentorMailFieldName()) {
      // 'MentorMail' anahtarından önce 'MentorAdi' ve 'MentorSoyadi' ekleniyor
      updatedEventData[cnf.getMentorNameFieldName()] = newGivenName || 'not a Contact';
      updatedEventData[getMentorSurnameFieldName()] = newFamilyName || 'not a Contact';
    }
    // Diğer anahtar-değer çiftlerini ekle
    updatedEventData[key] = eventData_[key];
  }

  return updatedEventData;
}
