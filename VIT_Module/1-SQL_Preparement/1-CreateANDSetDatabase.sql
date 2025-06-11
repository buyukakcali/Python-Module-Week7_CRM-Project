CREATE DATABASE IF NOT EXISTS durakoku_crm_v10 DEFAULT CHARACTER SET utf8mb4  DEFAULT COLLATE utf8mb4_turkish_ci ;

USE durakoku_crm_v10;


START TRANSACTION;

CREATE TABLE `users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `RegistrationDatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Username` varchar(44) NOT NULL,
  `Password` text NOT NULL,
  `Authority` varchar(45) NOT NULL,
  `UName` varchar(64) NOT NULL,
  `USurname` varchar(64) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Username_UNIQUE` (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form1_data` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_RowID` int(11) NOT NULL,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Period` varchar(10) NOT NULL,
  `crm_Name` varchar(64) NOT NULL,
  `crm_Surname` varchar(64) NOT NULL,
  `crm_Email` varchar(64) NOT NULL,
  `crm_Phone` varchar(44) NOT NULL,
  `crm_PostCode` varchar(22) NOT NULL,
  `crm_Province` varchar(64) NOT NULL,
  `crm_SuAnkiDurum` text NOT NULL,
  `crm_EgitimDurum` text NOT NULL,
  `crm_EkonomikDurum` text NOT NULL,
  `crm_DilKursunaDevam` text NOT NULL,
  `crm_IngilizceSeviye` varchar(3) NOT NULL,
  `crm_HollandacaSeviye` varchar(3) NOT NULL,
  `crm_UAFDurum` varchar(5) NOT NULL,
  `crm_BootcampOrOtherCourse` text NOT NULL,
  `crm_ITTecrube` text NOT NULL,
  `crm_ProjeDahil` text NOT NULL,
  `crm_CalismakIstedigi` text NOT NULL,  
  `crm_Sorular` text NOT NULL,
  `crm_MotivasyonunNedir` text NOT NULL,
  `crm_GelecekPlani` text NOT NULL,
  `crm_SaatKarisikligiOnay` varchar(5) NOT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form1_applicant` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Name` varchar(64) NOT NULL,
  `crm_Surname` varchar(64) NOT NULL,
  `crm_Email` varchar(64) NOT NULL,
  `crm_Phone` varchar(44) NOT NULL,
  `crm_PostCode` varchar(22) NOT NULL,
  `crm_Province` varchar(64) NOT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form1_application` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_ApplicantID` int(11) NOT NULL,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Period` varchar(10) NOT NULL,
  `crm_SuAnkiDurum` text NOT NULL,
  `crm_EgitimDurum` text NOT NULL,
  `crm_EkonomikDurum` text NOT NULL,
  `crm_DilKursunaDevam` text NOT NULL,
  `crm_IngilizceSeviye` varchar(3) NOT NULL,
  `crm_HollandacaSeviye` varchar(3) NOT NULL,
  `crm_UAFDurum` varchar(5) NOT NULL,
  `crm_BootcampOrOtherCourse` text NOT NULL,
  `crm_ITTecrube` text NOT NULL,
  `crm_ProjeDahil` text NOT NULL,
  `crm_CalismakIstedigi` text NOT NULL,
  `crm_Sorular` text NOT NULL,
  `crm_MotivasyonunNedir` text NOT NULL,
  `crm_GelecekPlani` text NOT NULL,
  `crm_SaatKarisikligiOnay` varchar(5) NOT NULL,
  `crm_FirstInterview` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`crm_ID`),
  KEY `fk_form1_application_idx` (`crm_ApplicantID`),
  CONSTRAINT `fk_form1_application` FOREIGN KEY (`crm_ApplicantID`) REFERENCES `form1_applicant` (`crm_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form1_applicant_old` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_ID_in_applicantTable` int(11) DEFAULT NULL,
  `crm_WhenUpdated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `crm_Timestamp` datetime DEFAULT NULL,
  `crm_Name` varchar(64) DEFAULT NULL,
  `crm_Surname` varchar(64) DEFAULT NULL,
  `crm_Email` varchar(64) DEFAULT NULL,
  `crm_Phone` varchar(44) DEFAULT NULL,
  `crm_PostCode` varchar(22) DEFAULT NULL,
  `crm_Province` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form1_application_old` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_ID_in_applicationTable` int(11) DEFAULT NULL,
  `crm_WhenUpdated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `crm_ApplicantID` int(11) DEFAULT NULL,
  `crm_Timestamp` datetime DEFAULT NULL,
  `crm_Period` varchar(10) DEFAULT NULL,
  `crm_SuAnkiDurum` text DEFAULT NULL,
  `crm_EgitimDurum` text DEFAULT NULL,
  `crm_EkonomikDurum` text DEFAULT NULL,
  `crm_DilKursunaDevam` text DEFAULT NULL,
  `crm_IngilizceSeviye` varchar(3) DEFAULT NULL,
  `crm_HollandacaSeviye` varchar(3) DEFAULT NULL,
  `crm_UAFDurum` varchar(5) DEFAULT NULL,
  `crm_BootcampOrOtherCourse` text DEFAULT NULL,
  `crm_ITTecrube` text DEFAULT NULL,
  `crm_ProjeDahil` text DEFAULT NULL,
  `crm_CalismakIstedigi` text DEFAULT NULL,
  `crm_Sorular` text DEFAULT NULL,
  `crm_MotivasyonunNedir` text DEFAULT NULL,
  `crm_GelecekPlani` text DEFAULT NULL,
  `crm_SaatKarisikligiOnay` varchar(5) DEFAULT NULL,
  `crm_FirstInterview` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `appointments_current` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_Timestamp` datetime NOT NULL,
  `crm_EventID` varchar(255) NOT NULL,
  `crm_InterviewDatetime` datetime NOT NULL,
  `crm_MentorName` varchar(64) DEFAULT NULL,
  `crm_MentorSurname` varchar(64) DEFAULT NULL,
  `crm_MentorMail` varchar(64) NOT NULL,
  `crm_Summary` text DEFAULT NULL,
  `crm_Description` text DEFAULT NULL,
  `crm_Location` text DEFAULT NULL,
  `crm_OnlineMeetingLink` text DEFAULT NULL,
  `crm_ResponseStatus` text DEFAULT NULL,
  `crm_AttendeeEmails` text DEFAULT NULL,
  `crm_AttendeeID` int(11) DEFAULT NULL,
  PRIMARY KEY (`crm_ID`),
  UNIQUE KEY `EventID_UNIQUE` (`crm_EventID`(255)),
  KEY `fk_appointments_current_idx` (`crm_AttendeeID`),
  CONSTRAINT `fk_appointments_current` FOREIGN KEY (`crm_AttendeeID`) REFERENCES `form1_applicant` (`crm_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `appointments_old_or_deleted` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_WhenDeleted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `crm_ID_Deleted` int(11) NOT NULL,
  `crm_Timestamp` datetime NOT NULL,
  `crm_EventID` varchar(255) NOT NULL,
  `crm_InterviewDatetime` datetime NOT NULL,
  `crm_MentorName` varchar(64) DEFAULT NULL,
  `crm_MentorSurname` varchar(64) DEFAULT NULL,
  `crm_MentorMail` varchar(64) NOT NULL,
  `crm_Summary` text DEFAULT NULL,
  `crm_Description` text DEFAULT NULL,
  `crm_Location` text DEFAULT NULL,
  `crm_OnlineMeetingLink` text DEFAULT NULL,
  `crm_AttendeeEmails` text DEFAULT NULL,
  `crm_ResponseStatus` text DEFAULT NULL,
  `crm_AttendeeID` int(11) DEFAULT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form2_data` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_RowID` int(11) NOT NULL,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Period` varchar(10) NOT NULL,
  `crm_MentorMail` varchar(64) NOT NULL,
  `crm_ApplicantMail` varchar(64) NOT NULL,
  `crm_ITSkills` int(11) NOT NULL,
  `crm_Availability` int(11) NOT NULL,
  `crm_Recommendation` text NOT NULL,
  `crm_Comment` text DEFAULT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form2_evaluations` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Period` varchar(10) NOT NULL,
  `crm_MentorName` varchar(64) NOT NULL,
  `crm_MentorSurname` varchar(64) NOT NULL,
  `crm_MentorMail` varchar(64) NOT NULL,
  `crm_ApplicantID` int(11) NOT NULL,
  `crm_ITSkills` int(11) NOT NULL,
  `crm_Availability` int(11) NOT NULL,
  `crm_Recommendation` text NOT NULL,
  `crm_Comment` text NOT NULL,
  `crm_ProjectReturnDatetime` datetime DEFAULT NULL,
  `crm_IsApplicantACandidate` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`crm_ID`),
  KEY `fk_form2_evaluations_idx` (`crm_ApplicantID`),
  CONSTRAINT `fk_form2_evaluations` FOREIGN KEY (`crm_ApplicantID`) REFERENCES `form1_applicant` (`crm_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form2_evaluations_old` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_WhenUpdated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `crm_ID_in_form2_evaluations` int(11) DEFAULT NULL,
  `crm_Timestamp` datetime DEFAULT NULL,
  `crm_Period` varchar(10) DEFAULT NULL,
  `crm_MentorName` varchar(64) DEFAULT NULL,
  `crm_MentorSurname` varchar(64) DEFAULT NULL,
  `crm_MentorMail` varchar(64) DEFAULT NULL,
  `crm_ApplicantID` int(11) DEFAULT NULL,
  `crm_ITSkills` int(11) DEFAULT NULL,
  `crm_Availability` int(11) DEFAULT NULL,
  `crm_Recommendation` text DEFAULT NULL,
  `crm_Comment` text DEFAULT NULL,
  `crm_ProjectReturnDatetime` datetime DEFAULT NULL,
  `crm_IsApplicantACandidate` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form3_data` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_RowID` int(11) NOT NULL,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Period` varchar(10) NOT NULL,
  `crm_MentorMail` varchar(64) NOT NULL,
  `crm_CandidateMail` varchar(64) NOT NULL,
  `crm_CodingSkills` int(11) NOT NULL,
  `crm_AssistantEvaluation1` text NOT NULL,
  `crm_AssistantEvaluation2` text NOT NULL,
  `crm_AssistantEvaluation3` text NOT NULL,
  `crm_MentorEvaluation` text NOT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form3_final_evaluations` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Period` varchar(10) NOT NULL,
  `crm_MentorName` varchar(64) NOT NULL,
  `crm_MentorSurname` varchar(64) NOT NULL,
  `crm_MentorMail` varchar(64) NOT NULL,
  `crm_CandidateID` int(11) NOT NULL,
  `crm_CodingSkills` int(11) NOT NULL,
  `crm_AssistantEvaluation1` text NOT NULL,
  `crm_AssistantEvaluation2` text NOT NULL,
  `crm_AssistantEvaluation3` text NOT NULL,
  `crm_MentorEvaluation` text NOT NULL,
  `crm_IsCandidateATrainee` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`crm_ID`),
  KEY `fk_form3_evaluations_idx` (`crm_CandidateID`),
  CONSTRAINT `fk_form3_evaluations` FOREIGN KEY (`crm_CandidateID`) REFERENCES `form1_applicant` (`crm_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form3_final_evaluations_old` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_WhenUpdated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `crm_ID_in_form3_final_evaluations` int(11) DEFAULT NULL,
  `crm_Timestamp` datetime DEFAULT NULL,
  `crm_Period` varchar(10) DEFAULT NULL,
  `crm_MentorName` varchar(64) DEFAULT NULL,
  `crm_MentorSurname` varchar(64) DEFAULT NULL,
  `crm_MentorMail` varchar(64) DEFAULT NULL,
  `crm_CandidateID` int(11) DEFAULT NULL,
  `crm_CodingSkills` int(11) DEFAULT NULL,
  `crm_AssistantEvaluation1` text DEFAULT NULL,
  `crm_AssistantEvaluation2` text DEFAULT NULL,
  `crm_AssistantEvaluation3` text DEFAULT NULL,
  `crm_MentorEvaluation` text DEFAULT NULL,
  `crm_IsCandidateATrainee` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `crm_trigger_logs` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `log_message` text DEFAULT NULL,
  `log_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `crm_warnings` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_log_message` text DEFAULT NULL,
  `crm_log_time` datetime DEFAULT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

INSERT INTO users (Username, Password, Authority, UName, USurname) VALUES ('admin', '$2b$12$/2tQZ/X3Obnpzscb.8dbYeFPYJKnasCqRnY3wylTzukcySwTrb3Vi' , 'admin', 'admin', 'admin');

DELIMITER //

CREATE TRIGGER trg_after_insert_form1_data
AFTER INSERT ON form1_data
FOR EACH ROW
BEGIN
    DECLARE applicantID INT;
    DECLARE newID INT;
    
    -- Applicant control via email
    SELECT crm_ID INTO applicantID FROM form1_applicant WHERE crm_Email = NEW.crm_Email LIMIT 1;
    
    -- If there is no applicant
    IF applicantID IS NULL THEN
    -- add new applicant
        INSERT INTO form1_applicant (crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province)
        VALUES (NEW.crm_Timestamp, NEW.crm_Name, NEW.crm_Surname, NEW.crm_Email, NEW.crm_Phone, NEW.crm_PostCode, NEW.crm_Province);
        SET applicantID = LAST_INSERT_ID();        
        -- add log
		INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('New applicant is added to form1_applicant table', NEW.crm_Timestamp);
        
        -- add new application
        INSERT INTO form1_application (crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_EgitimDurum, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_UAFDurum, crm_BootcampOrOtherCourse, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_Sorular, crm_MotivasyonunNedir, crm_GelecekPlani, crm_SaatKarisikligiOnay)
        VALUES (applicantID, NEW.crm_Timestamp, NEW.crm_Period, NEW.crm_SuAnkiDurum, NEW.crm_EgitimDurum, NEW.crm_EkonomikDurum, NEW.crm_DilKursunaDevam, NEW.crm_IngilizceSeviye, NEW.crm_HollandacaSeviye, NEW.crm_UAFDurum, NEW.crm_BootcampOrOtherCourse, NEW.crm_ITTecrube, NEW.crm_ProjeDahil, NEW.crm_CalismakIstedigi, NEW.crm_Sorular, NEW.crm_MotivasyonunNedir, NEW.crm_GelecekPlani, NEW.crm_SaatKarisikligiOnay);
        -- add log
		INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('New application is added to form1_application table', NEW.crm_Timestamp);
    ELSE
        -- <<< Under ELSE here, the Applicant information will be updated! >>> --
        -- This is the part that does the most complicated work. 
        -- If the person wants to update their application with the same email address a few days later, it works. 
        
        -- >> Check the applicant's data and update if there are any changes
        IF (SELECT crm_Name FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Name OR
           (SELECT crm_Surname FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Surname OR
           (SELECT crm_Phone FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Phone OR
           (SELECT crm_PostCode FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_PostCode OR
           (SELECT crm_Province FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Province THEN 			
				INSERT INTO form1_applicant_old (crm_ID_in_ApplicantTable, crm_WhenUpdated, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province)
				SELECT crm_ID, NEW.crm_Timestamp, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province
				FROM form1_applicant
				WHERE crm_ID = applicantID;
            
				UPDATE form1_applicant
				SET crm_Timestamp = NEW.crm_Timestamp, crm_Name = NEW.crm_Name, crm_Surname = NEW.crm_Surname, crm_Phone = NEW.crm_Phone, crm_PostCode = NEW.crm_PostCode, crm_Province = NEW.crm_Province
				WHERE crm_ID = applicantID;            
            -- add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(WITH NEW FORM FILLING) Applicant information is updated "in trg_after_insert_form1_data"', NEW.crm_Timestamp);
        END IF;
        -- <<< -------------------------- >>> --
        
        -- Application period control and addition/update        
        SELECT crm_ID INTO newID FROM form1_application WHERE crm_ApplicantID = applicantID AND crm_Period = NEW.crm_Period;
        
        IF newID IS NULL THEN
            INSERT INTO form1_application (crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_EgitimDurum, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_UAFDurum, crm_BootcampOrOtherCourse, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_Sorular, crm_MotivasyonunNedir, crm_GelecekPlani, crm_SaatKarisikligiOnay)
			VALUES (applicantID, NEW.crm_Timestamp, NEW.crm_Period, NEW.crm_SuAnkiDurum, NEW.crm_EgitimDurum, NEW.crm_EkonomikDurum, NEW.crm_DilKursunaDevam, NEW.crm_IngilizceSeviye, NEW.crm_HollandacaSeviye, NEW.crm_UAFDurum, NEW.crm_BootcampOrOtherCourse, NEW.crm_ITTecrube, NEW.crm_ProjeDahil, NEW.crm_CalismakIstedigi, NEW.crm_Sorular, NEW.crm_MotivasyonunNedir, NEW.crm_GelecekPlani, NEW.crm_SaatKarisikligiOnay);
        -- add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('New application of existing applicant is added to form1_application table', NEW.crm_Timestamp);
        ELSE
			-- <<< Here, under ELSE, the Application information will be updated! >>> --
			-- This is the part that does the most complicated work. 
            -- If the person wants to update their application with the same email address a few days later, it works. 
            
            -- >> Check the application's data and update if there are any changes
			IF (SELECT crm_SuAnkiDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_SuAnkiDurum OR
               (SELECT crm_EgitimDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_EgitimDurum OR
               (SELECT crm_EkonomikDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_EkonomikDurum OR
               (SELECT crm_DilKursunaDevam FROM form1_application WHERE crm_ID = newID) <> NEW.crm_DilKursunaDevam OR
               (SELECT crm_IngilizceSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_IngilizceSeviye OR
               (SELECT crm_HollandacaSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_HollandacaSeviye OR
               (SELECT crm_UAFDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_UAFDurum OR
               (SELECT crm_BootcampOrOtherCourse FROM form1_application WHERE crm_ID = newID) <> NEW.crm_BootcampOrOtherCourse OR
               (SELECT crm_ITTecrube FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ITTecrube OR
               (SELECT crm_ProjeDahil FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ProjeDahil OR
               (SELECT crm_CalismakIstedigi FROM form1_application WHERE crm_ID = newID) <> NEW.crm_CalismakIstedigi OR
               (SELECT crm_Sorular FROM form1_application WHERE crm_ID = newID) <> NEW.crm_Sorular OR
               (SELECT crm_MotivasyonunNedir FROM form1_application WHERE crm_ID = newID) <> NEW.crm_MotivasyonunNedir OR
               (SELECT crm_GelecekPlani FROM form1_application WHERE crm_ID = newID) <> NEW.crm_GelecekPlani OR
               (SELECT crm_SaatKarisikligiOnay FROM form1_application WHERE crm_ID = newID) <> NEW.crm_SaatKarisikligiOnay THEN	-- controls of other columns will come here
					INSERT INTO form1_application_old (crm_ID_in_applicationTable, crm_WhenUpdated, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_EgitimDurum, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_UAFDurum, crm_BootcampOrOtherCourse, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_Sorular, crm_MotivasyonunNedir, crm_GelecekPlani, crm_SaatKarisikligiOnay, crm_FirstInterview) 
					SELECT crm_ID, NEW.crm_Timestamp, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_EgitimDurum, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_UAFDurum, crm_BootcampOrOtherCourse, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_Sorular, crm_MotivasyonunNedir, crm_GelecekPlani, crm_SaatKarisikligiOnay, crm_FirstInterview 
					FROM form1_application 
					WHERE crm_ID = newID;
						
					UPDATE form1_application 
					SET crm_Timestamp = NEW.crm_Timestamp, crm_SuAnkiDurum = NEW.crm_SuAnkiDurum, crm_EgitimDurum = NEW.crm_EgitimDurum, crm_EkonomikDurum = NEW.crm_EkonomikDurum, crm_DilKursunaDevam = NEW.crm_DilKursunaDevam, crm_IngilizceSeviye = NEW.crm_IngilizceSeviye, crm_HollandacaSeviye = NEW.crm_HollandacaSeviye, crm_UAFDurum = NEW.crm_UAFDurum, crm_BootcampOrOtherCourse = NEW.crm_BootcampOrOtherCourse, crm_ITTecrube = NEW.crm_ITTecrube, crm_ProjeDahil = NEW.crm_ProjeDahil, crm_CalismakIstedigi = NEW.crm_CalismakIstedigi, crm_Sorular = NEW.crm_Sorular, crm_MotivasyonunNedir = NEW.crm_MotivasyonunNedir, crm_GelecekPlani = NEW.crm_GelecekPlani, crm_SaatKarisikligiOnay = NEW.crm_SaatKarisikligiOnay 
					WHERE crm_ID = newID;
                -- add log
                INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(WITH NEW FORM FILLING) Application information is updated "in trg_after_insert_form1_data"', NEW.crm_Timestamp);
            END IF;
            -- <<< -------------------------- >>> --
            
        END IF;
    END IF;
    -- add log to verify that the trigger worked
    INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('trg_after_insert_form1_data trigger is executed', NEW.crm_Timestamp);
END//

DELIMITER ;



DELIMITER //

CREATE TRIGGER trg_after_update_form1_data
AFTER UPDATE ON form1_data
FOR EACH ROW
BEGIN
    DECLARE applicantID INT;
    DECLARE newID INT;
    
    -- Applicant control via email
    SELECT crm_ID INTO applicantID FROM form1_applicant WHERE crm_Email = NEW.crm_Email LIMIT 1;
    
    -- If there is no applicant, he/she is POSSIBLY changing his/her email address. (Expected to be rare), add log and update applicant information
    IF applicantID IS NULL THEN    
		-- ******************* --
        
		-- CHECK FROM OLD EMAIL
        SELECT crm_ID INTO applicantID FROM form1_applicant WHERE crm_Email = OLD.crm_Email LIMIT 1;
        
        -- (OLD) Check the applicant's data and update if there are any changes
        IF (SELECT crm_Name FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Name OR
           (SELECT crm_Surname FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Surname OR
           (SELECT crm_Email FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Email OR
           (SELECT crm_Phone FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Phone OR
           (SELECT crm_PostCode FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_PostCode OR
           (SELECT crm_Province FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Province THEN 
				INSERT INTO form1_applicant_old (crm_ID_in_ApplicantTable, crm_WhenUpdated, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province) 
				SELECT crm_ID, NEW.crm_Timestamp, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province 
				FROM form1_applicant 
				WHERE crm_ID = applicantID;
				
				UPDATE form1_applicant
				SET crm_Timestamp = NEW.crm_Timestamp, crm_Name = NEW.crm_Name, crm_Surname = NEW.crm_Surname, crm_Email = NEW.crm_Email, crm_Phone = NEW.crm_Phone, crm_PostCode = NEW.crm_PostCode, crm_Province = NEW.crm_Province
				WHERE crm_ID = applicantID;
            -- (OLD) add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(OLD) Application information (including email address) is updated "in trg_after_update_form1_data"', NEW.crm_Timestamp);
		ELSE
            INSERT INTO crm_trigger_logs (log_message, log_time)
            VALUES (CONCAT('(OLD) It means there is an error right now that I don\'t know why... ("in trg_after_update_form1_data") Line Number: ', (SELECT crm_RowID FROM form1_data WHERE crm_Email = OLD.crm_Email)), NEW.crm_Timestamp);
		END IF;
        
        -- (OLD) Application period control and addition/update
        SELECT crm_ID INTO newID FROM form1_application WHERE crm_ApplicantID = applicantID AND crm_Period = NEW.crm_Period;    
        IF newID IS NULL THEN        
            -- (OLD) add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(OLD) Unexpected code situation! This code shuldn\'t be executed... ("in trg_after_update_form1_data")', NEW.crm_Timestamp);
        ELSE
            -- (OLD) Check the application's data and update if there are any changes
			IF (SELECT crm_SuAnkiDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_SuAnkiDurum OR
               (SELECT crm_EgitimDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_EgitimDurum OR
               (SELECT crm_EkonomikDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_EkonomikDurum OR
               (SELECT crm_DilKursunaDevam FROM form1_application WHERE crm_ID = newID) <> NEW.crm_DilKursunaDevam OR
               (SELECT crm_IngilizceSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_IngilizceSeviye OR
               (SELECT crm_HollandacaSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_HollandacaSeviye OR
               (SELECT crm_UAFDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_UAFDurum OR
               (SELECT crm_BootcampOrOtherCourse FROM form1_application WHERE crm_ID = newID) <> NEW.crm_BootcampOrOtherCourse OR
               (SELECT crm_ITTecrube FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ITTecrube OR
               (SELECT crm_ProjeDahil FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ProjeDahil OR
               (SELECT crm_CalismakIstedigi FROM form1_application WHERE crm_ID = newID) <> NEW.crm_CalismakIstedigi OR
               (SELECT crm_Sorular FROM form1_application WHERE crm_ID = newID) <> NEW.crm_Sorular OR
               (SELECT crm_MotivasyonunNedir FROM form1_application WHERE crm_ID = newID) <> NEW.crm_MotivasyonunNedir OR
               (SELECT crm_GelecekPlani FROM form1_application WHERE crm_ID = newID) <> NEW.crm_GelecekPlani OR
               (SELECT crm_SaatKarisikligiOnay FROM form1_application WHERE crm_ID = newID) <> NEW.crm_SaatKarisikligiOnay THEN	-- controls of other columns will come here
					INSERT INTO form1_application_old (crm_ID_in_applicationTable, crm_WhenUpdated, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_EgitimDurum, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_UAFDurum, crm_BootcampOrOtherCourse, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_Sorular, crm_MotivasyonunNedir, crm_GelecekPlani, crm_SaatKarisikligiOnay, crm_FirstInterview) 
					SELECT crm_ID, NEW.crm_Timestamp, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_EgitimDurum, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_UAFDurum, crm_BootcampOrOtherCourse, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_Sorular, crm_MotivasyonunNedir, crm_GelecekPlani, crm_SaatKarisikligiOnay, crm_FirstInterview 
					FROM form1_application 
					WHERE crm_ID = newID;
						
					UPDATE form1_application 
					SET crm_Timestamp = NEW.crm_Timestamp, crm_SuAnkiDurum = NEW.crm_SuAnkiDurum, crm_EgitimDurum = NEW.crm_EgitimDurum, crm_EkonomikDurum = NEW.crm_EkonomikDurum, crm_DilKursunaDevam = NEW.crm_DilKursunaDevam, crm_IngilizceSeviye = NEW.crm_IngilizceSeviye, crm_HollandacaSeviye = NEW.crm_HollandacaSeviye, crm_UAFDurum = NEW.crm_UAFDurum, crm_BootcampOrOtherCourse = NEW.crm_BootcampOrOtherCourse, crm_ITTecrube = NEW.crm_ITTecrube, crm_ProjeDahil = NEW.crm_ProjeDahil, crm_CalismakIstedigi = NEW.crm_CalismakIstedigi, crm_Sorular = NEW.crm_Sorular, crm_MotivasyonunNedir = NEW.crm_MotivasyonunNedir, crm_GelecekPlani = NEW.crm_GelecekPlani, crm_SaatKarisikligiOnay = NEW.crm_SaatKarisikligiOnay 
					WHERE crm_ID = newID;
				-- (OLD) add log
				INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(OLD) Application information is updated "in trg_after_update_form1_data"', NEW.crm_Timestamp);
			END IF;
        END IF;        
        -- ******************* --
        
    ELSE
        -- Check the applicant's data and update if there are any changes
        IF (SELECT crm_Name FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Name OR
           (SELECT crm_Surname FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Surname OR
           (SELECT crm_Phone FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Phone OR
           (SELECT crm_PostCode FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_PostCode OR
           (SELECT crm_Province FROM form1_applicant WHERE crm_ID = applicantID) <> NEW.crm_Province THEN
				INSERT INTO form1_applicant_old (crm_ID_in_ApplicantTable, crm_WhenUpdated, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province)
				SELECT crm_ID, NEW.crm_Timestamp, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province
				FROM form1_applicant
				WHERE crm_ID = applicantID;
				
				UPDATE form1_applicant
				SET crm_Timestamp = NEW.crm_Timestamp, crm_Name = NEW.crm_Name, crm_Surname = NEW.crm_Surname, crm_Phone = NEW.crm_Phone, crm_PostCode = NEW.crm_PostCode, crm_Province = NEW.crm_Province
				WHERE crm_ID = applicantID;           
            -- add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('Applicant information is updated "in trg_after_update_form1_data"', NEW.crm_Timestamp);
        END IF;
        
        -- Application period control and addition/update
        SELECT crm_ID INTO newID FROM form1_application WHERE crm_ApplicantID = applicantID AND crm_Period = NEW.crm_Period;
        IF newID IS NULL THEN        
            -- add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('Unexpected code situation! This code shuldn\'t be executed... ("in trg_after_update_form1_data")', NEW.crm_Timestamp);
        ELSE
            -- Check the application's data and update if there are any changes
			IF (SELECT crm_SuAnkiDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_SuAnkiDurum OR
               (SELECT crm_EgitimDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_EgitimDurum OR
               (SELECT crm_EkonomikDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_EkonomikDurum OR
               (SELECT crm_DilKursunaDevam FROM form1_application WHERE crm_ID = newID) <> NEW.crm_DilKursunaDevam OR
               (SELECT crm_IngilizceSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_IngilizceSeviye OR
               (SELECT crm_HollandacaSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_HollandacaSeviye OR
               (SELECT crm_UAFDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_UAFDurum OR
               (SELECT crm_BootcampOrOtherCourse FROM form1_application WHERE crm_ID = newID) <> NEW.crm_BootcampOrOtherCourse OR
               (SELECT crm_ITTecrube FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ITTecrube OR
               (SELECT crm_ProjeDahil FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ProjeDahil OR
               (SELECT crm_CalismakIstedigi FROM form1_application WHERE crm_ID = newID) <> NEW.crm_CalismakIstedigi OR
               (SELECT crm_Sorular FROM form1_application WHERE crm_ID = newID) <> NEW.crm_Sorular OR
               (SELECT crm_MotivasyonunNedir FROM form1_application WHERE crm_ID = newID) <> NEW.crm_MotivasyonunNedir OR
               (SELECT crm_GelecekPlani FROM form1_application WHERE crm_ID = newID) <> NEW.crm_GelecekPlani OR
               (SELECT crm_SaatKarisikligiOnay FROM form1_application WHERE crm_ID = newID) <> NEW.crm_SaatKarisikligiOnay THEN	-- controls of other columns will come here
					INSERT INTO form1_application_old (crm_ID_in_applicationTable, crm_WhenUpdated, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_EgitimDurum, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_UAFDurum, crm_BootcampOrOtherCourse, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_Sorular, crm_MotivasyonunNedir, crm_GelecekPlani, crm_SaatKarisikligiOnay, crm_FirstInterview) 
					SELECT crm_ID, NEW.crm_Timestamp, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_EgitimDurum, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_UAFDurum, crm_BootcampOrOtherCourse, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_Sorular, crm_MotivasyonunNedir, crm_GelecekPlani, crm_SaatKarisikligiOnay, crm_FirstInterview 
					FROM form1_application 
					WHERE crm_ID = newID;
						
					UPDATE form1_application 
					SET crm_Timestamp = NEW.crm_Timestamp, crm_SuAnkiDurum = NEW.crm_SuAnkiDurum, crm_EgitimDurum = NEW.crm_EgitimDurum, crm_EkonomikDurum = NEW.crm_EkonomikDurum, crm_DilKursunaDevam = NEW.crm_DilKursunaDevam, crm_IngilizceSeviye = NEW.crm_IngilizceSeviye, crm_HollandacaSeviye = NEW.crm_HollandacaSeviye, crm_UAFDurum = NEW.crm_UAFDurum, crm_BootcampOrOtherCourse = NEW.crm_BootcampOrOtherCourse, crm_ITTecrube = NEW.crm_ITTecrube, crm_ProjeDahil = NEW.crm_ProjeDahil, crm_CalismakIstedigi = NEW.crm_CalismakIstedigi, crm_Sorular = NEW.crm_Sorular, crm_MotivasyonunNedir = NEW.crm_MotivasyonunNedir, crm_GelecekPlani = NEW.crm_GelecekPlani, crm_SaatKarisikligiOnay = NEW.crm_SaatKarisikligiOnay 
					WHERE crm_ID = newID;
				-- add log
				INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('Application information is updated "in trg_after_update_form1_data"', NEW.crm_Timestamp);
			END IF;
        END IF;
    END IF;    
    -- add log to verify that the trigger worked
    INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('trg_after_update_form1_data tigger is executed', NEW.crm_Timestamp);
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_backup_appointments_old_or_deleted
AFTER DELETE ON appointments_current
FOR EACH ROW
BEGIN
    INSERT INTO appointments_old_or_deleted (
        crm_WhenDeleted,
        crm_ID_Deleted,
        crm_Timestamp,
        crm_EventID,
        crm_InterviewDatetime,
        crm_MentorName,
        crm_MentorSurname,
        crm_MentorMail,
        crm_Summary,
        crm_Description,
        crm_Location,
        crm_OnlineMeetingLink,
        crm_AttendeeEmails,
        crm_ResponseStatus,
        crm_AttendeeID
    ) VALUES (
        CURRENT_Timestamp,
        OLD.crm_ID,
        OLD.crm_Timestamp,
        OLD.crm_EventID,
        OLD.crm_InterviewDatetime,
        OLD.crm_MentorName,
        OLD.crm_MentorSurname,
        OLD.crm_MentorMail,
        OLD.crm_Summary,
        OLD.crm_Description,
        OLD.crm_Location,
        OLD.crm_OnlineMeetingLink,
        OLD.crm_AttendeeEmails,
        OLD.crm_ResponseStatus,
        OLD.crm_AttendeeID
    );
    -- Add log
    INSERT INTO crm_trigger_logs (log_message, log_time) VALUES (CONCAT('The event ( crm_ID = ' , OLD.crm_ID, ',  crm_EventID = ', OLD.crm_EventID, ' ) is deleted from appointments_current table "in trg_backup_appointments_old_or_deleted"'), CURRENT_Timestamp);
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_after_insert_form2_data
AFTER INSERT ON form2_data
FOR EACH ROW
BEGIN
    DECLARE applicantID INT;
    DECLARE interviewedApplicantID INT;
    DECLARE mentorName varchar(45);
    DECLARE mentorSurname varchar(45);
    DECLARE mentorMail varchar(45);
    
    -- Getting the last added MentorMail value from form2_data (it is needed, very important: especially for form update action)
    SELECT crm_MentorMail INTO mentorMail FROM form2_data WHERE crm_ID = NEW.crm_ID;
    
    -- Getting MentorName, MentorSurname via MentorMail value
    SELECT crm_MentorName, crm_MentorSurname INTO mentorName, mentorSurname FROM appointments_current WHERE crm_MentorMail = mentorMail LIMIT 1;
    
    -- Getting and controlling Candidate control via name and surname. WARNING: collation settings type for comparison should not be case sensitive
    SELECT crm_ID INTO applicantID FROM form1_applicant WHERE TRIM(crm_Email) = TRIM(NEW.crm_ApplicantMail) LIMIT 1;
    SELECT crm_ApplicantID INTO interviewedApplicantID FROM form2_evaluations WHERE crm_ApplicantID = applicantID AND crm_Period = NEW.crm_Period;
    
    
	-- Actions ==>
    IF applicantID IS NULL THEN
		INSERT INTO crm_warnings (crm_log_message, crm_log_time) VALUES ('Mentor, varolmayan bir aday icin degerlendirme doldurdu/gonderdi "in trg_after_insert_form2_data trigger"', NEW.crm_Timestamp);
        INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('Mentor, varolmayan bir aday icin degerlendirme doldurdu/gonderdi "in trg_after_insert_form2_data trigger"', NEW.crm_Timestamp);
        -- form2data icinden ilgili satir silinebilir. ama bu sefer de excell ile ayni olma ozelligini yitirir... Dusun bunu!
        -- alternatif: buradan warnings diye bir tabloya kayit yaparim. uygulama her acildiginda bu tabloda yeni satir varsa uyari verir. uyari gorundukten 
        -- sonra warnings_old tablosuna tasinir. veya baska bir yontem dusunuruz. tek tablo senaryosu olarak...
        -- burasi icin eklerken bir hata oldu diye uyari yazdiririz...
	ELSEIF (applicantID IS NOT NULL) AND (interviewedApplicantID IS NULL) THEN
		-- add new candidate
		SET interviewedApplicantID = applicantID;	-- Eger yeni ekleme yapiliyorsa interviewedApplicantID yi applicantID olarak atayabiliriz.
        INSERT INTO form2_evaluations (crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_ApplicantID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment)
        VALUES (NEW.crm_Timestamp, NEW.crm_Period, mentorName, mentorSurname, NEW.crm_MentorMail, interviewedApplicantID, NEW.crm_ITSkills, NEW.crm_Availability, NEW.crm_Recommendation, NEW.crm_Comment);
        
        -- add log
		INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('New evaluation is added to form2_evaluations table "in trg_after_insert_form2_data trigger"', NEW.crm_Timestamp);
        
    ELSE
    
    -- <<< Under ELSE here, the evaluation information will be updated via filling a totally new form! >>> --
        -- This is the part that does the most complicated work. 
        -- If mentor wants to update his/her evaluation for the same candidate (with candidate email) a few days later, it works.
        
        -- >> Check the applicant's data and update if there are any changes
        IF (SELECT crm_Timestamp FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Timestamp OR
           (SELECT crm_MentorName FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> mentorName OR
           (SELECT crm_MentorSurname FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> mentorSurname OR
           (SELECT crm_MentorMail FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_MentorMail OR
           (SELECT crm_ITSkills FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_ITSkills OR
           (SELECT crm_Availability FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Availability OR
           (SELECT crm_Recommendation FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Recommendation OR
           (SELECT crm_Comment FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Comment THEN 			
				INSERT INTO form2_evaluations_old (crm_WhenUpdated, crm_ID_in_form2_evaluations, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_ApplicantID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_ProjectReturnDatetime, crm_IsApplicantACandidate)
				SELECT NEW.crm_Timestamp, crm_ID, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_ApplicantID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_ProjectReturnDatetime, crm_IsApplicantACandidate
				FROM form2_evaluations 
                WHERE crm_ApplicantID = interviewedApplicantID;
            
				UPDATE form2_evaluations
				SET crm_Timestamp = NEW.crm_Timestamp, crm_MentorName = mentorName, crm_MentorSurname = mentorSurname, crm_MentorMail = NEW.crm_MentorMail, crm_ITSkills = NEW.crm_ITSkills, crm_Availability = NEW.crm_Availability, crm_Recommendation = NEW.crm_Recommendation, crm_Comment = NEW.crm_Comment 
                WHERE crm_ApplicantID = interviewedApplicantID;         
            -- add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(WITH NEW FORM FILLING) Evaluation data is updated "in trg_after_insert_form2_data"', NEW.crm_Timestamp);
        END IF;
    END IF;
		
    -- add log to verify that the trigger worked
    INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('trg_after_insert_form2_data trigger is executed', NEW.crm_Timestamp);
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_after_update_form2_data
AFTER UPDATE ON form2_data
FOR EACH ROW
BEGIN
    DECLARE applicantID INT;
    DECLARE interviewedApplicantID INT;
    DECLARE mentorName varchar(45);
    DECLARE mentorSurname varchar(45);
    DECLARE mentorMail varchar(45);
    
    -- Getting the last added MentorMail value from form2_data (it is needed, very important: especially for form update action)
    SELECT crm_MentorMail INTO mentorMail FROM form2_data WHERE crm_ID = NEW.crm_ID;
    
    -- Getting MentorName, MentorSurname via MentorMail value
    SELECT crm_MentorName, crm_MentorSurname INTO mentorName, mentorSurname FROM appointments_current WHERE crm_MentorMail = mentorMail LIMIT 1;
    
    -- Getting and controlling Candidate control via name and surname. WARNING: collation settings type for comparison should not be case sensitive
    SELECT crm_ID INTO applicantID FROM form1_applicant WHERE TRIM(crm_Email) = TRIM(NEW.crm_ApplicantMail) LIMIT 1;
    SELECT crm_ApplicantID INTO interviewedApplicantID FROM form2_evaluations WHERE crm_ApplicantID = applicantID AND crm_Period = NEW.crm_Period;
    
    
    -- Actions ==>
	IF applicantID IS NULL THEN
		-- This code is set in the app script side to never run!
		INSERT INTO crm_warnings (crm_log_message, crm_log_time) VALUES ('(This code is set in the app script side to never run!) Mentor filled out/submitted an assessment for a non-existent candidate "in trg_after_update_form2_data trigger"', NEW.crm_Timestamp);
        INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(This code is set in the app script side to never run!) Mentor filled out/submitted an assessment for a non-existent candidate "in trg_after_update_form2_data trigger"', NEW.crm_Timestamp);
        
	ELSEIF (applicantID IS NOT NULL) AND (interviewedApplicantID IS NULL) THEN
		-- in the normal situations, no way to run this code block
        INSERT INTO crm_warnings (crm_log_message, crm_log_time) VALUES ('There is a serious problem. This code should not work! "in trg_after_update_form2_data trigger"', NEW.crm_Timestamp);
        INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('There is a serious problem. This code should not work! "in trg_after_update_form2_data trigger"', NEW.crm_Timestamp);
        
    ELSE
		-- the evaluation information will be updated via editing the same form!        
        -- >> Check the evaluation's data and update if there are any changes
        IF (SELECT crm_Timestamp FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Timestamp OR
           (SELECT crm_MentorName FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> mentorName OR
           (SELECT crm_MentorSurname FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> mentorSurname OR
           (SELECT crm_MentorMail FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> mentorMail OR
           (SELECT crm_ITSkills FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_ITSkills OR
           (SELECT crm_Availability FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Availability OR
           (SELECT crm_Recommendation FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Recommendation OR
           (SELECT crm_Comment FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Comment THEN 
				INSERT INTO form2_evaluations_old (crm_WhenUpdated, crm_ID_in_form2_evaluations, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_ApplicantID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_ProjectReturnDatetime, crm_IsApplicantACandidate)
				SELECT NEW.crm_Timestamp, crm_ID, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_ApplicantID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_ProjectReturnDatetime, crm_IsApplicantACandidate
				FROM form2_evaluations 
                WHERE crm_ApplicantID = interviewedApplicantID;
                
                UPDATE form2_evaluations
				SET crm_Timestamp = NEW.crm_Timestamp, crm_MentorName = mentorName, crm_MentorSurname = mentorSurname, crm_MentorMail = mentorMail, crm_ITSkills = NEW.crm_ITSkills, crm_Availability = NEW.crm_Availability, crm_Recommendation = NEW.crm_Recommendation, crm_Comment = NEW.crm_Comment 
                WHERE crm_ApplicantID = interviewedApplicantID;            
            -- add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(WITH NEW FORM FILLING) Evaluation data is updated "in trg_after_update_form2_data trigger"', NEW.crm_Timestamp);
        END IF;
    END IF;
		
    -- add log to verify that the trigger worked
    INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('trg_after_update_form2_data trigger is executed', NEW.crm_Timestamp);
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_after_insert_form3_data
AFTER INSERT ON form3_data
FOR EACH ROW
BEGIN
    DECLARE candidateID INT;
    DECLARE interviewedCandidateID INT;
    DECLARE mentorName varchar(45);
    DECLARE mentorSurname varchar(45);
    DECLARE mentorMail varchar(45);
    
    -- Getting the last added MentorMail value from form3_data (it is needed, very important: especially for form update action)
    SELECT crm_MentorMail INTO mentorMail FROM form3_data WHERE crm_ID = NEW.crm_ID;
    
    -- Getting MentorName, MentorSurname via MentorMail value
    SELECT crm_MentorName, crm_MentorSurname INTO mentorName, mentorSurname FROM appointments_current WHERE crm_MentorMail = mentorMail LIMIT 1;
    
    -- Getting and controlling Trainee Candiddate control via name and surname. WARNING: collation settings type for comparison should not be case sensitive
    SELECT crm_ID INTO candidateID FROM form1_applicant WHERE TRIM(crm_Email) = TRIM(NEW.crm_CandidateMail) LIMIT 1;
    SELECT crm_CandidateID INTO interviewedCandidateID FROM form3_final_evaluations WHERE crm_CandidateID = candidateID AND crm_Period = NEW.crm_Period;
    
    
	-- Actions ==>
    IF candidateID IS NULL THEN
		INSERT INTO crm_warnings (crm_log_message, crm_log_time) VALUES ('Mentor, varolmayan bir aday icin degerlendirme doldurdu/gonderdi "in trg_after_insert_form3_data trigger"', NEW.crm_Timestamp);
        INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('Mentor, varolmayan bir aday icin degerlendirme doldurdu/gonderdi "in trg_after_insert_form3_data trigger"', NEW.crm_Timestamp);
        
	ELSEIF (candidateID IS NOT NULL) AND (interviewedCandidateID IS NULL) THEN
		-- add new trainee candidate
		SET interviewedCandidateID = candidateID;	-- Eger yeni ekleme yapiliyorsa interviewedCandidateID yi candidateID olarak atayabiliriz.
        INSERT INTO form3_final_evaluations (crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_CandidateID, crm_CodingSkills, crm_AssistantEvaluation1, crm_AssistantEvaluation2, crm_AssistantEvaluation3, crm_MentorEvaluation)
        VALUES (NEW.crm_Timestamp, NEW.crm_Period, mentorName, mentorSurname, NEW.crm_MentorMail, interviewedCandidateID, NEW.crm_CodingSkills, NEW.crm_AssistantEvaluation1, NEW.crm_AssistantEvaluation2, NEW.crm_AssistantEvaluation3, NEW.crm_MentorEvaluation);
        
        -- add log
		INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('New evaluation is added to form3_final_evaluations table "in trg_after_insert_form3_data trigger"', NEW.crm_Timestamp);
        
    ELSE
    
    -- <<< Under ELSE here, the evaluation information will be updated via filling a totally new form! >>> --
        -- This is the part that does the most complicated work. 
        -- If mentor wants to update his/her evaluation for the same trainee candidate (with candidate email) a few days later, it works. 
        
        -- >> Check the candidate's data and update if there are any changes
        IF (SELECT crm_Timestamp FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_Timestamp OR
           (SELECT crm_MentorName FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> mentorName OR
           (SELECT crm_MentorSurname FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> mentorSurname OR
           (SELECT crm_MentorMail FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_MentorMail OR
           (SELECT crm_CodingSkills FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_CodingSkills OR
           (SELECT crm_AssistantEvaluation1 FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_AssistantEvaluation1 OR
           (SELECT crm_AssistantEvaluation2 FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_AssistantEvaluation2 OR
           (SELECT crm_AssistantEvaluation3 FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_AssistantEvaluation3 OR
           (SELECT crm_MentorEvaluation FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_MentorEvaluation THEN 			
				INSERT INTO form3_final_evaluations_old (crm_WhenUpdated, crm_ID_in_form3_final_evaluations, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_CandidateID, crm_CodingSkills, crm_AssistantEvaluation1, crm_AssistantEvaluation2, crm_AssistantEvaluation3, crm_MentorEvaluation, crm_IsCandidateATrainee)
				SELECT NEW.crm_Timestamp, crm_ID, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_CandidateID, crm_CodingSkills, crm_AssistantEvaluation1, crm_AssistantEvaluation2, crm_AssistantEvaluation3, crm_MentorEvaluation, crm_IsCandidateATrainee
				FROM form3_final_evaluations 
                WHERE crm_CandidateID = interviewedCandidateID;
            
				UPDATE form3_final_evaluations
				SET crm_Timestamp = NEW.crm_Timestamp, crm_MentorName = mentorName, crm_MentorSurname = mentorSurname, crm_MentorMail = NEW.crm_MentorMail, crm_CodingSkills = NEW.crm_CodingSkills, crm_AssistantEvaluation1 = NEW.crm_AssistantEvaluation1, crm_AssistantEvaluation2 = NEW.crm_AssistantEvaluation2, crm_AssistantEvaluation3 = NEW.crm_AssistantEvaluation3, crm_MentorEvaluation = NEW.crm_MentorEvaluation 
                WHERE crm_CandidateID = interviewedCandidateID;         
            -- add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(WITH NEW FORM FILLING) Evaluation data is updated "in trg_after_insert_form3_data"', NEW.crm_Timestamp);
        END IF;
    END IF;
		
    -- add log to verify that the trigger worked
    INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('trg_after_insert_form3_data trigger is executed', NEW.crm_Timestamp);
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER trg_after_update_form3_data
AFTER UPDATE ON form3_data
FOR EACH ROW
BEGIN
    DECLARE candidateID INT;
    DECLARE interviewedCandidateID INT;
    DECLARE mentorName varchar(45);
    DECLARE mentorSurname varchar(45);
    DECLARE mentorMail varchar(45);
    
    -- Getting the last added MentorMail value from form3_data (it is needed, very important: especially for form update action)
    SELECT crm_MentorMail INTO mentorMail FROM form3_data WHERE crm_ID = NEW.crm_ID;
    
    -- Getting MentorName, MentorSurname via MentorMail value
    SELECT crm_MentorName, crm_MentorSurname INTO mentorName, mentorSurname FROM appointments_current WHERE crm_MentorMail = mentorMail LIMIT 1;
    
    -- Getting and controlling Trainee Candiddate control via name and surname. WARNING: collation settings type for comparison should not be case sensitive
    SELECT crm_ID INTO candidateID FROM form1_applicant WHERE TRIM(crm_Email) = TRIM(NEW.crm_CandidateMail) LIMIT 1;
    SELECT crm_CandidateID INTO interviewedCandidateID FROM form3_final_evaluations WHERE crm_CandidateID = candidateID AND crm_Period = NEW.crm_Period;
    
    
	-- Actions ==>
	IF candidateID IS NULL THEN
		-- This code is set in the app script side to never run!
		INSERT INTO crm_warnings (crm_log_message, crm_log_time) VALUES ('(This code is set in the app script side to never run!) Mentor filled out/submitted an assessment for a non-existent candidate "in trg_after_update_form3_data trigger"', NEW.crm_Timestamp);
        INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(This code is set in the app script side to never run!) Mentor filled out/submitted an assessment for a non-existent candidate "in trg_after_update_form3_data trigger"', NEW.crm_Timestamp);
        
	ELSEIF (candidateID IS NOT NULL) AND (interviewedCandidateID IS NULL) THEN
		-- in the normal situations, no way to run this code block
        INSERT INTO crm_warnings (crm_log_message, crm_log_time) VALUES ('There is a serious problem. This code should not work! "in trg_after_update_form3_data trigger"', NEW.crm_Timestamp);
        INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('There is a serious problem. This code should not work! "in trg_after_update_form3_data trigger"', NEW.crm_Timestamp);
        
    ELSE
		-- the evaluation information will be updated via editing the same form!        
        -- >> Check the evaluation's data and update if there are any changes
        IF (SELECT crm_Timestamp FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_Timestamp OR
           (SELECT crm_MentorName FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> mentorName OR
           (SELECT crm_MentorSurname FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> mentorSurname OR
           (SELECT crm_MentorMail FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_MentorMail OR
           (SELECT crm_CodingSkills FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_CodingSkills OR
           (SELECT crm_AssistantEvaluation1 FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_AssistantEvaluation1 OR
           (SELECT crm_AssistantEvaluation2 FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_AssistantEvaluation2 OR
           (SELECT crm_AssistantEvaluation3 FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_AssistantEvaluation3 OR
           (SELECT crm_MentorEvaluation FROM form3_final_evaluations WHERE crm_CandidateID = interviewedCandidateID) <> NEW.crm_MentorEvaluation THEN 
				INSERT INTO form3_final_evaluations_old (crm_WhenUpdated, crm_ID_in_form3_final_evaluations, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_CandidateID, crm_CodingSkills, crm_AssistantEvaluation1, crm_AssistantEvaluation2, crm_AssistantEvaluation3, crm_MentorEvaluation, crm_IsCandidateATrainee)
				SELECT NEW.crm_Timestamp, crm_ID, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_CandidateID, crm_CodingSkills, crm_AssistantEvaluation1, crm_AssistantEvaluation2, crm_AssistantEvaluation3, crm_MentorEvaluation, crm_IsCandidateATrainee
				FROM form3_final_evaluations 
                WHERE crm_CandidateID = interviewedCandidateID;
                
                UPDATE form3_final_evaluations
				SET crm_Timestamp = NEW.crm_Timestamp, crm_MentorName = mentorName, crm_MentorSurname = mentorSurname, crm_MentorMail = NEW.crm_MentorMail, crm_CodingSkills = NEW.crm_CodingSkills, crm_AssistantEvaluation1 = NEW.crm_AssistantEvaluation1, crm_AssistantEvaluation2 = NEW.crm_AssistantEvaluation2, crm_AssistantEvaluation3 = NEW.crm_AssistantEvaluation3, crm_MentorEvaluation = NEW.crm_MentorEvaluation 
                WHERE crm_CandidateID = interviewedCandidateID;            
            -- add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('(WITH NEW FORM FILLING) Evaluation data is updated "in trg_after_update_form3_data trigger"', NEW.crm_Timestamp);
        END IF;
    END IF;
		
    -- add log to verify that the trigger worked
    INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('trg_after_update_form3_data trigger is executed', NEW.crm_Timestamp);
END//

DELIMITER ;


COMMIT;