from datetime import datetime

from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget

import main
from UI_Files.interviews_ui import Ui_FormInterviews


class InterviewsPage(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user  # Variable name is absolutely perfect for why it is here
        self.sort_order = {}  # Dictionary to keep track of sort order for each column
        self.form_interviews = Ui_FormInterviews()
        self.form_interviews.setupUi(self)

        self.worksheet = main.connection_hub('credentials/key.json', 'Mulakatlar2', 'Sayfa1')
        self.interviews = self.worksheet.get_all_values()
        # Rebuilds the list based on the data type of the cells.
        self.interviews = main.remake_it_with_types(self.interviews)

        main.write2table(self.form_interviews, [self.interviews[0]])  # This code updates the tableWidget headers
        self.menu_admin = None
        self.menu_user = None

        self.form_interviews.lineEditSearch.textEdited.connect(self.search_name_live)
        self.form_interviews.lineEditSearch.returnPressed.connect(self.search_name)
        self.form_interviews.pushButtonSubmittedProjects.clicked.connect(self.get_submitted_projects)
        self.form_interviews.pushButtonProjectArrivals.clicked.connect(self.get_projects_arrivals)
        self.form_interviews.pushButtonBackMenu.clicked.connect(self.back_menu)
        self.form_interviews.pushButtonExit.clicked.connect(self.app_exit)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_interviews.tableWidget.cellEntered.connect(self.on_cell_entered)

        # Connect the cellEntered signal to the on_cell_entered method
        self.form_interviews.tableWidget.cellClicked.connect(self.on_cell_clicked)

        # Connect the header's sectionClicked signal to the on_header_clicked method
        self.form_interviews.tableWidget.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

        # This code enables mouse tracking on tableWidget. It is needed for all mouse activity options above!
        self.form_interviews.tableWidget.setMouseTracking(True)

    def search_name(self):
        searched_people = [self.interviews[0]]
        for person in self.interviews[1:]:
            # If the text in the textbox appears within one of the names in the list AND is not empty at the same time!
            if (self.form_interviews.lineEditSearch.text().lower() in str(person[1]).lower()
                    and self.form_interviews.lineEditSearch.text() != ''):
                searched_people.append(person)

        # Make empty the search area
        self.form_interviews.lineEditSearch.setText('')

        if len(searched_people) > 1:  # If the searched_people variable is not empty!
            pass
        else:
            no_user = ['No User Found!']
            [no_user.append('-') for i in range(len(self.interviews[0]) - 1)]
            searched_people.append(no_user)
            # searched_people.append(['No user found!', '-', '-'])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_interviews, searched_people)

    def search_name_live(self):
        searched_people = [self.interviews[0]]
        for person in self.interviews[1:]:
            # If the text in the textbox appears within one of the names in the list AND is not empty at the same time!
            if (self.form_interviews.lineEditSearch.text().lower() in str(person[1]).lower()
                    and self.form_interviews.lineEditSearch.text() != ''):
                searched_people.append(person)

        if len(searched_people) > 1:  # If the searched_people variable is not empty!
            pass
        else:
            no_user = ['No User Found!']
            [no_user.append('-') for i in range(len(self.interviews[0]) - 1)]
            searched_people.append(no_user)
            # searched_people.append(['No user found!', '-', '-'])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_interviews, searched_people)

    def get_submitted_projects(self):
        submitted_projects = [self.interviews[0]]
        for i in self.interviews[1:]:
            if i[2]:
                submitted_projects.append(i)

        if len(submitted_projects) > 1:  # If the submitted_projects variable is not empty!
            pass
        else:
            no_user = ['There is no submitted project!']
            [no_user.append('-') for i in range(len(self.interviews[0]) - 1)]
            submitted_projects.append(no_user)
            # submitted_projects.append(['There is no submitted project!', '-', '-', '-'])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_interviews, submitted_projects)

    def get_projects_arrivals(self):
        projects_arrivals = [self.interviews[0]]
        for i in self.interviews[1:]:
            if i[3]:
                projects_arrivals.append(i)

        if len(projects_arrivals) > 1:  # If the submitted_projects variable is not empty!
            pass
        else:
            no_user = ['There is no arrival project!']
            [no_user.append('-') for i in range(len(self.interviews[0]) - 1)]
            projects_arrivals.append(no_user)
            # projects_arrivals.append(['There is no arrival project!', '-', '-', '-', '-'])
            # Above - one line - code works as same as active code. But active code is automated for cell amount
        return main.write2table(self.form_interviews, projects_arrivals)

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
        item_text = self.form_interviews.tableWidget.item(row, column).text()

        # Show a tooltip with the cell text
        tooltip = self.form_interviews.tableWidget.viewport().mapToGlobal(
            self.form_interviews.tableWidget.visualItemRect(
                self.form_interviews.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text)

    # This code is for cell clicking
    # If you want to show a persistent tooltip with the cell text. You need to use this code.
    # I coded it for 'on_cell_clicked' method
    def on_cell_clicked(self, row, column):
        # Get the text of the clicked cell
        item_text = self.form_interviews.tableWidget.item(row, column).text()

        # Show a persistent tooltip with the cell text
        tooltip = self.form_interviews.tableWidget.viewport().mapToGlobal(
            self.form_interviews.tableWidget.visualItemRect(
                self.form_interviews.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text, self.form_interviews.tableWidget)

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
        self.form_interviews.tableWidget.sortItems(logical_index, order=new_order)


# ........................................... Presentation Codes END ..................................................#


if __name__ == "__main__":
    app = QApplication([])
    main_window = InterviewsPage(['a', 'b', 'admin'])
    main_window.show()
    app.exec()
