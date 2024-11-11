import re
from datetime import datetime
import bcrypt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pytz
from PyQt6.QtCore import Qt, QSize, QObject
from PyQt6.QtGui import QFontMetrics, QFont, QColor
from PyQt6.QtWidgets import (QTableWidgetItem, QToolTip, QPushButton, QComboBox, QTableWidget, QDialog, QVBoxLayout,
                             QLabel, QHBoxLayout, QDateTimeEdit, QLineEdit, QInputDialog)

import my_classes as myc

cnf = myc.Config()


# This is the most complicated and important function, especially for styling and user-friendly interfaces
def handle_widget_styles(self_, widgets):
    """
    Changes the style of the clicked widget between given QPushButton and QComboBox widgets,
    Restores the style of the previous clicked widget.

    Additionally, it applies custom style definitions based on object type (QPushButton, QComboBox, QToolTip).

    :param widgets: List of QPushButton and QComboBox widgets to be styled
    :param self_: The form itself (the form to which the widgets belong)
    """
    last_clicked_widget = None
    last_widget_original_style = ("background-color: qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.494, y2:0, "
                                  "stop:0 rgba(71, 71, 71, 255), stop:1 rgba(255, 255, 255, 255));")

    # Style definitions for different object types
    push_button_style = """
        QPushButton {
            border-radius:15px;
            background-color:rgb(20, 135, 135);
            border:2px solid rgb(162, 0, 0);
        }
    """

    combo_box_style = """
        QComboBox {
            border-radius: 15px;
            background-color: rgb(25, 200, 200);
            color: rgb(255, 255, 255);
            padding: 1px 18px 1px 3px;
            background-color: rgb(20, 135, 135); /* QComboBox background changes on hover */
            border: 2px solid rgb(162, 0, 0);
        }

        QComboBox:placeholder {
            padding-left: 10px;
            padding-right: 10px;
        }

        QComboBox::drop-down {
            border: none;
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border-left-width: 1px;
            border-left-color: darkGray;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
        }

        QComboBox::down-arrow {
            width: 14px;
            height: 14px;
        }

        QComboBox QAbstractItemView::item {
            background-color: rgb(25, 200, 200);
            color: rgb(255, 255, 255);
        }

        QComboBox QAbstractItemView {
            border: 1px solid darkGray;
            selection-background-color: rgb(20, 135, 135);
            background-color: rgb(25, 200, 200);
            border-radius: 15px;
        }

        QComboBox:hover {
            background-color: rgb(20, 135, 135); /* QComboBox background changes on hover */
            border: 2px solid rgb(255, 80, 0); /* Adding border line with Hover */
        }

        QToolTip {
            border-radius: 15px;
            background-color: yellow; 
            color: black; 
            border: 1px solid black;
        }
    """

    global_style = """
        background-color: qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.494, y2:0, stop:0 rgba(71, 71, 71, 255), stop:1 rgba(255, 255, 255, 255));
        color: white;
        QTableWidget { background-color: rgba(0, 0, 0,0%);}
        QToolTip {
            background-color: yellow;
            color: black;
            border: 1px solid black;
        }
    """

    # Changes the style of the clicked widget
    def on_widget_clicked(clicked_widget):
        nonlocal last_clicked_widget, last_widget_original_style

        form_name = self_.objectName()

        # ---------------------------------- FORM CONTROL AREA ---------------------------------------- #
        # -- It is not connected to widget styles, when this area finishes, style codes will continue -- #

        # An area created to make specific definitions for each form or the objects on it.
        if form_name == 'FormApplications':
            # Like __init__ function:
            # -----------------------
            # If you wanna run something at the initializing of the form, add here

            if clicked_widget == self_.form_applications.pushButtonBackMenu:
                pass

            elif clicked_widget == self_.form_applications.pushButtonExit:
                pass

        elif form_name == 'FormInterviews':
            # Like __init__ function:
            # -----------------------
            # If you wanna run something at the initializing of the form, add here

            """ I detected a strange behavior in these codes. If the disable function is called, it prevents the 
                creation of the context menu, regardless of which context menu it is. Therefore, as an approach, if 
                there is a context menu to be disabled, I first disable it. Then I call what I want to activate with 
                the enable function. I think the codes used to create or disable the context menu cause this.
            """
            if clicked_widget == self_.form_interviews.pushButtonUnassignedApplicants:
                # If the applicant is determined as a candidate, it is available under the tableWidget in the form and
                # serves an informative function.
                self_.form_interviews.labelInfo1.show()
                self_.form_interviews.labelInfo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self_.form_interviews.labelInfo1.setToolTip('Shows applicants who have been assigned an interview date.'
                                                            '(First Interview)')
                self_.form_interviews.labelInfo1.setStyleSheet("""
                                    QLabel { 
                                        background-color: "#FF5733"; 
                                        color: white; 
                                        border-radius: 5px;
                                        padding: 10px; 
                                    }
                                    QToolTip { background-color: yellow; color: black; border: 1px solid black; }
                                    """)

                # Add tooltip for "Situation" column
                tooltip_text = "This column's mean:\n0: new application record\n1: applicant is invited to the first interview"
                add_tooltip_to_table_widget_header(self_.form_interviews.tableWidget, 23, tooltip_text)


            elif clicked_widget == self_.form_interviews.pushButtonAssignedApplicants:
                self_.form_interviews.labelInfo1.close()

            elif clicked_widget == self_.form_interviews.pushButtonInterviewedApplicants:
                self_.form_interviews.labelInfo1.close()

                # If the applicant is determined as a candidate, it is available under the tableWidget in the form and
                # serves an informative function.
                self_.form_interviews.labelInfo1.show()
                self_.form_interviews.labelInfo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self_.form_interviews.labelInfo1.setToolTip('Shows applicants who have been assigned as Candidates.')
                self_.form_interviews.labelInfo1.setStyleSheet("""
                    QLabel { background-color: rgb(123,104,238); color: white; border-radius : 5px; padding: 10px; }
                    QToolTip { background-color: yellow; color: black; border: 1px solid black; }
                    """)

                # Add tooltip for "Situation" column
                tooltip_text = "This column's mean:\n0: interviewed applicant\n1: record is assigned as a candidate\n2: candidate is invited to the second(project) interview"
                add_tooltip_to_table_widget_header(self_.form_interviews.tableWidget, 12, tooltip_text)


            elif clicked_widget == self_.form_interviews.pushButtonBackMenu:
                pass

            elif clicked_widget == self_.form_interviews.pushButtonExit:
                pass

            else:
                # Close labelInfo1 label.
                self_.form_interviews.labelInfo1.close()

        elif form_name == 'FormCandidates':
            # Like __init__ function:
            # -----------------------
            # If you wanna run something at the initializing of the form, add here

            if clicked_widget == self_.form_candidates.pushButtonGetCandidates:
                # If a project homework e-mail has been sent to the candidate, it is located under the table widget in
                # the form and serves an informative function.
                self_.form_candidates.labelInfo1.show()
                self_.form_candidates.labelInfo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self_.form_candidates.labelInfo1.setToolTip(
                    'It shows the candidates whose project assignment e-mail has been sent and '
                    'whose interview date has been determined.')
                self_.form_candidates.labelInfo1.setStyleSheet("""
                                                QLabel { 
                                                    background-color: orange; 
                                                    color: white; 
                                                    border-radius : 5px; 
                                                    padding: 10px;
                                                }
                                                QToolTip{background-color:yellow; color:black; border: 1px solid black;}
                                                """)

                # Add tooltip for "Situation" column
                tooltip_text = "This column's mean:\n1: record is candidate now\n2: candidate is invited to the second(project) interview"
                add_tooltip_to_table_widget_header(self_.form_candidates.tableWidget, 9, tooltip_text)

                disable_context_menu(self_.form_candidates, self_.show_context_menu_add_remove_trainees)    # disable
                enable_context_menu(self_.form_candidates, self_.show_context_menu_assign_mentor)  # then enable



            elif clicked_widget == self_.form_candidates.comboBoxProjectSubmitStatus:
                self_.form_candidates.labelInfo1.close()

                # Add tooltip for "Situation" column
                tooltip_text = "This column's mean:\n1: record is candidate now\n2: candidate is invited to the second(project) interview"
                add_tooltip_to_table_widget_header(self_.form_candidates.tableWidget, 6, tooltip_text)

                disable_context_menu(self_.form_candidates, self_.show_context_menu_assign_mentor)  # disable
                disable_context_menu(self_.form_candidates, self_.show_context_menu_add_remove_trainees)  # disable


            elif clicked_widget == self_.form_candidates.pushButtonInterviewedCandidates:
                # Add tooltip for "Situation" column
                tooltip_text = "This column's mean:\n0: interviewed candidate\n1: determined for trainee selection"  # "\n2: determined as a trainee"
                add_tooltip_to_table_widget_header(self_.form_candidates.tableWidget, 14, tooltip_text)

                # If a project homework e-mail has been sent to the candidate, it is located under the table widget in
                # the form and serves an informative function.
                self_.form_candidates.labelInfo1.show()
                self_.form_candidates.labelInfo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self_.form_candidates.labelInfo1.setToolTip('Shows records assigned as Trainees.')
                self_.form_candidates.labelInfo1.setStyleSheet("""
                                                                QLabel { 
                                                                    background-color: rgb(0, 170, 0); 
                                                                    color: white; 
                                                                    border-radius : 5px; 
                                                                    padding: 10px; 
                                                                }
                                                                QToolTip { 
                                                                    background-color: yellow; 
                                                                    color: black; 
                                                                    border: 1px solid black; 
                                                                }
                                                                """)

                disable_context_menu(self_.form_candidates, self_.show_context_menu_assign_mentor)  # first disable
                enable_context_menu(self_.form_candidates, self_.show_context_menu_add_remove_trainees)  # then enable


            elif clicked_widget == self_.form_candidates.comboBoxTrainees:
                self_.form_candidates.labelInfo1.close()

                disable_context_menu(self_.form_candidates, self_.show_context_menu_assign_mentor)  # disable
                disable_context_menu(self_.form_candidates, self_.show_context_menu_add_remove_trainees)  # disable

            elif clicked_widget == self_.form_candidates.pushButtonBackMenu:
                pass

            elif clicked_widget == self_.form_candidates.pushButtonExit:
                pass

            else:
                self_.form_candidates.labelInfo1.close()

        else:  # Else for form names. (FormManagement etc.)
            pass

    # -------------------------------- FORM CONTROL AREA FINISHES ------------------------------- #
    # You are still in the 'on_widget_clicked' sub-function

        # Restore style of previous clicked widget
        if last_clicked_widget:
            last_clicked_widget.setStyleSheet(last_widget_original_style)

        # Keep current style of clicked widget
        last_widget_original_style = clicked_widget.styleSheet()

        # Apply style based on widget type
        if isinstance(clicked_widget, QPushButton):
            clicked_widget.setStyleSheet(push_button_style)
        elif isinstance(clicked_widget, QComboBox):
            clicked_widget.setStyleSheet(combo_box_style)

        # Update clicked widget
        last_clicked_widget = clicked_widget

    # Apply global style here
    self_.setStyleSheet(global_style)

    # Connect signal to all widgets
    for widget in widgets:
        if isinstance(widget, QPushButton):
            widget.clicked.connect(lambda checked, w=widget: on_widget_clicked(w))
        elif isinstance(widget, QComboBox):
            widget.activated.connect(lambda index, w=widget: on_widget_clicked(w))

    # # Apply global style here
    # self_.setStyleSheet(global_style)


