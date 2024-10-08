function parseTimestamp(timestamp) {
  try {
    // Giriş değerini string'e çevir
    if (typeof timestamp !== 'string') {
      timestamp = timestamp.toString();
    }

    // ISO 8601 formatı
    if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$/.test(timestamp)) {
      return new Date(timestamp).toISOString();
    }

    // ABD formatı (M/D/YYYY H:MM:SS AM/PM)
    if (/^\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{2}:\d{2} (AM|PM)$/.test(timestamp)) {
      return new Date(timestamp).toISOString();
    }

    // Avrupa formatı (D.M.YYYY H:MM:SS)
    if (/^\d{1,2}\.\d{1,2}\.\d{4} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('.');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[2], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[0], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // Yıl, Ay, Gün formatı (YYYY/M/D H:MM:SS)
    if (/^\d{4}\/\d{1,2}\/\d{1,2} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('/');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[0], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[2], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // Gün/Ay/Yıl formatı (D/M/YYYY H:MM:SS)
    if (/^\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('/');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[2], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[0], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // Gün-Ay-Yıl formatı (D-M-YYYY H:MM:SS)
    if (/^\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('-');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[2], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[0], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // Yıl.Ay.Gün formatı (YYYY.M.D H:MM:SS)
    if (/^\d{4}\.\d{1,2}\.\d{1,2} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('.');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[0], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[2], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // YYYY-MM-DD formatı (YYYY-MM-DD H:MM:SS)
    if (/^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}$/.test(timestamp)) {
      var parts = timestamp.split(' ');
      var dateParts = parts[0].split('-');
      var timeParts = parts[1].split(':');
      return new Date(Date.UTC(
        parseInt(dateParts[0], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[2], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2], 10)
      )).toISOString();
    }

    // YYYY-MM-DD formatı (sadece tarih)
    if (/^\d{4}-\d{2}-\d{2}$/.test(timestamp)) {
      return new Date(timestamp).toISOString();
    }

    // MM/DD/YYYY formatı
    if (/^\d{2}\/\d{2}\/\d{4}$/.test(timestamp)) {
      return new Date(timestamp).toISOString();
    }

    // YYYY/MM/DD formatı
    if (/^\d{4}\/\d{2}\/\d{2}$/.test(timestamp)) {
      var parts = timestamp.split('/');
      return new Date(Date.UTC(
        parseInt(parts[0], 10),
        parseInt(parts[1], 10) - 1,
        parseInt(parts[2], 10)
      )).toISOString();
    }

    // Kompakt format (YYYYMMDDTHHMMSS)
    if (/^\d{8}T\d{6}$/.test(timestamp)) {
      return new Date(
        timestamp.substr(0, 4),
        parseInt(timestamp.substr(4, 2), 10) - 1,
        timestamp.substr(6, 2),
        timestamp.substr(9, 2),
        timestamp.substr(11, 2),
        timestamp.substr(13, 2)
      ).toISOString();
    }

    // Standart JavaScript Date.toString() formatı
    if (/^[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2} GMT[+-]\d{4} \(.*\)$/.test(timestamp)) {
      return new Date(timestamp).toISOString();
    }

    // Eğer hiçbir format eşleşmezse
    throw new Error('Tanınmayan zaman damgası formatı: ' + timestamp);

  } catch (e) {
    console.error('Error  occurred in parseTimestamp function: ' + e.stack);
  }
}

/*

Açıklama:
ISO 8601 formatı: (^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$)
ABD formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}\/\d{1,2}\/\d{4} \d{1,2}:\d{2}:\d{2} (AM|PM)$)
Avrupa formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}\.\d{1,2}\.\d{4} \d{2}:\d{2}:\d{2}$)
Yıl, Ay, Gün formatı: Tek haneli gün ve ayları da destekler (^\d{4}\/\d{1,2}\/\d{1,2} \d{2}:\d{2}:\d{2}$)
Gün/Ay/Yıl formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2}:\d{2}$)
Gün-Ay-Yıl formatı: Tek haneli gün ve ayları da destekler (^\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}:\d{2}$)
Yıl.Ay.Gün formatı: Tek haneli gün ve ayları da destekler (^\d{4}\.\d{1,2}\.\d{1,2} \d{2}:\d{2}:\d{2}$)
YYYY-MM-DD formatı: Tek haneli gün ve ayları da destekler (^\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}$)
Sadece tarih (YYYY-MM-DD): (^\d{4}-\d{2}-\d{2}$)
MM/DD/YYYY formatı: (^\d{2}\/\d{2}\/\d{4}$)
YYYY/MM/DD formatı: (^\d{4}\/\d{2}\/\d{2}$)
Kompakt format: (^\d{8}T\d{6}$)
Standart JavaScript Date.toString() formatı: (^[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2} GMT[+-]\d{4} \(.*\)$)

Not: Tüm formatlar, uygun olduğunda tek haneli gün ve ayları destekler.
Fonksiyon, giriş değerini otomatik olarak string'e çevirir.
Çıktı her zaman ISO 8601 formatında olacaktır.

*/
