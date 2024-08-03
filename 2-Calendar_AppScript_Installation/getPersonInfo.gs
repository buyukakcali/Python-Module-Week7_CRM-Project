// // Google People API'yi kullanmak için OAuth2 kütüphanesini ekleyin
// // Kütüphane Kimliği: 1B7FSrk5Zi6L1rSxxTDgDEUsPzlukDsi4KGuTMorsTQHhGBzBkMun4iDF
var CLIENT_ID = '';
var CLIENT_SECRET = '';
var SCOPE = 'https://www.googleapis.com/auth/contacts.readonly';
var TOKEN_PROPERTY_NAME = 'people_api_token';


// OAuth2 kurulumu ve kimlik doğrulama işlemi
function getOAuthService() {
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
}

function authCallback(request) {
  var oauthService = getOAuthService();
  var authorized = oauthService.handleCallback(request);
  if (authorized) {
    return HtmlService.createHtmlOutput('Başarıyla yetkilendirildi.').setWidth(500).setHeight(150);
  } else {
    return HtmlService.createHtmlOutput('Yetkilendirme başarısız.').setWidth(500).setHeight(150);
  }
}

function getPersonInfo(email) {
  var oauthService = getOAuthService();
  if (!oauthService.hasAccess()) {
    var authorizationUrl = oauthService.getAuthorizationUrl();
    Logger.log('Aşağıdaki URL\'yi ziyaret edin ve yetkilendirme işlemini tamamlayın: %s', authorizationUrl);
    return HtmlService.createHtmlOutput('Aşağıdaki URL\'yi ziyaret edin ve yetkilendirme işlemini tamamlayın: <a href="' + authorizationUrl + '" target="_blank">' + authorizationUrl + '</a>');
  }

  try {
    var connections = [];
    var nextPageToken = '';
    do {
      var url = 'https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses';
      if (nextPageToken) {
        url += '&pageToken=' + nextPageToken;
      }
      
      var response = UrlFetchApp.fetch(url, {
        headers: {
          Authorization: 'Bearer ' + oauthService.getAccessToken()
        }
      });
      var data = JSON.parse(response.getContentText());
      if (data.connections) {
        connections = connections.concat(data.connections);
      }
      nextPageToken = data.nextPageToken;
    } while (nextPageToken);

    Logger.log('Total connections retrieved: ' + connections.length);
    
    var person = connections.find(function(connection) {
      return connection.emailAddresses && 
             connection.emailAddresses.some(function(emailObj) {
               return emailObj.value.toLowerCase() === email.toLowerCase();
             });
    });

    if (person) {
      var name = person.names ? person.names[0].displayName : "İsim bulunamadı";
      return {
        fullName: name,
        givenName: person.names ? person.names[0].givenName : "Ad bulunamadı",
        familyName: person.names ? person.names[0].familyName : "Soyad bulunamadı"
      };
    } else {
      return "Kişi bulunamadı veya kişi listenizde yok.";
    }
  } catch (e) {
    Logger.log('Hata: ' + e.toString());
    return "Hata: " + e.toString();
  }
}

// Fonksiyonu test et
function testGetPersonInfo() {
  var email = "gizel4533@gmail.com"; // Test etmek istediğiniz e-posta adresi
  Logger.log(getPersonInfo(email));
}
