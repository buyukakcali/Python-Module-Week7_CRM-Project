function insertMentorInfo(eventData, newGivenName, newFamilyName) {
  var updatedEventData = {};

  // 'MentorAdi' ve 'MentorSoyadi' eklenmeden önceki anahtar-değer çiftlerini ekle
  for (var key in eventData) {
    if (key === 'MentorMail') {
      // 'MentorMail' anahtarından önce 'MentorAdi' ve 'MentorSoyadi' ekleniyor
      updatedEventData['MentorAdi'] = newGivenName || 'not a Contact';
      updatedEventData['MentorSoyadi'] = newFamilyName || 'not a Contact';
    }
    // Diğer anahtar-değer çiftlerini ekle
    updatedEventData[key] = eventData[key];
  }

  return updatedEventData;
}
