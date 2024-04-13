from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QApplication, QToolTip

import main
from UI_Files.applications_ui import Ui_FormApplications


class ApplicationsPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user  # Variable name is absolutely perfect for why it is here
        self.sort_order = {}  # Dictionary to keep track of sort order for each column
        self.worksheet = None
        self.VIT1 = None
        self.VIT2 = None
        self.form_applications = Ui_FormApplications()
        self.form_applications.setupUi(self)
        self.worksheet = main.connection_hub('credentials/key.json', 'Basvurular', 'Sayfa1')
        self.applications = self.worksheet.get_all_values()
        # Rebuilds the list based on the data type of the cells.
        self.applications = main.remake_it_with_types(self.applications)

        #   This is a special code list manipulation for "total applications"
        #   You can change the wanted columns for tableWidget here
        #
        #
        self.excluding_list = [x for x in range(21, 27)]  # Unwanted columns
        new_list = main.list_exclude(list(self.applications), self.excluding_list)
        self.applications = new_list
        #
        #
        #
        # This code updates the tableWidget headers
        main.write2table(self.form_applications, main.list_exclude([self.applications[0]], self.excluding_list))

        self.menu_user = None
        self.menu_admin = None

        self.form_applications.pushButtonSearch.clicked.connect(self.app_search)
        self.form_applications.pushButtonAllApplications.clicked.connect(self.app_all_applications)
        self.form_applications.pushButtonPlannedMeetings.clicked.connect(self.app_planned_meetings)
        self.form_applications.pushButtonUnscheduledMeeting.clicked.connect(self.app_unscheduled_meetings)
        self.form_applications.pushButtonPreviousVitCheck.clicked.connect(self.app_previous_application_check)
        self.form_applications.pushButtonDuplicateRegistrations.clicked.connect(self.app_duplicate_records)
        self.form_applications.pushButtonDifferentialRegistrations.clicked.connect(self.app_differential_registrations)
        self.form_applications.pushButtonFilterApplications.clicked.connect(self.app_filter_applications)
        self.form_applications.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_applications.pushButtonExit.clicked.connect(self.app_exit)

        # Activity code to offer new filtering options when you click on the titles
        # self.form_applications.tableWidget.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_applications.tableWidget.cellEntered.connect(self.on_cell_entered)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_applications.tableWidget.cellClicked.connect(self.on_cell_clicked)

        # Connect the header's sectionClicked signal to the on_header_clicked method
        self.form_applications.tableWidget.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # This code enables mouse tracking on tableWidget. It is needed for all mouse activity options above!
        self.form_applications.tableWidget.setMouseTracking(True)

    def app_search(self):
        searched_applications = [self.applications[0]]
        for application in self.applications[1:]:
            if (self.form_applications.lineEditSearch.text().strip().lower() in application[1].strip().lower()
                    and self.form_applications.lineEditSearch.text().strip().lower() != ''):
                searched_applications.append(application)

        # Make empty the search area
        self.form_applications.lineEditSearch.setText('')

        if len(searched_applications) > 1:  # If the searched_people variable is not empty!
            pass
        else:
            no_application = ['No User or Mentor Found!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            searched_applications.append(no_application)
            # searched_applications.append(['No User or Mentor Found!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, searched_applications)

    def app_all_applications(self):
        main.write2table(self.form_applications, self.applications)

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
        planned_applications.extend(self.app_column_checker(self.applications, "OK", 20))
        if len(planned_applications) > 1:  # If the planned_applications variable is not empty!
            pass
        else:
            no_application = ['There is no planned meetings!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            planned_applications.append(no_application)
            # planned_applications.append(['There is no planned meetings!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, planned_applications)

    def app_unscheduled_meetings(self):
        unscheduled_applications = [self.applications[0]]
        unscheduled_applications.extend(self.app_column_checker(self.applications, "ATANMADI", 20))
        if len(unscheduled_applications) > 1:  # If the unscheduled_applications variable is not empty!
            pass
        else:
            no_application = ['There is no unscheduled meetings!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            unscheduled_applications.append(no_application)
            # unscheduled_applications.append(['There is no unscheduled meetings!', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, unscheduled_applications)

    def app_duplicate_records(self):
        duplicate_list = [self.applications[0]]

        for i in range(len(self.applications[1:])):
            for j in range(i + 1, len(self.applications[1:])):
                if (self.applications[1:][i][1] == self.applications[1:][j][1]
                        or self.applications[1:][i][2] == self.applications[1:][j][2]):
                    duplicate_list.append(self.applications[1:][i])
                    duplicate_list.append(self.applications[1:][j])
        if len(duplicate_list) > 1:  # If the duplicate_list variable is not empty!
            pass
        else:
            no_application = ['There is no double applicant!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            duplicate_list.append(no_application)
            # duplicate_list.append(['There is no double applicant!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, duplicate_list)

    # This method will be used in next method only
    # This method finds common elements in two lists with given properties
    @staticmethod
    def find_common_elements(nested_list1, nested_list2):
        common_elements = []
        for sublist1 in nested_list1:
            for sublist2 in nested_list2:
                if (sublist1[1].strip().lower() in sublist2[1].strip().lower() or sublist2[1].strip().lower() in
                        sublist1[1].strip().lower() or sublist1[2].strip().lower() == sublist2[2].strip().lower()):
                    common_elements.append(sublist1)
                    common_elements.append(sublist2)
        return common_elements

    # !!! Explanations for program user, not for developers: This method(below method with above method's help)
    # finds users that apply with the same email or the same name before
    def app_previous_application_check(self):
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT1', 'Sayfa1')
        self.VIT1 = self.worksheet.get_all_values()
        self.VIT1 = main.list_exclude(list(self.VIT1), self.excluding_list)
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT2', 'Sayfa1')
        self.VIT2 = self.worksheet.get_all_values()
        self.VIT2 = main.list_exclude(list(self.VIT2), self.excluding_list)

        double_applicants = [self.applications[0]]  # Adding headers to the list

        double_applicants.extend(self.find_common_elements(self.VIT1[1:], self.VIT2[1:]))
        double_applicants.extend(self.find_common_elements(self.VIT1[1:], self.applications[1:]))
        double_applicants.extend(self.find_common_elements(self.VIT2[1:], self.applications[1:]))

        unique_list = []
        [unique_list.append(x) for x in double_applicants if x not in unique_list]
        double_applicants = unique_list

        # These codes(below) are my first codes. I improved new codes above later with help of chatgpt.
        #
        # for user in self.VIT1:
        #     if self.find_same(self.applications, user):
        #         double_applicants.append(user)
        #     elif self.find_same(self.VIT2, user):
        #         double_applicants.append(user)
        #     else:
        #         continue
        #
        # for user in self.VIT2:
        #     if self.find_same(self.applications, user):
        #         double_applicants.append(user)
        #
        #
        # @staticmethod
        # def find_same(a_list, element):
        #     for i in a_list:
        #         if element[1] in i[1] and element[2] in i[2]:
        #             return True
        #     else:
        #         return False

        # The code below reorders the list according to the data in the first index of the elements of the relevant
        # nested list.
        sorted_list = sorted(double_applicants, key=lambda x: x[1].lower())

        if len(sorted_list) > 1:  # If the searched_people variable is not empty!
            pass
        else:
            no_application = ['There is no double applicant!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
            sorted_list.append(no_application)
            # sorted_list.append(['No User or Mentor Found!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_applications, sorted_list)

    # Bu method icin (asagidaki) istenen seyin cok gerekli olup olmadigi konusunda emin degilim. Farkli kayitlar
    # isminde bir method yazacaksak bence bu soyle calismaliydi. Misal bir kisi (adi ayni olacak, sonucta resmi ve
    # hukuki bir kayit durumu soz konusu.) birinci mail adresiyle kayit olmus. Ama emin olamamis diger bir mail
    # adresiyle bir kez daha kaydolmus. Yani bence yazacagimiz method bu kisileri alip getirmeliydi... (Uygulamada bu
    # ne kadar gerekli, isinize yarar, bilmiyorum tabi ki)
    def app_differential_registrations(self):
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT1', 'Sayfa1')
        self.VIT1 = self.worksheet.get_all_values()
        self.worksheet = main.connection_hub('credentials/key.json', 'VIT2', 'Sayfa1')
        self.VIT2 = self.worksheet.get_all_values()

        differential_users = [self.VIT1[0]]
        for user1 in self.VIT1[1:]:
            found = False
            for user2 in self.VIT2[1:]:
                if user1[1] in user2[1]:
                    found = True
                    break
            if not found:
                differential_users.append(user1)

        for user2 in self.VIT2:
            found = False
            for user1 in self.VIT1:
                if user2[1] in user1[1]:
                    found = True
                    break
            if not found:
                differential_users.append(user2)

        if len(differential_users) > 1:  # If the searched_people variable is not empty!
            pass
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
            if application[1].strip().lower() not in unique_names:
                filtered_unique_applications.append(application)
                unique_names.add(application[1].strip().lower())
        if len(filtered_unique_applications) > 1:  # If the filtered_unique_applications variable is not empty!
            pass
        else:
            no_application = ['There is no application!']
            [no_application.append('-') for i in range(len(self.applications[0]) - 1)]
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

# ........................................... Presentation Codes END ..................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = ApplicationsPage(['s', 'd', 'user'])
    main_window.show()
    app.exec()
