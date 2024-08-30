function sendEmail(emailAddress, mailType, dataList_) {
  Logger.log('Hedef e-mail: ' + emailAddress);

  // HTML şablonunu yükleyin ve içeriğini alın
  var htmlTemplate = HtmlService.createTemplateFromFile(mailType);

  // HTML içeriğini işleyin
  // HTML şablonuna işlem ID'sini geçirin
  htmlTemplate.mentorName = dataList_['mentorName'];
  htmlTemplate.mentorSurname = dataList_['mentorSurname'];
  htmlTemplate.candidateName = dataList_['candidateName'];
  htmlTemplate.candidateSurname = dataList_['candidateSurname'];
  var htmlMessage = htmlTemplate.evaluate().getContent();

  // Gönderilecek e-posta içeriğini belirleyin
  if (mailType === 'evaluationMailTemplate'){
    var subject = "WeRHere VIT Projesi Aday Degerlendirme Formu Linki";
  } else if(mailType === 'baskabirtemplate'){
    var subject = "Baska birkonu";
  } else {
    var subject = "Etkinlik attendee eklemeyle ilgili sorunlu email!";
  }

  // E-posta gönderim işlemi
  emailSent = false;
  if (isValidEmail(emailAddress)){
    try {
      MailApp.sendEmail({
        to: emailAddress,
        subject: subject,
        htmlBody: htmlMessage
      });
      emailSent = true; // Eğer e-posta gönderimi başarılıysa değişkeni true yap
    } catch (error) {
      Logger.log('E-posta gönderiminde hata: ' + error.message);
    }
  }

  // E-posta gönderim durumuna göre log yazdır
  if (emailSent) {
    Logger.log('E-posta başarıyla gönderildi: ' + emailAddress);
  } else {
    Logger.log('E-posta gönderilemedi: ' + emailAddress);
  }
}

function isValidEmail(email) {
  // E-posta adresinin geçerliliğini kontrol eden regex deseni
  var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  // Logger.log('Mail Gecerlilik Durumu:' +regex.test(email));
  return regex.test(email);
}

// Kullanım örnekleri
// console.log(isValidEmail("example@example.com")); // true
// console.log(isValidEmail("example.com")); // false
// console.log(isValidEmail("example@.com")); // false
// console.log(isValidEmail("example@com")); // false
// console.log(isValidEmail("example@example..com")); // false
// console.log(isValidEmail("example@sub.example.com")); // true