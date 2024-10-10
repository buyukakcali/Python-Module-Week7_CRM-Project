# Form implementation generated from reading ui file 'UI_Files/candidates_ui.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FormCandidates(object):
    def setupUi(self, FormCandidates):
        FormCandidates.setObjectName("FormCandidates")
        FormCandidates.resize(890, 525)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FormCandidates.sizePolicy().hasHeightForWidth())
        FormCandidates.setSizePolicy(sizePolicy)
        FormCandidates.setMinimumSize(QtCore.QSize(835, 525))
        font = QtGui.QFont()
        font.setPointSize(7)
        FormCandidates.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UI_Files\\pictures/logo_organization1.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        FormCandidates.setWindowIcon(icon)
        FormCandidates.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.494, y2:0, stop:0 rgba(71, 71, 71, 255), stop:1 rgba(255, 255, 255, 255));")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(FormCandidates)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelPicture = QtWidgets.QLabel(parent=FormCandidates)
        self.labelPicture.setMinimumSize(QtCore.QSize(150, 130))
        self.labelPicture.setMaximumSize(QtCore.QSize(150, 130))
        self.labelPicture.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.labelPicture.setText("")
        self.labelPicture.setPixmap(QtGui.QPixmap("UI_Files\\pictures/menu_interviews.png"))
        self.labelPicture.setScaledContents(True)
        self.labelPicture.setObjectName("labelPicture")
        self.horizontalLayout.addWidget(self.labelPicture)
        self.labelLogo1 = QtWidgets.QLabel(parent=FormCandidates)
        self.labelLogo1.setMinimumSize(QtCore.QSize(130, 140))
        self.labelLogo1.setMaximumSize(QtCore.QSize(130, 140))
        self.labelLogo1.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.labelLogo1.setText("")
        self.labelLogo1.setPixmap(QtGui.QPixmap("UI_Files\\pictures/logo_organization1.ico"))
        self.labelLogo1.setObjectName("labelLogo1")
        self.horizontalLayout.addWidget(self.labelLogo1)
        self.labelLogo2 = QtWidgets.QLabel(parent=FormCandidates)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLogo2.sizePolicy().hasHeightForWidth())
        self.labelLogo2.setSizePolicy(sizePolicy)
        self.labelLogo2.setMinimumSize(QtCore.QSize(522, 110))
        self.labelLogo2.setMaximumSize(QtCore.QSize(522, 110))
        self.labelLogo2.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.labelLogo2.setText("")
        self.labelLogo2.setPixmap(QtGui.QPixmap("UI_Files\\pictures/logo_organization2.png"))
        self.labelLogo2.setScaledContents(True)
        self.labelLogo2.setObjectName("labelLogo2")
        self.horizontalLayout.addWidget(self.labelLogo2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelAreaKeeper1 = QtWidgets.QLabel(parent=FormCandidates)
        self.labelAreaKeeper1.setMinimumSize(QtCore.QSize(190, 40))
        self.labelAreaKeeper1.setMaximumSize(QtCore.QSize(190, 40))
        self.labelAreaKeeper1.setStyleSheet("QLabel {\n"
"    background-color: rgba(0, 0, 0, 0);\n"
"}")
        self.labelAreaKeeper1.setText("")
        self.labelAreaKeeper1.setObjectName("labelAreaKeeper1")
        self.horizontalLayout_2.addWidget(self.labelAreaKeeper1)
        self.labelMenu = QtWidgets.QLabel(parent=FormCandidates)
        self.labelMenu.setMinimumSize(QtCore.QSize(350, 40))
        self.labelMenu.setMaximumSize(QtCore.QSize(350, 40))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(22)
        font.setBold(True)
        self.labelMenu.setFont(font)
        self.labelMenu.setStyleSheet("background-color: rgba(0, 0, 0,0%);\n"
"color: rgb(71, 84, 88);")
        self.labelMenu.setScaledContents(True)
        self.labelMenu.setObjectName("labelMenu")
        self.horizontalLayout_2.addWidget(self.labelMenu)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.comboBoxFilterOptions = QtWidgets.QComboBox(parent=FormCandidates)
        self.comboBoxFilterOptions.setMinimumSize(QtCore.QSize(300, 0))
        self.comboBoxFilterOptions.setStyleSheet("QComboBox {\n"
"    border-radius : 15px;\n"
"    border: 3px solid rgb(85, 255, 255);\n"
"    background-color: rgba(0, 0, 0,55%);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 2px solid rgb(255, 80, 0);\n"
"}\n"
"\n"
"QComboBox:focus  {\n"
"  border: 2px solid rgb(162, 0, 0);\n"
"  background-color: rgb(47, 47, 47);\n"
"}\n"
"")
        self.comboBoxFilterOptions.setObjectName("comboBoxFilterOptions")
        self.horizontalLayout_2.addWidget(self.comboBoxFilterOptions)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(parent=FormCandidates)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 1, 1, 1)
        self.frameButtons = QtWidgets.QFrame(parent=FormCandidates)
        self.frameButtons.setMinimumSize(QtCore.QSize(190, 290))
        self.frameButtons.setMaximumSize(QtCore.QSize(190, 16777215))
        self.frameButtons.setStyleSheet("QFrame {\n"
"    background-color: rgb(0, 0, 0, 0);\n"
"}")
        self.frameButtons.setObjectName("frameButtons")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frameButtons)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEditSearch = QtWidgets.QLineEdit(parent=self.frameButtons)
        self.lineEditSearch.setEnabled(True)
        self.lineEditSearch.setMinimumSize(QtCore.QSize(170, 35))
        self.lineEditSearch.setMaximumSize(QtCore.QSize(170, 35))
        self.lineEditSearch.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.lineEditSearch.setStyleSheet("QLineEdit {\n"
"  border: 2px solid rgb(35, 218, 233);\n"
"  border-radius: 15px;\n"
"  color: #FFF;\n"
"  padding-left: 15px;\n"
"  background-color: rgba(0, 0, 0,55%); \n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(255, 80, 0);\n"
"}\n"
"\n"
"QLineEdit:focus  {\n"
"  border: 2px solid rgb(162, 0, 0);\n"
"  background-color: rgb(47, 47, 47);\n"
"}\n"
"")
        self.lineEditSearch.setText("")
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.verticalLayout.addWidget(self.lineEditSearch)
        self.pushButtonGetCandidates = QtWidgets.QPushButton(parent=self.frameButtons)
        self.pushButtonGetCandidates.setMinimumSize(QtCore.QSize(170, 35))
        self.pushButtonGetCandidates.setMaximumSize(QtCore.QSize(170, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonGetCandidates.setFont(font)
        self.pushButtonGetCandidates.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
"    border: 2px solid rgb(255, 80, 0);\n"
"}")
        self.pushButtonGetCandidates.setObjectName("pushButtonGetCandidates")
        self.verticalLayout.addWidget(self.pushButtonGetCandidates)
        self.pushButtonInterviewedCandidates = QtWidgets.QPushButton(parent=self.frameButtons)
        self.pushButtonInterviewedCandidates.setMinimumSize(QtCore.QSize(170, 35))
        self.pushButtonInterviewedCandidates.setMaximumSize(QtCore.QSize(170, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonInterviewedCandidates.setFont(font)
        self.pushButtonInterviewedCandidates.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
"    border: 2px solid rgb(255, 80, 0);\n"
"}")
        self.pushButtonInterviewedCandidates.setObjectName("pushButtonInterviewedCandidates")
        self.verticalLayout.addWidget(self.pushButtonInterviewedCandidates)
        self.comboBoxTrainees = QtWidgets.QComboBox(parent=self.frameButtons)
        self.comboBoxTrainees.setMinimumSize(QtCore.QSize(170, 35))
        self.comboBoxTrainees.setMaximumSize(QtCore.QSize(170, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.comboBoxTrainees.setFont(font)
        self.comboBoxTrainees.setStyleSheet("QComboBox {\n"
"    border-radius: 15px;\n"
"    background-color: rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"    padding: 1px 18px 1px 3px;\n"
"}\n"
"\n"
"QComboBox:placeholder {\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    border: none;\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    width: 14px;\n"
"    height: 14px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"    background-color: rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid darkgray;\n"
"    selection-background-color: rgb(20, 135, 135);\n"
"    background-color: rgb(25, 200, 200);\n"
"    border-radius: 15px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: rgb(20, 135, 135); /* QComboBox arka planı hover anında değişiyor */\n"
"    border: 2px solid rgb(255, 80, 0); /* Hover ile kenar çizgisi ekleniyor */\n"
"}\n"
"\n"
"QToolTip {\n"
"     border-radius: 15px;\n"
"    background-color: yellow; \n"
"    color: black; \n"
"    border: 1px solid black;\n"
"}")
        self.comboBoxTrainees.setObjectName("comboBoxTrainees")
        self.verticalLayout.addWidget(self.comboBoxTrainees)
        self.pushButtonBackMenu = QtWidgets.QPushButton(parent=self.frameButtons)
        self.pushButtonBackMenu.setMinimumSize(QtCore.QSize(170, 35))
        self.pushButtonBackMenu.setMaximumSize(QtCore.QSize(170, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonBackMenu.setFont(font)
        self.pushButtonBackMenu.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
"    border: 2px solid rgb(255, 80, 0);\n"
"}")
        self.pushButtonBackMenu.setObjectName("pushButtonBackMenu")
        self.verticalLayout.addWidget(self.pushButtonBackMenu)
        self.pushButtonExit = QtWidgets.QPushButton(parent=self.frameButtons)
        self.pushButtonExit.setMinimumSize(QtCore.QSize(170, 35))
        self.pushButtonExit.setMaximumSize(QtCore.QSize(170, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButtonExit.setFont(font)
        self.pushButtonExit.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
"    border: 2px solid rgb(255, 80, 0);\n"
"}")
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.verticalLayout.addWidget(self.pushButtonExit)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.gridLayout.addWidget(self.frameButtons, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelAreaKeeper2 = QtWidgets.QLabel(parent=FormCandidates)
        self.labelAreaKeeper2.setMinimumSize(QtCore.QSize(190, 10))
        self.labelAreaKeeper2.setMaximumSize(QtCore.QSize(190, 10))
        self.labelAreaKeeper2.setStyleSheet("QLabel {\n"
"    background-color: rgba(0, 0, 0, 0);\n"
"}")
        self.labelAreaKeeper2.setText("")
        self.labelAreaKeeper2.setObjectName("labelAreaKeeper2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.labelAreaKeeper2)
        self.labelInfo1 = QtWidgets.QLabel(parent=FormCandidates)
        self.labelInfo1.setEnabled(False)
        self.labelInfo1.setMinimumSize(QtCore.QSize(10, 10))
        self.labelInfo1.setMaximumSize(QtCore.QSize(10, 10))
        self.labelInfo1.setText("")
        self.labelInfo1.setObjectName("labelInfo1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.labelInfo1)
        self.verticalLayout_2.addLayout(self.formLayout)

        self.retranslateUi(FormCandidates)
        QtCore.QMetaObject.connectSlotsByName(FormCandidates)

    def retranslateUi(self, FormCandidates):
        _translate = QtCore.QCoreApplication.translate
        FormCandidates.setWindowTitle(_translate("FormCandidates", "CANDIDATES PAGE"))
        self.labelMenu.setText(_translate("FormCandidates", "CANDIDATES MENU"))
        self.lineEditSearch.setPlaceholderText(_translate("FormCandidates", "      Name or Surname"))
        self.pushButtonGetCandidates.setText(_translate("FormCandidates", "Get Candidates"))
        self.pushButtonInterviewedCandidates.setText(_translate("FormCandidates", "Interviewed Candidates"))
        self.comboBoxTrainees.setPlaceholderText(_translate("FormCandidates", "              Trainess "))
        self.pushButtonBackMenu.setText(_translate("FormCandidates", "Back Menu"))
        self.pushButtonExit.setText(_translate("FormCandidates", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormCandidates = QtWidgets.QWidget()
    ui = Ui_FormCandidates()
    ui.setupUi(FormCandidates)
    FormCandidates.show()
    sys.exit(app.exec())
