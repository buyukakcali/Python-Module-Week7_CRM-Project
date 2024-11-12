function getWhitelist() {
  try {
    var scriptProperties = PropertiesService.getScriptProperties();

    var validTables = scriptProperties.getProperty('VALID_TABLES').split(', ');
    var validColumns = scriptProperties.getProperty('VALID_COLUMNS').split(', ');

    return {
      validTables: validTables,
      validColumns: validColumns
    };
  } catch (e) {
    console.error('Error occurred in getWhitelist function: ' + e.stack);
  }
}