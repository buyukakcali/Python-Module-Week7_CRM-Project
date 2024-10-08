function addAttendeesToCalendarEvent() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var sheetData = sheet.getDataRange().getValues();
  var headers = sheetData.shift(); // Başlık satırını ayır

  try {
    var cnf = new Config();
    var calendarId = cnf.getCalendarId();
    var calendar = CalendarApp.getCalendarById(calendarId);

    var eventIdColumnIndex = 1; // 2. kolon
    var summaryColumnIndex = 6; // 7. kolon (0'dan başlayarak)
    var attendeeMailColumnIndex = 10; // 11. kolon (0'dan başlayarak)
    var attendeeResponseStatusColumnIndex = 11; // 12. kolon
    var folderShareLink = null;

    // 'Project Homework Deadline' sütununun indeksini bul

    var headerOfParentFolderColumnName = cnf.getHeaderOfParentFolderColumnName();
    var headerOfDeadlineColumnName = cnf.getHeaderOfDeadlineColumnName();

    // Yeni sheet'in ID'si (buraya yeni sheet ID'sini ekleyin)
    var configurationSheetName = cnf.getConfigurationSheetFileName();
    var configSheetId = getConfigurationSheetId(configurationSheetName);  // Configuration dosyasinin adina gore sheet'in ID'si elde ediliyor.

    // Yeni sheet'e erişmek
    var sheetConfig = SpreadsheetApp.openById(configSheetId);
    var sheetConfigData = sheetConfig.getDataRange().getValues();
    var headers = sheetConfigData.shift(); // Başlık satırını ayırır

    // headerOfDeadlineColumnName değişkeninde yer alan değerin bulunduğu sütunun indeksini bul
    var parentFolderColumnIndex = headers.indexOf(headerOfParentFolderColumnName);
    var parentFolderName = sheetConfigData[0][parentFolderColumnIndex].toString().trim() || null;

    if (!parentFolderName) {
      Logger.log(configurationSheetName + ' sheetinde bulunmasi gereken klasor ismi su anda bos. Lutfen bu dosyayi ve verilerini kontrol edin! Elle veya python uygulamasi (CRM) ile ilgili verileri guncelleyin!!!');
      var fatalErrorAboutConfigurationSheetTemplate = cnf.getFatalErrorAboutConfigurationSheetTemplate();
      sendEmail(cnf.getOwnerOfTheCalendarMail(), fatalErrorAboutConfigurationSheetTemplate, {});
      Logger.log(configurationSheetName + ' sheet dosyasini kontrol etmesi icin sistem yoneticisine uyari/bilgi maili gonderildi. Ayrica katilimcilarin ilgili eventlere eklenme islemleri de iptal edilmis oldu. Duzelteme yapildiktan sonra otomatikman islem devam edecektir...');
      return
    }
    var parentFolder = DriveApp.getFolderById(parentFolderId);

    // deadlineColumnName değişkeninde yer alan değerin bulunduğu sütunun indeksini bul
    var deadlineColumnIndex = headers.indexOf(headerOfDeadlineColumnName);
    var deadline = sheetConfigData[0][deadlineColumnIndex].toString().trim();
    // var removeSharingDateTime = new Date(deadline);
    var deadline = new Date(deadline);

    // Logger.log('deadline: ' + deadline);
    // Logger.log('typeof(deadline): ' + typeof(deadline));

    for (var i = 1; i < sheetData.length; i++) {                // Starts from 1, because first row is for headers
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
              // Logger.log();
              // Logger.log('DETAY BILGISI: ' + JSON.stringify(event));
              var eventStartTime = event.getStartTime();
              var eventEndTime = event.getEndTime();

              // Etkinlik detaylarını al ve davetli ekle
              var eventDetails = {
                guests: event.getGuestList().map(guest => guest.getEmail()).concat(attendeeMail),
                sendInvites: true
              };
              Logger.log('eventDetails.guests: ' + eventDetails.guests);

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
                // Adaylara gonderilecek mailde sunum yazisini burada(description) guncelleyebiliriz. Mentorun etkinligi olustururken ne yazdigi veya bos biraktigini onemsemeden, otomatik olarak burada bir sunum yazariz. Mesela Sayin katilimci, detaylardaki gibi olan toplantida zamaninda hazir bulunmanizi beklemekteyiz... gibi vs. degiskenlerle bizzat sahsin ismiyle hitap da edebiliriz... event.setDescription methoduyla... Ayni sekilde summary icinde resmi bir baslik ayarlayabiliriz.... Ozetle, musteriye/basvurana sunum yapacagimiz sekle burada getiririz!
                description: event.getDescription(),
                start: { dateTime: eventStartTime.toISOString() },
                end: { dateTime: eventEndTime.toISOString() },
                attendees: eventDetails.guests.map(email => ({ email: email })),
                sendUpdates: 'all' // Burada sendUpdates parametresini ayarlıyoruz
              };

              // Adding extra text to the event description
              var note = '<p>Onemli Not: Eger Microsoft\'a ait bir mail adresi kullaniyorsaniz, Microsoft\'un, Google Takvim davetiyelerini islemesiyle ilgili bir sorundan dolayi etkinlik davetini gelen mailden kabul etseniz bile(RSVP seklinde gelen bolumden), bu cevap bizlere ulasamayabilir.<br><br>Bunun icin, daha asagida yer alan bolumde yer alan cevap secenegini (Yes, No, Maybe, More Options) kullanabilir veya etkinligin detaylarini goruntuleyerek, Google\'a ait bir sayfadan etkinlik davetini kabul edebilirsiniz.<br><br>Sabriniz icin tesekkur ederiz.</p><br><p>WeRHere Organization</p>';
              updateRequest.description = (updateRequest.description || '') + note;


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
                  folderShareLink = createAndShareFolder(attendeeMail, parentFolder.getName());
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
      } else { // Burayi devredisi biraktim. Cinku bu log dosyasini yazma isi islemci gucunu kullaniyor, toplam islem suresi uzuyor.
        Logger.log('Skipped row ' + (i + 1) + ': Invalid Attendee Mail or Response Status is not null');
      }
    }

  } catch (e) {
    console.error('Error occurred in addAttendeesToCalendarEvent function: ' + e);
  }
}
