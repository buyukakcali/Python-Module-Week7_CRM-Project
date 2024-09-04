function addAttendeesToCalendarEvent() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var sheetData = sheet.getDataRange().getValues();
  var evaluationLinkMail = 'evaluationMailTemplate';

  try {
    var cnf = new Config();
    var calendarId = cnf.getCalendarId();
    var calendar = CalendarApp.getCalendarById(calendarId);

    var attendeeMailColumnIndex = 10; // 11. kolon (0'dan başlayarak)
    var eventIdColumnIndex = 1; // 2. kolon
    var attendeeResponseStatusColumnIndex = 11; // 12. kolon

    for (var i = 1; i < sheetData.length; i++) {                // Starts from 1, because first row is for headers
      var attendeeMail = sheetData[i][attendeeMailColumnIndex];
      var eventId = sheetData[i][eventIdColumnIndex];
      var attendeeResponseStatus = sheetData[i][attendeeResponseStatusColumnIndex];

      if (attendeeMail && attendeeMail.trim() !== "" &&
          (attendeeResponseStatus === null || attendeeResponseStatus === "null")) {
        if (eventId && eventId.trim() !== "") {
          try {
            var event = calendar.getEventById(eventId);
            if (event) {
              var eventStartTime = event.getStartTime();
              var eventEndTime = event.getEndTime();

              // Etkinlik detaylarını al ve davetli ekle
              var eventDetails = {
                guests: event.getGuestList().map(guest => guest.getEmail()).concat(attendeeMail),
                sendInvites: true
              };

              // creatorEmail verisini de eventDetails.guests listesine ekleyelim
              var creatorEmail = event.getCreators().length > 0 ? event.getCreators()[0] : null;
              if (creatorEmail) {
                eventDetails.guests.push(creatorEmail);
              }

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

              updateRequest.attendees.forEach(email=> {
                Logger.log('attendee: ' + email.email);
              });

              calendarApi.patch(updateRequest, calendarId, eventId, {sendUpdates: 'all'});
              Logger.log('Attendee ' + attendeeMail + ' added to event ' + eventId);

              // Send evaluation form link to mentor
              var dataList = {'mentorName':sheetData[i][3], 'mentorSurname':sheetData[i][4], 'candidateName':sheetData[i][12], 'candidateSurname':sheetData[i][13], 'candidateMail':sheetData[i][attendeeMailColumnIndex]};
              sendEmail(creatorEmail, evaluationLinkMail, dataList);
              Logger.log('Degerlendirme formu linki ve aday bilgileri, mentore gonderildi.');
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
