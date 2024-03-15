from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from applications_ui import Ui_Form
import gspread

credentials = 'key.json'
gc = gspread.service_account(filename=credentials)
spreadsheet = gc.open('Basvurular')
worksheet = spreadsheet.get_worksheet(0)


class ApplicationsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_Form()  # Ui_Form sınıfından bir örnek oluştur
        self.ui.setupUi(self)  # Arayüzü oluştur

        # Arayüz öğelerine bağlanacak butonların sinyal-slot bağlantıları
        self.ui.pushButton_app_all_app.clicked.connect(self.show_all_applications)
        self.ui.pushButton_app_planned_mentor.clicked.connect(self.show_planned_mentor_meetings)
        self.ui.pushButton_app_unscheduled_meeting.clicked.connect(self.show_unscheduled_meetings)
        self.ui.pushButton_app_pre_vit_control.clicked.connect(self.show_previous_vit_control)
        self.ui.pushButton_app_rep_registrations.clicked.connect(self.show_repeated_registrations)
        self.ui.pushButton_diff_registration.clicked.connect(self.show_different_registrations)
        self.ui.pushButton_app_preferences.clicked.connect(self.go_to_preferences)
        self.ui.pushButton_app_filter_app.clicked.connect(self.filter_applications)
        self.ui.pushButton_app_exit.clicked.connect(self.exit_application)

        # Search butonuna tıklanma işlemi için sinyal-slot bağlantısı
        self.ui.pushButton_app_search.clicked.connect(self.search_applications)

    # Arayüzdeki butonların işlevlerini tanımlayacağımız fonksiyonlar
    def filter_applications_by_name(self):
        text = self.ui.lineEdit.text().strip().lower()  # LineEdit'teki metni al ve küçük harfe çevir
        if not text:  # Metin boşsa tüm başvuruları göster
            self.show_all_applications()
            return

        filtered_rows = []  # Eşleşen satırları tutacak liste
        all_applications = worksheet.get_all_values()  # Tüm başvuruları al
        headers = all_applications[0]  # Başlıkları al

        # Ad ve soyadları kontrol et ve eşleşenleri filtered_rows listesine ekle
        for i, row in enumerate(all_applications):
            if i == 0:  # Başlıkları atla
                continue
            name = row[1].strip().lower()  # Adı al ve küçük harfe çevir
            if name.startswith(text):  # Metinle başlayan adları filtrele
                filtered_rows.append(row)

        # Tabloyu temizle
        self.ui.tableWidget.clearContents()
        # Tabloya başlık ekle
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        # Eşleşen satırları tabloya ekle
        self.ui.tableWidget.setRowCount(len(filtered_rows))
        for i, row in enumerate(filtered_rows):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.ui.tableWidget.setItem(i, j, item)
    def show_all_applications(self):
        # Tüm başvuruları al
        all_applications = worksheet.get_all_values()

        # Tabloyu temizle
        self.ui.tableWidget.clearContents()

        # Tabloya başlık ekle
        headers = all_applications[0]
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)

        # Tabloya verileri ekle
        self.ui.tableWidget.setRowCount(len(all_applications) - 1)  # Başlık hariç toplam satır sayısı
        for i, row in enumerate(all_applications[1:], 0):  # Başlığı atladığımız için indeksi 1'den başlatıyoruz
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.ui.tableWidget.setItem(i, j, item)

    def show_planned_mentor_meetings(self):
        pass

    def show_unscheduled_meetings(self):
        # Halen mentor atanmamış kişileri ekrana getirme işlemi

        # Başlıkları ve tüm başvuruları al
        headers = worksheet.row_values(1)
        all_applications = worksheet.get_all_values()

        # Mentor ataması yapılmamış kişilerin bilgilerini bul
        unscheduled_applications = []
        for row in all_applications[1:]:
            mentor_status = row[5]  # "Mentor gorusmesi" sütununu uygun şekilde ayarlayın
            if mentor_status == "ATANMADI":
                unscheduled_applications.append(row)

        # Tabloyu temizle
        self.ui.tableWidget.clearContents()

        # Tabloya başlık ekle
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)

        # Kişilerin bilgilerini tabloya ekle
        self.ui.tableWidget.setRowCount(len(unscheduled_applications))
        for i, row in enumerate(unscheduled_applications):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.ui.tableWidget.setItem(i, j, item)

    def show_previous_vit_control(self):
        # Önceki VIT kontrollerinde ortak bulunan adayları ekrana getirme işlemi
        pass

    def show_repeated_registrations(self):
        # Tekrarlanan kayıtları ekrana getirme işlemi
        pass

    def show_different_registrations(self):
        # Farklı kayıtları ekrana getirme işlemi
        pass

    def go_to_preferences(self):
        # Tercihler menüsüne geçiş işlemi
        pass

    def filter_applications(self):
        # Mükerrer kayıtları filtreleme işlemi
        pass

    def exit_application(self):
        # Uygulamadan çıkma işlemi
        QApplication.quit()

    def search_applications(self):
        # Ad veya soyada göre başvuruları arama işlemi
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = ApplicationsPage()
    form.show()
    sys.exit(app.exec())
