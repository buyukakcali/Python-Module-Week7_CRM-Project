function insertMentorInfo(eventData_, newGivenName, newFamilyName) {
  try {
    var cnf = new Config(); // Config sınıfının bir örneğini oluşturun
    var updatedEventData = {};

    // 'MentorName' ve 'MentorSurname' eklenmeden önceki anahtar-değer çiftlerini ekle
    for (var key in eventData_) {
      if (key === cnf.getMentorMailFieldName()) {
        // 'MentorMail' anahtarından önce 'MentorName' ve 'MentorSurname' ekleniyor
        updatedEventData[cnf.getMentorNameFieldName()] = newGivenName || 'not a Contact';
        updatedEventData[cnf.getMentorSurnameFieldName()] = newFamilyName || 'not a Contact';
      }
      // Diğer anahtar-değer çiftlerini ekle
      updatedEventData[key] = eventData_[key];
    }
    return updatedEventData;
  } catch (e) {
    console.error('Error: ' + e.stack);
  }
}
