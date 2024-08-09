DELIMITER //

CREATE TRIGGER trg_after_insert_form_data
AFTER INSERT ON form_data
FOR EACH ROW
BEGIN
    DECLARE applicantID INT;
    DECLARE newID INT;
    
    -- Applicant control via email
    SELECT ID INTO applicantID FROM form_applicant WHERE Email = NEW.Email LIMIT 1;

    -- If there is no applicant
    IF applicantID IS NULL THEN
    -- add new applicant
        INSERT INTO form_applicant (Timestamp_, Name, Surname, Email, Phone, PostCode, Province)
        VALUES (NEW.Timestamp_, NEW.Name, NEW.Surname, NEW.Email, NEW.Phone, NEW.PostCode, NEW.Province);
        SET applicantID = LAST_INSERT_ID();
        -- add log
		INSERT INTO trigger_logs (log_message, log_time) VALUES ('New applicant is added to form_applicant table', NEW.Timestamp_);

        -- add new application
        INSERT INTO form_application (ApplicantID, Timestamp_, Period, SuAnkiDurum, ITPHEgitimKatilmak, EkonomikDurum, DilKursunaDevam, IngilizceSeviye, HollandacaSeviye, BaskiGoruyor, BootcampBitirdi, OnlineITKursu, ITTecrube, ProjeDahil, CalismakIstedigi, NedenKatilmakIstiyor, MotivasyonunNedir)
        VALUES (applicantID, NEW.Timestamp_, NEW.Period, NEW.SuAnkiDurum, NEW.ITPHEgitimKatilmak, NEW.EkonomikDurum, NEW.DilKursunaDevam, NEW.IngilizceSeviye, NEW.HollandacaSeviye, NEW.BaskiGoruyor, NEW.BootcampBitirdi, NEW.OnlineITKursu, NEW.ITTecrube, NEW.ProjeDahil, NEW.CalismakIstedigi, NEW.NedenKatilmakIstiyor, NEW.MotivasyonunNedir);
        -- add log
		INSERT INTO trigger_logs (log_message, log_time) VALUES ('New application is added to form_application table', NEW.Timestamp_);
    ELSE
        -- <<< Under ELSE here, the Applicant information will be updated! >>> --
        -- This is the part that does the most complicated work.
        -- If the person wants to update their application with the same email address a few days later, it works.
        -- Although the number of rows in the sheet increases, the number of rows in form_data does not. It just gets updated.

        -- >> Check the applicant's data and update if there are any changes
        IF (SELECT Name FROM form_applicant WHERE ID = applicantID) <> NEW.Name OR
           (SELECT Surname FROM form_applicant WHERE ID = applicantID) <> NEW.Surname OR
           (SELECT Phone FROM form_applicant WHERE ID = applicantID) <> NEW.Phone OR
           (SELECT PostCode FROM form_applicant WHERE ID = applicantID) <> NEW.PostCode OR
           (SELECT Province FROM form_applicant WHERE ID = applicantID) <> NEW.Province THEN

			INSERT INTO form_old_applicant (ID_in_ApplicantTable, WhenUpdated, Timestamp_, Name, Surname, Email, Phone, PostCode, Province)
            SELECT ID, NEW.Timestamp_, Timestamp_, Name, Surname, Email, Phone, PostCode, Province
            FROM form_applicant
            WHERE ID = applicantID;

            UPDATE form_applicant
            SET Timestamp_ = NEW.Timestamp_, Name = NEW.Name, Surname = NEW.Surname, Phone = NEW.Phone, PostCode = NEW.PostCode, Province = NEW.Province
            WHERE ID = applicantID;
            -- add log
            INSERT INTO trigger_logs (log_message, log_time) VALUES ('(WITH NEW FORM FILLING) Applicant information is updated "in trg_after_insert_data"', NEW.Timestamp_);
        END IF;
        -- <<< -------------------------- >>> --

        -- Application period control and addition/update
        SELECT ID INTO newID FROM form_application WHERE ApplicantID = applicantID AND Period = NEW.Period LIMIT 1;
        IF newID IS NULL THEN
            INSERT INTO form_application (ApplicantID, Timestamp_, Period, SuAnkiDurum, ITPHEgitimKatilmak, EkonomikDurum, DilKursunaDevam, IngilizceSeviye, HollandacaSeviye, BaskiGoruyor, BootcampBitirdi, OnlineITKursu, ITTecrube, ProjeDahil, CalismakIstedigi, NedenKatilmakIstiyor, MotivasyonunNedir)
            VALUES (applicantID, NEW.Timestamp_, NEW.Period, NEW.SuAnkiDurum, NEW.ITPHEgitimKatilmak, NEW.EkonomikDurum, NEW.DilKursunaDevam, NEW.IngilizceSeviye, NEW.HollandacaSeviye, NEW.BaskiGoruyor, NEW.BootcampBitirdi, NEW.OnlineITKursu, NEW.ITTecrube, NEW.ProjeDahil, NEW.CalismakIstedigi, NEW.NedenKatilmakIstiyor, NEW.MotivasyonunNedir);
            -- add log
            INSERT INTO trigger_logs (log_message, log_time) VALUES ('New application of existing applicant is added to form_application table', NEW.Timestamp_);
        ELSE
			-- <<< Here, under ELSE, the Application information will be updated! >>> --
			-- This is the part that does the most complicated work.
            -- If the person wants to update their application with the same email address a few days later, it works.
            -- Even though the number of rows in sheet increases, the number of rows in form_data does not. It just gets updated.

            -- >> Check the application's data and update if there are any changes
			IF (SELECT SuAnkiDurum FROM form_application WHERE ID = newID) <> NEW.SuAnkiDurum OR
            (SELECT ITPHEgitimKatilmak FROM form_application WHERE ID = newID) <> NEW.ITPHEgitimKatilmak OR
            (SELECT EkonomikDurum FROM form_application WHERE ID = newID) <> NEW.EkonomikDurum OR
            (SELECT DilKursunaDevam FROM form_application WHERE ID = newID) <> NEW.DilKursunaDevam OR
            (SELECT IngilizceSeviye FROM form_application WHERE ID = newID) <> NEW.IngilizceSeviye OR
            (SELECT HollandacaSeviye FROM form_application WHERE ID = newID) <> NEW.HollandacaSeviye OR
            (SELECT BaskiGoruyor FROM form_application WHERE ID = newID) <> NEW.BaskiGoruyor OR
            (SELECT BootcampBitirdi FROM form_application WHERE ID = newID) <> NEW.BootcampBitirdi OR
            (SELECT OnlineITKursu FROM form_application WHERE ID = newID) <> NEW.OnlineITKursu OR
            (SELECT ITTecrube FROM form_application WHERE ID = newID) <> NEW.ITTecrube OR
            (SELECT ProjeDahil FROM form_application WHERE ID = newID) <> NEW.ProjeDahil OR
            (SELECT CalismakIstedigi FROM form_application WHERE ID = newID) <> NEW.CalismakIstedigi OR
            (SELECT NedenKatilmakIstiyor FROM form_application WHERE ID = newID) <> NEW.NedenKatilmakIstiyor OR
            (SELECT MotivasyonunNedir FROM form_application WHERE ID = newID) <> NEW.MotivasyonunNedir THEN	-- controls of other columns will come here
				INSERT INTO form_old_application (ID_in_applicationTable, WhenUpdated, ApplicantID, Timestamp_, Period, SuAnkiDurum, ITPHEgitimKatilmak, EkonomikDurum, DilKursunaDevam, IngilizceSeviye, HollandacaSeviye, BaskiGoruyor, BootcampBitirdi, OnlineITKursu, ITTecrube, ProjeDahil, CalismakIstedigi, NedenKatilmakIstiyor, MotivasyonunNedir, FirstInterview, SecondInterview)
				SELECT ID, NEW.Timestamp_, ApplicantID, Timestamp_, Period, SuAnkiDurum, ITPHEgitimKatilmak, EkonomikDurum, DilKursunaDevam, IngilizceSeviye, HollandacaSeviye, BaskiGoruyor, BootcampBitirdi, OnlineITKursu, ITTecrube, ProjeDahil, CalismakIstedigi, NedenKatilmakIstiyor, MotivasyonunNedir, FirstInterview, SecondInterview
				FROM form_application
				WHERE ID = newID;

				UPDATE form_application
				SET Timestamp_ = NEW.Timestamp_, SuAnkiDurum = NEW.SuAnkiDurum, ITPHEgitimKatilmak = NEW.ITPHEgitimKatilmak, EkonomikDurum = NEW.EkonomikDurum, DilKursunaDevam = NEW.DilKursunaDevam, IngilizceSeviye = NEW.IngilizceSeviye, HollandacaSeviye = NEW.HollandacaSeviye, BaskiGoruyor = NEW.BaskiGoruyor, BootcampBitirdi = NEW.BootcampBitirdi, OnlineITKursu = NEW.OnlineITKursu, ITTecrube = NEW.ITTecrube, ProjeDahil = NEW.ProjeDahil, CalismakIstedigi = NEW.CalismakIstedigi, NedenKatilmakIstiyor = NEW.NedenKatilmakIstiyor, MotivasyonunNedir = NEW.MotivasyonunNedir
				WHERE ID = newID;
				-- add log
				INSERT INTO trigger_logs (log_message, log_time) VALUES ('(WITH NEW FORM FILLING) Application information is updated "in trg_after_insert_data"', NEW.Timestamp_);
			END IF;
            -- <<< -------------------------- >>> --

        END IF;
    END IF;
    -- add log to verify that the trigger worked
    INSERT INTO trigger_logs (log_message, log_time) VALUES ('trg_after_insert_form_data trigger is executed', NEW.Timestamp_);
