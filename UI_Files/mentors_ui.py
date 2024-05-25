# Form implementation generated from reading ui file 'UI_Files/mentors_ui.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FormMentor(object):
    def setupUi(self, FormMentor):
        FormMentor.setObjectName("FormMentor")
        FormMentor.resize(1180, 550)
        FormMentor.setMinimumSize(QtCore.QSize(1180, 550))
        FormMentor.setMaximumSize(QtCore.QSize(1180, 550))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UI_Files\\pictures/werhere_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        FormMentor.setWindowIcon(icon)
        FormMentor.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.494, y2:0, stop:0 rgba(71, 71, 71, 255), stop:1 rgba(255, 255, 255, 255));")
        self.labelPicture = QtWidgets.QLabel(parent=FormMentor)
        self.labelPicture.setGeometry(QtCore.QRect(20, 20, 211, 141))
        self.labelPicture.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.labelPicture.setText("")
        self.labelPicture.setPixmap(QtGui.QPixmap("UI_Files\\pictures/mentor_menu.png"))
        self.labelPicture.setScaledContents(True)
        self.labelPicture.setObjectName("labelPicture")
        self.labelLogo = QtWidgets.QLabel(parent=FormMentor)
        self.labelLogo.setGeometry(QtCore.QRect(370, 10, 261, 101))
        self.labelLogo.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.labelLogo.setText("")
        self.labelLogo.setPixmap(QtGui.QPixmap("UI_Files\\pictures/werhere_logo.ico"))
        self.labelLogo.setObjectName("labelLogo")
        self.labelMentors = QtWidgets.QLabel(parent=FormMentor)
        self.labelMentors.setGeometry(QtCore.QRect(630, 38, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(26)
        font.setBold(True)
        self.labelMentors.setFont(font)
        self.labelMentors.setStyleSheet("background-color: rgba(0, 0, 0,0%);\n"
"color: rgb(71, 84, 88);")
        self.labelMentors.setObjectName("labelMentors")
        self.pushButtonGetAllApplications = QtWidgets.QPushButton(parent=FormMentor)
        self.pushButtonGetAllApplications.setGeometry(QtCore.QRect(30, 270, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonGetAllApplications.setFont(font)
        self.pushButtonGetAllApplications.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
" border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButtonGetAllApplications.setObjectName("pushButtonGetAllApplications")
        self.pushButtonExit = QtWidgets.QPushButton(parent=FormMentor)
        self.pushButtonExit.setGeometry(QtCore.QRect(30, 450, 171, 31))
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
" border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.lineEditSearch = QtWidgets.QLineEdit(parent=FormMentor)
        self.lineEditSearch.setEnabled(True)
        self.lineEditSearch.setGeometry(QtCore.QRect(30, 180, 171, 31))
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
        self.pushButtonBackMenu = QtWidgets.QPushButton(parent=FormMentor)
        self.pushButtonBackMenu.setGeometry(QtCore.QRect(30, 360, 171, 31))
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
        self.tableWidget = QtWidgets.QTableWidget(parent=FormMentor)
        self.tableWidget.setGeometry(QtCore.QRect(230, 170, 921, 341))
        self.tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.tableWidget.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.tableWidget.setAutoScrollMargin(16)
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
        self.tableWidget.horizontalHeader().setDefaultSectionSize(115)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(True)
        self.comboBoxFilterOptions = QtWidgets.QComboBox(parent=FormMentor)
        self.comboBoxFilterOptions.setGeometry(QtCore.QRect(790, 120, 361, 31))
        self.comboBoxFilterOptions.setStyleSheet("border-radius : 15px;\n"
"border: 3px solid rgb(85, 255, 255);\n"
"background-color: rgba(0, 0, 0,55%);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.comboBoxFilterOptions.setObjectName("comboBoxFilterOptions")

        self.retranslateUi(FormMentor)
        QtCore.QMetaObject.connectSlotsByName(FormMentor)
        FormMentor.setTabOrder(self.lineEditSearch, self.pushButtonGetAllApplications)
        FormMentor.setTabOrder(self.pushButtonGetAllApplications, self.tableWidget)
        FormMentor.setTabOrder(self.tableWidget, self.comboBoxFilterOptions)
        FormMentor.setTabOrder(self.comboBoxFilterOptions, self.pushButtonBackMenu)
        FormMentor.setTabOrder(self.pushButtonBackMenu, self.pushButtonExit)

    def retranslateUi(self, FormMentor):
        _translate = QtCore.QCoreApplication.translate
        FormMentor.setWindowTitle(_translate("FormMentor", "MENTOR MENU"))
        self.labelMentors.setText(_translate("FormMentor", "MENTORS"))
        self.pushButtonGetAllApplications.setText(_translate("FormMentor", "Get All Applications"))
        self.pushButtonExit.setText(_translate("FormMentor", "Exit"))
        self.lineEditSearch.setPlaceholderText(_translate("FormMentor", "      Name or Surname"))
        self.pushButtonBackMenu.setText(_translate("FormMentor", "Back Menu"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("FormMentor", "Interview Date"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("FormMentor", "Candidate Name \n"
"Surname"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("FormMentor", "Mentor Name\n"
"Surname"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("FormMentor", "IT Knowledge"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("FormMentor", "Availability"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("FormMentor", "Thoughts About \n"
"  the Candidate"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("FormMentor", "Candidate\'s \n"
"Attendance Status"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("FormMentor", "Comments About \n"
"the Candidate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormMentor = QtWidgets.QWidget()
    ui = Ui_FormMentor()
    ui.setupUi(FormMentor)
    FormMentor.show()
    sys.exit(app.exec())
