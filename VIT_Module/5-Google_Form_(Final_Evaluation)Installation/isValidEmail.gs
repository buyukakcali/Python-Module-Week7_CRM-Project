function isValidEmail(email) {
  try {
    // E-posta adresinin geçerliliğini kontrol eden regex deseni
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // Logger.log('Mail Gecerlilik Durumu:' +regex.test(email));
    return regex.test(email);
  } catch (e) {
    console.error('Error occurred in isValidEmail function: ' + e.stack);
  }
}
