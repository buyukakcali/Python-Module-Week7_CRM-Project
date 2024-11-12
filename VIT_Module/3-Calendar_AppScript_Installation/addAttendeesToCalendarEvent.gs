function addAttendeesToCalendarEvent() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var sheetData = sheet.getDataRange().getValues();
  var headers0 = sheetData.shift(); // Başlık satırını ayır

  try {
    var cnf = new Config();
    var calendarId = cnf.getCalendarId();
    var calendar = CalendarApp.getCalendarById(calendarId);

    var eventIdColumnIndex = 1; // 2. kolon
    var summaryColumnIndex = 6; // 7. kolon (0'dan başlayarak)
    var attendeeMailColumnIndex = 10; // 11. kolon (0'dan başlayarak)
    var attendeeResponseStatusColumnIndex = 11; // 12. kolon
    var folderShareLink = null;

    var configurationSheetName = cnf.getConfigurationSheetFileName();
    var parentFolderName = null;
    var deadLine = null;
    parentFolderName = getConfigurationSheetValues()['parentFolderName'];
    deadLine = getConfigurationSheetValues()['deadline'];
    // Logger.log('resultStringify:' + JSON.stringify(getConfigurationSheetValues()));
    deadline = new Date(deadLine);

    var rightNow = new Date();
    if (!parentFolderName || rightNow >= deadline) {
      Logger.log(configurationSheetName + " sheetinde bulunmasi gereken 'parent klasor ismi' bos veya 'son teslim tarihi' hatali. Lutfen '" + configurationSheetName + "' dosyasini ve verilerini kontrol edin! Elle veya python uygulamasi (CRM) ile ilgili verileri guncelleyin!!!");
      var fatalErrorAboutConfigurationSheetTemplate = cnf.getFatalErrorAboutConfigurationSheetTemplate();
      sendEmail(cnf.getOwnerOfTheCalendarMail(), fatalErrorAboutConfigurationSheetTemplate, {});
      Logger.log(configurationSheetName + ' sheet dosyasini kontrol etmesi icin sistem yoneticisine uyari/bilgi maili gonderildi. Ayrica katilimcilarin ilgili eventlere eklenme islemleri de iptal edilmis oldu. Duzelteme yapildiktan sonra en gec 1 saat icinde islem otomatikman devam edecektir...');
      return
    }

    for (var i = 0; i < sheetData.length; i++) {                // It starts from 0 because the header line was separated above
      var attendeeMail = sheetData[i][attendeeMailColumnIndex];
      var eventId = sheetData[i][eventIdColumnIndex];
      var attendeeResponseStatus = sheetData[i][attendeeResponseStatusColumnIndex];
      var summaryFromSheet = sheetData[i][summaryColumnIndex].toString();

      if (attendeeMail && attendeeMail.trim() !== "" &&
        (attendeeResponseStatus === null || attendeeResponseStatus === "null")) {
        if (eventId && eventId.trim() !== "") {
          try {
            var event = calendar.getEventById(eventId);
            // Logger.log('event.id  ??== eventId \n' + event.getId() + ' ??== ' + eventId);
            if (event) {
              // Logger.log('DETAY BILGISI: ' + JSON.stringify(event));
              var eventStartTime = event.getStartTime();
              var eventEndTime = event.getEndTime();

              // Etkinlik detaylarını al ve davetli ekle
              var eventDetails = {
                guests: event.getGuestList().map(guest => guest.getEmail()).concat(attendeeMail),
                sendInvites: true
              };
              // Logger.log('eventDetails.guests: ' + eventDetails.guests);

              // creatorEmail verisini de eventDetails.guests listesine ekleyelim
              var creatorEmail = event.getCreators().length > 0 ? event.getCreators()[0] : null;
              if (creatorEmail) {
                eventDetails.guests.push(creatorEmail);
              }
              // Logger.log('after adding creatoremail eventDetails.guests: ' + eventDetails.guests);

              // Event'i güncellemek ve e-posta göndermek için API kullanımı
              event.setGuestsCanModify(false);
              var calendarId = calendar.getId();
              var calendarApi = Calendar.Events;

              // Google Calendar API'sini kullanarak etkinliği güncelle ve sendUpdates parametresini ayarla
              var updateRequest = {
                summary: event.getTitle(),
                description: (cnf.getPersonalDescription() || event.getDescription()),
                start: { dateTime: eventStartTime.toISOString() },
                end: { dateTime: eventEndTime.toISOString() },
                attendees: eventDetails.guests.map(email => ({ email: email })),
                sendUpdates: 'all' // Burada sendUpdates parametresini ayarlıyoruz
              };
              // Mulakatlar icin mail icerigi duzenlemeleri
              updateRequest.description = (updateRequest.description || '') + cnf.getNote1() + cnf.getOrganizationSignature();


              // updateRequest.attendees.forEach(email=> {
              //   Logger.log('attendee: ' + email.email);
              // });

              calendarApi.patch(updateRequest, calendarId, eventId, {sendUpdates: 'all'});
              Logger.log('Attendee ' + attendeeMail + ' added to event ' + eventId);

              // Send emails:
              var dataList = {};

              if (summaryFromSheet && summaryFromSheet.trim()[0].startsWith('1')) {
                // First Interview Appointment: Send the evaluation form link to the mentor
                dataList = {'crm_MentorName':sheetData[i][3], 'crm_MentorSurname':sheetData[i][4], 'crm_AttendeeName':sheetData[i][12], 'crm_AttendeeSurname':sheetData[i][13], 'crm_AttendeeEmails':sheetData[i][attendeeMailColumnIndex], 'sharedFolder':'', 'deadline':''};
                var evaluationMailTemplate = cnf.getEvaluationMailTemplate();
                sendEmail(creatorEmail, evaluationMailTemplate, dataList);
                Logger.log('Degerlendirme formu linki ve aday bilgileri, mentore gonderildi.');

              } else if (summaryFromSheet && summaryFromSheet.trim()[0].startsWith('2')) {
                // Project Interview Appointment: A Google Drive folder will be created and shared for the applicant and the link will be returned.
                if (attendeeMail !== 'null') {
                  // Katilimcinin mail adresi ile olusturulacak klasorun icinde bulunacagi klasorun adi, parametre olarak gonderiliyor.
                  folderShareLink = createAndShareFolder(attendeeMail);
                }
                // Send the shared folder link to the attendee
                dataList = {'crm_MentorName':sheetData[i][3], 'crm_MentorSurname':sheetData[i][4], 'crm_AttendeeName':sheetData[i][12], 'crm_AttendeeSurname':sheetData[i][13], 'crm_AttendeeEmails':sheetData[i][attendeeMailColumnIndex], 'sharedFolder':folderShareLink, 'deadline':deadline};
                var projectHomeworkMailTemplate = cnf.getProjectHomeworkMailTemplate();
                sendEmail(attendeeMail, projectHomeworkMailTemplate, dataList);
                var projectHomeworkEvaluationFormMailTemplate = cnf.getProjectHomeworkEvaluationFormMailTemplate();
                sendEmail(creatorEmail, projectHomeworkEvaluationFormMailTemplate, dataList);
                Logger.log('Google Drive linki adaya ve Proje Odevi Degerlendirme Formu linki de mentore gonderildi.');

              } else {
                Logger.log('Calendar operations for any other thing');
                Logger.log('Summary: ' + summaryFromSheet);
              }
            } else {
              Logger.log('Event not found with ID: ' + eventId);
            }
          } catch (error) {
            Logger.log('Error adding attendee to event: ' + error);
          }
        } else {
          Logger.log('Empty or invalid Event ID for row ' + (i + 1));
        }
      } else { // Burayi devredisi biraktim. Cunku bu log dosyasini yazma isi islemci gucunu kullaniyor, toplam islem suresi uzuyor.
        Logger.log('Skipped row ' + (i + 1) + ': Invalid Attendee Mail or Response Status is not null');
      }
    }

  } catch (e) {
    console.error('Error occurred in addAttendeesToCalendarEvent function: ' + e);
  }
}