# Finds the last application period
def last_period():
    try:
        q1 = ("SELECT " + cnf.applicationTableFieldNames[3] + " " +
              "FROM " + cnf.applicationTable + " " +
              "WHERE " + cnf.applicationTableFieldNames[0] + " = " +
              "(SELECT MAX(" + cnf.applicationTableFieldNames[0] + ") " + "FROM " + cnf.applicationTable + ")")
        # q1 = "SELECT crm_Period FROM form1_application WHERE crm_ID = (SELECT MAX(crm_ID) FROM form1_application)"
        return execute_read_query(cnf.open_conn(), q1)[0][0]
    except Exception as e:
        raise Exception(f"Error occurred in last_period function: {e}")


# Search function for all modules
def search(filtering_list: list, headers: list, filtering_column: int, searched_text: str):
    try:
        if filtering_list:
            searched_data = []

            # Search and find results
            for row in filtering_list:
                if (searched_text.strip().lower() in str(row[filtering_column]).strip().lower()
                        and searched_text.strip().lower() != ''):
                    searched_data.append(row)
                elif searched_text == '':
                    searched_data = list(filtering_list)

            if len(searched_data) > 0:  # If there are any found as a result of the search
                filtering_list = searched_data  # Assign as filtering list
            else:
                default_nothing_found = ['Nothing Found!']
                [default_nothing_found.append('-') for _ in range(len(headers) - 1)]
                searched_data.append(default_nothing_found)
                filtering_list = searched_data
        return filtering_list
    except Exception as e:
        raise Exception(f"Error occurred in search function: {e}")


