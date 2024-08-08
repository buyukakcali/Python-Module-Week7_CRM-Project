function deleteEvent(cnf_, conn_, sheet_, currentEventIds_, sheetData_, lastApplicationPeriod_, lastApplicationPeriodStartDate_) {
  // .................................SILME ISLEMLERI........................................... //
  var deletedCount_ = 0;
  
  // .................. Configurtaion Area Starts ................... //
  var applicationTable = cnf_.getApplicationTable();
  var applicationPeriodFieldName = cnf_.getApplicationPeriodFieldName();
  var firstInterviewFieldName = cnf_.getFirstInterviewFieldName();
  var applicantIdFieldName = cnf_.getApplicantIdFieldName();

  var appointmentsTable = cnf_.getAppointmentsTable();
  var eventIdFieldName = cnf_.getEventIdFieldName();
  var menteeIdFiledName = cnf_.getMenteeIdFieldName();
  var java_sql_Types = cnf_.getJava_sql_Types();
  // .................. Configurtaion Area Ends  .................... //

  try {
    // Silinen veya zamanı geçmiş etkinlikleri kontrol et ve kaldır
    for (var i = sheetData_.length - 1; i >= 0; i--) {
      var sheetEventId = sheetData_[i][1]; // eventId'nin 2. sütunda olduğunu varsayıyoruz
      if (currentEventIds_.has(sheetEventId) === false) {
        // Logger.log('Sadece silinenler ile ilgili bolumde girmesi gerekiyor!')
        
        // NOT: lastApplicationPeriodStartDate degeri MulakatZamani'ndan buyukse, yani yeni bir basvuru donemi acilmissa MentorAtama islemi otomatik iptal edilmez. Bu kod yalnizca randevunun bir sekilde silinmis olmasi sebebiyle olusabilecek karisikligi engeller. Mesela mentor bir randevu tarihi olusturmustur. Bundan sonra CRM Uygulama kullanicisi/yoneticisi bir basvurani bu mentorun olusturdugu randevuya atamistir. Ne var ki mentor, yoneticiye bilgi vermeden randevuyu silerse, basvuranla ilgili mentor atama islemini otomatikman iptal etmis oluruz. 
        // tek birtransaction icinde olmali
        // Buraya bir de mail atma islevi konularak Basvuran ve Yoneticinin bilgilendirilmesi saglanabilir.

        // Logger.log(lastApplicationPeriodStartDate_ + '<?' + sheetData_[i][2]);        
        if (lastApplicationPeriodStartDate_ < sheetData_[i][2]){ // Burasi son basvuru donemi devam ederken silinen randevular icin calisir!
          var queryIsAssignedAppointment = 'SELECT ' + menteeIdFiledName + ' FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = \'' + sheetEventId + '\'';
          var stmtIsAssignedAppointment = conn_.createStatement();
          var menteeId = null;
          var resultIsAssignedAppointment = null;
          
          try {
            resultIsAssignedAppointment = stmtIsAssignedAppointment.executeQuery(queryIsAssignedAppointment);
            if (resultIsAssignedAppointment.next()) {
              menteeId = resultIsAssignedAppointment.getInt(menteeIdFiledName);  // MentiID degeri burada olacak
            }
          } catch (e) {
            console.error('Error: ' + e);
          } finally {
            stmtIsAssignedAppointment.close();    // Statement kapatılıyor
            resultIsAssignedAppointment.close();  // ResultSet kapatiliyor
          }
          
          if (menteeId !== 0 && menteeId !== null) {
            //  Logger.log('Mentor atanmis olanlari once bosaltip sonra silmek icin buraya girer!');
            // Empty the record from appointments table
            var queryUnassignAppointment = 'UPDATE ' + appointmentsTable + ' SET ' + menteeIdFiledName + ' = ? WHERE ' + eventIdFieldName + ' = ?';
            var stmtUnassignAppointment = conn_.prepareStatement(queryUnassignAppointment);
            stmtUnassignAppointment.setNull(1, java_sql_Types.INTEGER);
            stmtUnassignAppointment.setString(2, sheetEventId);
            // Logger.log('Sorgu Metni: ' + queryUnassignAppointment);
            var resultUnassignAppointment = null;
            
            // Empty the record from form_basvuru table too
            var queryUnassignApplicant = 'UPDATE ' + applicationTable + ' SET ' +firstInterviewFieldName+ ' = ? WHERE ' +applicantIdFieldName+ ' = ? AND ' + applicationPeriodFieldName + ' = ?';
            var stmtUnassignApplicant = conn_.prepareStatement(queryUnassignApplicant);
            stmtUnassignApplicant.setInt(1, 0);
            stmtUnassignApplicant.setInt(2, menteeId);
            stmtUnassignApplicant.setString(3, lastApplicationPeriod_);
            // Logger.log('Sorgu Metni: ' + queryUnassignApplicant)
            var resultUnassignApplicant = null;

            try {
              resultUnassignAppointment = stmtUnassignAppointment.executeUpdate();
              resultUnassignApplicant = stmtUnassignApplicant.executeUpdate();

              // Logger.log('resultUnassignAppointment: ' + resultUnassignAppointment);
              // Logger.log('resultUnassignApplicant: ' + resultUnassignApplicant);              
              if (resultUnassignAppointment && resultUnassignApplicant) {
                Logger.log('Mentor atama islemi geri alindi / iptal edildi!\nDetay:  '+ appointmentsTable +' ve ' + applicationTable + ' tablolarindaki atamalar null ve 0 olarak yeniden guncellendi.');
              }
            } catch (e) {
              console.error('Error: ' + e);
            } finally {
              stmtUnassignAppointment.close();    // 1. statement kapatılıyor
              stmtUnassignApplicant.close();      // 2. statement kapatılıyor
            }
          }

          sheet_.deleteRow(i + 2); // +2 çünkü başlık satırı ve 0-tabanlı indeks
          // Silme sorgusunu hazırlayın
          var queryDeleteEvent = 'DELETE FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = ?';
          var stmtDeleteEvent = conn_.prepareStatement(queryDeleteEvent);
          stmtDeleteEvent.setString(1, sheetEventId);
          var resultStmtDeleteEvent = null;
          
          try {
            resultStmtDeleteEvent = stmtDeleteEvent.executeUpdate();
            if (resultStmtDeleteEvent > 0) {
              Logger.log('Basvuru donemi icinde iptal edilen randevu kaydi(' +eventIdFieldName + '= ' + sheetEventId + ') silinerek appointments_old_or_deleted tablosuna tasindi.');
            } else {
              Logger.log(eventIdFieldName + ': ' + sheetEventId + ' olan kayıt bulunamadı.');
            }
          } catch (e) {
            console.error('Error: ' + e);
          }
          finally {
            stmtDeleteEvent.close();    // Statement kapatılıyor
          }
        } else {
          sheet_.deleteRow(i + 2); // +2 çünkü başlık satırı ve 0-tabanlı indeks
          // Silme sorgusunu hazırlayın
          var queryDeleteEventLast = 'DELETE FROM ' + appointmentsTable + ' WHERE ' + eventIdFieldName + ' = ?';
          var stmtDeleteEventLast = conn_.prepareStatement(queryDeleteEventLast);
          stmtDeleteEventLast.setString(1, sheetEventId);
          var resultStmtDeleteEventLast = null;

          try {
            resultStmtDeleteEventLast = stmtDeleteEventLast.executeUpdate();
            if (resultStmtDeleteEventLast > 0) {
              Logger.log('Yeni bir basvuru donemi basladigi icin olan kayit(' + eventIdFieldName + '= ' + sheetEventId + ') silinerek old_or_deleted tablosuna tasindi.');
            } else {
              Logger.log(eventIdFieldName + '= ' + sheetEventId + ' olan kayit bulunamadi.');
            }
          } catch (e) {
            console.error('Error: ' + e);
          }
          finally {
            stmtDeleteEventLast.close();    // Statement kapatılıyor
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
