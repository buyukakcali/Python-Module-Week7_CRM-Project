# Form implementation generated from reading ui file 'user_admin_preference_ui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 500)
        Form.setMinimumSize(QtCore.QSize(500, 500))
        Form.setMaximumSize(QtCore.QSize(500, 500))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pictures/wehere_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.499773, y1:1, x2:0.5, y2:0.00568182, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(120, 20, 261, 101))
        self.label.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pictures/wehere_logo.ico"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(80, 130, 341, 311))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("pictures/user_loop.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.pushButton_user_admin_exit = QtWidgets.QPushButton(parent=Form)
        self.pushButton_user_admin_exit.setGeometry(QtCore.QRect(278, 341, 75, 75))
        self.pushButton_user_admin_exit.setMinimumSize(QtCore.QSize(75, 75))
        self.pushButton_user_admin_exit.setMaximumSize(QtCore.QSize(75, 75))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        self.pushButton_user_admin_exit.setFont(font)
        self.pushButton_user_admin_exit.setStyleSheet("QPushButton{\n"
"    border-radius : 37px;\n"
"    background-color: rgb(243, 199, 65);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    \n"
"    background-color: rgb(162, 132, 43);\n"
"}\n"
"")
        self.pushButton_user_admin_exit.setObjectName("pushButton_user_admin_exit")
        self.pushButton_user_admin_applications = QtWidgets.QPushButton(parent=Form)
        self.pushButton_user_admin_applications.setGeometry(QtCore.QRect(213, 155, 75, 75))
        self.pushButton_user_admin_applications.setMinimumSize(QtCore.QSize(75, 75))
        self.pushButton_user_admin_applications.setMaximumSize(QtCore.QSize(75, 75))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        self.pushButton_user_admin_applications.setFont(font)
        self.pushButton_user_admin_applications.setStyleSheet("QPushButton{\n"
"    border-radius : 37px;\n"
"    \n"
"    background-color: rgb(0, 204, 209);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    \n"
"    \n"
"    background-color: rgb(0, 251, 255);\n"
"}\n"
"")
        self.pushButton_user_admin_applications.setObjectName("pushButton_user_admin_applications")
        self.pushButton_user_admin_menu = QtWidgets.QPushButton(parent=Form)
        self.pushButton_user_admin_menu.setGeometry(QtCore.QRect(210, 250, 75, 75))
        self.pushButton_user_admin_menu.setMinimumSize(QtCore.QSize(75, 75))
        self.pushButton_user_admin_menu.setMaximumSize(QtCore.QSize(75, 75))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        self.pushButton_user_admin_menu.setFont(font)
        self.pushButton_user_admin_menu.setStyleSheet("QPushButton{\n"
"    border-radius : 37px;\n"
"    background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 123, 0, 255), stop:1 rgba(0, 255, 255, 255));\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    \n"
"    background-color: rgb(0, 170, 28);\n"
"}\n"
"")
        self.pushButton_user_admin_menu.setObjectName("pushButton_user_admin_menu")
        self.pushButton_user_admin_mentor_meeting = QtWidgets.QPushButton(parent=Form)
        self.pushButton_user_admin_mentor_meeting.setGeometry(QtCore.QRect(106, 224, 75, 75))
        self.pushButton_user_admin_mentor_meeting.setMinimumSize(QtCore.QSize(75, 75))
        self.pushButton_user_admin_mentor_meeting.setMaximumSize(QtCore.QSize(75, 75))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        self.pushButton_user_admin_mentor_meeting.setFont(font)
        self.pushButton_user_admin_mentor_meeting.setStyleSheet("QPushButton{\n"
"    border-radius : 37px;\n"
"    background-color: rgb(255, 109, 102);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(195, 82, 78);\n"
"}\n"
"")
        self.pushButton_user_admin_mentor_meeting.setObjectName("pushButton_user_admin_mentor_meeting")
        self.pushButton_user_admin_login_page = QtWidgets.QPushButton(parent=Form)
        self.pushButton_user_admin_login_page.setGeometry(QtCore.QRect(150, 342, 75, 75))
        self.pushButton_user_admin_login_page.setMinimumSize(QtCore.QSize(75, 75))
        self.pushButton_user_admin_login_page.setMaximumSize(QtCore.QSize(75, 75))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        self.pushButton_user_admin_login_page.setFont(font)
        self.pushButton_user_admin_login_page.setStyleSheet("QPushButton{\n"
"    border-radius : 37px;\n"
"    background-color: rgb(255, 140, 61);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(184, 100, 44);\n"
"}\n"
"")
        self.pushButton_user_admin_login_page.setObjectName("pushButton_user_admin_login_page")
        self.pushButton_user_admin_interviews = QtWidgets.QPushButton(parent=Form)
        self.pushButton_user_admin_interviews.setGeometry(QtCore.QRect(319, 223, 75, 75))
        self.pushButton_user_admin_interviews.setMinimumSize(QtCore.QSize(75, 75))
        self.pushButton_user_admin_interviews.setMaximumSize(QtCore.QSize(75, 75))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        self.pushButton_user_admin_interviews.setFont(font)
        self.pushButton_user_admin_interviews.setStyleSheet("QPushButton{\n"
"    border-radius : 37px;\n"
"    background-color: rgb(0, 108, 143);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(0, 152, 198);\n"
"}\n"
"")
        self.pushButton_user_admin_interviews.setObjectName("pushButton_user_admin_interviews")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "USER ADMIN PREFENCE"))
        self.pushButton_user_admin_exit.setText(_translate("Form", "Exit"))
        self.pushButton_user_admin_applications.setText(_translate("Form", "Applications"))
        self.pushButton_user_admin_menu.setText(_translate("Form", "Admin\n"
"Menu"))
        self.pushButton_user_admin_mentor_meeting.setText(_translate("Form", "Mentor \n"
"Meeting"))
        self.pushButton_user_admin_login_page.setText(_translate("Form", "Login \n"
"Page"))
        self.pushButton_user_admin_interviews.setText(_translate("Form", "Interviews"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
