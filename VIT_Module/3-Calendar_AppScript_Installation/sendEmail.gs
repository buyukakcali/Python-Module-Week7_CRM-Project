function sendEmail(emailAddress, mailType, dataList_) {
  try {
    // Logger.log('Target email: ' + emailAddress);
    
    // HTML şablonunu yükleyin ve içeriğini alın
    var htmlTemplate = HtmlService.createTemplateFromFile(mailType);
    var cnf = new Config();

    // HTML içeriğini işleyin
    // HTML şablonuna işlem ID'sini geçirin
    htmlTemplate.mentorName = dataList_['crm_MentorName'] || null;
    htmlTemplate.mentorSurname = dataList_['crm_MentorSurname'] || null;
    htmlTemplate.attendeeName = dataList_['crm_AttendeeName'] || null;
    htmlTemplate.attendeeSurname = dataList_['crm_AttendeeSurname'] || null;
    htmlTemplate.attendeeMail = dataList_['crm_AttendeeEmails'] || null;
    htmlTemplate.interviewDateTime = dataList_['crm_InterviewDatetime'] || null;
    htmlTemplate.sharedFolder = dataList_['sharedFolder'] || null;
    htmlTemplate.deadline = dataList_['deadline'] || null;
    htmlTemplate.ownerMail = cnf.getOwnerOfTheCalendarMail();
    htmlTemplate.configurationSheetName = cnf.getConfigurationSheetFileName();

    var htmlMessage = htmlTemplate.evaluate().getContent();

    // Gönderilecek e-posta içeriğini belirleyin
    if (mailType === 'evaluationMailTemplate'){;
      var subject = "WeRHere VIT Projesi Basvuru Degerlendirme Formu Linki";
    } else if(mailType === 'wrongEventCreationMailTemplate'){
      var subject = "Hatali/Eksik/Uyumsuz Etkinlik Olusturma";
    } else if(mailType === 'wrongEventUpdateMailTemplate'){
      var subject = "Hatali/Eksik/Uyumsuz Etkinlik Guncellemesi";
    } else if(mailType === 'projectHomeworkMailTemplate'){
      var subject = "Proje Odevi Yukleme Linki";
    } else if(mailType === 'projectHomeworkEvaluationFormMailTemplate'){
      var subject = "WeRHere VIT Projesi Aday Degerlendirme Formu Linki (Proje Odevi Toplantisi icin)";
    } else if(mailType === 'fatalErrorAboutConfigurationSheetTemplate'){
      var subject = "CRM PRojesi Kritik Sistem Hatasi";
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
    console.error('Error occurred in sendMail function: ' + e.stack);
  }
}
