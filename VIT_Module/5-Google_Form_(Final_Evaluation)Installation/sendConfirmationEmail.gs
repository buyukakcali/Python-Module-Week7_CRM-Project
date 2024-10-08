function sendConfirmationEmail(emailAddress, mailType, dataList) {
  try {
    // Logger.log('Target e-mail: ' + emailAddress);

    // Load the HTML template and get its content
    var htmlTemplate = HtmlService.createTemplateFromFile(mailType);

    // Render HTML content
    htmlTemplate.candidateName = dataList[0];
    htmlTemplate.candidateSurname = dataList[1];
    var htmlMessage = htmlTemplate.evaluate().getContent();

    // Determine the email content to be sent
    if (mailType === 'finalEvaluationIsRecordedTemplate'){
      var subject = "Final Değerlendirmeniz Alındı";
    } else if(mailType === 'finalEvaluationIsUpdatedTemplate'){
      var subject = "Final Değerlendirmeniz Güncellendi";
    }  else if(mailType === 'wrongCandiddateEmailTemplate'){
      var subject = "Final Degerlendirmeniz alinMADI/guncellenMEDI";
    } else if(mailType === 'baskaBirTemplate'){
      var subject = "Baska birkonu";
    } else {
      var subject = "There is a problem sending information mail!";
    }

    // Email sending process
    emailSent = false;
    if (isValidEmail(emailAddress)){
      try {
        MailApp.sendEmail({
          to: emailAddress,
          subject: subject,
          htmlBody: htmlMessage
        });
        emailSent = true; // If the email sending is successful, set the variable to true
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
    console.error('Error occurred in sendConfirmationEmail function: ' + e.stack);
  }
}