# Function used to write data to QTableWidget objects
def write2table(form, headers: list, a_list: list):
    try:
        table_widget = form.tableWidget
        table_widget.clearContents()  # Clear table
        table_widget.setColumnCount(len(headers))  # Add title to table
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(a_list))  # Fill in the table

        for i, row in enumerate(a_list):
            for j, col in enumerate(row):
                if isinstance(col, datetime):
                    item = str(col).strip()  # with strip() method, we make maintenance to the data.
                    item = convert_server_time_to_local(item)
                    col = datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
                    item = QTableWidgetItem(col.strftime('%Y-%m-%d %H:%M:%S'))
                    item.setData(Qt.ItemDataRole.UserRole, col)  # Store the datetime object
                else:
                    item = QTableWidgetItem(str(col))
                    if str(col).isdigit():
                        text = str(col)
                        item = myc.NumericItem(
                            text)  # An example of a tableWidget class defined at the top of this page
                    item.setData(Qt.ItemDataRole.UserRole, col)
                table_widget.setItem(i, j, item)
                resize_columns(table_widget)
        return True
    except Exception as e:
        raise Exception(f"Error occurred in write2table function: {e}")


# Shows dialog what you want
def set_info_dialog(self_, header: str, message_text: str):
    dialog = QDialog(self_)
    dialog.setWindowTitle(header)

    # Make style settings similar to QToolTip view
    dialog.setStyleSheet("""
            QDialog {
                background-color: yellow;
                border: 1px solid black;
            }
            
            QLabel {
                color: black;
                background-color: rgb(0, 0, 0, 0);
                font-size: 14px;
            }
            
            QPushButton:hover{
                background-color: rgb(20, 135, 135);
                border: 2px solid rgb(255, 80, 0);
            }
            
            QToolTip {
                background-color: yellow;
                color: black;
                border: 1px solid black;
            }
        """)
    layout = QVBoxLayout(dialog)

    # Add information message
    info_label = QLabel(message_text)
    layout.addWidget(info_label)

    # Set maximum width to limit the width of the close button
    close_button = QPushButton("Close")
    close_button.setMaximumWidth(150)  # We limit the maximum width to 150 pixels

    # noinspection PyUnresolvedReferences
    close_button.clicked.connect(dialog.close)

    # Create a QHBoxLayout to center the button
    button_layout = QHBoxLayout()
    button_layout.addStretch()  # Adds space to the left
    button_layout.addWidget(close_button)  # Centers the button
    button_layout.addStretch()  # Adds space to the right
    layout.addLayout(button_layout)  # Add button_layout to main layout

    dialog.setLayout(layout)
    dialog.exec()


