from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QComboBox

import my_functions as myf
from UI_Files.applications_ui import Ui_FormApplications
from my_classes import Config


class ApplicationsPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user  # Variable name is absolutely perfect for why it is here
        self.sort_order = {}  # Dictionary to keep track of sort order for each column

        self.active_list = None
        self.filtering_list = None  # This is active nested list, it changes on that you click to the buttons to buttons
        self.applications = None

        self.worksheet = None
        self.VIT1 = None
        self.VIT2 = None

        self.form_applications = Ui_FormApplications()
        self.form_applications.setupUi(self)
        self.menu_user = None
        self.menu_admin = None

        # Persistent form settings activated at startup:
        self.form_applications.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.form_applications.tableWidget.setStyleSheet("""
                        QTableWidget { background-color: rgba(0, 0, 0,0%);}
                        QToolTip { background-color: yellow; color: black; border: 1px solid black; }
                        """)

        # Initial load view and first filtering column settings
        self.filtering_column = 2
        self.form_applications.comboBoxFilterOptions.setPlaceholderText("Filter Area")
        self.headers = ["Zaman damgası", "Başvuru dönemi", "Adınız", "Soyadınız", "Mail adresiniz", "Telefon numaranız",
            "Posta kodunuz", "Yaşadığınız Eyalet", "Şu anki durumunuz",
            "Yakın zamanda başlayacak ITPH Cybersecurity veya Powerplatform Eğitimlerine katılmak ister misiniz",
            "Ekonomik durumunuz", "Şu anda bir dil kursuna devam ediyor musunuz?", "Yabancı dil seviyeniz [İngilizce]",
            "Yabancı dil seviyeniz [Hollandaca]", "Belediyenizden çalışma ile ilgili baskı görüyor musunuz?",
            "Başka bir IT kursu (Bootcamp) bitirdiniz mi?",
            "İnternetten herhangi bir IT kursu takip ettiniz mi (Coursera, Udemy gibi)",
            "Daha önce herhangi bir IT iş tecrübeniz var mı?",
            "Şu anda herhangi bir projeye dahil misiniz? (Öğretmenlik projesi veya Leerwerktraject v.s)",
            "IT sektöründe hangi bölüm veya bölümlerde çalışmak istiyorsunuz? (Birden fazla seçenek seçebilirsiniz)",
            "Neden VIT projesine katılmak istiyorsunuz? (Birden fazla seçenek seçebilirsiniz)",
            "Aşağıya bu projeye katılmak veya IT sektöründe kariyer yapmak için sizi harekete geçiren motivasyondan "
            "bahseder misiniz?"]
        myf.write2table(self.form_applications, self.headers, [])   # This code updates the tableWidget headers


        # Connect signals to slots
        self.form_applications.lineEditSearch.textEdited.connect(self.search_application)
        self.form_applications.lineEditSearch.returnPressed.connect(self.search_application)
        self.form_applications.pushButtonLastPeriod.clicked.connect(self.get_last_period_applications)
        self.form_applications.pushButtonAllPeriods.clicked.connect(self.get_all_applications)
        self.form_applications.pushButtonPlannedMeetings.hide()
        self.form_applications.pushButtonUnscheduledMeeting.hide()
        self.form_applications.comboBoxDuplicatedApplications.hide()
        self.form_applications.pushButtonDifferentialRegistrations.hide()
        self.form_applications.pushButtonFilterApplications.hide()
        # self.form_applications.pushButtonPlannedMeetings.clicked.connect(self.app_planned_meetings)
        # self.form_applications.pushButtonUnscheduledMeeting.clicked.connect(self.app_unscheduled_meetings)
        self.form_applications.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
        # self.form_applications.comboBoxDuplicatedApplications.currentIndexChanged.connect(self.app_duplicate_records)
        # self.form_applications.pushButtonDifferentialRegistrations.clicked.connect(self.app_differential_registrations)
        # self.form_applications.pushButtonFilterApplications.clicked.connect(self.app_filter_applications)
        self.form_applications.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_applications.pushButtonExit.clicked.connect(self.app_exit)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_applications.tableWidget.cellEntered.connect(self.on_cell_entered)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_applications.tableWidget.cellClicked.connect(self.on_cell_clicked)

        # Connect the header's sectionClicked signal to the on_header_clicked method
        self.form_applications.tableWidget.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # Connect the header's sectionDoubleClicked signal to the on_header_double_clicked method
        # Activity code to offer new filtering options when you click on the titles
        self.form_applications.tableWidget.horizontalHeader().sectionDoubleClicked.connect(
            self.on_header_double_clicked)

        # This code enables mouse tracking on tableWidget. It is needed for all mouse activity options above!
        self.form_applications.tableWidget.setMouseTracking(True)

        # The display settings of the last clicked objects are determined.
        self.widgets = self.findChildren(QPushButton)  # Find all buttons of type QPushButton & assign them to the list
        self.widgets.extend(self.findChildren(QComboBox))   # Extend the list with QCombobox objects
        myf.handle_widget_styles(self, self.widgets)  # Manage button styles with central function

    def get_last_period_applications(self):
        try:
            myf.normalise_combo_boxes([None, self.form_applications.comboBoxFilterOptions])
            cnf = Config()

            # This query returns only the most recent applications
            q1 = ("SELECT "
                  "b." + cnf.applicationTableFieldNames[2] + ", b." + cnf.applicationTableFieldNames[3] +
                  ", a." + cnf.applicantTableFieldNames[2] + ", a." + cnf.applicantTableFieldNames[3] +
                  ", a." + cnf.applicantTableFieldNames[4] + ", a." + cnf.applicantTableFieldNames[5] +
                  ", a." + cnf.applicantTableFieldNames[6] + ", a." + cnf.applicantTableFieldNames[7] +
                  ", b." + cnf.applicationTableFieldNames[4] + ", b." + cnf.applicationTableFieldNames[5] +
                  ", b." + cnf.applicationTableFieldNames[6] + ", b." + cnf.applicationTableFieldNames[7] +
                  ", b." + cnf.applicationTableFieldNames[8] + ", b." + cnf.applicationTableFieldNames[9] +
                  ", b." + cnf.applicationTableFieldNames[10] + ", b." + cnf.applicationTableFieldNames[11] +
                  ", b." + cnf.applicationTableFieldNames[12] + ", b." + cnf.applicationTableFieldNames[13] +
                  ", b." + cnf.applicationTableFieldNames[14] + ", b." + cnf.applicationTableFieldNames[15] +
                  ", b." + cnf.applicationTableFieldNames[16] + ", b." + cnf.applicationTableFieldNames[17] + " " +
                  "FROM " + cnf.applicationTable + " b "
                  "INNER JOIN " + cnf.applicantTable + " a " +
                  "ON b." + cnf.applicationTableFieldNames[1] + " = a." + cnf.applicantTableFieldNames[0] + " " +
                  "WHERE b." + cnf.applicationTableFieldNames[3] + " = %s " +
                  "ORDER BY b." + cnf.applicationTableFieldNames[2] + " ASC")

            # q1 = ("SELECT "
            #       "b.crm_Timestamp, b.crm_Period, a.crm_Name, a.crm_Surname, a.crm_Email, a.crm_Phone, a.crm_PostCode, "
            #       "a.crm_Province, b.crm_SuAnkiDurum, b.crm_ITPHEgitimKatilmak, b.crm_EkonomikDurum, "
            #       "b.crm_DilKursunaDevam, b.crm_IngilizceSeviye, b.crm_HollandacaSeviye, b.crm_BaskiGoruyor, "
            #       "b.crm_BootcampBitirdi, b.crm_OnlineITKursu, b.crm_ITTecrube, b.crm_ProjeDahil, "
            #       "b.crm_CalismakIstedigi, b.crm_NedenKatilmakIstiyor, b.crm_MotivasyonunNedir "
            #       "FROM form1_application b "
            #       "INNER JOIN form1_applicant a ON b.crm_ApplicantID = a.crm_ID "
            #       "WHERE b.crm_Period = %s "
            #       "ORDER BY b.crm_Timestamp ASC")

            conn = cnf.open_conn()
            applications = myf.execute_read_query(conn, q1, (myf.last_period(),))

            # Recreate the list based on the data type of the cells
            self.active_list = myf.remake_it_with_types(applications)

            myf.write2table(self.form_applications, self.headers, self.active_list)

            # Fill the combobox for filtering while loading
            self.form_applications.comboBoxFilterOptions.clear()
            self.filtering_list = list(self.active_list)
            self.filtering_column = 2
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_applications.comboBoxFilterOptions.addItems(items)

        except ConnectionError as ce:
            print(f"Connection error occurred: {ce}")

        except (AttributeError, TypeError) as e:
            print(f"Data processing error: {e}")

        except Exception as e:
            raise Exception(f"Error occurred in get_last_period_applications method: {e}")

    def get_all_applications(self):
        try:
            myf.normalise_combo_boxes([None, self.form_applications.comboBoxFilterOptions])
            cnf = Config()

            # This query returns all records of applications in all periods
            q1 = ("SELECT "
                  "b." + cnf.applicationTableFieldNames[2] + ", b." + cnf.applicationTableFieldNames[3] +
                  ", a." + cnf.applicantTableFieldNames[2] + ", a." + cnf.applicantTableFieldNames[3] +
                  ", a." + cnf.applicantTableFieldNames[4] + ", a." + cnf.applicantTableFieldNames[5] +
                  ", a." + cnf.applicantTableFieldNames[6] + ", a." + cnf.applicantTableFieldNames[7] +
                  ", b." + cnf.applicationTableFieldNames[4] + ", b." + cnf.applicationTableFieldNames[5] +
                  ", b." + cnf.applicationTableFieldNames[6] + ", b." + cnf.applicationTableFieldNames[7] +
                  ", b." + cnf.applicationTableFieldNames[8] + ", b." + cnf.applicationTableFieldNames[9] +
                  ", b." + cnf.applicationTableFieldNames[10] + ", b." + cnf.applicationTableFieldNames[11] +
                  ", b." + cnf.applicationTableFieldNames[12] + ", b." + cnf.applicationTableFieldNames[13] +
                  ", b." + cnf.applicationTableFieldNames[14] + ", b." + cnf.applicationTableFieldNames[15] +
                  ", b." + cnf.applicationTableFieldNames[16] + ", b." + cnf.applicationTableFieldNames[17] + " " +
                  "FROM " + cnf.applicationTable + " b " +
                  "INNER JOIN " + cnf.applicantTable + " a " +
                  "ON b." + cnf.applicationTableFieldNames[1] + " = a." + cnf.applicantTableFieldNames[0] + " " +
                  "ORDER BY b." + cnf.applicationTableFieldNames[2] + " ASC")

            # q1 = ("SELECT "
            #       "b.crm_Timestamp, b.crm_Period, a.crm_Name, a.crm_Surname, a.crm_Email, a.crm_Phone, a.crm_PostCode, "
            #       "a.crm_Province, b.crm_SuAnkiDurum, b.crm_ITPHEgitimKatilmak, b.crm_EkonomikDurum, "
            #       "b.crm_DilKursunaDevam, b.crm_IngilizceSeviye, b.crm_HollandacaSeviye, b.crm_BaskiGoruyor, "
            #       "b.crm_BootcampBitirdi, b.crm_OnlineITKursu, b.crm_ITTecrube, b.crm_ProjeDahil, "
            #       "b.crm_CalismakIstedigi, b.crm_NedenKatilmakIstiyor, b.crm_MotivasyonunNedir "
            #       "FROM form1_application b "
            #       "INNER JOIN form1_applicant a ON b.crm_ApplicantID = a.crm_ID "
            #       "ORDER BY b.crm_Timestamp ASC")

            applications = myf.execute_read_query(cnf.open_conn(), q1)

            # Rebuilds the list based on the data type of the cells.
            self.active_list = myf.remake_it_with_types(applications)

            myf.write2table(self.form_applications, self.headers, self.active_list)

            # Fill the combobox for filtering while loading
            self.form_applications.comboBoxFilterOptions.clear()
            self.filtering_list = list(self.active_list)
            self.filtering_column = 2
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_applications.comboBoxFilterOptions.addItems(items)
        except ConnectionError as ce:
            print(f"Connection error occurred: {ce}")
            # Relevant logging or error reporting can be done
        except (AttributeError, TypeError) as at:
            print(f"Data processing error: {at}")
        except Exception as e:
            raise Exception(f"Error occurred in get_all_applications method: {e}")

        # same_applicants = self.find_same_application(all_vit_list[1:], self.form_applications.comboBoxPreviousApplications.currentText())
        # double_applicants.extend(same_applicants)
        # # ... this row (New Code)
        #
        # if len(double_applicants) > 1:  # If the double_applicants variable is not empty!
        #     # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
        #     # -3 row down-
        #     self.filtering_list = double_applicants  # Assigned for filtering.
        #     self.form_applications.comboBoxFilterOptions.clear()
        #     self.form_applications.comboBoxFilterOptions.addItems(main.filter_active_options(self.filtering_list, self.filtering_column))
        # else:
        #     no_application = ['There is no double applicant!']
        #     [no_application.append('-') for i in range(len(self.filtering_list[0]) - 1)]
        #     double_applicants.append(no_application)
        #     # double_applicants.append(['There is no double applicant!', '-', '-', '-', '-', '-', '-', '-', ])
        #     # Above - one line - code works as same as active code. But active code is automated for cell amount
        # return main.write2table(self.form_applications, double_applicants)

    # # This method is for next two method
    # @staticmethod  # This method is used with next two method together
    # def app_column_checker(a_list, text, col):
    #     searched_applications = []
    #     for application in a_list[1:]:
    #         if text in application[col]:
    #             searched_applications.append(application)
    #     return searched_applications

    # def app_planned_meetings(self):
    #     planned_applications = [self.applications[0]]
    #     planned_applications.extend(self.app_column_checker(self.applications, "OK", 21))
    #
    #     if len(planned_applications) > 1:  # If the planned_applications variable is not empty!
    #         # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
    #         # -3 row down-
    #         self.filtering_list = planned_applications  # Assigned for filtering.
    #         self.form_applications.comboBoxFilterOptions.clear()
    #         self.form_applications.comboBoxFilterOptions.addItems(
    #             myf.filter_active_options(self.filtering_list, self.filtering_column))
    #     else:
    #         no_application = ['There is no planned meetings!']
    #         [no_application.append('-') for i in range(len(self.filtering_list[0]) - 1)]
    #         planned_applications.append(no_application)
    #         # planned_applications.append(['There is no planned meetings!', '-', '-', '-', '-', '-', '-', '-', ])
    #         # Above - one line - code works as same as active code. But active code is automated for cell amount
    #     return myf.write2table(self.form_applications, planned_applications)
    #
    # def app_unscheduled_meetings(self):
    #     unscheduled_applications = [self.applications[0]]
    #     unscheduled_applications.extend(self.app_column_checker(self.applications, "ATANMADI", 21))
    #
    #     if len(unscheduled_applications) > 1:  # If the unscheduled_applications variable is not empty!
    #         # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
    #         # -3 row down-
    #         self.filtering_list = unscheduled_applications  # Assigned for filtering.
    #         self.form_applications.comboBoxFilterOptions.clear()
    #         self.form_applications.comboBoxFilterOptions.addItems(
    #             myf.filter_active_options(self.filtering_list, self.filtering_column))
    #     else:
    #         no_application = ['There is no unscheduled meetings!']
    #         [no_application.append('-') for i in range(len(self.filtering_list[0]) - 1)]
    #         unscheduled_applications.append(no_application)
    #         # unscheduled_applications.append(['There is no unscheduled meetings!', '-', '-', '-', '-', '-', '-', ])
    #         # Above - one line - code works as same as active code. But active code is automated for cell amount
    #     return myf.write2table(self.form_applications, unscheduled_applications)

    # def app_duplicate_records(self):
    #     duplicate_list = [self.applications[0]]
    #
    #     # for i in range(len(self.filtering_list[1:])):
    #     #     if self.filtering_list[1:][i] not in duplicate_list:    # tekrar edilen eleman bilgisi bir kez yazilir.
    #     #         found = 0   # tekrar edilen eleman bilgisinin bir kez yazilmasina yardimci olan yapi/degisken
    #     #         for j in range(i + 1, len(self.filtering_list[1:])):
    #     #             if self.filtering_list[1:][i][2] == self.filtering_list[1:][j][2]:
    #     #                 found += 1
    #     #                 if found == 1:
    #     #                     duplicate_list.append(self.filtering_list[1:][i])
    #     #                 duplicate_list.append(self.filtering_list[1:][j])
    #
    #     same_records = self.find_same_application(self.applications[1:],
    #                                               self.form_applications.comboBoxDuplicatedApplications.currentText())
    #     duplicate_list.extend(same_records)
    #
    #     if len(duplicate_list) > 1:  # If the duplicate_list variable is not empty!
    #         # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
    #         # -3 row down-
    #         self.filtering_list = duplicate_list  # Assigned for filtering.
    #         self.form_applications.comboBoxFilterOptions.clear()
    #         self.form_applications.comboBoxFilterOptions.addItems(
    #             myf.filter_active_options(self.filtering_list, self.filtering_column))
    #     else:
    #         no_application = ['There is no double applicant!']
    #         [no_application.append('-') for i in range(len(self.filtering_list[0]) - 1)]
    #         duplicate_list.append(no_application)
    #         # duplicate_list.append(['There is no double applicant!', '-', '-', '-', '-', '-', '-', '-', ])
    #         # Above - one line - code works as same as active code. But active code is automated for cell amount
    #     return myf.write2table(self.form_applications, duplicate_list)
    #
    # # New auxiliary function for app_previous_application_check()
    # # after discussing meeting with Ibrahim abi & Omer abi on 2024.04.16 at 22:00
    #
    # def find_same_application(self, a_list, cmbboxName):
    #     duplicated = []
    #     column = 0
    #     if cmbboxName == 'Previous VIT Check by name' or cmbboxName == 'Duplicated Applications Check by name':
    #         column = 2
    #         self.filtering_column = 2
    #     elif cmbboxName == 'Previous VIT Check by mail' or cmbboxName == 'Duplicated Applications Check by mail':
    #         column = 3
    #         self.filtering_column = 3
    #     elif cmbboxName == 'Previous VIT Check by postcode' or cmbboxName == 'Duplicated Applications Check by postcode':
    #         column = 5
    #         self.filtering_column = 5
    #     # for i, row1 in enumerate(a_list):
    #     #     tekrar = 0
    #     #     for j, row2 in enumerate(a_list[i + 1:]):
    #     #         if row1[column] == row2[column]:
    #     #             if tekrar < 1:
    #     #                 duplicated.append(row1)
    #     #             duplicated.append(row2)
    #     #             tekrar += 1
    #     ####
    #     for i in range(len(a_list)):
    #         found = 0  # tekrar edilen eleman bilgisinin bir kez yazilmasina yardimci olan yapi/degisken
    #         if a_list[i] not in duplicated:  # tekrar edilen eleman bilgisi bir kez yazilir.
    #             for j in range(i + 1, len(a_list)):
    #                 if a_list[i][column].lower() == a_list[j][column].lower():
    #                     found += 1
    #                     if found == 1:
    #                         duplicated.append(a_list[i])
    #                     duplicated.append(a_list[j])
    #     return duplicated

    # !!! Explanations for program user, not for developers: This method(below method with above method's help)
    # finds users that apply with the same email or the same name before

    # Bu method icin (asagidaki) istenen seyin cok gerekli olup olmadigi konusunda emin degilim. Farkli kayitlar
    # isminde bir method yazacaksak bence bu soyle calismaliydi. Misal bir kisi (adi ayni olacak, sonucta resmi ve
    # hukuki bir kayit durumu soz konusu.) birinci mail adresiyle kayit olmus. Ama emin olamamis diger bir mail
    # adresiyle bir kez daha kaydolmus. Yani bence yazacagimiz method bu kisileri alip getirmeliydi... (Uygulamada bu
    # ne kadar gerekli, isinize yarar, bilmiyorum tabi ki)
    # def app_differential_registrations(self):
    #     # Burasi komple degisecek
    #     # self.filtering_list = self.applications    # I added it for filtering.
    #     self.worksheet = main.connection_hub('credentials/key.json', 'VIT1-2', 'Sayfa1')
    #     self.VIT1 = self.worksheet.get_all_values()
    #     self.worksheet = main.connection_hub('credentials/key.json', 'VIT2-2', 'Sayfa1')
    #     self.VIT2 = self.worksheet.get_all_values()
    #
    #     differential_users = [self.VIT1[0]]
    #     for user1 in self.VIT1[1:]:
    #         found = False
    #         for user2 in self.VIT2[1:]:
    #             if user1[2] in user2[2]:
    #                 found = True
    #                 break
    #         if not found:
    #             differential_users.append(user1)
    #
    #     for user2 in self.VIT2:
    #         found = False
    #         for user1 in self.VIT1:
    #             if user2[2] in user1[2]:
    #                 found = True
    #                 break
    #         if not found:
    #             differential_users.append(user2)
    #
    #     if len(differential_users) > 1:  # If the searched_people variable is not empty!
    #         # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
    #         # -3 row down-
    #         self.filtering_list = differential_users  # Assigned for filtering.
    #         self.form_applications.comboBoxFilterOptions.clear()
    #         self.form_applications.comboBoxFilterOptions.addItems(
    #             myf.filter_active_options(self.filtering_list, self.filtering_column))
    #     else:
    #         no_application = ['There is no differential applicant!']
    #         [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
    #         differential_users.append(no_application)
    #         # differential_users.append(['There is no differential applicant!', '-', '-', '-', '-', '-', '-', '-', ])
    #         # Above - one line - code works as same as active code. But active code is automated for cell amount
    #     return myf.write2table(self.form_applications, differential_users)
    #
    # def app_filter_applications(self):
    #     filtered_unique_applications = [self.applications[0]]
    #     unique_names = set()
    #     for application in self.applications[1:]:
    #         if application[2].strip().lower() not in unique_names:
    #             filtered_unique_applications.append(application)
    #             unique_names.add(application[2].strip().lower())
    #
    #     if len(filtered_unique_applications) > 1:  # If the filtered_unique_applications variable is not empty!
    #         # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
    #         # -3 row down-
    #         self.filtering_list = filtered_unique_applications  # Assigned for filtering.
    #         self.form_applications.comboBoxFilterOptions.clear()
    #         self.form_applications.comboBoxFilterOptions.addItems(
    #             myf.filter_active_options(self.filtering_list, self.filtering_column))
    #     else:
    #         no_application = ['There is no application!']
    #         [no_application.append('-') for i in range(len(self.filtering_list[0]) - 1)]
    #         filtered_unique_applications.append(no_application)
    #         # filtered_unique_applications.append(['There is no application!', '-', '-', '-', '-', '-', '-', '-', ])
    #         # Above - one line - code works as same as active code. But active code is automated for cell amount
    #     return myf.write2table(self.form_applications, filtered_unique_applications)

    def back_menu(self):
        try:
            if self.current_user[2] == "admin":
                from admin_menu import AdminMenuPage
                self.hide()
                self.menu_admin = AdminMenuPage(self.current_user)
                self.menu_admin.show()
            else:
                from menu import UserMenuPage
                self.hide()
                self.menu_user = UserMenuPage(self.current_user)
                self.menu_user.show()
        except Exception as e:
            raise Exception(f"Error occurred in back_menu method: {e}")

    def app_exit(self):
        try:
            self.close()
        except Exception as e:
            raise Exception(f"Error occurred in app_exit method: {e}")

    # Search settings for ApplicationsPage
    def search_application(self):
        try:
            myf.normalise_combo_boxes([None, self.form_applications.comboBoxFilterOptions])

            # If there is active_list, update filtering_list
            if self.active_list:
                self.filtering_list = list(self.active_list)  # Assign the list for filtering.

            # Get text in search field
            searched_text = self.form_applications.lineEditSearch.text()

            # Get results
            self.filtering_list = myf.search(self.filtering_list, self.headers, self.filtering_column, searched_text)

            # Write the results to the tableWidget
            myf.write2table(self.form_applications, self.headers, self.filtering_list)

            # Fill the combobox for filtering after every single search
            if self.active_list:
                self.filtering_list = list(self.active_list)
                items = myf.filter_active_options(self.filtering_list, self.filtering_column)
                self.form_applications.comboBoxFilterOptions.addItems(items)

        except (AttributeError, TypeError) as e:
            print(f"Data processing error in search_application method: {e}")
            # Logging or notification to the user can be made for data processing errors

        except Exception as e:
            print(f"An unexpected error occurred in search_application method: {e}")
            # A general catch can be made for unknown errors

    # Filter settings for ApplicationsPage
    def filter_table(self):
        try:
            self.form_applications.lineEditSearch.clear()  # clear the search box
            myf.filter_table(self.form_applications, self.headers, self.filtering_list, self.filtering_column)
        except Exception as e:
            raise Exception(f"Error in filter_table method: {e}")



    # .....................................................................................................................#
    # ............................................ PRESENTATION CODES START ...............................................#
    # .....................................................................................................................#

    # This code is written to make the contents appear briefly when hovering over the cell.
    def on_cell_entered(self, row, column):
        try:
            myf.on_cell_entered_f(self.form_applications, row, column)
        except Exception as e:
            raise Exception(f"Error in on_cell_entered method: {e}")

    # This code is for cell clicking
    # If you want to show a persistent tooltip with the cell text. You need to use this code and its function.
    def on_cell_clicked(self, row, column):
        try:
            myf.on_cell_clicked_f(self.form_applications, row, column)
        except Exception as e:
            raise Exception(f"Error in on_cell_clicked method: {e}")

    # This code is for header clicking. This method sorts the data based on the column that was clicked
    def on_header_clicked(self, logical_index):
        # Get the current sort order for the clicked column
        current_order = self.sort_order.get(logical_index, None)

        # Toggle between ascending and descending order
        if current_order == Qt.SortOrder.AscendingOrder:
            new_order = Qt.SortOrder.DescendingOrder
        else:
            new_order = Qt.SortOrder.AscendingOrder

        # Update the sort order dictionary
        self.sort_order[logical_index] = new_order

        # Sort the table based on the clicked column and the new sort order
        self.form_applications.tableWidget.sortItems(logical_index, order=new_order)

    # This method is for header double-clicking.
    # Activity code to offer new filtering options when you click on the titles
    def on_header_double_clicked(self, logical_index):
        try:
            # Check that filtering list is not empty and is of list type
            if not self.filtering_list or not isinstance(self.filtering_list, list):
                print("Filtering list is empty or not initialized")
                return

            # Check if logical_index is within the bounds of the list
            if logical_index >= len(self.filtering_list[0]):
                print(f"Invalid logical_index: {logical_index}")
                return

            # Get the value at the specified logical_index
            value = self.filtering_list[0][logical_index]
            # print(f"Value at index {logical_index}: {value}, Type: {type(value)}")

            # Check if value is None and not string
            if value is None:
                print(f"Value at index {logical_index} is None")
                return

            self.form_applications.comboBoxFilterOptions.clear()
            self.filtering_column = logical_index
            self.form_applications.comboBoxFilterOptions.setPlaceholderText("Filter Area")
            items = myf.filter_active_options(self.filtering_list, logical_index)
            # print('Filtered items: ', items)
            self.form_applications.comboBoxFilterOptions.addItems(items)
            myf.write2table(self.form_applications, self.headers, self.active_list)
            self.form_applications.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)

        except Exception as e:
            raise Exception(f"Error occurred in on_header_double_clicked method: {e}")

# ........................................... Presentation Codes END ..................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = ApplicationsPage(['a', '$2b$12$U67LNgs5U7xNND9PYczCZeVtQl/Hhn6vxACCOxNpmSRjyD2AvKsS2', 'admin', 'Fatih', 'BUYUKAKCALI'])
    main_window.show()
    app.exec()
