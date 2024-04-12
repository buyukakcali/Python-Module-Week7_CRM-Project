from psycopg2 import sql
from PyQt6.QtWidgets import QWidget, QApplication

import main
from UI_Files.menu_ui import Ui_FormUserMenu
import psycopg2


def run_query(query, data):
    # Database connection information
    database_name = "CRMv2.1"
    user = "postgres"
    password = "postgres"
    host = "localhost"
    port = "5432"  # Default PostgreSQL connection port

    # Connecting to PostgreSQL database
    try:
        connection = psycopg2.connect(
            dbname=database_name,
            user=user,
            password=password,
            host=host,
            port=port
        )

        cursor = connection.cursor()

        # Run SQL query
        cursor.execute(query, data)
        result = cursor.fetchall()  # result = cursor.fetchone()[0]  # Get the added kursiyerid
        connection.commit()
        connection.close()

    except Exception as e:
        print("Bağlantı hatası:", e)
        result = False
    return result


def compare_nested_list_and_tuple(nested_list, list_of_tuples):
    # İç içe liste ve liste içinde tuple boyutlarını kontrol et
    if len(nested_list) != len(list_of_tuples):
        print("Liste ve tuple yapısı farklı boyutlarda!")
        return

    # Her bir elemanı karşılaştır
    for i in range(len(nested_list)):
        sublist = nested_list[i]
        tuple_item = list_of_tuples[i]

        # İç içe listenin boyutu ile tuple'ın uzunluğunu kontrol et
        if len(sublist) != len(tuple_item):
            print(f"Eleman {i + 1}: İç içe liste ve tuple farklı boyutlarda!")
            continue

        # Elemanları karşılaştır
        for j in range(len(sublist)):
            if sublist[j] != tuple_item[j]:
                print(f"Farklı eleman bulundu: {sublist[j]} (liste) != {tuple_item[j]} (tuple)")


def check_new_updates():
    # Checking the Application Page list and updating it if necessary
    cloud_application_sheet = main.connection_hub('credentials/key.json', 'Basvurular', 'Sayfa1')
    cloud_application_data = cloud_application_sheet.get_all_values()
    cloud_application_data = main.remake_it_with_types(cloud_application_data)  # Rebuilds list based on the data type
    cloud_application_data_count = len(cloud_application_data) - 1  # Subtracting the number of column headers record

    # # Checking the Mentor Page list and updating it if necessary
    # cloud_mentor_sheet = main.connection_hub('credentials/key.json', 'Mentor', 'Sayfa1')
    # cloud_mentor_data = cloud_mentor_sheet.get_all_values()
    # cloud_mentor_data = main.remake_it_with_types(cloud_mentor_data)  # Rebuilds list based on the data type

    local_db_application_data = run_query("SELECT * FROM basvuru", '')
    local_db_application_data_count = run_query("SELECT COUNT(*) FROM basvuru", '')[0][0]

    # INSERT query for (kursiyer table)
    insert_kursiyer_query = sql.SQL("INSERT INTO kursiyer (AdSoyad, Email, Telefon, PostaKodu, YasadiginizEyalet) "
                                    "VALUES (%s, %s, %s, %s, %s) RETURNING kursiyerid;")

    # INSERT query for (basvuru table)
    insert_basvuru_query = sql.SQL(
        "INSERT INTO basvuru (zamandamgasi, kursiyerid, suankidurum, itphegitimkatilmak, "
        "ekonomikdurum, dilkursunadevam, ingilizceseviye, hollandacaseviye, baskigoruyor, "
        "bootcampbitirdi, onlineitkursu, ittecrube, projedahil, calismakistedigi, "
        "nedenkatilmakistiyor, basvurudonemi)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING basvuruid;"
    )

    if local_db_application_data_count != 0:
        print('Oleyyy')
        # if True:
            # # if not compare_nested_list_and_tuple(cloud_application_data[1:], local_db_application_data):
            #
            # # INSERT query for (kursiyer table)
            # insert_kursiyer_query = ("INSERT INTO kursiyer (AdSoyad, Email, Telefon, PostaKodu, YasadiginizEyalet) "
            #                          "VALUES (%s, %s, %s, %s, %s);")
            #
            # for i, row in enumerate(cloud_application_data):
            #     if i + 1 > len(local_db_application_data):
            #         kursiyer_data = []
            #         for j, col in enumerate(row):
            #             # Information of the kursiyer to be added The numbers here are the column indices where the
            #             # trainee's information is kept in the worksheet in the cloud.
            #             if j in (1, 2, 3, 4, 5):
            #                 kursiyer_data.append(str(col))
            #         kursiyer_data = tuple(kursiyer_data)
            #         donen = run_query(insert_kursiyer_query, kursiyer_data)
            #         print(donen)

                    # hemen burada basvuru tablosuna ve diger tablolara da insert islemleri uygulanmali

            # indisi bir artirarak clouddaki veriyi database e yazdir. ayrica yeni eklenenler diye bir liste
            # de olusturulup kullaniciya uyari olarak gosterilebilir
        # else:
        #     print('Google formlardan gelen yeni kayit yok!')
    else:
        for i, row in enumerate(cloud_application_data[1:]):
            if i + 1 > len(local_db_application_data):
                kursiyer_data = (row[1], row[2], row[3], row[4], row[5])
                kursiyer_id = run_query(insert_kursiyer_query, kursiyer_data)[0][0]
                basvuru_data = []
                for j, col in enumerate(row):
                    if j not in (1, 2, 3, 4, 5) and j < 20:
                        basvuru_data.append(col)

                basvuru_data.insert(1, kursiyer_id)     # add the kursiyer_id to the right place for the basvuru table
                basvuru_data = tuple(basvuru_data)
                print(basvuru_data)

                basvuru_id = run_query(insert_basvuru_query, basvuru_data)[0][0]

                # hemen burada basvuru tablosuna ve diger tablolara da insert islemleri uygulanmali

        # indisi bir artirarak clouddaki veriyi database e yazdir. ayrica yeni eklenenler diye bir liste
        # de olusturulup kullaniciya uyari olarak gosterilebilir


    #
    # count_mentor_query = "SELECT COUNT(*) FROM kursiyer"
    # local_db_mentor_data_count = run_query(count_mentor_query)[0][0]
    #
    # if local_db_mentor_data_count != cloud_mentor_data_count:
    #     localdb_mentor_data = run_query("SELECT * FROM kursiyer")
    #
    # # Checking the Interview Page list and updating it if necessary
    # cloud_interview_sheet = main.connection_hub('credentials/key.json', 'Mulakatlar', 'Sayfa1')
    # cloud_interview_data = cloud_interview_sheet.get_all_values()
    # cloud_interview_data_count = len(cloud_interview_data) - 1  # Subtracting the number of column headers record
    #
    # count_interview_query = "SELECT COUNT(*) FROM projetakip"
    # local_db_interview_data_count = run_query(count_interview_query)[0][0]
    #
    # if local_db_interview_data_count != cloud_interview_data_count:
    #     pass


class UserMenuPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user
        self.user_menu_form = Ui_FormUserMenu()
        self.user_menu_form.setupUi(self)
        # run_query()  # Every program opening, this code updates the database from cloud
        check_new_updates()

        # If a user opens the app, do!
        self.user_menu_form.labelUsers.show()
        self.user_menu_form.pushButtonManagement.close()

        self.user_menu_form.labelCurrentUser.setText(str(current_user[0]).split(' ')[0])

        self.settings_window_open = None
        self.login_window = None
        self.applications_window_open = None
        self.interviews_window_open = None
        self.mentor_menu_open = None

        self.user_menu_form.toolButtonAccount.clicked.connect(self.go_settings_page)
        self.user_menu_form.pushButtonInterviews.clicked.connect(self.go_interviews_page)
        self.user_menu_form.pushButtonApplications.clicked.connect(self.go_applications_page)
        self.user_menu_form.pushButtonMentorMeeting.clicked.connect(self.go_mentors_page)
        self.user_menu_form.pushButtonSignOut.clicked.connect(self.goback_login_page)
        self.user_menu_form.pushButtonExit.clicked.connect(self.app_exit)

    def go_settings_page(self):
        from settings import SettingsPage
        self.settings_window_open = SettingsPage(self.current_user)
        self.settings_window_open.show()

    def go_mentors_page(self):
        from mentors import MentorPage
        self.hide()
        self.mentor_menu_open = MentorPage(self.current_user)
        self.mentor_menu_open.show()

    def go_applications_page(self):
        from applications import ApplicationsPage
        self.hide()
        self.applications_window_open = ApplicationsPage(self.current_user)
        self.applications_window_open.show()

    def go_interviews_page(self):
        from interviews import InterviewsPage
        self.hide()
        self.interviews_window_open = InterviewsPage(self.current_user)
        self.interviews_window_open.show()

    def goback_login_page(self):
        from login import LoginPage
        self.hide()
        self.login_window = LoginPage()
        self.login_window.show()

    def app_exit(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    main_window = UserMenuPage(['s', 'd', 'user'])
    main_window.show()
    app.exec()