END//

DELIMITER ;



DELIMITER //

CREATE TRIGGER trg_after_update_form_data
AFTER UPDATE ON form_data
FOR EACH ROW
BEGIN
    DECLARE applicantID INT;
    DECLARE newID INT;

    -- Applicant control via email
    SELECT ID INTO applicantID FROM form_applicant WHERE Email = NEW.Email LIMIT 1;

    -- If there is no applicant, he/she is POSSIBLY changing his/her email address. (Expected to be rare), add log and update applicant information
    IF applicantID IS NULL THEN
		-- ******************* --

		-- CHECK FROM OLD EMAIL
        SELECT ID INTO applicantID FROM form_applicant WHERE Email = OLD.Email LIMIT 1;

        -- (OLD) Check the applicant's data and update if there are any changes
        IF (SELECT Name FROM form_applicant WHERE ID = applicantID) <> NEW.Name OR
           (SELECT Surname FROM form_applicant WHERE ID = applicantID) <> NEW.Surname OR
           (SELECT Email FROM form_applicant WHERE ID = applicantID) <> NEW.Email OR
           (SELECT Phone FROM form_applicant WHERE ID = applicantID) <> NEW.Phone OR
           (SELECT PostCode FROM form_applicant WHERE ID = applicantID) <> NEW.PostCode OR
           (SELECT Province FROM form_applicant WHERE ID = applicantID) <> NEW.Province THEN

            INSERT INTO form_old_applicant (ID_in_ApplicantTable, WhenUpdated, Timestamp_, Name, Surname, Email, Phone, PostCode, Province)
            SELECT ID, NEW.Timestamp_, Timestamp_, Name, Surname, Email, Phone, PostCode, Province
            FROM form_applicant
            WHERE ID = applicantID;

            UPDATE form_applicant
            SET Timestamp_ = NEW.Timestamp_, Name = NEW.Name, Surname = NEW.Surname, Email = NEW.Email, Phone = NEW.Phone, PostCode = NEW.PostCode, Province = NEW.Province
            WHERE ID = applicantID;
            -- (OLD) add log
            INSERT INTO trigger_logs (log_message, log_time) VALUES ('(OLD) Application information (including email address) is updated "in trg_after_update_form_data"', NEW.Timestamp_);
		ELSE
            INSERT INTO trigger_logs (log_message, log_time)
            VALUES (CONCAT('(OLD) It means there is an error right now that I don\'t know why... ("in trg_after_update_form_data") Line Number: ', (SELECT RowID FROM form_data WHERE Email = OLD.Email)), NEW.Timestamp_);
		END IF;

        -- (OLD) Application period control and addition/update
        SELECT ID INTO newID FROM form_application WHERE ApplicantID = applicantID AND Period = NEW.Period;
        IF newID IS NULL THEN
            -- (OLD) add log
            INSERT INTO trigger_logs (log_message, log_time) VALUES ('(OLD) Unexpected code situation! This code shuldn\'t be executed... ("in trg_after_update_form_data")', NEW.Timestamp_);
        ELSE
            -- (OLD) Check the application's data and update if there are any changes
			IF (SELECT SuAnkiDurum FROM form_application WHERE ID = newID) <> NEW.SuAnkiDurum OR
            (SELECT ITPHEgitimKatilmak FROM form_application WHERE ID = newID) <> NEW.ITPHEgitimKatilmak OR
            (SELECT EkonomikDurum FROM form_application WHERE ID = newID) <> NEW.EkonomikDurum OR
            (SELECT DilKursunaDevam FROM form_application WHERE ID = newID) <> NEW.DilKursunaDevam OR
            (SELECT IngilizceSeviye FROM form_application WHERE ID = newID) <> NEW.IngilizceSeviye OR
            (SELECT HollandacaSeviye FROM form_application WHERE ID = newID) <> NEW.HollandacaSeviye OR
            (SELECT BaskiGoruyor FROM form_application WHERE ID = newID) <> NEW.BaskiGoruyor OR
            (SELECT BootcampBitirdi FROM form_application WHERE ID = newID) <> NEW.BootcampBitirdi OR
            (SELECT OnlineITKursu FROM form_application WHERE ID = newID) <> NEW.OnlineITKursu OR
            (SELECT ITTecrube FROM form_application WHERE ID = newID) <> NEW.ITTecrube OR
            (SELECT ProjeDahil FROM form_application WHERE ID = newID) <> NEW.ProjeDahil OR
            (SELECT CalismakIstedigi FROM form_application WHERE ID = newID) <> NEW.CalismakIstedigi OR
            (SELECT NedenKatilmakIstiyor FROM form_application WHERE ID = newID) <> NEW.NedenKatilmakIstiyor OR
            (SELECT MotivasyonunNedir FROM form_application WHERE ID = newID) <> NEW.MotivasyonunNedir THEN
				INSERT INTO form_old_application (ID_in_applicationTable, WhenUpdated, ApplicantID, Timestamp_, Period, SuAnkiDurum, ITPHEgitimKatilmak, EkonomikDurum, DilKursunaDevam, IngilizceSeviye, HollandacaSeviye, BaskiGoruyor, BootcampBitirdi, OnlineITKursu, ITTecrube, ProjeDahil, CalismakIstedigi, NedenKatilmakIstiyor, MotivasyonunNedir, FirstInterview, SecondInterview)
				SELECT ID, NEW.Timestamp_, ApplicantID, Timestamp_, Period, SuAnkiDurum, ITPHEgitimKatilmak, EkonomikDurum, DilKursunaDevam, IngilizceSeviye, HollandacaSeviye, BaskiGoruyor, BootcampBitirdi, OnlineITKursu, ITTecrube, ProjeDahil, CalismakIstedigi, NedenKatilmakIstiyor, MotivasyonunNedir, FirstInterview, SecondInterview
				FROM form_application
				WHERE ID = newID;

				UPDATE form_application
				SET Timestamp_ = NEW.Timestamp_, SuAnkiDurum = NEW.SuAnkiDurum, ITPHEgitimKatilmak = NEW.ITPHEgitimKatilmak, EkonomikDurum = NEW.EkonomikDurum, DilKursunaDevam = NEW.DilKursunaDevam, IngilizceSeviye = NEW.IngilizceSeviye, HollandacaSeviye = NEW.HollandacaSeviye, BaskiGoruyor = NEW.BaskiGoruyor, BootcampBitirdi = NEW.BootcampBitirdi, OnlineITKursu = NEW.OnlineITKursu, ITTecrube = NEW.ITTecrube, ProjeDahil = NEW.ProjeDahil, CalismakIstedigi = NEW.CalismakIstedigi, NedenKatilmakIstiyor = NEW.NedenKatilmakIstiyor, MotivasyonunNedir = NEW.MotivasyonunNedir
				WHERE ID = newID;
				-- (OLD) add log
				INSERT INTO trigger_logs (log_message, log_time) VALUES ('(OLD) Application information is updated "in trg_after_update_form_data"', NEW.Timestamp_);
			END IF;
        END IF;
        -- ******************* --

    ELSE
        -- Check the applicant's data and update if there are any changes
        IF (SELECT Name FROM form_applicant WHERE ID = applicantID) <> NEW.Name OR
           (SELECT Surname FROM form_applicant WHERE ID = applicantID) <> NEW.Surname OR
           (SELECT Phone FROM form_applicant WHERE ID = applicantID) <> NEW.Phone OR
           (SELECT PostCode FROM form_applicant WHERE ID = applicantID) <> NEW.PostCode OR
           (SELECT Province FROM form_applicant WHERE ID = applicantID) <> NEW.Province THEN

            INSERT INTO form_old_applicant (ID_in_ApplicantTable, WhenUpdated, Timestamp_, Name, Surname, Email, Phone, PostCode, Province)
            SELECT ID, NEW.Timestamp_, Timestamp_, Name, Surname, Email, Phone, PostCode, Province
            FROM form_applicant
            WHERE ID = applicantID;

            UPDATE form_applicant
            SET Timestamp_ = NEW.Timestamp_, Name = NEW.Name, Surname = NEW.Surname, Phone = NEW.Phone, PostCode = NEW.PostCode, Province = NEW.Province
            WHERE ID = applicantID;
            -- add log
            INSERT INTO trigger_logs (log_message, log_time) VALUES ('Applicant information is updated "in trg_after_update_form_data"', NEW.Timestamp_);
        END IF;

        -- Application period control and addition/update
        SELECT ID INTO newID FROM form_application WHERE ApplicantID = applicantID AND Period = NEW.Period;
        IF newID IS NULL THEN
            -- add log
            INSERT INTO trigger_logs (log_message, log_time) VALUES ('Unexpected code situation! This code shuldn\'t be executed... ("in trg_after_update_form_data")', NEW.Timestamp_);
        ELSE
            -- Check the application's data and update if there are any changes
			IF (SELECT SuAnkiDurum FROM form_application WHERE ID = newID) <> NEW.SuAnkiDurum OR
            (SELECT ITPHEgitimKatilmak FROM form_application WHERE ID = newID) <> NEW.ITPHEgitimKatilmak OR
            (SELECT EkonomikDurum FROM form_application WHERE ID = newID) <> NEW.EkonomikDurum OR
            (SELECT DilKursunaDevam FROM form_application WHERE ID = newID) <> NEW.DilKursunaDevam OR
            (SELECT IngilizceSeviye FROM form_application WHERE ID = newID) <> NEW.IngilizceSeviye OR
            (SELECT HollandacaSeviye FROM form_application WHERE ID = newID) <> NEW.HollandacaSeviye OR
            (SELECT BaskiGoruyor FROM form_application WHERE ID = newID) <> NEW.BaskiGoruyor OR
            (SELECT BootcampBitirdi FROM form_application WHERE ID = newID) <> NEW.BootcampBitirdi OR
            (SELECT OnlineITKursu FROM form_application WHERE ID = newID) <> NEW.OnlineITKursu OR
            (SELECT ITTecrube FROM form_application WHERE ID = newID) <> NEW.ITTecrube OR
            (SELECT ProjeDahil FROM form_application WHERE ID = newID) <> NEW.ProjeDahil OR
            (SELECT CalismakIstedigi FROM form_application WHERE ID = newID) <> NEW.CalismakIstedigi OR
            (SELECT NedenKatilmakIstiyor FROM form_application WHERE ID = newID) <> NEW.NedenKatilmakIstiyor OR
            (SELECT MotivasyonunNedir FROM form_application WHERE ID = newID) <> NEW.MotivasyonunNedir THEN
				INSERT INTO form_old_application (ID_in_applicationTable, WhenUpdated, ApplicantID, Timestamp_, Period, SuAnkiDurum, ITPHEgitimKatilmak, EkonomikDurum, DilKursunaDevam, IngilizceSeviye, HollandacaSeviye, BaskiGoruyor, BootcampBitirdi, OnlineITKursu, ITTecrube, ProjeDahil, CalismakIstedigi, NedenKatilmakIstiyor, MotivasyonunNedir, FirstInterview, SecondInterview)
				SELECT ID, NEW.Timestamp_, ApplicantID, Timestamp_, Period, SuAnkiDurum, ITPHEgitimKatilmak, EkonomikDurum, DilKursunaDevam, IngilizceSeviye, HollandacaSeviye, BaskiGoruyor, BootcampBitirdi, OnlineITKursu, ITTecrube, ProjeDahil, CalismakIstedigi, NedenKatilmakIstiyor, MotivasyonunNedir, FirstInterview, SecondInterview
				FROM form_application
				WHERE ID = newID;

				UPDATE form_application
				SET Timestamp_ = NEW.Timestamp_, SuAnkiDurum = NEW.SuAnkiDurum, ITPHEgitimKatilmak = NEW.ITPHEgitimKatilmak, EkonomikDurum = NEW.EkonomikDurum, DilKursunaDevam = NEW.DilKursunaDevam, IngilizceSeviye = NEW.IngilizceSeviye, HollandacaSeviye = NEW.HollandacaSeviye, BaskiGoruyor = NEW.BaskiGoruyor, BootcampBitirdi = NEW.BootcampBitirdi, OnlineITKursu = NEW.OnlineITKursu, ITTecrube = NEW.ITTecrube, ProjeDahil = NEW.ProjeDahil, CalismakIstedigi = NEW.CalismakIstedigi, NedenKatilmakIstiyor = NEW.NedenKatilmakIstiyor, MotivasyonunNedir = NEW.MotivasyonunNedir
				WHERE ID = newID;
				-- add log
				INSERT INTO trigger_logs (log_message, log_time) VALUES ('Application information is updated "in trg_after_update_form_data"', NEW.Timestamp_);
			END IF;
        END IF;
    END IF;
    -- add log to verify that the trigger worked
    INSERT INTO trigger_logs (log_message, log_time) VALUES ('trg_after_update_form_data tigger is executed', NEW.Timestamp_);
END//

DELIMITER ;