# It is only used within the write2table function and ensures that all tables appear properly.
def resize_columns(table_widget: QTableWidget):
    try:
        # Automatically adjust column widths according to content: this also controls headers: Alternative code
        table_widget.resizeColumnsToContents()

        # It just adjusts the column width based on the content. headers are ignored!
        # resize_columns_by_content_only(table_widget)
    except Exception as e:
        raise Exception(f"Error occurred in resize_columns function: {e}")


# Makes the tableWidget (i.e. data) appear properly based on the content only (header is ignored)
def resize_columns_by_content_only(table_widget: QTableWidget):
    try:
        # Get number of columns
        column_count = table_widget.columnCount()
        row_count = table_widget.rowCount()

        # Use QFontMetrics to calculate text width with current font
        font_metrics = QFontMetrics(table_widget.font())

        # Calculate the width of each column
        for col in range(column_count):
            max_width = 85  # Set width to 85 initially
            for row in range(row_count):
                # Get the contents of each cell
                item = table_widget.item(row, col)
                if item:
                    # Get text in cell and calculate its width
                    text = item.text()
                    text_width = font_metrics.horizontalAdvance(text)
                    max_width = max(max_width, text_width)

            # Set the column width to the longest text, we add +10 to leave some space
            table_widget.setColumnWidth(col, max_width + 10)
    except Exception as e:
        raise Exception(f"Error occurred in resize_columns_by_content_only function: {e}")


