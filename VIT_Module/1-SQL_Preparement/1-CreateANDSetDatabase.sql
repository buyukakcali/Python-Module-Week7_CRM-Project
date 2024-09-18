START TRANSACTION;

CREATE TABLE `users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `RegistrationDatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Username` varchar(30) NOT NULL,
  `Password` text NOT NULL,
  `Authority` varchar(10) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form1_data` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_RowID` int(11) NOT NULL,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Period` varchar(5) NOT NULL,
  `crm_Name` varchar(45) NOT NULL,
  `crm_Surname` varchar(45) NOT NULL,
  `crm_Email` varchar(45) NOT NULL,
  `crm_Phone` varchar(17) NOT NULL,
  `crm_PostCode` varchar(8) NOT NULL,
  `crm_Province` varchar(45) NOT NULL,
  `crm_SuAnkiDurum` text NOT NULL,
  `crm_ITPHEgitimKatilmak` text NOT NULL,
  `crm_EkonomikDurum` text NOT NULL,
  `crm_DilKursunaDevam` text NOT NULL,
  `crm_IngilizceSeviye` varchar(3) NOT NULL,
  `crm_HollandacaSeviye` varchar(3) NOT NULL,
  `crm_BaskiGoruyor` text NOT NULL,
  `crm_BootcampBitirdi` text NOT NULL,
  `crm_OnlineITKursu` text NOT NULL,
  `crm_ITTecrube` text NOT NULL,
  `crm_ProjeDahil` text NOT NULL,
  `crm_CalismakIstedigi` text NOT NULL,
  `crm_NedenKatilmakIstiyor` text NOT NULL,
  `crm_MotivasyonunNedir` text NOT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form1_applicant` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Name` varchar(45) NOT NULL,
  `crm_Surname` varchar(45) NOT NULL,
  `crm_Email` varchar(45) NOT NULL,
  `crm_Phone` varchar(17) NOT NULL,
  `crm_PostCode` varchar(8) NOT NULL,
  `crm_Province` varchar(45) NOT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form1_application` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_ApplicantID` int(11) NOT NULL,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Period` varchar(5) NOT NULL,
  `crm_SuAnkiDurum` text NOT NULL,
  `crm_ITPHEgitimKatilmak` text NOT NULL,
  `crm_EkonomikDurum` text NOT NULL,
  `crm_DilKursunaDevam` text NOT NULL,
  `crm_IngilizceSeviye` varchar(3) NOT NULL,
  `crm_HollandacaSeviye` varchar(3) NOT NULL,
  `crm_BaskiGoruyor` text NOT NULL,
  `crm_BootcampBitirdi` text NOT NULL,
  `crm_OnlineITKursu` text NOT NULL,
  `crm_ITTecrube` text NOT NULL,
  `crm_ProjeDahil` text NOT NULL,
  `crm_CalismakIstedigi` text NOT NULL,
  `crm_NedenKatilmakIstiyor` text NOT NULL,
  `crm_MotivasyonunNedir` text NOT NULL,
  `crm_FirstInterview` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`crm_ID`),
  KEY `fk_form1_application_idx` (`crm_ApplicantID`),
  CONSTRAINT `fk_form1_application` FOREIGN KEY (`crm_ApplicantID`) REFERENCES `form1_applicant` (`crm_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form1_old_applicant` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_ID_in_applicantTable` int(11) DEFAULT NULL,
  `crm_WhenUpdated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `crm_Timestamp` datetime DEFAULT NULL,
  `crm_Name` varchar(45) DEFAULT NULL,
  `crm_Surname` varchar(45) DEFAULT NULL,
  `crm_Email` varchar(45) DEFAULT NULL,
  `crm_Phone` varchar(17) DEFAULT NULL,
  `crm_PostCode` varchar(8) DEFAULT NULL,
  `crm_Province` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form1_old_application` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_ID_in_applicationTable` int(11) DEFAULT NULL,
  `crm_WhenUpdated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `crm_ApplicantID` int(11) DEFAULT NULL,
  `crm_Timestamp` datetime DEFAULT NULL,
  `crm_Period` varchar(5) DEFAULT NULL,
  `crm_SuAnkiDurum` text DEFAULT NULL,
  `crm_ITPHEgitimKatilmak` text DEFAULT NULL,
  `crm_EkonomikDurum` text DEFAULT NULL,
  `crm_DilKursunaDevam` text DEFAULT NULL,
  `crm_IngilizceSeviye` varchar(3) DEFAULT NULL,
  `crm_HollandacaSeviye` varchar(3) DEFAULT NULL,
  `crm_BaskiGoruyor` text DEFAULT NULL,
  `crm_BootcampBitirdi` text DEFAULT NULL,
  `crm_OnlineITKursu` text DEFAULT NULL,
  `crm_ITTecrube` text DEFAULT NULL,
  `crm_ProjeDahil` text DEFAULT NULL,
  `crm_CalismakIstedigi` text DEFAULT NULL,
  `crm_NedenKatilmakIstiyor` text DEFAULT NULL,
  `crm_MotivasyonunNedir` text DEFAULT NULL,
  `crm_FirstInterview` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `appointments_current` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_Timestamp` datetime NOT NULL,
  `crm_EventID` varchar(255) NOT NULL,
  `crm_InterviewDatetime` datetime NOT NULL,
  `crm_MentorName` varchar(45) DEFAULT NULL,
  `crm_MentorSurname` varchar(45) DEFAULT NULL,
  `crm_MentorMail` varchar(45) NOT NULL,
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
  `crm_MentorName` varchar(45) DEFAULT NULL,
  `crm_MentorSurname` varchar(45) DEFAULT NULL,
  `crm_MentorMail` varchar(45) NOT NULL,
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
  `crm_RowID` varchar(45) NOT NULL,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Period` varchar(5) NOT NULL,
  `crm_MentorMail` varchar(45) NOT NULL,
  `crm_ApplicantMail` varchar(45) NOT NULL,
  `crm_ITSkills` int(11) NOT NULL,
  `crm_Availability` int(11) NOT NULL,
  `crm_Recommendation` text NOT NULL,
  `crm_Comment` text DEFAULT NULL,
  PRIMARY KEY (`crm_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

CREATE TABLE `form2_evaluations` (
  `crm_ID` int(11) NOT NULL AUTO_INCREMENT,
  `crm_Timestamp` datetime NOT NULL,
  `crm_Period` varchar(5) NOT NULL,
  `crm_MentorName` varchar(45) NOT NULL,
  `crm_MentorSurname` varchar(45) NOT NULL,
  `crm_MentorMail` varchar(45) NOT NULL,
  `crm_ApplicantID` int(11) NOT NULL,
  `crm_ITSkills` int(11) NOT NULL,
  `crm_Availability` int(11) NOT NULL,
  `crm_Recommendation` text NOT NULL,
  `crm_Comment` text NOT NULL,
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
  `crm_Period` varchar(5) DEFAULT NULL,
  `crm_MentorName` varchar(45) DEFAULT NULL,
  `crm_MentorSurname` varchar(45) DEFAULT NULL,
  `crm_MentorMail` varchar(45) DEFAULT NULL,
  `crm_ApplicantID` int(11) DEFAULT NULL,
  `crm_ITSkills` int(11) DEFAULT NULL,
  `crm_Availability` int(11) DEFAULT NULL,
  `crm_Recommendation` text DEFAULT NULL,
  `crm_Comment` text DEFAULT NULL,
  `crm_IsApplicantACandidate` tinyint(1) DEFAULT NULL,
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
        INSERT INTO form1_application (crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir)
        VALUES (applicantID, NEW.crm_Timestamp, NEW.crm_Period, NEW.crm_SuAnkiDurum, NEW.crm_ITPHEgitimKatilmak, NEW.crm_EkonomikDurum, NEW.crm_DilKursunaDevam, NEW.crm_IngilizceSeviye, NEW.crm_HollandacaSeviye, NEW.crm_BaskiGoruyor, NEW.crm_BootcampBitirdi, NEW.crm_OnlineITKursu, NEW.crm_ITTecrube, NEW.crm_ProjeDahil, NEW.crm_CalismakIstedigi, NEW.crm_NedenKatilmakIstiyor, NEW.crm_MotivasyonunNedir);
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
				INSERT INTO form1_old_applicant (crm_ID_in_ApplicantTable, crm_WhenUpdated, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province)
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
            INSERT INTO form1_application (crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir)
            VALUES (applicantID, NEW.crm_Timestamp, NEW.crm_Period, NEW.crm_SuAnkiDurum, NEW.crm_ITPHEgitimKatilmak, NEW.crm_EkonomikDurum, NEW.crm_DilKursunaDevam, NEW.crm_IngilizceSeviye, NEW.crm_HollandacaSeviye, NEW.crm_BaskiGoruyor, NEW.crm_BootcampBitirdi, NEW.crm_OnlineITKursu, NEW.crm_ITTecrube, NEW.crm_ProjeDahil, NEW.crm_CalismakIstedigi, NEW.crm_NedenKatilmakIstiyor, NEW.crm_MotivasyonunNedir);
            -- add log
            INSERT INTO crm_trigger_logs (log_message, log_time) VALUES ('New application of existing applicant is added to form1_application table', NEW.crm_Timestamp);
        ELSE
			-- <<< Here, under ELSE, the Application information will be updated! >>> --
			-- This is the part that does the most complicated work. 
            -- If the person wants to update their application with the same email address a few days later, it works. 
            
            -- >> Check the application's data and update if there are any changes
			IF (SELECT crm_SuAnkiDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_SuAnkiDurum OR
               (SELECT crm_ITPHEgitimKatilmak FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ITPHEgitimKatilmak OR
               (SELECT crm_EkonomikDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_EkonomikDurum OR
               (SELECT crm_DilKursunaDevam FROM form1_application WHERE crm_ID = newID) <> NEW.crm_DilKursunaDevam OR
               (SELECT crm_IngilizceSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_IngilizceSeviye OR
               (SELECT crm_HollandacaSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_HollandacaSeviye OR
               (SELECT crm_BaskiGoruyor FROM form1_application WHERE crm_ID = newID) <> NEW.crm_BaskiGoruyor OR
               (SELECT crm_BootcampBitirdi FROM form1_application WHERE crm_ID = newID) <> NEW.crm_BootcampBitirdi OR
               (SELECT crm_OnlineITKursu FROM form1_application WHERE crm_ID = newID) <> NEW.crm_OnlineITKursu OR
               (SELECT crm_ITTecrube FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ITTecrube OR
               (SELECT crm_ProjeDahil FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ProjeDahil OR
               (SELECT crm_CalismakIstedigi FROM form1_application WHERE crm_ID = newID) <> NEW.crm_CalismakIstedigi OR
               (SELECT crm_NedenKatilmakIstiyor FROM form1_application WHERE crm_ID = newID) <> NEW.crm_NedenKatilmakIstiyor OR
               (SELECT crm_MotivasyonunNedir FROM form1_application WHERE crm_ID = newID) <> NEW.crm_MotivasyonunNedir THEN	-- controls of other columns will come here
					INSERT INTO form1_old_application (crm_ID_in_applicationTable, crm_WhenUpdated, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir, crm_FirstInterview) 
					SELECT crm_ID, NEW.crm_Timestamp, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir, crm_FirstInterview 
					FROM form1_application 
					WHERE crm_ID = newID;
						
					UPDATE form1_application 
					SET crm_Timestamp = NEW.crm_Timestamp, crm_SuAnkiDurum = NEW.crm_SuAnkiDurum, crm_ITPHEgitimKatilmak = NEW.crm_ITPHEgitimKatilmak, crm_EkonomikDurum = NEW.crm_EkonomikDurum, crm_DilKursunaDevam = NEW.crm_DilKursunaDevam, crm_IngilizceSeviye = NEW.crm_IngilizceSeviye, crm_HollandacaSeviye = NEW.crm_HollandacaSeviye, crm_BaskiGoruyor = NEW.crm_BaskiGoruyor, crm_BootcampBitirdi = NEW.crm_BootcampBitirdi, crm_OnlineITKursu = NEW.crm_OnlineITKursu, crm_ITTecrube = NEW.crm_ITTecrube, crm_ProjeDahil = NEW.crm_ProjeDahil, crm_CalismakIstedigi = NEW.crm_CalismakIstedigi, crm_NedenKatilmakIstiyor = NEW.crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir = NEW.crm_MotivasyonunNedir
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
				INSERT INTO form1_old_applicant (crm_ID_in_ApplicantTable, crm_WhenUpdated, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province) 
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
			IF	(SELECT crm_SuAnkiDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_SuAnkiDurum OR
				(SELECT crm_ITPHEgitimKatilmak FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ITPHEgitimKatilmak OR
				(SELECT crm_EkonomikDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_EkonomikDurum OR
				(SELECT crm_DilKursunaDevam FROM form1_application WHERE crm_ID = newID) <> NEW.crm_DilKursunaDevam OR
				(SELECT crm_IngilizceSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_IngilizceSeviye OR
				(SELECT crm_HollandacaSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_HollandacaSeviye OR
				(SELECT crm_BaskiGoruyor FROM form1_application WHERE crm_ID = newID) <> NEW.crm_BaskiGoruyor OR
				(SELECT crm_BootcampBitirdi FROM form1_application WHERE crm_ID = newID) <> NEW.crm_BootcampBitirdi OR
				(SELECT crm_OnlineITKursu FROM form1_application WHERE crm_ID = newID) <> NEW.crm_OnlineITKursu OR
				(SELECT crm_ITTecrube FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ITTecrube OR
				(SELECT crm_ProjeDahil FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ProjeDahil OR
				(SELECT crm_CalismakIstedigi FROM form1_application WHERE crm_ID = newID) <> NEW.crm_CalismakIstedigi OR
				(SELECT crm_NedenKatilmakIstiyor FROM form1_application WHERE crm_ID = newID) <> NEW.crm_NedenKatilmakIstiyor OR
				(SELECT crm_MotivasyonunNedir FROM form1_application WHERE crm_ID = newID) <> NEW.crm_MotivasyonunNedir THEN
					INSERT INTO form1_old_application (crm_ID_in_applicationTable, crm_WhenUpdated, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir, crm_FirstInterview)
					SELECT crm_ID, NEW.crm_Timestamp, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir, crm_FirstInterview 
					FROM form1_application 
					WHERE crm_ID = newID;
					
					UPDATE form1_application
					SET crm_Timestamp = NEW.crm_Timestamp, crm_SuAnkiDurum = NEW.crm_SuAnkiDurum, crm_ITPHEgitimKatilmak = NEW.crm_ITPHEgitimKatilmak, crm_EkonomikDurum = NEW.crm_EkonomikDurum, crm_DilKursunaDevam = NEW.crm_DilKursunaDevam, crm_IngilizceSeviye = NEW.crm_IngilizceSeviye, crm_HollandacaSeviye = NEW.crm_HollandacaSeviye, crm_BaskiGoruyor = NEW.crm_BaskiGoruyor, crm_BootcampBitirdi = NEW.crm_BootcampBitirdi, crm_OnlineITKursu = NEW.crm_OnlineITKursu, crm_ITTecrube = NEW.crm_ITTecrube, crm_ProjeDahil = NEW.crm_ProjeDahil, crm_CalismakIstedigi = NEW.crm_CalismakIstedigi, crm_NedenKatilmakIstiyor = NEW.crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir = NEW.crm_MotivasyonunNedir
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
				INSERT INTO form1_old_applicant (crm_ID_in_ApplicantTable, crm_WhenUpdated, crm_Timestamp, crm_Name, crm_Surname, crm_Email, crm_Phone, crm_PostCode, crm_Province)
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
			IF	(SELECT crm_SuAnkiDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_SuAnkiDurum OR
				(SELECT crm_ITPHEgitimKatilmak FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ITPHEgitimKatilmak OR
				(SELECT crm_EkonomikDurum FROM form1_application WHERE crm_ID = newID) <> NEW.crm_EkonomikDurum OR
				(SELECT crm_DilKursunaDevam FROM form1_application WHERE crm_ID = newID) <> NEW.crm_DilKursunaDevam OR
				(SELECT crm_IngilizceSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_IngilizceSeviye OR
				(SELECT crm_HollandacaSeviye FROM form1_application WHERE crm_ID = newID) <> NEW.crm_HollandacaSeviye OR
				(SELECT crm_BaskiGoruyor FROM form1_application WHERE crm_ID = newID) <> NEW.crm_BaskiGoruyor OR
				(SELECT crm_BootcampBitirdi FROM form1_application WHERE crm_ID = newID) <> NEW.crm_BootcampBitirdi OR
				(SELECT crm_OnlineITKursu FROM form1_application WHERE crm_ID = newID) <> NEW.crm_OnlineITKursu OR
				(SELECT crm_ITTecrube FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ITTecrube OR
				(SELECT crm_ProjeDahil FROM form1_application WHERE crm_ID = newID) <> NEW.crm_ProjeDahil OR
				(SELECT crm_CalismakIstedigi FROM form1_application WHERE crm_ID = newID) <> NEW.crm_CalismakIstedigi OR
				(SELECT crm_NedenKatilmakIstiyor FROM form1_application WHERE crm_ID = newID) <> NEW.crm_NedenKatilmakIstiyor OR
				(SELECT crm_MotivasyonunNedir FROM form1_application WHERE crm_ID = newID) <> NEW.crm_MotivasyonunNedir THEN
					INSERT INTO form1_old_application (crm_ID_in_applicationTable, crm_WhenUpdated, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir, crm_FirstInterview)
					SELECT crm_ID, NEW.crm_Timestamp, crm_ApplicantID, crm_Timestamp, crm_Period, crm_SuAnkiDurum, crm_ITPHEgitimKatilmak, crm_EkonomikDurum, crm_DilKursunaDevam, crm_IngilizceSeviye, crm_HollandacaSeviye, crm_BaskiGoruyor, crm_BootcampBitirdi, crm_OnlineITKursu, crm_ITTecrube, crm_ProjeDahil, crm_CalismakIstedigi, crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir, crm_FirstInterview
					FROM form1_application
					WHERE crm_ID = newID;
						
					UPDATE form1_application
					SET crm_Timestamp = NEW.crm_Timestamp, crm_SuAnkiDurum = NEW.crm_SuAnkiDurum, crm_ITPHEgitimKatilmak = NEW.crm_ITPHEgitimKatilmak, crm_EkonomikDurum = NEW.crm_EkonomikDurum, crm_DilKursunaDevam = NEW.crm_DilKursunaDevam, crm_IngilizceSeviye = NEW.crm_IngilizceSeviye, crm_HollandacaSeviye = NEW.crm_HollandacaSeviye, crm_BaskiGoruyor = NEW.crm_BaskiGoruyor, crm_BootcampBitirdi = NEW.crm_BootcampBitirdi, crm_OnlineITKursu = NEW.crm_OnlineITKursu, crm_ITTecrube = NEW.crm_ITTecrube, crm_ProjeDahil = NEW.crm_ProjeDahil, crm_CalismakIstedigi = NEW.crm_CalismakIstedigi, crm_NedenKatilmakIstiyor = NEW.crm_NedenKatilmakIstiyor, crm_MotivasyonunNedir = NEW.crm_MotivasyonunNedir
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
        -- If mentor wants to update his/her evaluation for the same candidate (with candidate name and surname) a few days later, it works. 
        
        -- >> Check the applicant's data and update if there are any changes
        IF (SELECT crm_Timestamp FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Timestamp OR
           (SELECT crm_MentorName FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> mentorName OR
           (SELECT crm_MentorSurname FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> mentorSurname OR
           (SELECT crm_MentorMail FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_MentorMail OR
           (SELECT crm_ITSkills FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_ITSkills OR
           (SELECT crm_Availability FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Availability OR
           (SELECT crm_Recommendation FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Recommendation OR
           (SELECT crm_Comment FROM form2_evaluations WHERE crm_ApplicantID = interviewedApplicantID) <> NEW.crm_Comment THEN 			
				INSERT INTO form2_evaluations_old (crm_WhenUpdated, crm_ID_in_form2_evaluations, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_ApplicantID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_IsApplicantACandidate)
				SELECT NEW.crm_Timestamp, crm_ID, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_ApplicantID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_IsApplicantACandidate
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
				INSERT INTO form2_evaluations_old (crm_WhenUpdated, crm_ID_in_form2_evaluations, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_ApplicantID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_IsApplicantACandidate)
				SELECT NEW.crm_Timestamp, crm_ID, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_ApplicantID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment, crm_IsApplicantACandidate
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


COMMIT;