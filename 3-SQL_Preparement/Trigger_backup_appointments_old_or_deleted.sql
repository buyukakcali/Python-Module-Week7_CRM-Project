DELIMITER //

CREATE TRIGGER trg_backup_appointments_old_or_deleted
AFTER DELETE ON appointments
FOR EACH ROW
BEGIN
    INSERT INTO appointments_old_or_deleted (
        WhenDeleted,
        ID_Deleted,
        Timestamp_,
        EventID,
        InterviewDatetime,
        MentorName,
        MentorSurname,
        MentorMail,
        Summary,
        Description,
        Location,
        OnlineMeetingLink,
        ResponseStatus,
        AttendeeID
    ) VALUES (
        CURRENT_Timestamp,
        OLD.ID,
        OLD.Timestamp_,
        OLD.EventID,
        OLD.InterviewDatetime,
        OLD.MentorName,
        OLD.MentorSurname,
        OLD.MentorMail,
        OLD.Summary,
        OLD.Description,
        OLD.Location,
        OLD.OnlineMeetingLink,
        OLD.ResponseStatus,
        OLD.AttendeeID
    );
    -- Add log
    INSERT INTO trigger_logs (log_message, log_time) VALUES (CONCAT('The event ( ID = ' , OLD.ID, ',  EventID = ', OLD.EventID, ' ) is deleted from appointments table "in trg_backup_appointments_old_or_deleted"'), CURRENT_Timestamp);
END //

DELIMITER ;