# Function that provides a neat appearance when opening context menus
def auto_resize_dialog_window_for_table(dialog: QDialog, table_widget: QTableWidget):
    try:
        # Get number of columns and rows
        column_count = table_widget.columnCount()
        row_count = table_widget.rowCount()

        # Use QFontMetrics to calculate text width with current font
        font_metrics = QFontMetrics(table_widget.font())

        # To keep the total width
        total_width = 0
        total_height = 0

        # Calculate the width of each column
        for col in range(column_count):
            max_width = 0  # Set width to 0 initially

            # Calculate header width
            header_text = table_widget.horizontalHeaderItem(col).text()
            header_width = font_metrics.horizontalAdvance(header_text)
            max_width = max(max_width, header_width)

            # Calculate width of Interview Datetime data
            item = table_widget.item(0, 0)
            if item:
                # Get text in cell and calculate its width
                text = item.text()
                text_width = font_metrics.horizontalAdvance(text)
                max_width = max(max_width, text_width)

            # Set the column width to the longest text, we add +10 to leave some space
            table_widget.setColumnWidth(col, max_width + 10)
            total_width += max_width + 13

        # Calculate row height (default height for each row)
        for row in range(row_count):
            total_height += table_widget.rowHeight(row)

        # Add header height
        total_height += table_widget.horizontalHeader().height()

        # Adjust window width and height
        dialog.setFixedSize(QSize(total_width + 20, total_height + 70))
    except Exception as e:
        raise Exception(f"Error occurred in auto_resize_window_for_table function: {e}")


# It is a function that returns a new copy of the data retrieved from the database in the correct data type.
# Not required for currently available data
def remake_it_with_types(a_list: list):
    try:
        n_list = []
        n_row = []
        for i, row in enumerate(a_list):
            for j, col in enumerate(row):
                try:
                    item = str(col).strip()  # with strip() method, we make maintenance to the data.
                    col = int(item)
                    # print(f"It's an integer! Value: {item}")
                except ValueError:
                    pass
                    # print("This is not an integer.")

                if is_valid_date_format(col):
                    item = str(col).strip()  # with strip() method, we make maintenance to the data.
                    col = datetime.strptime(item, "%Y-%m-%d %H:%M:%S")
                n_row.append(col)
                # print('n_row: ', n_row)
            n_list.append(n_row)
            n_row = []
            # print('n_list: ', n_list)
        return n_list
    except Exception as e:
        raise Exception(f"Error occurred in remake_it_with_types function: {e}")


# Colors rows in tableWidget objects according to parameter values
def highlight_candidates(form, control_column: int, control_value, text_color: str or QColor,
                         background_color: str or QColor):
    try:
        # Get number of rows and columns of table in desired form
        row_count = form.tableWidget.rowCount()
        column_count = form.tableWidget.columnCount()

        # check every row in form tableWidget
        for row in range(row_count):
            # Get crm_IsApplicantACandidate data in column control_column
            crm_id_item = form.tableWidget.item(row, control_column)
            # If crm_id_item meets the condition, paint the background and text color
            if crm_id_item:
                if str(crm_id_item.text()) == str(control_value):
                    for col in range(column_count):
                        item = form.tableWidget.item(row, col)
                        if item:  # If the item exists
                            # Force set styleSheets
                            item.setBackground(QColor(background_color))  # Set background color
                            item.setForeground(QColor(text_color))  # Set text color
    except Exception as e:
        raise Exception(f"Error occurred in highlight_candidates function: {e}")


