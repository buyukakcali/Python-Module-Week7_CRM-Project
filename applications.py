from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QApplication, QToolTip

import main
from UI_Files.applications_ui import Ui_FormApplications


class ApplicationsPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.applications = None
        self.filtering_list = None  # This is active nested list, it changes on that you click to the buttons to buttons
        self.current_user = current_user  # Variable name is absolutely perfect for why it is here
        self.sort_order = {}  # Dictionary to keep track of sort order for each column

        self.worksheet = None
        self.VIT1 = None
        self.VIT2 = None
        self.filtering_column = 2
        self.menu_user = None
        self.menu_admin = None

        self.form_applications = Ui_FormApplications()
        self.form_applications.setupUi(self)

        self.form_applications.comboBoxFilterOptions.setPlaceholderText("Filtreleme Alani")
        self.form_applications.comboBoxPreviousApplications.setPlaceholderText("Previous VIT Check by ...")
        self.form_applications.comboBoxPreviousApplications.addItems(['Previous VIT Check by name', 'Previous VIT Check by mail', 'Previous VIT Check by postcode'])
        self.form_applications.comboBoxDuplicatedApplications.setPlaceholderText("Duplicated Applications Check by ...")
        self.form_applications.comboBoxDuplicatedApplications.addItems(['Duplicated Applications Check by name', 'Duplicated Applications Check by mail', 'Duplicated Applications Check by postcode'])

        self.headers = [
            "Zaman damgası", "Başvuru dönemi", "Adınız", "Soyadınız", "Mail adresiniz", "Telefon numaranız",
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
            "Aşağıya bu projeye katılmak veya IT sektöründe kariyer yapmak için sizi harekete geçiren motivasyondan \n"
            "bahseder misiniz?"
        ]

        # This code updates the tableWidget headers
        main.write2table(self.form_applications, self.headers, [])

        self.form_applications.lineEditSearch.returnPressed.connect(self.app_search)
        self.form_applications.lineEditSearch.textEdited.connect(self.app_search_live)
        self.form_applications.pushButtonAllApplications.clicked.connect(self.app_last_period_applications)
        self.form_applications.comboBoxPreviousApplications.currentIndexChanged.connect(self.app_all_applications)
        self.form_applications.pushButtonPlannedMeetings.clicked.connect(self.app_planned_meetings)
        self.form_applications.pushButtonUnscheduledMeeting.clicked.connect(self.app_unscheduled_meetings)
        self.form_applications.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
        self.form_applications.comboBoxDuplicatedApplications.currentIndexChanged.connect(self.app_duplicate_records)
        self.form_applications.pushButtonDifferentialRegistrations.clicked.connect(self.app_differential_registrations)
        self.form_applications.pushButtonFilterApplications.clicked.connect(self.app_filter_applications)
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
        self.form_applications.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.on_header_double_clicked)

        # This code enables mouse tracking on tableWidget. It is needed for all mouse activity options above!
        self.form_applications.tableWidget.setMouseTracking(True)

    def filter_table(self):
        filtered_data = []
        selected_item = self.form_applications.comboBoxFilterOptions.currentText()

        for row in self.filtering_list:
            if row[self.filtering_column] == selected_item:
                filtered_data.append(row)

        if len(filtered_data) > 0:
            pass
        else:
            no_mentee = ['Nothing found for filtering!']
            [no_mentee.append('-') for i in range(len(self.headers) - 1)]
            filtered_data.append(no_mentee)
            # filtered_data.append(['Nothing found for filtering!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, self.headers, filtered_data)

    def app_search(self):
        # If the search field data changes, update self.filtering_list with the entire list
        if self.applications:
            self.filtering_list = list(self.applications)  # Assigned for filtering.

        if self.filtering_list:
            searched_applications = []
            for application in self.filtering_list:
                if (self.form_applications.lineEditSearch.text().strip().lower() in application[self.filtering_column].strip().lower()
                        and self.form_applications.lineEditSearch.text().strip().lower() != ''):
                    searched_applications.append(application)

            # Make empty the search area
            self.form_applications.lineEditSearch.setText('')

            if len(searched_applications) > 0:  # If the searched_people variable is not empty!
                # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
                # -3 row down-
                self.filtering_list = searched_applications  # Assigned for filtering.
                self.form_applications.comboBoxFilterOptions.clear()
                self.form_applications.comboBoxFilterOptions.addItems(
                    main.filter_active_options(self.filtering_list, self.filtering_column))
            else:
                self.form_applications.comboBoxFilterOptions.clear()  # clears the combobox
                no_application = ['Nothing Found!']
                [no_application.append('-') for i in range(len(self.headers) - 1)]
                searched_applications.append(no_application)
                self.filtering_list = searched_applications
                # searched_applications.append(['No User or Mentor Found!', '-', '-', '-', '-', '-', '-', '-', ])
                # Above - one line - code works as same as active code. But active code is automated for cell amount
            return main.write2table(self.form_applications, self.headers, self.filtering_list)

    # Search textbox's search method that searches as letters are typed
    def app_search_live(self):
        # If the search field data changes, update self.filtering_list with the entire list
        if self.applications:
            self.filtering_list = list(self.applications)   # Assigned for filtering.

        if self.filtering_list:
            searched_applications = []
            for application in self.filtering_list:
                if (self.form_applications.lineEditSearch.text().strip().lower() in application[self.filtering_column].strip().lower()
                        and self.form_applications.lineEditSearch.text().strip().lower() != ''):
                    searched_applications.append(application)

            if len(searched_applications) > 0:  # If the searched_people variable is not empty!
                # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
                # -3 row down-
                self.filtering_list = searched_applications  # Assigned for filtering.
                self.form_applications.comboBoxFilterOptions.clear()
                self.form_applications.comboBoxFilterOptions.addItems(main.filter_active_options(self.filtering_list, self.filtering_column))
            else:
                self.form_applications.comboBoxFilterOptions.clear()    # clears the combobox
                no_application = ['Nothing Found!']
                [no_application.append('-') for i in range(len(self.headers) - 1)]
                searched_applications.append(no_application)
                self.filtering_list = searched_applications
                # searched_applications.append(['No User or Mentor Found!', '-', '-', '-', '-', '-', '-', '-', ])
                # Above - one line - code works as same as active code. But active code is automated for cell amount
            return main.write2table(self.form_applications, self.headers, self.filtering_list)

    def app_last_period_applications(self):
        # This query returns only the most recent applications
        q1 = ("SELECT "
              "b.ZamanDamgasi, b.BasvuruDonemi, a.Ad, a.Soyad, a.Email, a.Telefon, a.PostaKodu, a.YasadiginizEyalet, "
              "b.SuAnkiDurum, b.ITPHEgitimKatilmak, b.EkonomikDurum, b.DilKursunaDevam, b.IngilizceSeviye, "
              "b.HollandacaSeviye, b.BaskiGoruyor, b.BootcampBitirdi, b.OnlineITKursu, b.ITTecrube, b.ProjeDahil, "
              "b.CalismakIstedigi, b.NedenKatilmakIstiyor, b.MotivasyonunNedir "
              "FROM form_basvuru b "
              "INNER JOIN form_basvuran a ON b.BasvuranID = a.ID "
              "WHERE b.BasvuruDonemi = %s "
              "ORDER BY b.ZamanDamgasi ASC")

        applications = main.execute_read_query(main.open_conn(), q1, (main.last_period,))

        # Rebuilds the list based on the data type of the cells.
        self.applications = main.remake_it_with_types(applications)

        # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
        # -3 row down-
        self.filtering_list = list(self.applications)  # Assigned for filtering.
        self.form_applications.comboBoxFilterOptions.clear()
        self.form_applications.comboBoxFilterOptions.addItems(main.filter_active_options(self.filtering_list, self.filtering_column))

        main.write2table(self.form_applications, self.headers, self.applications)

    def app_all_applications(self):
        # This query returns only the most recent applications
        q1 = ("SELECT "
              "b.ZamanDamgasi, b.BasvuruDonemi, a.Ad, a.Soyad, a.Email, a.Telefon, a.PostaKodu, a.YasadiginizEyalet, "
              "b.SuAnkiDurum, b.ITPHEgitimKatilmak, b.EkonomikDurum, b.DilKursunaDevam, b.IngilizceSeviye, "
              "b.HollandacaSeviye, b.BaskiGoruyor, b.BootcampBitirdi, b.OnlineITKursu, b.ITTecrube, b.ProjeDahil, "
              "b.CalismakIstedigi, b.NedenKatilmakIstiyor, b.MotivasyonunNedir "
              "FROM form_basvuru b "
              "INNER JOIN form_basvuran a ON b.BasvuranID = a.ID "
              "ORDER BY b.ZamanDamgasi ASC"
              )

        applications = main.execute_read_query(main.open_conn(), q1)

        # Rebuilds the list based on the data type of the cells.
        self.applications = main.remake_it_with_types(applications)

        # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
        # -3 row down-
        self.filtering_list = list(self.applications)  # Assigned for filtering.
        self.form_applications.comboBoxFilterOptions.clear()
        self.form_applications.comboBoxFilterOptions.addItems(
            main.filter_active_options(self.filtering_list, self.filtering_column))

        main.write2table(self.form_applications, self.headers, self.applications)

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

    # This method is for next two method
    @staticmethod  # This method is used with next two method together
    def app_column_checker(a_list, text, col):
        searched_applications = []
        for application in a_list[1:]:
            if text in application[col]:
                searched_applications.append(application)
        return searched_applications

    def app_planned_meetings(self):
        planned_applications = [self.applications[0]]
        planned_applications.extend(self.app_column_checker(self.applications, "OK", 21))

        if len(planned_applications) > 1:  # If the planned_applications variable is not empty!
            # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
            # -3 row down-
            self.filtering_list = planned_applications  # Assigned for filtering.
            self.form_applications.comboBoxFilterOptions.clear()
            self.form_applications.comboBoxFilterOptions.addItems(main.filter_active_options(self.filtering_list, self.filtering_column))
        else:
            no_application = ['There is no planned meetings!']
            [no_application.append('-') for i in range(len(self.filtering_list[0]) - 1)]
            planned_applications.append(no_application)
            # planned_applications.append(['There is no planned meetings!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, planned_applications)

    def app_unscheduled_meetings(self):
        unscheduled_applications = [self.applications[0]]
        unscheduled_applications.extend(self.app_column_checker(self.applications, "ATANMADI", 21))

        if len(unscheduled_applications) > 1:  # If the unscheduled_applications variable is not empty!
            # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
            # -3 row down-
            self.filtering_list = unscheduled_applications  # Assigned for filtering.
            self.form_applications.comboBoxFilterOptions.clear()
            self.form_applications.comboBoxFilterOptions.addItems(main.filter_active_options(self.filtering_list, self.filtering_column))
        else:
            no_application = ['There is no unscheduled meetings!']
            [no_application.append('-') for i in range(len(self.filtering_list[0]) - 1)]
            unscheduled_applications.append(no_application)
            # unscheduled_applications.append(['There is no unscheduled meetings!', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, unscheduled_applications)

    def app_duplicate_records(self):
        duplicate_list = [self.applications[0]]

        # for i in range(len(self.filtering_list[1:])):
        #     if self.filtering_list[1:][i] not in duplicate_list:    # tekrar edilen eleman bilgisi bir kez yazilir.
        #         found = 0   # tekrar edilen eleman bilgisinin bir kez yazilmasina yardimci olan yapi/degisken
        #         for j in range(i + 1, len(self.filtering_list[1:])):
        #             if self.filtering_list[1:][i][2] == self.filtering_list[1:][j][2]:
        #                 found += 1
        #                 if found == 1:
        #                     duplicate_list.append(self.filtering_list[1:][i])
        #                 duplicate_list.append(self.filtering_list[1:][j])

        same_records = self.find_same_application(self.applications[1:],
                                                     self.form_applications.comboBoxDuplicatedApplications.currentText())
        duplicate_list.extend(same_records)

        if len(duplicate_list) > 1:  # If the duplicate_list variable is not empty!
            # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
            # -3 row down-
            self.filtering_list = duplicate_list  # Assigned for filtering.
            self.form_applications.comboBoxFilterOptions.clear()
            self.form_applications.comboBoxFilterOptions.addItems(main.filter_active_options(self.filtering_list, self.filtering_column))
        else:
            no_application = ['There is no double applicant!']
            [no_application.append('-') for i in range(len(self.filtering_list[0]) - 1)]
            duplicate_list.append(no_application)
            # duplicate_list.append(['There is no double applicant!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, duplicate_list)

    # New auxiliary function for app_previous_application_check()
    # after discussing meeting with Ibrahim abi & Omer abi on 2024.04.16 at 22:00

    def find_same_application(self, a_list, cmbboxName):
        duplicated = []
        column = 0
        if cmbboxName == 'Previous VIT Check by name' or cmbboxName == 'Duplicated Applications Check by name':
            column = 2
            self.filtering_column = 2
        elif cmbboxName == 'Previous VIT Check by mail' or cmbboxName == 'Duplicated Applications Check by mail':
            column = 3
            self.filtering_column = 3
        elif cmbboxName == 'Previous VIT Check by postcode' or cmbboxName == 'Duplicated Applications Check by postcode':
            column = 5
            self.filtering_column = 5
        # for i, row1 in enumerate(a_list):
        #     tekrar = 0
        #     for j, row2 in enumerate(a_list[i + 1:]):
        #         if row1[column] == row2[column]:
        #             if tekrar < 1:
        #                 duplicated.append(row1)
        #             duplicated.append(row2)
        #             tekrar += 1
        ####
        for i in range(len(a_list)):
            found = 0   # tekrar edilen eleman bilgisinin bir kez yazilmasina yardimci olan yapi/degisken
            if a_list[i] not in duplicated:    # tekrar edilen eleman bilgisi bir kez yazilir.
                for j in range(i + 1, len(a_list)):
                    if a_list[i][column].lower() == a_list[j][column].lower():
                        found += 1
                        if found == 1:
                            duplicated.append(a_list[i])
                        duplicated.append(a_list[j])
        return duplicated

    # !!! Explanations for program user, not for developers: This method(below method with above method's help)
    # finds users that apply with the same email or the same name before

    # Bu method icin (asagidaki) istenen seyin cok gerekli olup olmadigi konusunda emin degilim. Farkli kayitlar
    # isminde bir method yazacaksak bence bu soyle calismaliydi. Misal bir kisi (adi ayni olacak, sonucta resmi ve
    # hukuki bir kayit durumu soz konusu.) birinci mail adresiyle kayit olmus. Ama emin olamamis diger bir mail
    # adresiyle bir kez daha kaydolmus. Yani bence yazacagimiz method bu kisileri alip getirmeliydi... (Uygulamada bu
    # ne kadar gerekli, isinize yarar, bilmiyorum tabi ki)
    def app_differential_registrations(self):
        # Burasi komple degisecek
        # self.filtering_list = self.applications    # I added it for filtering.
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT1-2', 'Sayfa1')
        self.VIT1 = self.worksheet.get_all_values()
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT2-2', 'Sayfa1')
        self.VIT2 = self.worksheet.get_all_values()

        differential_users = [self.VIT1[0]]
        for user1 in self.VIT1[1:]:
            found = False
            for user2 in self.VIT2[1:]:
                if user1[2] in user2[2]:
                    found = True
                    break
            if not found:
                differential_users.append(user1)

        for user2 in self.VIT2:
            found = False
            for user1 in self.VIT1:
                if user2[2] in user1[2]:
                    found = True
                    break
            if not found:
                differential_users.append(user2)

        if len(differential_users) > 1:  # If the searched_people variable is not empty!
            # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
            # -3 row down-
            self.filtering_list = differential_users  # Assigned for filtering.
            self.form_applications.comboBoxFilterOptions.clear()
            self.form_applications.comboBoxFilterOptions.addItems(main.filter_active_options(self.filtering_list, self.filtering_column))
        else:
            no_application = ['There is no differential applicant!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            differential_users.append(no_application)
            # differential_users.append(['There is no differential applicant!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, differential_users)

    def app_filter_applications(self):
        filtered_unique_applications = [self.applications[0]]
        unique_names = set()
        for application in self.applications[1:]:
            if application[2].strip().lower() not in unique_names:
                filtered_unique_applications.append(application)
                unique_names.add(application[2].strip().lower())

        if len(filtered_unique_applications) > 1:  # If the filtered_unique_applications variable is not empty!
            # The result obtained with the help of the method is printed into the comboBoxFilterOptions for filtering.
            # -3 row down-
            self.filtering_list = filtered_unique_applications  # Assigned for filtering.
            self.form_applications.comboBoxFilterOptions.clear()
            self.form_applications.comboBoxFilterOptions.addItems(main.filter_active_options(self.filtering_list, self.filtering_column))
        else:
            no_application = ['There is no application!']
            [no_application.append('-') for i in range(len(self.filtering_list[0]) - 1)]
            filtered_unique_applications.append(no_application)
            # filtered_unique_applications.append(['There is no application!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, filtered_unique_applications)

    def back_menu(self):
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

    def app_exit(self):
        self.close()

# .....................................................................................................................#
# ............................................ PRESENTATION CODES START ...............................................#
# .....................................................................................................................#

    # This code is written to make the contents appear briefly when hovering over the cell.
    def on_cell_entered(self, row, column):
        # Get the text of the cell at the specified row and column
        item_text = self.form_applications.tableWidget.item(row, column).text()

        # Show a tooltip with the cell text
        tooltip = self.form_applications.tableWidget.viewport().mapToGlobal(
            self.form_applications.tableWidget.visualItemRect(
                self.form_applications.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text)

        # This code is for cell clicking
        # If you want to show a persistent tooltip with the cell text. You need to use this code.
        # I coded it for 'on_cell_clicked' method
    def on_cell_clicked(self, row, column):
        # Get the text of the clicked cell
        item_text = self.form_applications.tableWidget.item(row, column).text()

        # Show a persistent tooltip with the cell text
        tooltip = self.form_applications.tableWidget.viewport().mapToGlobal(
            self.form_applications.tableWidget.visualItemRect(
                self.form_applications.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text, self.form_applications.tableWidget)

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

    # This code is for header double-clicking. Activity code to offer new filtering options when you click on the titles
    def on_header_double_clicked(self, logical_index):
        try:
            if self.filtering_list:
                # Checking the type of the value at the given logical_index
                value = self.filtering_list[0][logical_index]
                # print(f"Value at index {logical_index}: {value}, Type: {type(value)}")  # Debug output

                # Ensure the value is of type string
                if isinstance(value, str):
                    self.form_applications.comboBoxFilterOptions.clear()
                    self.filtering_column = logical_index
                    self.form_applications.comboBoxFilterOptions.setPlaceholderText("")
                    self.form_applications.comboBoxFilterOptions.addItems(
                        main.filter_active_options(self.filtering_list, logical_index))
                else:
                    print(
                        f"Value at index {logical_index} is not a string: {value}")  # Error output for non-string values
            else:
                print("Filtering list is empty or not initialized")
        except Exception as e:
            print(f"Error in on_header_double_clicked: {e}")  # Error output for debugging


# ........................................... Presentation Codes END ..................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = ApplicationsPage(('s', 'd', 'user'))
    main_window.show()
    app.exec()
