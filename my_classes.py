import mysql.connector
from PyQt6 import QtWidgets, QtCore
from mysql.connector import Error

from credentials import configuration_crm as conf


# ......................... KONFIGURASYON DEGERLERI BASLAR .............................#
class Config:
    def __init__(self):
        self.server_tz = "US/Pacific"

        self.applicationTable = "form_application"
        self.applicationTableFieldNames = ["ID", "ApplicantID", "Timestamp_", "Period", "SuAnkiDurum",
                                           "ITPHEgitimKatilmak", "EkonomikDurum", "DilKursunaDevam", "IngilizceSeviye",
                                           "HollandacaSeviye", "BaskiGoruyor", "BootcampBitirdi", "OnlineITKursu",
                                           "ITTecrube", "ProjeDahil", "CalismakIstedigi", "NedenKatilmakIstiyor",
                                           "MotivasyonunNedir", "FirstInterview", "SecondInterview"]

        self.applicantTable = "form_applicant"
        self.applicantTableFieldNames = ["ID", "Timestamp_", "Name", "Surname", "Email", "Phone", "PostCode",
                                         "Province"]

        self.appointmentsTable = "appointments_current"
        self.appointmentsTableFieldNames = ["ID", "Timestamp_", "EventID", "InterviewDatetime", "MentorName",
                                            "MentorSurname", "MentorMail", "Summary", "Description", "Location",
                                            "OnlineMeetingLink", "ResponseStatus", "AttendeeID"]

        self.appointments_old_or_deletedTable = "appointments_old_or_deleted"
        self.appointments_old_or_deletedTableFieldNames = ["ID", "WhenDeleted", "ID_Deleted", "Timestamp_", "EventID",
                                                           "InterviewDatetime", "MentorName", "MentorSurname",
                                                           "MentorMail", "Summary", "Description", "Location",
                                                           "OnlineMeetingLink", "ResponseStatus", "AttendeeID"]

    # Create a connection to the database
    @staticmethod
    def open_conn():
        conn = None
        try:
            conn = mysql.connector.connect(
                host=conf.host,
                user=conf.user,
                passwd=conf.password,
                database=conf.database,
                charset=conf.charset
            )
            # print("MySQL Database connection successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return conn


# ......................... KONFIGURASYON DEGERLERI BITER ..............................#


# Class that allows operations to be performed by converting the type of data held in TableWidget cells to integer,
# which is its original type in string.
class NumericItem(QtWidgets.QTableWidgetItem):
    def __lt__(self, other):
        return (self.data(QtCore.Qt.ItemDataRole.UserRole) <
                other.data(QtCore.Qt.ItemDataRole.UserRole))