# This function is a datetime checker function. It checks a string value is datetime or not.
def is_valid_date_format(date_str: str):
    try:
        date_str = str(date_str)  # If the parameter is not a string, first convert it to string type
        formats = [
            r'^\d{2}[./-]\d{2}[./-]\d{4}$',
            r'^\d{4}[./-]\d{2}[./-]\d{2}$',
            r'^\d{2}[./-]\d{2}[./-]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
            r'^\d{4}[./-]\d{2}[./-]\d{2} \d{2}[:.]\d{2}[:.]\d{2}$',
            r'^\d{1}[./-]\d{2}[./-]\d{4}$',
            r'^\d{2}[./-]\d{1}[./-]\d{4}$',
            r'^\d{1}[./-]\d{1}[./-]\d{4}$',
            r'^\d{4}[./-]\d{2}[./-]\d{1}$',
            r'^\d{4}[./-]\d{1}[./-]\d{2}$',
            r'^\d{4}[./-]\d{1}[./-]\d{1}$',
            r'^\d{1}[./-]\d{2}[./-]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
            r'^\d{2}[./-]\d{1}[./-]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
            r'^\d{1}[./-]\d{1}[./-]\d{4} \d{2}[:.]\d{2}[:.]\d{2}$',
            r'^\d{4}[./-]\d{2}[./-]\d{1} \d{2}[:.]\d{2}[:.]\d{2}$',
            r'^\d{4}[./-]\d{1}[./-]\d{2} \d{2}[:.]\d{2}[:.]\d{2}$',
            r'^\d{4}[./-]\d{1}[./-]\d{1} \d{2}[:.]\d{2}[:.]\d{2}$',
        ]
        return any(re.match(pattern, date_str) for pattern in formats)
    except Exception as e:
        raise Exception(f"Error occurred in is_valid_date_format function: {e}")


# It synchronizes the UTC time to local time.
# (It is not used in the project, but maybe we need when we carry our db to another server)
def convert_to_local_time(utc_date_str: str):
    try:
        utc_date = datetime.fromisoformat(utc_date_str)    # Create UTC date
        utc_zone = pytz.UTC # Create UTC time zone
        utc_date = utc_date.replace(tzinfo=utc_zone)    # Set UTC time zone

        # Get system local timezone
        local_tz = datetime.now().astimezone().tzinfo  # Get local time zone automatically
        converted_date = utc_date.astimezone(local_tz)  # Conversion from UTC to local time

        # Format and return local time
        return converted_date.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        raise Exception(f"Error occurred in convert_to_local_time function: {e}")


# It synchronizes the server-time where the DB is located with the time when the application is used.
def convert_server_time_to_local(server_date, server_timezone=cnf.server_tz):
    """
    Converts the date in the server-time-zone to the local-time-zone.

    :param server_date: Server date (format: 'YYYY-MM-DD HH:MM:SS' or datetime object)
    :param server_timezone: Server's time zone (e.g. 'America/New_York')
    :return: Date string formatted in local time zone
    """
    try:
        server_tz = pytz.timezone(server_timezone)  # Get server time zone

        # If server_date is string convert to datetime type
        if isinstance(server_date, str):
            server_date = datetime.strptime(server_date, '%Y-%m-%d %H:%M:%S')
        server_date = server_tz.localize(server_date)  # Localize server date with server timezone

        local_tz = datetime.now().astimezone().tzinfo  # Get local time zone
        converted_date = server_date.astimezone(local_tz)  # Conversion from server time to local time

        # Format and return local time
        return converted_date.strftime('%Y-%m-%d %H:%M:%S')

    except ValueError as ve:
        raise ValueError(f"Invalid datetime format: {ve}")
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValueError(f"Unknown time-zone: {server_timezone}")


def filter_active_options(a_list: list, filtering_column: int):
    try:
        option_elements = []
        for row in a_list:
            try:
                value = row[filtering_column]
                # print(f"Row: {row},\n Value: {value}, Type: {type(value)}")  # Debug output
                option_elements.append(str(value).strip())
            except Exception as err:
                print(f"Error processing row {row}: {err}")  # Error output for debugging
                continue

        filter_options = list(set(option_elements))

        if filter_options:
            if filter_options[0].isdigit():
                filter_options = sorted(filter_options, key=int)
            else:
                filter_options.sort()
        return filter_options
    except Exception as e:
        raise Exception(f"Error occurred in filter_active_options function: {e}")


def filter_table(form, headers: list, filtering_list: list, filtering_column: int):
    try:
        filtered_data = []
        selected_item = form.comboBoxFilterOptions.currentText().strip()

        for row in filtering_list:
            if str(row[filtering_column]).strip().lower() == str(selected_item).strip().lower():
                filtered_data.append(row)

        if filtered_data and len(filtered_data) > 0:
            pass
        else:
            if filtering_list and len(filtering_list[0]) > 0:
                default_nothing_found = ['Nothing Found!']
                [default_nothing_found.append('-') for i in range(len(filtering_list[0]) - 1)]
                filtered_data.append(default_nothing_found)
            else:
                print("Filtering list is empty")
        return write2table(form, headers, filtered_data)
    except Exception as e:
        raise Exception(f"Error occurred in filter_table function: ") from e


