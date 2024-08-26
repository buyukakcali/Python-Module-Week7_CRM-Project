DELIMITER //

CREATE TRIGGER trg_after_insert_form2_data
AFTER INSERT ON form2_data
FOR EACH ROW
BEGIN
    DECLARE applicantID INT;
    DECLARE candidateID INT;
    DECLARE mentorName varchar(45);
    DECLARE mentorSurname varchar(45);
    DECLARE mentorMail varchar(45);
    
    -- Getting MentorName, MentorSurname via MentorMail value
    SELECT crm_MentorMail INTO mentorMail FROM form2_data WHERE crm_ID = NEW.crm_ID;
    
    -- Getting MentorName, MentorSurname via MentorMail value
    SELECT crm_MentorName, crm_MentorSurname INTO mentorName, mentorSurname FROM appointments_current WHERE crm_MentorMail = mentorMail LIMIT 1;
    
    -- Getting and controlling Candidate control via name and surname. WARNING: collation settings type for comparison should not be case sensitive
    SELECT crm_ID INTO applicantID FROM form1_applicant WHERE TRIM(crm_Name) = TRIM(NEW.crm_CandidateName) AND TRIM(crm_Surname) = TRIM(NEW.crm_CandidateSurname) LIMIT 1;
    SELECT crm_CandidateID INTO candidateID FROM form2_evaluations WHERE crm_CandidateID = applicantID AND crm_Period = NEW.crm_Period;
    
    
	IF applicantID IS NULL THEN
		INSERT INTO crm_warnings (crm_log_message, crm_log_time) VALUES ('Mentor, adayin ad ve soyadini yanlis girdi in trg_after_insert_form2_data trigger', NEW.crm_Timestamp);
        INSERT INTO trigger_logs (log_message, log_time) VALUES ('Mentor, adayin ad ve soyadini yanlis girdi NOT to form2_evaluations table', NEW.crm_Timestamp);
        -- form2data icinden ilgili satir silinebilir. ama bu sefer de excell ile ayni olma ozelligini yitirir... Dusun bunu!
        -- alternatif: buradan warnings diye bir tabloya kayit yaparim. uygulama her acildiginda bu tabloda yeni satir varsa uyari verir. uyari gorundukten 
        -- sonra warnings_old tablosuna tasinir. veya baska bir yontem dusunuruz. tek tablo senaryosu olarak...
        -- burasi icin eklerken bir hata oldu diye uyari yazdiririz...
	ELSEIF (applicantID IS NOT NULL) AND (candidateID IS NULL) THEN
		-- add new candidate
		SET candidateID = applicantID;	-- Eger yeni ekleme yapiliyorsa candidateID yi applicantID olarak atayabiliriz.
        INSERT INTO form2_evaluations (crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_CandidateID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment)
        VALUES (NEW.crm_Timestamp, NEW.crm_Period, mentorName, mentorSurname, NEW.crm_MentorMail, candidateID, NEW.crm_ITSkills, NEW.crm_Availability, NEW.crm_Recommendation, NEW.crm_Comment);
        
        -- add log
		INSERT INTO trigger_logs (log_message, log_time) VALUES ('New evaluation is added to form2_evaluations table', NEW.crm_Timestamp);
        
    ELSE
    
    -- <<< Under ELSE here, the evaluation information will be updated via filling a totally new form! >>> --
        -- This is the part that does the most complicated work. 
        -- If mentor wants to update his/her evaluation for the same candidate (with candidate name and surname) a few days later, it works. 
        
        -- >> Check the applicant's data and update if there are any changes
        IF (SELECT crm_Timestamp FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_Timestamp OR
           (SELECT crm_MentorName FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> mentorName OR
           (SELECT crm_MentorSurname FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> mentorSurname OR
           (SELECT crm_MentorMail FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_MentorMail OR
           (SELECT crm_ITSkills FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_ITSkills OR
           (SELECT crm_Availability FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_Availability OR
           (SELECT crm_Recommendation FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_Recommendation OR
           (SELECT crm_Comment FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_Comment THEN 			
				INSERT INTO form2_evaluations_old (crm_WhenUpdated, crm_ID_in_form2_evaluations, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_CandidateID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment)
				SELECT NEW.crm_Timestamp, crm_ID, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_CandidateID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment
				FROM form2_evaluations 
                WHERE crm_CandidateID = candidateID;
            
				UPDATE form2_evaluations
				SET crm_Timestamp = NEW.crm_Timestamp, crm_MentorName = mentorName, crm_MentorSurname = mentorSurname, crm_MentorMail = NEW.crm_MentorMail, crm_ITSkills = NEW.crm_ITSkills, crm_Availability = NEW.crm_Availability, crm_Recommendation = NEW.crm_Recommendation, crm_Comment = NEW.crm_Comment 
                WHERE crm_CandidateID = candidateID;         
            -- add log
            INSERT INTO trigger_logs (log_message, log_time) VALUES ('(WITH NEW FORM FILLING) Evaluation data is updated "in trg_after_insert_form2_data"', NEW.crm_Timestamp);
        END IF;
    END IF;
		
    -- add log to verify that the trigger worked
    INSERT INTO trigger_logs (log_message, log_time) VALUES ('trg_after_insert_form2_data trigger is executed', NEW.crm_Timestamp);
END//

DELIMITER ;