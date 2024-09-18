import mysql.connector
from PyQt6 import QtWidgets, QtCore
from mysql.connector import Error

from credentials import configuration_crm as conf


# ......................... KONFIGURASYON DEGERLERI BASLAR .............................#
class Config:
    def __init__(self):
        self.server_tz = "US/Pacific"

        self.applicationTable = "form1_application"
        self.applicationTableFieldNames = ["crm_ID", "crm_ApplicantID", "crm_Timestamp", "crm_Period",
                                           "crm_SuAnkiDurum", "crm_ITPHEgitimKatilmak", "crm_EkonomikDurum",
                                           "crm_DilKursunaDevam", "crm_IngilizceSeviye", "crm_HollandacaSeviye",
                                           "crm_BaskiGoruyor", "crm_BootcampBitirdi", "crm_OnlineITKursu",
                                           "crm_ITTecrube", "crm_ProjeDahil", "crm_CalismakIstedigi",
                                           "crm_NedenKatilmakIstiyor", "crm_MotivasyonunNedir", "crm_FirstInterview",
                                           "crm_SecondInterview"
                                           ]

        self.applicantTable = "form1_applicant"
        self.applicantTableFieldNames = ["crm_ID", "crm_Timestamp", "crm_Name", "crm_Surname", "crm_Email",
                                         "crm_Phone", "crm_PostCode", "crm_Province"
                                         ]

        self.appointmentsTable = "appointments_current"
        self.appointmentsTableFieldNames = ["crm_ID", "crm_Timestamp", "crm_EventID", "crm_InterviewDatetime",
                                            "crm_MentorName", "crm_MentorSurname", "crm_MentorMail", "crm_Summary",
                                            "crm_Description", "crm_Location", "crm_OnlineMeetingLink",
                                            "crm_ResponseStatus", "crm_AttendeeID"
                                            ]

        self.appointments_old_or_deletedTable = "appointments_old_or_deleted"
        self.appointments_old_or_deletedTableFieldNames = ["crm_ID", "crm_WhenDeleted", "crm_ID_Deleted",
                                                           "crm_Timestamp", "crm_EventID", "crm_InterviewDatetime",
                                                           "crm_MentorName", "crm_MentorSurname", "crm_MentorMail",
                                                           "crm_Summary", "crm_Description", "crm_Location",
                                                           "crm_OnlineMeetingLink", "crm_ResponseStatus",
                                                           "crm_AttendeeID"
                                                           ]

        self.evaluationTable = "form2_evaluations"
        self.evaluationTableFieldNames = ["crm_ID", "crm_Timestamp", "crm_Period", "crm_MentorName", "crm_MentorSurname",
                                          "crm_MentorMail", "crm_Name", "crm_Surname", "crm_Email", "crm_ITSkills",
                                          "crm_Availability", "crm_Recommendation", "crm_Comment",
                                          "crm_IsApplicantACandidate"
                                          ]

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