def execute_write_query(conn, query: str, args: tuple = None):
    if conn:
        cursor = conn.cursor()
    else:
        print('There is no connection! Aborting...')
        return

    try:
        cursor.execute(query, args)
        affected_rows = cursor.rowcount  # We get the number of rows affected
        conn.commit()
        conn.close()
        return affected_rows
    except Exception as e:
        conn.close()
        raise Exception(f"Error occurred in execute_query function: ") from e


def execute_read_query(conn, query: str, args: tuple = None):
    result = None

    if conn:
        cursor = conn.cursor()
    else:
        print('There is no connection! Aborting...')
        return result

    try:
        cursor.execute(query, args)
        result = cursor.fetchall()
        conn.close()
    except Exception as e:
        conn.close()
        print(f"Error occurred in execute_read_query function: {e}")
    finally:
        return result


# Connects to google sheet files for reading and writing, returns sheet data.
def connect_to_google_sheets(sheet_name: str):
    try:
        # Set Google Sheets API connection
        google_credentials_file = cnf.google_credentials_file  # Your credentials file
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(google_credentials_file, scope)
        client = gspread.authorize(creds)  # Sign in with authentication credentials
        return client.open(sheet_name).sheet1

    except Exception as e:
        raise Exception(f"Error occurred in connect_to_google_sheets function: {e}")


# Function to connect to 2-Events_All_Interviews sheet using gspread
def update_events_all_interviews_sheet(event_id, attendee_name, attendee_surname, attendee_email):
    try:
        # Open Google Sheet file
        # 2-Events_All_Interviews sheet
        google_events_all_interviews_sheet_name = cnf.google_events_all_interviews_sheet_name
        sheet = connect_to_google_sheets(google_events_all_interviews_sheet_name)

        # Get all data in Event ID column (column number with Event ID is number 2)
        event_ids = sheet.col_values(2)

        # Find the row with the relevant Event ID
        for idx, sheet_event_id in enumerate(event_ids):
            if sheet_event_id == event_id:
                # In the relevant row, update the Attendee Name, Surname, and Mail columns
                sheet.update_cell(idx + 1, 11, attendee_email)  # 11: Attendee Mail column
                sheet.update_cell(idx + 1, 13, attendee_name)  # 13: Attendee Name column
                sheet.update_cell(idx + 1, 14, attendee_surname)  # 14: Attendee Surname column
                break
        else:
            print(f"Event ID {event_id} not found in the sheet.")
    except Exception as e:
        raise Exception(f"Error occurred in update_events_all_interviews_sheet function: {e}")


# be able to add tooltips to these: QPushButton, QComboBox, QLabel, QLineEdit, QTableWidget, QDateTimeEdit, QInputDialog
def add_tooltip_to_any_form_object(obj: QObject, tooltip_text: str):
    """
    Adds a tooltip to the given QPushButton or QComboBox object and makes its background yellow.

    :param obj: A QPushButton, QComboBox, QLabel, QLineEdit, QTableWidget, QDateTimeEdit or QInputDialog object
    :param tooltip_text: Message to show in Tooltip
    """
    try:
        if isinstance(obj, (QPushButton, QComboBox, QLabel, QLineEdit, QTableWidget, QDateTimeEdit, QInputDialog)):
            obj.setToolTip(tooltip_text)

            # Set tooltip style
            QToolTip.setFont(QFont('SansSerif', 10))  # Tooltip font and size
            style_sheet = obj.styleSheet()
            style_sheet = style_sheet + ("""
                QToolTip {
                    background-color: yellow;
                    color: black;
                    border: 1px solid black;
                }
            """)
            obj.setStyleSheet(style_sheet)
        else:
            raise TypeError("Object must be an object in the list.\nList = "
                            "[QPushButton, QComboBox, QLabel, QLineEdit, QTableWidget, QDateTimeEdit, QInputDialog]")
    except Exception as e:
        raise Exception(f"Error occurred in add_tooltip_to_any_form_object function: {e}")


