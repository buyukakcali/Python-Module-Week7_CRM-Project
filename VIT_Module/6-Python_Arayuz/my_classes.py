from PyQt6 import QtWidgets, QtCore
import xml.etree.ElementTree as ET
import mysql.connector


# ......................... CONFIGURATION VALUES BEGIN .............................#
class Config:
    def __init__(self):
        self.server_tz = "US/Pacific"
        self.orj_style = """
                        QPushButton{
                            border-radius : 15px;
                            background-color : rgb(25, 200, 200);
                            color: rgb(255, 255, 255); 
                        }
                        
                        QPushButton:hover{
                            background-color: rgb(20, 135, 135);
                            border: 2px solid rgb(255, 80, 0);
                        }
                        
                        QPushButton:focus  {
                          border: 2px solid rgb(162, 0, 0);
                        }
                        
                        QLineEdit {
                            color: darkRed;
                            background-color: rgb(253, 255, 230);
                        }
                        
                        QLineEdit:hover {
                            border: 2px solid rgb(255, 80, 0);
                        }
                        
                        QLineEdit:focus  {
                          border: 2px solid rgb(162, 0, 0);
                        }
                        
                        
                        QToolTip {
                            border-radius: 15px;
                            background-color: yellow; 
                            color: black; 
                            border: 1px solid black;
                        }

                        QComboBox {
                            color: darkRed;
                            border-radius: 5px;
                            padding: 1px 18px 1px 3px;
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
                            border-left-color: darkgray;
                            border-left-style: solid;
                            border-top-right-radius: 3px;
                            border-bottom-right-radius: 3px;
                            border-top-left-radius: 3px;
                            border-bottom-left-radius: 3px;
                        }
                        
                        QComboBox::down-arrow {
                            width: 14px;
                            height: 14px;
                        }
                        
                        QComboBox QAbstractItemView::item {
                            color: rgb(255, 255, 255);
                            border: 1px solid rgb(255, 80, 0);
                            selection-background-color: rgb(245, 245, 245);
                            border-radius: 5px;
                        }
                        
                        QComboBox:hover {
                            border: 2px solid rgb(255, 80, 0); /* Hover ile kenar çizgisi ekleniyor */
                        }
                        
                        QComboBox:focus  {
                          border: 2px solid rgb(162, 0, 0);
                        }
                                                
                        QToolTip {
                            border-radius: 15px;
                            background-color: yellow; 
                            color: black; 
                            border: 1px solid black;
                        }
                    """

        self.applicationTable = "form1_application"
        self.applicationTableFieldNames = ["crm_ID", "crm_ApplicantID", "crm_Timestamp", "crm_Period",
                                           "crm_SuAnkiDurum", "crm_ITPHEgitimKatilmak", "crm_EkonomikDurum",
                                           "crm_DilKursunaDevam", "crm_IngilizceSeviye", "crm_HollandacaSeviye",
                                           "crm_BaskiGoruyor", "crm_BootcampBitirdi", "crm_OnlineITKursu",
                                           "crm_ITTecrube", "crm_ProjeDahil", "crm_CalismakIstedigi",
                                           "crm_NedenKatilmakIstiyor", "crm_MotivasyonunNedir", "crm_FirstInterview",
                                           "crm_SecondInterview"]

        self.applicantTable = "form1_applicant"
        self.applicantTableFieldNames = ["crm_ID", "crm_Timestamp", "crm_Name", "crm_Surname", "crm_Email",
                                         "crm_Phone", "crm_PostCode", "crm_Province"]

        self.appointmentsTable = "appointments_current"
        self.appointmentsTableFieldNames = ["crm_ID", "crm_Timestamp", "crm_EventID", "crm_InterviewDatetime",
                                            "crm_MentorName", "crm_MentorSurname", "crm_MentorMail", "crm_Summary",
                                            "crm_Description", "crm_Location", "crm_OnlineMeetingLink",
                                            "crm_ResponseStatus", "crm_AttendeeID"]

        self.appointments_old_or_deletedTable = "appointments_old_or_deleted"
        self.appointments_old_or_deletedTableFieldNames = ["crm_ID", "crm_WhenDeleted", "crm_ID_Deleted",
                                                           "crm_Timestamp", "crm_EventID", "crm_InterviewDatetime",
                                                           "crm_MentorName", "crm_MentorSurname", "crm_MentorMail",
                                                           "crm_Summary", "crm_Description", "crm_Location",
                                                           "crm_OnlineMeetingLink", "crm_ResponseStatus",
                                                           "crm_AttendeeID"]

        self.evaluationTable = "form2_evaluations"
        self.evaluationTableFieldNames = ["crm_ID", "crm_Timestamp", "crm_Period", "crm_MentorName", "crm_MentorSurname",
                                          "crm_MentorMail", "crm_ApplicantID", "crm_ITSkills",
                                          "crm_Availability", "crm_Recommendation", "crm_Comment",
                                          "crm_ProjectReturnDatetime", "crm_IsApplicantACandidate"]

        self.finalEvaluationTable = "form3_final_evaluations"
        self.finalEvaluationTableFieldNames = ["crm_ID", "crm_Timestamp", "crm_Period", "crm_MentorName",
                                               "crm_MentorSurname", "crm_MentorMail", "crm_CandidateID",
                                               "crm_CodingSkills", "crm_AssistantEvaluation1",
                                               "crm_AssistantEvaluation2", "crm_AssistantEvaluation3",
                                               "crm_MentorEvaluation", "crm_IsCandidateATrainee"]

        self.finalEvaluationOldTable = "form3_final_evaluations_old"
        self.finalEvaluationOldTableFieldNames =["crm_ID", "crm_WhenUpdated", "crm_ID_in_form3_evaluations",
                                                 "crm_Timestamp", "crm_Period", "crm_MentorName",
                                                 "crm_MentorSurname", "crm_MentorMail", "crm_CandidateID",
                                                 "crm_CodingSkills", "crm_AssistantEvaluation1",
                                                 "crm_AssistantEvaluation2", "crm_AssistantEvaluation3",
                                                 "crm_MentorEvaluation", "crm_IsCandidateATrainee"]

        self.google_credentials_file = 'credentials/key.json'   # Your credentials file
        self.google_events_all_interviews_sheet_name = '2-Events_All_Interviews'  # 2-Events_All_Interviews sheet
        self.google_applicant_evaluations_sheet_name = '3-Application_Evaluations_Form_Answers'  # 3-Application_Evaluations_Form_Answers
        self.configuration_sheet_file_name = "configuration"    # configuration sheet name
        self.header_of_parent_folder_column_name = "Project Homeworks Parent Folder Name"
        self.header_of_deadline_column_name = "Project Homework Deadline"

    # Create a connection to the database
    @staticmethod
    def open_conn():
        try:
            tree = ET.parse("credentials/config.xml")
            root = tree.getroot()

            config = {
                "host": root.find("host").text,
                "port": int(root.find("port").text),
                "user": root.find("user").text,
                "password": root.find("password").text,
                "database": root.find("database").text,
                "charset": root.find("charset").text
            }

            conn = mysql.connector.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                passwd=config['password'],
                database=config['database'],
                charset=config['charset']
            )
            # print("MySQL Database connection successful")
            return conn
        except Exception as e:
            raise Exception(f"Error occurred in open_conn static method: {e}")


# ......................... CONFIGURATION VALUES END ..............................#


# Class that allows operations to be performed by converting the type of data held in TableWidget cells to integer,
# which is its original type in string.
class NumericItem(QtWidgets.QTableWidgetItem):
    def __lt__(self, other):
        return (self.data(QtCore.Qt.ItemDataRole.UserRole) <
                other.data(QtCore.Qt.ItemDataRole.UserRole))
