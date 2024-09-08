import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QToolTip
from PyQt6.QtGui import QFont

from oauth2client.service_account import ServiceAccountCredentials

from UI_Files.candidates_ui import Ui_FormCandidates
import my_functions as myf
from my_classes import Config

class CandidatesPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user  # Variable name is absolutely perfect for why it is here
        self.sort_order = {}  # Dictionary to keep track of sort order for each column

        self.filtering_list = []
        self.active_list = None

        self.form_candidates = Ui_FormCandidates()
        self.form_candidates.setupUi(self)

        # Initial load view settings
        self.filtering_column = 10
        self.headers = ['Zaman damgası', 'Basvuru Donemi', 'Mentor Ad', 'Mentor Soyad', 'Mentor Mail', 'Aday Ad',
                        'Aday Soyad', 'Aday Mail', 'Aday IT sektör bilgisi', 'Aday yoğunluk', 'Düşünceler', 'Yorumlar'
                        ]
        myf.write2table(self.form_candidates, self.headers, [])  # This code updates the tableWidget headers
        self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Katılımcı Hakkındaki Tavsiyelere Göre Filtreleyin")

        # Connect signals to slots
        self.form_candidates.lineEditSearch.textEdited.connect(self.search_live)
        self.form_candidates.lineEditSearch.returnPressed.connect(self.search)
        self.form_candidates.pushButtonGetCandidates.clicked.connect(self.get_candidates)
        self.form_candidates.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
        self.form_candidates.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_candidates.pushButtonExit.clicked.connect(self.app_exit)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_candidates.tableWidget.cellEntered.connect(self.on_cell_entered)

        # Connect the cellClicked signal to the on_cell_clicked method
        self.form_candidates.tableWidget.cellClicked.connect(self.on_cell_clicked)

        # Connect the header's sectionClicked signal to the on_header_clicked method
        self.form_candidates.tableWidget.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # Connect the header's sectionDoubleClicked signal to the on_header_double_clicked method
        self.form_candidates.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.on_header_double_clicked)

        # This code enables mouse tracking on tableWidget. It is needed for all mouse activity options above!
        self.form_candidates.tableWidget.setMouseTracking(True)

    def search(self):
        self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Filtrelemek icin basliga cift tiklayin!")
        self.form_candidates.comboBoxFilterOptions.clear()

        # If the search field data changes, update self.filtering_list with the entire list
        if self.active_list:
            self.filtering_list = list(self.active_list)  # Assigned for filtering.

        if self.filtering_list:
            searched_things = []
            for element in self.filtering_list:
                if (self.form_candidates.lineEditSearch.text().strip().lower() in element[
                    self.filtering_column].strip().lower()
                        and self.form_candidates.lineEditSearch.text().strip().lower() != ''):
                    searched_things.append(element)
                elif self.form_candidates.lineEditSearch.text() == '':
                    searched_things = list(self.active_list)

            # Make empty the search area
            self.form_candidates.lineEditSearch.setText('')

            if len(searched_things) > 0:  # If the searched_people variable is not empty!
                self.filtering_list = searched_things  # Assigned for filtering.
                # self.form_interviews.comboBoxFilterOptions.clear()
                # self.form_interviews.comboBoxFilterOptions.addItems(
                #     main.filter_active_options(self.filtering_list, self.filtering_column))
            else:
                # self.form_interviews.comboBoxFilterOptions.clear()  # clears the combobox
                no_application = ['Nothing Found!']
                [no_application.append('-') for i in range(len(self.headers) - 1)]
                searched_things.append(no_application)
                self.filtering_list = searched_things
            return myf.write2table(self.form_candidates, self.headers, self.filtering_list)

    def search_live(self):
        self.form_candidates.comboBoxFilterOptions.setPlaceholderText("Filtrelemek icin basliga cift tiklayin!")
        self.form_candidates.comboBoxFilterOptions.clear()

        # If the search field data changes, update self.filtering_list with the entire list
        if self.active_list:
            self.filtering_list = list(self.active_list)  # Assigned for filtering.

        if self.filtering_list:
            searched_things = []
            for element in self.filtering_list:
                if (self.form_candidates.lineEditSearch.text().strip().lower() in element[
                    self.filtering_column].strip().lower()
                        and self.form_candidates.lineEditSearch.text().strip().lower() != ''):
                    searched_things.append(element)
                elif self.form_candidates.lineEditSearch.text() == '':
                    searched_things = list(self.active_list)

            # Make empty the search area
            # self.form_interviews.lineEditSearch.setText('')

            if len(searched_things) > 0:  # If the searched_people variable is not empty!
                self.filtering_list = searched_things  # Assigned for filtering.
                # self.form_interviews.comboBoxFilterOptions.clear()
                # self.form_interviews.comboBoxFilterOptions.addItems(
                #     main.filter_active_options(self.filtering_list, self.filtering_column))
            else:
                # self.form_interviews.comboBoxFilterOptions.clear()  # clears the combobox
                no_application = ['Nothing Found!']
                [no_application.append('-') for i in range(len(self.headers) - 1)]
                searched_things.append(no_application)
                self.filtering_list = searched_things
            return myf.write2table(self.form_candidates, self.headers, self.filtering_list)

    def get_candidates(self):
        try:
            cnf = Config()
            # self.disconnect_cell_entered_signal()
            # self.normalise_combobox_assigned_applicants()

            q1 = ("SELECT "
                  "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, "
                  "fa.crm_Name, fa.crm_Surname, fa.crm_Email, fe.crm_ITSkills, fe.crm_Availability, fe.crm_Recommendation, "
                  "fe.crm_Comment "
                  "FROM "
                  "form2_evaluations fe "
                  "LEFT JOIN appointments_current ac ON fe.crm_MentorMail = ac.crm_MentorMail "
                  "INNER JOIN form1_applicant fa ON fe.crm_CandidateID = fa.crm_ID "
                  "WHERE fe.crm_Period = %s "
                  "GROUP BY "
                  "fe.crm_ID, fe.crm_Timestamp, fe.crm_Period, ac.crm_MentorName, ac.crm_MentorSurname, ac.crm_MentorMail, "
                  "fa.crm_Name, fa.crm_Surname, fa.crm_Email, fe.crm_ITSkills, fe.crm_Availability, fe.crm_Recommendation, "
                  "fe.crm_Comment"
                  )

            candidates = myf.execute_read_query(cnf.open_conn(), q1, (myf.last_period(),))

            # Rebuilds the list based on the data type of the cells.
            candidates = myf.remake_it_with_types(candidates)
            self.active_list = [row[1:] for row in candidates]  # ID hariç diğer verileri ata

            self.filtering_list = list(self.active_list)  # Assigned for filtering.
            myf.write2table(self.form_candidates, self.headers, self.active_list)

            # Fill the combobox for default filtering while loading
            items = myf.filter_active_options(self.filtering_list, self.filtering_column)
            self.form_candidates.comboBoxFilterOptions.addItems(items)
        except Exception as e:
            raise Exception(f"Error in get_candidates method: ") from e

    def filter_table(self):
        try:
            filtered_data = []
            selected_item = self.form_candidates.comboBoxFilterOptions.currentText().strip()

            for row in self.filtering_list:
                if str(row[self.filtering_column]).strip().lower() == str(selected_item).strip().lower():
                        filtered_data.append(row)

            if filtered_data and len(filtered_data) > 0:
                pass
            else:
                if self.filtering_list and len(self.filtering_list[0]) > 0:
                    no_candidate = ['No User or Candidate Found!']
                    [no_candidate.append('-') for i in range(len(self.filtering_list[0]) - 1)]
                    filtered_data.append(no_candidate)
                else:
                    print("Filtering list is empty")
            return myf.write2table(self.form_candidates, self.headers, filtered_data)
        except Exception  as e:
            raise Exception(f"Error in filter_table method: ") from e

    # @property     # Ex Code! It is not in use anymore. It's still at here for educational purposes
    # def filter_options(self):
    #     option_elements = []
    #     for row in self.mentees[1:]:
    #         option_elements.append(row[self.filtering_column].strip())
    #     filter_options = list(set(option_elements))
    #     filter_options.sort()
    #     # This(two rows which are below) is an issue that is inside the code, and it is in a specific language.
    #     # It must be changed while updating the application for any other language
    #     filter_options.remove('Diger')
    #     filter_options.append('Diger')
    #     return filter_options

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
            raise Exception(f"Error in back_menu method: ") from e

    def app_exit(self):
        self.close()

    # .................................................................................................................#
    # .......................................... PRESENTATION CODES START .............................................#
    # .................................................................................................................#

    # This method is written to make the contents appear briefly when hovering over the cell.
    def on_cell_entered(self, row, column):
        try:
            # Get the text of the cell at the specified row and column
            item_text = self.form_candidates.tableWidget.item(row, column).text()

            # Show a tooltip with the cell text
            tooltip = self.form_candidates.tableWidget.viewport().mapToGlobal(
                self.form_candidates.tableWidget.visualItemRect(
                    self.form_candidates.tableWidget.item(row, column)).topLeft())
            QToolTip.setFont(QFont("SansSerif", 10))
            QToolTip.showText(tooltip, item_text)
        except Exception as e:
            raise Exception(f"Error in on_cell_entered method: ") from e

    # This method is for cell clicking
    # If you want to show a persistent tooltip with the cell text. You need to use this code.
    # I coded it for 'on_cell_clicked' method
    def on_cell_clicked(self, row, column):
        try:
            # Get the text of the clicked cell
            item_text = self.form_candidates.tableWidget.item(row, column).text()

            # Show a persistent tooltip with the cell text
            tooltip = self.form_candidates.tableWidget.viewport().mapToGlobal(
                self.form_candidates.tableWidget.visualItemRect(
                    self.form_candidates.tableWidget.item(row, column)).topLeft())
            QToolTip.setFont(QFont("SansSerif", 10))
            QToolTip.showText(tooltip, item_text, self.form_candidates.tableWidget)
        except Exception as e:
            raise Exception(f"Error in on_cell_clicked method: ") from e

    # This method is for header clicking. It sorts the data based on the column that was clicked
    def on_header_clicked(self, logical_index):
        try:
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
            self.form_candidates.tableWidget.sortItems(logical_index, order=new_order)
        except Exception as e:
            raise Exception(f"Error in on_header_clicked method: ") from e

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

            self.form_candidates.comboBoxFilterOptions.clear()
            self.filtering_column = logical_index
            self.form_candidates.comboBoxFilterOptions.setPlaceholderText("")
            items = myf.filter_active_options(self.filtering_list, logical_index)
            # print('Filtered items: ', items)
            self.form_candidates.comboBoxFilterOptions.addItems(items)
        except Exception as e:
            raise Exception(f"Error in on_header_double_clicked method: ") from e

    def disconnect_cell_entered_signal(self):
        try:
            # Disconnect the cellEntered signal to disable on_cell_entered method
            self.form_candidates.tableWidget.cellEntered.disconnect(self.on_cell_entered)
        except TypeError:
            # Eğer sinyal zaten bağlantısı kesilmişse, hata oluşur; bu hatayı yok sayarız.
            pass
        except Exception as e:
            raise Exception(f"Error in disconnect_cell_entered_signal method: ") from e

    def reenable_cell_entered_signal(self):
        try:
            # Connect the cellEntered signal to re-enable on_cell_entered method
            self.form_candidates.tableWidget.cellEntered.connect(self.on_cell_entered)
        except TypeError:
            # Eğer sinyal zaten bağlıysa, hata oluşur; bu hatayı yok sayarız.
            pass
        except Exception as e:
            raise Exception(f"Error in reenable_cell_entered_signal method: ") from e

    def enable_assign_mentor_context_menu(self):
        try:
            self.form_candidates.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.form_candidates.tableWidget.customContextMenuRequested.connect(self.show_context_menu)
        except Exception as e:
            raise Exception(f"Error in enable_assign_mentor_context_menu method: ") from e

    def disable_assign_mentor_context_menu(self):
        self.form_candidates.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        try:
            self.form_candidates.tableWidget.customContextMenuRequested.disconnect(self.show_context_menu)
        except TypeError:
            # Eğer bağlantı zaten kesilmişse, bu hatayı görmezden gel
            pass
        except Exception as e:
            raise Exception(f"Error in disable_assign_mentor_context_menu method: ") from e

    # ......................................... Presentation Codes END ................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = CandidatesPage(('a', 'b', 'admin'))
    main_window.show()
    app.exec()