# Function for adding Tooltip to the header section of the QTableWidget object
def add_tooltip_to_table_widget_header(table_widget: QTableWidget, column_index: int, tooltip_text: str):
    """
    Adds a tooltip to the header of the given tableWidget column.

    :param table_widget: QTableWidget object
    :param column_index: Index of the column to which the tooltip will be added
    :param tooltip_text: Message to show in Tooltip
    """
    try:
        header_item = table_widget.horizontalHeaderItem(column_index)
        if header_item:
            header_item.setToolTip(tooltip_text)
    except Exception as e:
        raise Exception(f"Error occurred in add_tooltip_to_header function: {e}")


# This is a function specific to this project.
# The first object should be a combobox with items, the second should be a combobox for filtering.
def normalise_combo_boxes(objects: list, args: list = None):
    try:
        if isinstance(objects[0], QComboBox):
            objects[0].clear()
            objects[0].setPlaceholderText(args[0])
            objects[0].addItems([args[1], args[2]])

        if isinstance(objects[1], QComboBox):
            objects[1].clear()
            objects[1].setPlaceholderText("Filter Area")
    except Exception as e:
        raise Exception(f"Error occurred in normalise_combo_boxes function: {e}")


# Password hashing function by bcrypt
def hash_password(password: str):
    try:
        # Hash the password by generating a salt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
    except Exception as e:
        raise Exception(f"Error occurred in hash_password function: {e}")


# Password verification function
def check_password(password: str, hashed_password):
    try:
        # Compare the given password by hashing it
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except Exception as e:
        raise Exception(f"Error occurred in check_password function: {e}")


# Code to enable adding context-menu to right-click
def enable_context_menu(form, context_menu):
    try:
        form.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        form.tableWidget.customContextMenuRequested.connect(context_menu)
    except Exception as e:
        raise Exception(f"Error occurred in enable_context_menu function: {e}")


# Code to disable adding context-menu to right-click.
def disable_context_menu(form, context_menu):
    try:
        form.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        form.tableWidget.customContextMenuRequested.disconnect(context_menu)
    except TypeError:
        # If the connection is already lost, ignore this error
        pass
    except Exception as e:
        raise Exception(f"Error occurred in disable_context_menu function: {e}")


# Code to disable cell_entered signal
def disable_cell_entered_signal_f(form, method):
    try:
        # Disconnect the cellEntered signal to disable on_cell_entered method
        form.tableWidget.cellEntered.disconnect(method)
    except TypeError:
        # If the signal is already disconnected, an error occurs; We ignore this error.
        pass
    except Exception as e:
        raise Exception(f"Error occurred in disconnect_cell_entered_signal function: {e}")


# Code that enables the cell_entered signal
def re_enable_cell_entered_signal_f(form, method):
    try:
        # Connect the cellEntered signal to re-enable on_cell_entered method
        form.tableWidget.cellEntered.connect(method)
    except TypeError:
        # If the signal is already connected, an error occurs; We ignore this error.
        pass
    except Exception as e:
        raise Exception(f"Error occurred in re_enable_cell_entered_signal function: {e}")


# This code is written to make the contents appear briefly when hovering over the cell.
def on_cell_entered_f(form, row: int, column: int):
    try:
        # Get the text of the cell at the specified row and column
        item_text = form.tableWidget.item(row, column).text()

        # Show a tooltip with the cell text
        tooltip = form.tableWidget.viewport().mapToGlobal(form.tableWidget.visualItemRect(
            form.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text)
    except Exception as e:
        raise Exception(f"Error occurred in on_cell_entered_f function: {e}")


# This code is for cell clicking
# If you want to show a persistent tooltip with the cell text. You need to use this function and its method together.
def on_cell_clicked_f(form, row: int, column: int):
    try:
        # Get the text of the clicked cell
        item_text = form.tableWidget.item(row, column).text()

        # Show a persistent tooltip with the cell text
        tooltip = form.tableWidget.viewport().mapToGlobal(form.tableWidget.visualItemRect(
            form.tableWidget.item(row, column)).topLeft())
        QToolTip.setFont(QFont("SansSerif", 10))
        QToolTip.showText(tooltip, item_text, form.tableWidget)
    except Exception as e:
        raise Exception(f"Error occurred in on_cell_clicked_f function: {e}")


if __name__ == '__main__':
    pass