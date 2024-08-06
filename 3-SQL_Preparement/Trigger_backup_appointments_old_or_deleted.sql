DELIMITER //

CREATE TRIGGER backup_appointments_old_or_deleted
AFTER DELETE ON appointments
FOR EACH ROW
BEGIN
    INSERT INTO appointments_old_or_deleted (
        NeZamanSilindi,
        ID_Silinen,
        ZamanDamgasi,
        EtkinlikID,
        MulakatZamani,
        MentorAdi,
        MentorSoyadi,
        MentorMail,
        Summary,
        Description,
        Location,
        OnlineMeetingLink,
        ResponseStatus,
        MentiID
    ) VALUES (
        CURRENT_TIMESTAMP,
        OLD.ID,
        OLD.ZamanDamgasi,
        OLD.EtkinlikID,
        OLD.MulakatZamani,
        OLD.MentorAdi,
        OLD.MentorSoyadi,
        OLD.MentorMail,
        OLD.Summary,
        OLD.Description,
        OLD.Location,
        OLD.OnlineMeetingLink,
        OLD.ResponseStatus,
        OLD.MentiID
    );
    -- Add log
    INSERT INTO trigger_logs (log_message, log_time) VALUES (CONCAT('The event ( ID = ' , OLD.ID, ',  EventID = ', OLD.EtkinlikID, ' ) is deleted from appointments table "in backup_appointments_old_or_deleted"'), CURRENT_TIMESTAMP);
END //

DELIMITER ;