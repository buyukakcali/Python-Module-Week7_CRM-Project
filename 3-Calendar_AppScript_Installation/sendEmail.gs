function sendEmail(emailAddress, mailType, dataList_) {
  try {
    // Logger.log('Target email: ' + emailAddress);
    
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
    } else if(mailType === 'anyOtherTemplate'){
      var subject = "Any other subject";
    } else {
      var subject = "Problematic email regarding adding event attendee!";
    }

    // E-posta gönderim işlemiE-posta gönderilemedi:
    emailSent = false;
    if (isValidEmail(emailAddress)){
      try {
        MailApp.sendEmail({
          to: emailAddress,
          subject: subject,
          htmlBody: htmlMessage
        });
        emailSent = true; // Eğer e-posta gönderimi başarılıysa değişkeni true yap
      } catch (e) {
        console.error('Error sending email: ' + e.stack);
      }
    }

    // E-posta gönderim durumuna göre log yazdır
    if (emailSent) {
      Logger.log('Email sent successfully: ' + emailAddress);
    } else {
      Logger.log('Email could not be sent: ' + emailAddress);
    }
  } catch (e) {
    console.error('Error occured in sendMail function: ' + e.stack);
  }
}

function isValidEmail(email) {
  try {
    // E-posta adresinin geçerliliğini kontrol eden regex deseni
    var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // Logger.log('Mail Gecerlilik Durumu:' +regex.test(email));
    return regex.test(email);
  } catch (e) {
    console.error('Error occured in isValidEmail function: ' + e.stack);
  }  
}

// Kullanım örnekleri
// console.log(isValidEmail("example@example.com")); // true
// console.log(isValidEmail("example.com")); // false
// console.log(isValidEmail("example@.com")); // false
// console.log(isValidEmail("example@com")); // false
// console.log(isValidEmail("example@example..com")); // false
// console.log(isValidEmail("example@sub.example.com")); // true
