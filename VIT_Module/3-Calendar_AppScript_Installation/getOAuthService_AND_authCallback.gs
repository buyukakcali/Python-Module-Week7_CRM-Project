// // Google People API'yi kullanmak için OAuth2 kütüphanesini ekleyin
// // Kütüphane Kimliği: 1B7FSrk5Zi6L1rSxxTDgDEUsPzlukDsi4KGuTMorsTQHhGBzBkMun4iDF
var SCOPE = 'https://www.googleapis.com/auth/contacts.readonly';
var TOKEN_PROPERTY_NAME = 'people_api_token';


// OAuth2 kurulumu ve kimlik doğrulama işlemi
function getOAuthService() {
  try {
    var cnf = new Config();
    var CLIENT_ID = cnf.getClientId();
    var CLIENT_SECRET = cnf.getSecretKey();

    return OAuth2.createService('GooglePeopleAPI')
      .setAuthorizationBaseUrl('https://accounts.google.com/o/oauth2/auth')
      .setTokenUrl('https://accounts.google.com/o/oauth2/token')
      .setClientId(CLIENT_ID)
      .setClientSecret(CLIENT_SECRET)
      .setCallbackFunction('authCallback')
      .setPropertyStore(PropertiesService.getUserProperties())
      .setScope(SCOPE)
      .setParam('access_type', 'offline')
      .setParam('approval_prompt', 'force');
  } catch (e) {
    console.error('Error occurred in getOAuthService function: ' + e.stack);
  }
}

function authCallback(request) {
  try {
    var oauthService = getOAuthService();
    var authorized = oauthService.handleCallback(request);
    if (authorized) {
      return HtmlService.createHtmlOutput('Başarıyla yetkilendirildi.').setWidth(500).setHeight(150);
    } else {
      return HtmlService.createHtmlOutput('Yetkilendirme başarısız.').setWidth(500).setHeight(150);
    }
  } catch (e) {
    console.error('Error occurred in authCallback function: ' + e.stack);
  }
}
