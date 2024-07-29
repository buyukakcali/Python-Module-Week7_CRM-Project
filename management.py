import base64
from email.mime.text import MIMEText
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime
import pickle
import os.path

from UI_Files.management_ui import Ui_FormManagement

# Google Calendar ve Gmail API yetkilendirme kapsamları
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/calendar']


class ManagementPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user
        self.form_management = Ui_FormManagement()
        self.form_management.setupUi(self)

        self.events = None

        self.menu_user = None
        self.menu_admin = None

        self.form_management.pushButtonGetAllEvents.clicked.connect(self.get_calendar_events)
        self.form_management.pushButtonSendEmail.clicked.connect(self.send_invitations)
        self.form_management.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_management.pushButtonExit.clicked.connect(self.close)

    def get_calendar_events(self):
        # Yetkilendirme
        creds = self.get_credentials()
        service = build('calendar', 'v3', credentials=creds)

        # Bugünün tarihini al
        now = datetime.datetime.utcnow().isoformat() + 'Z'

        # Etkinlikleri al
        events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10,
                                              singleEvents=True, orderBy='startTime').execute()
        self.events = events_result.get('items', [])

        # Tabloya etkinlikleri ekle
        table = self.form_management.tableWidget
        table.setRowCount(0)  # Önceki verileri temizle

        for event in self.events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            formatted_start = datetime.datetime.fromisoformat(start).strftime("%d-%m-%Y %H:%M")
            attendees = event.get('attendees', [])
            participant_emails = ", ".join([attendee['email'] for attendee in attendees if attendee.get('email')])
            organizer_email = event['organizer'].get('email', 'Unknown')

            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
            table.setItem(rowPosition, 0, QTableWidgetItem(event.get('summary', 'No Name')))
            table.setItem(rowPosition, 1, QTableWidgetItem(formatted_start))
            table.setItem(rowPosition, 2, QTableWidgetItem(participant_emails))
            table.setItem(rowPosition, 3, QTableWidgetItem(organizer_email))

    def get_credentials(self):
        # Token dosyasını kontrol et
        if os.path.exists('credentials/token.pickle'):
            with open('credentials/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        else:
            creds = None

        # Yetkilendirme yoksa veya geçersizse yeniden yetkilendirme yap
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("Yeni yetkilendirme başlatılıyor...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                print("Yeni yetkilendirme tamamlandı.")

            # Yeni yetkilendirme bilgilerini kaydet
            with open('credentials/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def send_invitations(self):
        # Gmail API'siyle yetkilendirme
        creds = self.get_credentials()
        service = build('gmail', 'v1', credentials=creds)

        for event in self.events:
            attendees = [attendee['email'] for attendee in event.get('attendees', []) if attendee.get('email')]
            event_id = event['id']

            for email in attendees:
                try:
                    message = self.create_message("werherevit@gmail.com", email, "Invitation", "You are invited!")
                    self.send_message(service, "me", message)
                    print(f"Davet gönderildi: {email}")
                except Exception as e:
                    print(f"E-posta gönderilirken bir hata oluştu: {e}")

    def create_message(self, sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes())
        raw_message = raw_message.decode('utf-8')
        return {'raw': raw_message}

    def send_message(self, service, user_id, message):
        try:
            message = service.users().messages().send(userId=user_id, body=message).execute()
        except Exception as e:
            print("E-posta gonderilirken bir hata oluştu:", e)

    def back_menu(self):
        if self.current_user[2] != "admin":
            from menu import UserMenuPage
            self.hide()
            self.form_management.menu_user = UserMenuPage(self.current_user)
            self.form_management.menu_user.show()
        else:
            from admin_menu import AdminMenuPage
            self.hide()
            self.form_management.menu_admin = AdminMenuPage(self.current_user)
            self.form_management.menu_admin.show()


if __name__ == "__main__":
    app = QApplication([])
    main_window = ManagementPage(('a', 'b', 'admin'))
    main_window.show()
    app.exec()
