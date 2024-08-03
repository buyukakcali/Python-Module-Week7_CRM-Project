function convertToTimestamp(dateString) {
  var formats = [
    { regex: /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?(?:Z|[+-]\d{2}:\d{2})?$/, parser: parseISO },
    { regex: /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/, parser: parseYYYYMMDD_HHMMSS },
    { regex: /^\d{4}-\d{2}-\d{2}$/, parser: parseYYYYMMDD },
    { regex: /^\d{2}\/\d{2}\/\d{4}$/, parser: parseMMDDYYYY },
    { regex: /^\d{2}-\d{2}-\d{4}$/, parser: parseDDMMYYYY },
    { regex: /^\d{4}\/\d{2}\/\d{2}$/, parser: parseYYYYMMDD_Slash },
    { regex: /^\d{8}T\d{6}$/, parser: parseCompact },
    { regex: /^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}$/, parser: parseDDMMYYYY_HHMMSS },
    { regex: /^\d{1,2}\.\d{1,2}\.\d{4} \d{2}:\d{2}:\d{2}$/, parser: parseDMMYYYY_HHMMSS },
    { regex: /^\d{1,2}\/\d{1,2}\/\d{4} \d{2}:\d{2}:\d{2}$/, parser: parseMDYYYY_HHMMSS },
    { regex: /^\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}:\d{2}$/, parser: parseDMYYYY_HHMMSS },
    { regex: /^\d{1,2}\.\d{1,2}\.\d{4} \d{2}:\d{2}:\d{2}$/, parser: parseMDYYYY_HHMMSS },
    { regex: /^[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2} GMT[+-]\d{4} \(.*\)$/, parser: parseDateString }
  ];

  for (var i = 0; i < formats.length; i++) {
    var format = formats[i];
    if (format.regex.test(dateString)) {
      return format.parser(dateString);
    }
  }

  // Default parser for other date formats, including all time zones and country formats
  return parseDefault(dateString);
}

function parseISO(dateString) {
  return new Date(dateString);
}

function parseYYYYMMDD_HHMMSS(dateString) {
  var parts = dateString.split(/[- :]/);
  return new Date(parts[0], parts[1] - 1, parts[2], parts[3], parts[4], parts[5]);
}

function parseYYYYMMDD(dateString) {
  var parts = dateString.split('-');
  return new Date(parts[0], parts[1] - 1, parts[2]);
}

function parseMMDDYYYY(dateString) {
  var parts = dateString.split('/');
  return new Date(parts[2], parts[0] - 1, parts[1]);
}

function parseDDMMYYYY(dateString) {
  var parts = dateString.split('-');
  return new Date(parts[2], parts[1] - 1, parts[0]);
}

function parseYYYYMMDD_Slash(dateString) {
  var parts = dateString.split('/');
  return new Date(parts[0], parts[1] - 1, parts[2]);
}

function parseCompact(dateString) {
  var year = parseInt(dateString.substring(0, 4), 10);
  var month = parseInt(dateString.substring(4, 6), 10) - 1;
  var day = parseInt(dateString.substring(6, 8), 10);
  var hour = parseInt(dateString.substring(9, 11), 10);
  var minute = parseInt(dateString.substring(11, 13), 10);
  var second = parseInt(dateString.substring(13, 15), 10);
  return new Date(year, month, day, hour, minute, second);
}

function parseDDMMYYYY_HHMMSS(dateString) {
  var parts = dateString.split(/[. :]/);
  var day = parts[0];
  var month = parts[1];
  var year = parts[2];
  var hour = parts[3];
  var minute = parts[4];
  var second = parts[5];
  
  return new Date(year, month - 1, day, hour, minute, second);
}

function parseDMMYYYY_HHMMSS(dateString) {
  var parts = dateString.split(/[. :]/);
  var day = parts[0];
  var month = parts[1];
  var year = parts[2];
  var hour = parts[3];
  var minute = parts[4];
  var second = parts[5];

  return new Date(year, month - 1, day, hour, minute, second);
}

function parseMDYYYY_HHMMSS(dateString) {
  var parts = dateString.split(/[\/. :]/);
  var month = parts[0];
  var day = parts[1];
  var year = parts[2];
  var hour = parts[3];
  var minute = parts[4];
  var second = parts[5];

  return new Date(year, month - 1, day, hour, minute, second);
}

function parseDMYYYY_HHMMSS(dateString) {
  var parts = dateString.split(/[- :]/);
  var day = parts[0];
  var month = parts[1];
  var year = parts[2];
  var hour = parts[3];
  var minute = parts[4];
  var second = parts[5];

  return new Date(year, month - 1, day, hour, minute, second);
}

function parseDateString(dateString) {
  return new Date(dateString);
}

function parseDefault(dateString) {
  return new Date(dateString);
}