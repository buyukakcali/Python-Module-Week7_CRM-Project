# Form implementation generated from reading ui file 'UI_Files/applications_ui.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FormApplications(object):
    def setupUi(self, FormApplications):
        FormApplications.setObjectName("FormApplications")
        FormApplications.resize(1080, 680)
        FormApplications.setMinimumSize(QtCore.QSize(1080, 680))
        FormApplications.setMaximumSize(QtCore.QSize(1080, 680))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UI_Files\\pictures/werhere_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        FormApplications.setWindowIcon(icon)
        FormApplications.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.494, y2:0, stop:0 rgba(71, 71, 71, 255), stop:1 rgba(255, 255, 255, 255));")
        self.pushButtonAllApplications = QtWidgets.QPushButton(parent=FormApplications)
        self.pushButtonAllApplications.setGeometry(QtCore.QRect(40, 200, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonAllApplications.setFont(font)
        self.pushButtonAllApplications.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
"    border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButtonAllApplications.setObjectName("pushButtonAllApplications")
        self.labelLogo = QtWidgets.QLabel(parent=FormApplications)
        self.labelLogo.setGeometry(QtCore.QRect(270, 22, 261, 101))
        self.labelLogo.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.labelLogo.setText("")
        self.labelLogo.setPixmap(QtGui.QPixmap("UI_Files\\pictures/werhere_logo.ico"))
        self.labelLogo.setObjectName("labelLogo")
        self.pushButtonPlannedMeetings = QtWidgets.QPushButton(parent=FormApplications)
        self.pushButtonPlannedMeetings.setGeometry(QtCore.QRect(40, 250, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonPlannedMeetings.setFont(font)
        self.pushButtonPlannedMeetings.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
"    border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButtonPlannedMeetings.setObjectName("pushButtonPlannedMeetings")
        self.pushButtonUnscheduledMeeting = QtWidgets.QPushButton(parent=FormApplications)
        self.pushButtonUnscheduledMeeting.setGeometry(QtCore.QRect(40, 300, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonUnscheduledMeeting.setFont(font)
        self.pushButtonUnscheduledMeeting.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
"    border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButtonUnscheduledMeeting.setObjectName("pushButtonUnscheduledMeeting")
        self.pushButtonDifferentialRegistrations = QtWidgets.QPushButton(parent=FormApplications)
        self.pushButtonDifferentialRegistrations.setGeometry(QtCore.QRect(40, 450, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonDifferentialRegistrations.setFont(font)
        self.pushButtonDifferentialRegistrations.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
" border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButtonDifferentialRegistrations.setObjectName("pushButtonDifferentialRegistrations")
        self.pushButtonBackMenu = QtWidgets.QPushButton(parent=FormApplications)
        self.pushButtonBackMenu.setGeometry(QtCore.QRect(40, 550, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonBackMenu.setFont(font)
        self.pushButtonBackMenu.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
" border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButtonBackMenu.setObjectName("pushButtonBackMenu")
        self.pushButtonFilterApplications = QtWidgets.QPushButton(parent=FormApplications)
        self.pushButtonFilterApplications.setGeometry(QtCore.QRect(40, 500, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonFilterApplications.setFont(font)
        self.pushButtonFilterApplications.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
" border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButtonFilterApplications.setObjectName("pushButtonFilterApplications")
        self.pushButtonExit = QtWidgets.QPushButton(parent=FormApplications)
        self.pushButtonExit.setGeometry(QtCore.QRect(40, 600, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonExit.setFont(font)
        self.pushButtonExit.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
"    border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.tableWidget = QtWidgets.QTableWidget(parent=FormApplications)
        self.tableWidget.setGeometry(QtCore.QRect(250, 130, 801, 521))
        self.tableWidget.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.lineEditSearch = QtWidgets.QLineEdit(parent=FormApplications)
        self.lineEditSearch.setEnabled(True)
        self.lineEditSearch.setGeometry(QtCore.QRect(40, 140, 171, 31))
        self.lineEditSearch.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.lineEditSearch.setStyleSheet("QLineEdit {\n"
"  border: 2px solid rgb(38, 38, 48);\n"
"  border-radius: 15px;\n"
"  color: #FFF;\n"
"  padding-left: 15px;\n"
"  background-color: rgba(0, 0, 0,55%);\n"
" \n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(0, 255, 255);\n"
"}\n"
"\n"
" QLineEdit:focus  {\n"
"  border: 2px solid rgb(35, 218, 233);\n"
"  background-color: rgb(47, 47, 47);\n"
"}\n"
"\n"
"   \n"
"\n"
"\n"
"\n"
"")
        self.lineEditSearch.setText("")
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.labelProjectApplications = QtWidgets.QLabel(parent=FormApplications)
        self.labelProjectApplications.setGeometry(QtCore.QRect(530, 50, 491, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(26)
        font.setBold(True)
        self.labelProjectApplications.setFont(font)
        self.labelProjectApplications.setStyleSheet("background-color: rgba(0, 0, 0,0%);\n"
"color: rgb(71, 84, 88);")
        self.labelProjectApplications.setObjectName("labelProjectApplications")
        self.labelPicture = QtWidgets.QLabel(parent=FormApplications)
        self.labelPicture.setGeometry(QtCore.QRect(8, 10, 231, 121))
        self.labelPicture.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.labelPicture.setText("")
        self.labelPicture.setPixmap(QtGui.QPixmap("UI_Files\\pictures/project_app.png"))
        self.labelPicture.setScaledContents(True)
        self.labelPicture.setObjectName("labelPicture")
        self.comboBoxPreviousApplications = QtWidgets.QComboBox(parent=FormApplications)
        self.comboBoxPreviousApplications.setGeometry(QtCore.QRect(40, 400, 171, 31))
        self.comboBoxPreviousApplications.setStyleSheet("QComboBox{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QComboBox:hover{\n"
"    border-radius : 15px;\n"
"    background-color: rgb(20, 135, 135);\n"
"    border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.comboBoxPreviousApplications.setObjectName("comboBoxPreviousApplications")
        self.comboBoxFilterOptions = QtWidgets.QComboBox(parent=FormApplications)
        self.comboBoxFilterOptions.setGeometry(QtCore.QRect(690, 100, 361, 31))
        self.comboBoxFilterOptions.setStyleSheet("border-radius : 15px;\n"
"border: 3px solid rgb(85, 255, 255);\n"
"background-color: rgba(0, 0, 0,55%);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.comboBoxFilterOptions.setObjectName("comboBoxFilterOptions")
        self.comboBoxDuplicatedApplications = QtWidgets.QComboBox(parent=FormApplications)
        self.comboBoxDuplicatedApplications.setGeometry(QtCore.QRect(40, 350, 171, 31))
        self.comboBoxDuplicatedApplications.setStyleSheet("QComboBox{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QComboBox:hover{\n"
"    border-radius : 15px;\n"
"    background-color: rgb(20, 135, 135);\n"
"    border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.comboBoxDuplicatedApplications.setObjectName("comboBoxDuplicatedApplications")

        self.retranslateUi(FormApplications)
        QtCore.QMetaObject.connectSlotsByName(FormApplications)
        FormApplications.setTabOrder(self.lineEditSearch, self.pushButtonAllApplications)
        FormApplications.setTabOrder(self.pushButtonAllApplications, self.pushButtonPlannedMeetings)
        FormApplications.setTabOrder(self.pushButtonPlannedMeetings, self.pushButtonUnscheduledMeeting)
        FormApplications.setTabOrder(self.pushButtonUnscheduledMeeting, self.pushButtonDifferentialRegistrations)
        FormApplications.setTabOrder(self.pushButtonDifferentialRegistrations, self.pushButtonFilterApplications)
        FormApplications.setTabOrder(self.pushButtonFilterApplications, self.tableWidget)
        FormApplications.setTabOrder(self.tableWidget, self.pushButtonBackMenu)
        FormApplications.setTabOrder(self.pushButtonBackMenu, self.pushButtonExit)

    def retranslateUi(self, FormApplications):
        _translate = QtCore.QCoreApplication.translate
        FormApplications.setWindowTitle(_translate("FormApplications", "APPLICATION"))
        self.pushButtonAllApplications.setText(_translate("FormApplications", "All Applications"))
        self.pushButtonPlannedMeetings.setText(_translate("FormApplications", "Planned Meetings"))
        self.pushButtonUnscheduledMeeting.setText(_translate("FormApplications", "Unscheduled Meetings"))
        self.pushButtonDifferentialRegistrations.setText(_translate("FormApplications", "Differential Registrations"))
        self.pushButtonBackMenu.setText(_translate("FormApplications", "Back Menu"))
        self.pushButtonFilterApplications.setText(_translate("FormApplications", "Filter Applications\n"
"(Unique)"))
        self.pushButtonExit.setText(_translate("FormApplications", "Exit"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("FormApplications", "Date"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("FormApplications", "Name Surname"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("FormApplications", "Mail"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("FormApplications", "Telephone"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("FormApplications", "Post Code"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("FormApplications", "State"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("FormApplications", "Status"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("FormApplications", "Economical \n"
"Situation"))
        self.lineEditSearch.setPlaceholderText(_translate("FormApplications", "      Name or Surname"))
        self.labelProjectApplications.setText(_translate("FormApplications", "PROJECT APPLICATIONS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormApplications = QtWidgets.QWidget()
    ui = Ui_FormApplications()
    ui.setupUi(FormApplications)
    FormApplications.show()
    sys.exit(app.exec())
