from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QApplication, QToolTip
from PyQt6.QtGui import QFont

import main
from UI_Files.mentors_ui import Ui_FormMentor


class MentorPage(QWidget):
    def __init__(self, current_user) -> None:
        super().__init__()
        self.current_user = current_user  # Variable name is absolutely perfect for why it is here
        self.sort_order = {}  # Dictionary to keep track of sort order for each column
        self.form_mentor = Ui_FormMentor()
        self.form_mentor.setupUi(self)

        # The number written here determines the column to be sorted in the combobox below at the app beginning.
        # However, different filtering opportunities can be obtained by double-clicking to the headers while the
        # application is running.
        self.filtering_column = 5
        self.form_mentor.comboBoxFilterOptions.setPlaceholderText("Katılımcı Hakkındaki Tavsiyelere Göre Filtreleyin")

        self.worksheet = main.connection_hub('credentials/key.json', 'Mentor2', 'Sayfa1')
        self.mentees = self.worksheet.get_all_values()
        self.mentees = main.remake_it_with_types(self.mentees)  # Rebuilds the list based on the data type of the cells.

        main.write2table(self.form_mentor, [self.mentees[0]])  # This code updates the tableWidget headers
        self.menu_user = None
        self.menu_admin = None

        self.form_mentor.lineEditSearch.textEdited.connect(self.search_live)
        self.form_mentor.lineEditSearch.returnPressed.connect(self.search)
        self.form_mentor.pushButtonGetAllApplications.clicked.connect(self.get_all_applications)
        self.form_mentor.comboBoxFilterOptions.currentIndexChanged.connect(self.filter_table)
        self.form_mentor.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_mentor.pushButtonExit.clicked.connect(self.app_exit)
        self.form_mentor.comboBoxFilterOptions.addItems(main.filter_active_options(self.mentees, self.filtering_column))

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_mentor.tableWidget.cellEntered.connect(self.on_cell_entered)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_mentor.tableWidget.cellClicked.connect(self.on_cell_clicked)

        # Connect the header's sectionClicked signal to the on_header_clicked method
        self.form_mentor.tableWidget.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # Connect the header's sectionDoubleClicked signal to the on_header_double_clicked method
        self.form_mentor.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.on_header_double_clicked)

        # This code enables mouse tracking on tableWidget. It is needed for all mouse activity options above!
        self.form_mentor.tableWidget.setMouseTracking(True)

    def search(self):
        searched_mentees = [self.mentees[0]]
        for mentee in self.mentees[1:]:
            if ((self.form_mentor.lineEditSearch.text().lower() in mentee[2].lower()
                 or self.form_mentor.lineEditSearch.text().lower() in mentee[3].lower())
                    and self.form_mentor.lineEditSearch.text().lower() != ''):
                searched_mentees.append(mentee)

        # Make empty the search area
        self.form_mentor.lineEditSearch.setText('')

        if len(searched_mentees) > 1:
            pass
        else:
            no_mentee = ['No User or Mentor Found!']
            [no_mentee.append('-') for i in range(len(self.mentees[0]) - 1)]
            searched_mentees.append(no_mentee)
            # searched_mentees.append(['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_mentor, searched_mentees)

    def search_live(self):
        searched_mentees = [self.mentees[0]]
        for mentee in self.mentees[1:]:
            if ((self.form_mentor.lineEditSearch.text().lower() in mentee[2].lower()
                 or self.form_mentor.lineEditSearch.text().lower() in mentee[3].lower())
                    and self.form_mentor.lineEditSearch.text().lower() != ''):
                searched_mentees.append(mentee)
        if len(searched_mentees) > 1:
            pass
        else:
            no_mentee = ['No User or Mentor Found!']
            [no_mentee.append('-') for i in range(len(self.mentees[0]) - 1)]
            searched_mentees.append(no_mentee)
            # searched_mentees.append(['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_mentor, searched_mentees)

    def get_all_applications(self):
        main.write2table(self.form_mentor, self.mentees)

    def filter_table(self):
        filtered_data = [self.mentees[0]]
        selected_item = self.form_mentor.comboBoxFilterOptions.currentText().strip()

        for row in self.mentees[1:]:
            if row[self.filtering_column].strip().lower() == selected_item.strip().lower():
                filtered_data.append(row)

        if len(filtered_data) > 1:
            pass
        else:
            no_mentee = ['No User or Mentor Found!']
            [no_mentee.append('-') for i in range(len(self.mentees[0]) - 1)]
            filtered_data.append(no_mentee)
            # filtered_data.append(['No User or Mentor Found.!', '-', '-', '-', '-', '-', '-', '-', ])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_mentor, filtered_data)

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

    # .................................................................................................................#
    # ........................................ PRESENTATION CODES START ...............................................#
    # .................................................................................................................#

    # This code is written to make the contents appear briefly when hovering over the cell.
    def on_cell_entered(self, row, column):
        # Get the text of the cell at the specified row and column
        item_text = self.form_mentor.tableWidget.item(row, column).text()

        # Show a tooltip with the cell text
        tooltip = self.form_mentor.tableWidget.viewport().mapToGlobal(
            self.form_mentor.tableWidget.visualItemRect(self.form_mentor.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text)

    # This code is for cell clicking
    # If you want to show a persistent tooltip with the cell text. You need to use this code.
    # I coded it for 'on_cell_clicked' method
    def on_cell_clicked(self, row, column):
        # Get the text of the clicked cell
        item_text = self.form_mentor.tableWidget.item(row, column).text()

        # Show a persistent tooltip with the cell text
        tooltip = self.form_mentor.tableWidget.viewport().mapToGlobal(
            self.form_mentor.tableWidget.visualItemRect(self.form_mentor.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text, self.form_mentor.tableWidget)

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
        self.form_mentor.tableWidget.sortItems(logical_index, order=new_order)

    # This code is for header double-clicking. Activity code to offer new filtering options when you click on the titles
    def on_header_double_clicked(self, logical_index):
        if type(self.mentees[1][logical_index]) is str:
            self.form_mentor.comboBoxFilterOptions.clear()
            self.filtering_column = logical_index
            self.form_mentor.comboBoxFilterOptions.setPlaceholderText("")
            self.form_mentor.comboBoxFilterOptions.addItems(main.filter_active_options(self.mentees, logical_index))


# ........................................... Presentation Codes END ..................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = MentorPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()
