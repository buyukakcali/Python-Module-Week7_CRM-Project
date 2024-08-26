DELIMITER //

CREATE TRIGGER trg_after_update_form2_data
AFTER UPDATE ON form2_data
FOR EACH ROW
BEGIN
    DECLARE applicantID INT;
    DECLARE candidateID INT;
    DECLARE mentorName varchar(45);
    DECLARE mentorSurname varchar(45);
    DECLARE mentorMail varchar(45);
    
    -- Getting the last added MentorMail value from form2_data
    SELECT crm_MentorMail INTO mentorMail FROM form2_data WHERE crm_ID = NEW.crm_ID;
    
    -- Getting MentorName, MentorSurname via MentorMail value
    SELECT crm_MentorName, crm_MentorSurname INTO mentorName, mentorSurname FROM form2_evaluations WHERE crm_MentorMail = mentorMail LIMIT 1;
    
    -- Getting and controlling Candidate control via name and surname. WARNING: collation settings type for comparison should not be case sensitive
    SELECT crm_ID INTO applicantID FROM form1_applicant WHERE TRIM(crm_Name) = TRIM(NEW.crm_CandidateName) AND TRIM(crm_Surname) = TRIM(NEW.crm_CandidateSurname) LIMIT 1;
    SELECT crm_CandidateID INTO candidateID FROM form2_evaluations WHERE crm_CandidateID = applicantID AND crm_Period = NEW.crm_Period;
    
    
	IF applicantID IS NULL THEN
		INSERT INTO crm_warnings (crm_log_message, crm_log_time) VALUES ('Mentor, adayin ad ve soyadini yanlis girdi in trg_after_update_form2_data trigger', NEW.crm_Timestamp);
        INSERT INTO trigger_logs (log_message, log_time) VALUES ('Mentor adayin ad ve soyadini yanlis girdi NOT to form2_evaluations table', NEW.crm_Timestamp);
        -- form2data icinden ilgili satir silinebilir. ama bu sefer de excell ile ayni olma ozelligini yitirir... Dusun bunu!
        -- alternatif: buradan warnings diye bir tabloya kayit yaparim. uygulama her acildiginda bu tabloda yeni satir varsa uyari verir. uyari gorundukten 
        -- sonra warnings_old tablosuna tasinir. veya baska bir yontem dusunuruz. tek tablo senaryosu olarak...
        -- burasi icin guncellerken bir hata oldu, mentor guncelleyemedi diye uyari yazdiririz...
	ELSEIF (applicantID IS NOT NULL) AND (candidateID IS NULL) THEN
    -- in the normal situations, no way to run this code block
        INSERT INTO crm_warnings (crm_log_message, crm_log_time) VALUES ('Ciddi bir sorun var. bu kodun calismamasi gerekir! form2_data table', NEW.crm_Timestamp);
        INSERT INTO trigger_logs (log_message, log_time) VALUES ('Ciddi bir sorun var. bu kodun calismamasi gerekir! form2_data table', NEW.crm_Timestamp);
        
    ELSE
		-- the evaluation information will be updated via editing the same form!
        
        -- >> Check the evaluation's data and update if there are any changes
        IF (SELECT crm_Timestamp FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_Timestamp OR
           (SELECT crm_MentorName FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> mentorName OR
           (SELECT crm_MentorSurname FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> mentorSurname OR
           (SELECT crm_MentorMail FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> mentorMail OR
           (SELECT crm_ITSkills FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_ITSkills OR
           (SELECT crm_Availability FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_Availability OR
           (SELECT crm_Recommendation FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_Recommendation OR
           (SELECT crm_Comment FROM form2_evaluations WHERE crm_CandidateID = candidateID) <> NEW.crm_Comment THEN 			
				INSERT INTO form2_evaluations_old (crm_WhenUpdated, crm_ID_in_form2_evaluations, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_CandidateID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment)
				SELECT NEW.crm_Timestamp, crm_ID, crm_Timestamp, crm_Period, crm_MentorName, crm_MentorSurname, crm_MentorMail, crm_CandidateID, crm_ITSkills, crm_Availability, crm_Recommendation, crm_Comment
				FROM form2_evaluations 
                WHERE crm_CandidateID = candidateID;
                
                UPDATE form2_evaluations
				SET crm_Timestamp = NEW.crm_Timestamp, crm_MentorName = mentorName, crm_MentorSurname = mentorSurname, crm_MentorMail = mentorMail, crm_ITSkills = NEW.crm_ITSkills, crm_Availability = NEW.crm_Availability, crm_Recommendation = NEW.crm_Recommendation, crm_Comment = NEW.crm_Comment 
                WHERE crm_CandidateID = candidateID;            
            -- add log
            INSERT INTO trigger_logs (log_message, log_time) VALUES ('(WITH NEW FORM FILLING) Evaluation data is updated "in trg_after_update_form2_data"', NEW.crm_Timestamp);
        END IF;
    END IF;
		
    -- add log to verify that the trigger worked
    INSERT INTO trigger_logs (log_message, log_time) VALUES ('trg_after_update_form2_data trigger is executed', NEW.crm_Timestamp);
END//

DELIMITER ;
