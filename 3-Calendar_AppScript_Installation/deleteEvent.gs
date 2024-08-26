function deleteEvent(cnf_, conn_, currentEventIds_, sheetData_, lastApplicationPeriod_, lastApplicationPeriodStartDate_) {
  // .................................DELETION PROCEDURES ........................................... //
  var deletedCount_ = 0;

  // .................. Variables Area ................... //
  var applicationTable = cnf_.getApplicationTable();
  var applicationPeriodFieldName = cnf_.getApplicationPeriodFieldName();
  var firstInterviewFieldName = cnf_.getFirstInterviewFieldName();
  var applicantIdFieldName = cnf_.getApplicantIdFieldName();

  var appointmentsTable = cnf_.getAppointmentsTable();
  var eventIdFieldName = cnf_.getEventIdFieldName();
  var attendeeIdFiledName = cnf_.getAttendeeIdFieldName();
  var java_sql_Types = cnf_.getJava_sql_Types();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  // ..................................................... //

  try {
    // Check and remove deleted or expired events
    for (var i = sheetData_.length - 1; i >= 0; i--) {
      var sheetEventId = sheetData_[i][1]; // We assume eventId is in column 2
      if (currentEventIds_.has(sheetEventId) === false) {
        // Logger.log('Only the section about deleted items needs to be filled in!')

        // NOT: If the lastApplicationPeriodStartDate value is greater than InterviewDatetime, that is, if a new application period is opened, the MentorApplication process is not automatically canceled. This code only prevents any confusion that may occur if the appointment has been deleted in some way. For example, the mentor has created an appointment date. After that, the CRM Application user/manager assigned an applicant to the appointment created by this mentor. However, if the mentor deletes the appointment without informing the manager, we will automatically cancel the mentor appointment process for the applicant.
        // Buraya bir de mail atma islevi konularak Basvuran ve Yoneticinin bilgilendirilmesi saglanabilir.

        // Logger.log(lastApplicationPeriodStartDate_ + '<?' + sheetData_[i][2]);
        if (lastApplicationPeriodStartDate_ < sheetData_[i][2]){ // This works for appointments that are deleted while the final application period is in progress!
          var queryIsAssignedAppointment = 'SELECT ' + attendeeIdFiledName + ' FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = \'' + sheetEventId + '\'';
          var stmtIsAssignedAppointment = conn_.createStatement();
          var attendeeId = null;
          var resultIsAssignedAppointment = null;

          try {
            resultIsAssignedAppointment = stmtIsAssignedAppointment.executeQuery(queryIsAssignedAppointment);
            if (resultIsAssignedAppointment.next()) {
              attendeeId = resultIsAssignedAppointment.getInt(attendeeIdFiledName);  // AttendeeID value will be here
            }
          } catch (e) {
            console.error('Error: ' + e);
          } finally {
            stmtIsAssignedAppointment.close();    // Statement is closing
            resultIsAssignedAppointment.close();  // ResultSet is closing
          }

          if (attendeeId !== 0 && attendeeId !== null) {
            //  Logger.log('It is entered here to empty the appointment values of the applicants who have been assigned a mentor in the relevant tables and then delete them!');
            // Empty the record from appointments table
            var queryUnassignAppointment = 'UPDATE ' + appointmentsTable + ' SET ' + attendeeIdFiledName + ' = ? WHERE ' + eventIdFieldName + ' = ?';
            var stmtUnassignAppointment = conn_.prepareStatement(queryUnassignAppointment);
            stmtUnassignAppointment.setNull(1, java_sql_Types.INTEGER);
            stmtUnassignAppointment.setString(2, sheetEventId);
            // Logger.log('Sorgu Metni: ' + queryUnassignAppointment);
            var resultUnassignAppointment = null;

            // Empty the record from form_application table too
            var queryUnassignApplicant = 'UPDATE ' + applicationTable + ' SET ' +firstInterviewFieldName+ ' = ? WHERE ' +applicantIdFieldName+ ' = ? AND ' + applicationPeriodFieldName + ' = ?';
            var stmtUnassignApplicant = conn_.prepareStatement(queryUnassignApplicant);
            stmtUnassignApplicant.setInt(1, 0);
            stmtUnassignApplicant.setInt(2, attendeeId);
            stmtUnassignApplicant.setString(3, lastApplicationPeriod_);
            // Logger.log('Sorgu Metni: ' + queryUnassignApplicant)
            var resultUnassignApplicant = null;

            try {
              resultUnassignAppointment = stmtUnassignAppointment.executeUpdate();
              resultUnassignApplicant = stmtUnassignApplicant.executeUpdate();

              // Logger.log('resultUnassignAppointment: ' + resultUnassignAppointment);
              // Logger.log('resultUnassignApplicant: ' + resultUnassignApplicant);
              if (resultUnassignAppointment && resultUnassignApplicant) {
                Logger.log('Mentor appointment has been withdrawn/cancelled!\nDetails: The assignments in tables '+ appointmentsTable +' and ' + applicationTable + ' have been updated to null and 0.');
              }
            } catch (e) {
              console.error('Error: ' + e);
            } finally {
              stmtUnassignAppointment.close();    // 1. statement is closing
              stmtUnassignApplicant.close();      // 2. statement is closing
            }
          }

          sheet.deleteRow(i + 2); // +2 because header row and 0-based index
          // Prepare the delete query
          var queryDeleteEvent = 'DELETE FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = ?';
          var stmtDeleteEvent = conn_.prepareStatement(queryDeleteEvent);
          stmtDeleteEvent.setString(1, sheetEventId);
          var resultStmtDeleteEvent = null;

          try {
            resultStmtDeleteEvent = stmtDeleteEvent.executeUpdate();
            if (resultStmtDeleteEvent > 0) {
              Logger.log('Appointment record(' +eventIdFieldName + '= ' + sheetEventId + ') canceled during the application period was deleted and moved to the appointments_old_or_deleted table.');
            } else {
              Logger.log('No record (' + eventIdFieldName + '= ' + sheetEventId + ') was found.');
            }
          } catch (e) {
            console.error('Error: ' + e);
          }
          finally {
            stmtDeleteEvent.close();    // Statement is closing
          }
        } else {
          sheet.deleteRow(i + 2); // +2 because header row and 0-based index
          // Prepare the delete query
          var queryDeleteEventLast = 'DELETE FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = ?';
          var stmtDeleteEventLast = conn_.prepareStatement(queryDeleteEventLast);
          stmtDeleteEventLast.setString(1, sheetEventId);
          var resultStmtDeleteEventLast = null;

          try {
            resultStmtDeleteEventLast = stmtDeleteEventLast.executeUpdate();
            if (resultStmtDeleteEventLast > 0) {
              Logger.log('Due to the start of the new application period, the appointment record(' + eventIdFieldName + '= ' + sheetEventId + ') has been deleted and moved to the appointments_old_or_deleted table.');
            } else {
              Logger.log('No record (' + eventIdFieldName + '= ' + sheetEventId + ' was found.');
            }
          } catch (e) {
            console.error('Error: ' + e);
          }
          finally {
            stmtDeleteEventLast.close();    // Statement is closing
          }
        }
        deletedCount_++;
      }
    }
  } catch (e) {
    console.error('Error occured in deleteEvent function: ' + e);
  } finally {
    return deletedCount_;
  }  
}
