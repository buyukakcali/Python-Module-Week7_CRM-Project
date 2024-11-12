// This function is SQL INJECTION DANGER free function.
// But in other functions, I tried another type of method (using WhiteLists for table and column names).

function deleteEvent(currentEventIds, sheetData, lastApplicationPeriod, lastApplicationPeriodStartDate) {
  // .................................DELETION PROCEDURES ........................................... //
  var cnf = new Config();

  // .................. Variables Area ................... //
  // var applicationTable = cnf_.getApplicationTable();
  // var applicationPeriodFieldName = cnf_.getApplicationPeriodFieldName();
  // var firstInterviewFieldName = cnf_.getFirstInterviewFieldName();
  // var applicantIdFieldName = cnf_.getApplicantIdFieldName();

  // var appointmentsTable = cnf_.getAppointmentsTable();
  // var eventIdFieldName = cnf_.getEventIdFieldName();
  var attendeeIdFiledName = cnf.getAttendeeIdFieldName();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  // ..................................................... //

  try {
    // Check and remove deleted or expired events
    for (var i = sheetData.length - 1; i >= 0; i--) {
      var sheetEventId = sheetData[i][1]; // We assume eventId is in column 2
      var summaryFromSheet = sheetData[i][6].toString(); // We assume summary is in column 7
      // Logger.log('summaryFromSheet: ' + summaryFromSheet);
      if (currentEventIds.has(sheetEventId) === false) {
        var conn = cnf.openConn();
        // Logger.log('Only the section about deleted items needs to be filled in!')

        // NOT: If the lastApplicationPeriodStartDate value is greater than InterviewDatetime, that is, if a new application period is opened, the MentorApplication process is not automatically canceled. This code only prevents any confusion that may occur if the appointment has been deleted in some way. For example, the mentor has created an appointment date. After that, the CRM Application user/manager assigned an applicant to the appointment created by this mentor. However, if the mentor deletes the appointment without informing the manager, we will automatically cancel the mentor appointment process for the applicant.
        // Buraya bir de mail atma islevi konularak Basvuran ve Yoneticinin bilgilendirilmesi saglanabilir.

        // Logger.log(lastApplicationPeriodStartDate + '<?' + sheetData[i][2]);
        if (lastApplicationPeriodStartDate < sheetData[i][2]){ // This works for appointments that are deleted while the final application period is in progress!
          var queryIsAssignedAppointment = `SELECT crm_AttendeeID FROM appointments_current WHERE crm_EventID = ?`;
          var stmtIsAssignedAppointment = conn.prepareStatement(queryIsAssignedAppointment);
          stmtIsAssignedAppointment.setString(1, sheetEventId);

          var attendeeId = null;
          var resultIsAssignedAppointment = null;

          try {
            resultIsAssignedAppointment = stmtIsAssignedAppointment.executeQuery();
            if (resultIsAssignedAppointment.next()) {
              attendeeId = resultIsAssignedAppointment.getInt(attendeeIdFiledName);  // AttendeeID value will be here
            }
          } catch (e) {
            console.error('Error: ' + e.stack);
          } finally {
            stmtIsAssignedAppointment.close();    // Statement is closing
            resultIsAssignedAppointment.close();  // ResultSet is closing
          }

          if (attendeeId !== 0 && attendeeId !== null) {
            //  Logger.log('It is entered here to empty the appointment values of the applicants who have been assigned a mentor in the relevant tables and then delete them!');
            // Empty the record from appointments table
            var queryUnassignAppointment = 'UPDATE appointments_current SET crm_AttendeeID = ? WHERE crm_EventID = ?';
            var stmtUnassignAppointment = conn.prepareStatement(queryUnassignAppointment);
            stmtUnassignAppointment.setNull(1, Jdbc.Types.INTEGER);
            stmtUnassignAppointment.setString(2, sheetEventId);
            // Logger.log('Query string: ' + queryUnassignAppointment);
            var resultUnassignAppointment = null;

            if (summaryFromSheet && summaryFromSheet.trim()[0].startsWith('1')) {
              // First Interview Appointment
              // Empty the record from form_application table too
              var queryUnassignApplicant = 'UPDATE form1_application SET crm_FirstInterview = ? WHERE crm_ApplicantID = ? AND crm_Period = ?';
              var stmtUnassignApplicant = conn.prepareStatement(queryUnassignApplicant);
              stmtUnassignApplicant.setInt(1, 0);
              stmtUnassignApplicant.setInt(2, attendeeId);
              stmtUnassignApplicant.setString(3, lastApplicationPeriod);
              // Logger.log('Query string: ' + queryUnassignApplicant)
              var resultUnassignApplicant = null;

              try {
                resultUnassignAppointment = stmtUnassignAppointment.executeUpdate();
                resultUnassignApplicant = stmtUnassignApplicant.executeUpdate();

                // Logger.log('resultUnassignAppointment: ' + resultUnassignAppointment);
                // Logger.log('resultUnassignApplicant: ' + resultUnassignApplicant);
                if (resultUnassignAppointment && resultUnassignApplicant) {
                  Logger.log('Mentor appointment has been withdrawn/cancelled!\nDetails: The assignments in tables \'appointments\'  and \'application\' have been updated to null and 0');
                }
              } catch (e) {
                console.error('Error: ' + e.stack);
              } finally {
                stmtUnassignAppointment.close();    // 1. statement is closing
                stmtUnassignApplicant.close();      // 2. statement is closing
              }

            } else if (summaryFromSheet && summaryFromSheet.trim()[0].startsWith('2')) {
                // Project Interview Appointment
                // Empty the record from form_application table too
              var queryUnassignCandidate = 'UPDATE form2_evaluations SET crm_IsApplicantACandidate = ? WHERE crm_ApplicantID = ? AND crm_Period = ?';
              var stmtUnassignCandidate = conn.prepareStatement(queryUnassignCandidate);
              stmtUnassignCandidate.setInt(1, 1);
              stmtUnassignCandidate.setInt(2, attendeeId);
              stmtUnassignCandidate.setString(3, lastApplicationPeriod);
              // Logger.log('Query string: ' + queryUnassignCandidate)
              var resultUnassignCandidate = null;

              try {
                resultUnassignAppointment = stmtUnassignAppointment.executeUpdate();
                resultUnassignCandidate = stmtUnassignCandidate.executeUpdate();

                // Logger.log('resultUnassignAppointment: ' + resultUnassignAppointment);
                // Logger.log('resultUnassignCandidate: ' + resultUnassignCandidate);
                if (resultUnassignAppointment && resultUnassignCandidate) {
                  Logger.log('Mentor appointment has been withdrawn/cancelled!\nDetails: The assignments in tables \'appointments\'  and \'evaluations\' have been updated to null and 1');
                }
              } catch (e) {
                console.error('Error: ' + e.stack);
              } finally {
                stmtUnassignAppointment.close();    // 1. statement is closing
                stmtUnassignCandidate.close();      // 2. statement is closing
              }
            } else {
              Logger.log('For any other thing');
              Logger.log('Summary: ' + summaryFromSheet);
            }
          }

          sheet.deleteRow(i + 2); // +2 because header row and 0-based index
          // Prepare the delete query
          var queryDeleteEvent = 'DELETE FROM appointments_current WHERE crm_EventID = ?';
          var stmtDeleteEvent = conn.prepareStatement(queryDeleteEvent);
          stmtDeleteEvent.setString(1, sheetEventId);

          var resultStmtDeleteEvent = null;
          try {
            resultStmtDeleteEvent = stmtDeleteEvent.executeUpdate();
            if (resultStmtDeleteEvent > 0) {
              Logger.log('Appointment record(Event Id= ' + sheetEventId + ') canceled during the application period was deleted and moved to the appointments_old_or_deleted table.');
            } else {
              Logger.log('No record (Event Id= ' + sheetEventId + ') was found.');
            }
          } catch (e) {
            console.error('Error: ' + e.stack);
          }
          finally {
            stmtDeleteEvent.close();    // Statement is closing
          }
        } else {
          // Buraya mevcut sheet dosyasinin bir kopyasini arsivleyen bir kod yazabiliriz. Databasedekinden ziyade yedek olarak kalir. Sormak lazim once, zira bence gereksiz...
          sheet.deleteRow(i + 2); // +2 because header row and 0-based index
          // Prepare the delete query
          var queryDeleteEventLast = 'DELETE FROM appointments_current WHERE crm_EventID = ?';
          var stmtDeleteEventLast = conn.prepareStatement(queryDeleteEventLast);
          stmtDeleteEventLast.setString(1, sheetEventId);

          var resultStmtDeleteEventLast = null;
          try {
            resultStmtDeleteEventLast = stmtDeleteEventLast.executeUpdate();
            if (resultStmtDeleteEventLast > 0) {
              Logger.log('Due to the start of the new application period, the appointment record(Event Id= ' + sheetEventId + ') has been deleted and moved to the appointments_old_or_deleted table.');
            } else {
              Logger.log('No record (Event Id= ' + sheetEventId + ') was found.');
            }
          } catch (e) {
            console.error('Error: ' + e.stack);
          }
          finally {
            stmtDeleteEventLast.close();    // Statement is closing
          }
        }
      }
    }
  } catch (e) {
    console.error('Error occurred in deleteEvent function: ' + e.stack);
  } finally {
    if (conn) {
      conn.close();  // Connection kapatılıyor
    }
  }
}
