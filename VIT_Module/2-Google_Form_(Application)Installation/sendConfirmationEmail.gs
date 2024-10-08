function sendConfirmationEmail(emailAddress, mailType, dataList ) {
  try {
    // Logger.log('Hedef e-mail: ' + emailAddress);

    // HTML şablonunu yükleyin ve içeriğini alın
    var htmlTemplate = HtmlService.createTemplateFromFile(mailType);

    // HTML içeriğini işleyin
    // HTML şablonuna işlem ID'sini geçirin
    htmlTemplate.transactionId = dataList['transactionId'];
    htmlTemplate.name = dataList['applicantName'];
    htmlTemplate.surname = dataList['applicantSurname'];
    var htmlMessage = htmlTemplate.evaluate().getContent();

    // Gönderilecek e-posta içeriğini belirleyin
    if (mailType === 'newApplicationAddedTemplate'){
      var subject = "Başvurunuz Alındı";
    } else if(mailType === 'applicationUpdatedTemplate'){
      var subject = "Basvurunuz Guncellendi";
    } else if(mailType === 'basvuruGuncellemedeHataTemplate'){
      var subject = "Basvurunuz Guncellemede Kritik*(Uygulama) Hata";
    } else {
      var subject = "Başvurunuz Guncellenemedi";
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
      } catch (e) {
        console.error('E-posta gönderiminde hata: ' + e.stack);
      }
    }

    // E-posta gönderim durumuna göre log yazdır
    if (emailSent) {
      Logger.log('E-posta başarıyla gönderildi: ' + emailAddress);
    } else {
      Logger.log('E-posta gönderilemedi: ' + emailAddress);
    }
  } catch (e) {
    console.error('Error occurred in sendConfirmationEmail function: ' + e.stack);
  }
}
