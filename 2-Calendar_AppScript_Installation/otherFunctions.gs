// Değerleri karşılaştırma fonksiyonu - (event guncellenmis mi diye kontrol etmek icin)
function hasChanges(oldRow, eventData_, datetimeFieldNames) {
  for (var i = 0; i < Object.values(eventData_).length; i++) {
    var oldValue = oldRow[i];
    var newValue = Object.values(eventData_)[i];
    
    // Tarih/saat alanları için özel karşılaştırma
    if (datetimeFieldNames.includes(Object.keys(eventData_)[i])) {
      oldValue = new Date(oldValue).getTime();
      newValue = new Date(newValue).getTime();
    }
    
    // Diğer alanlar için tip dönüşümü
    else {
      oldValue = String(oldValue);
      newValue = String(newValue);
    }

    if (oldValue !== newValue) {
      Logger.log('Degisen veri bulundu, ana fonksiyona donulecek!\nDegisen Veri: ' + Object.keys(eventData_)[i] + ' değişti: ' + oldValue + ' => ' + newValue);
      return true;
    }
  }
  return false;
}


function convertToUTC(isoString) {
  // ISO string'i Date nesnesine çevir
  const date = new Date(isoString);

  // Geçerli bir tarih olup olmadığını kontrol et
  if (isNaN(date.getTime())) {
    throw new Error('Geçersiz tarih formatı: ' + isoString);
  }

  // UTC timestamp (milisaniye cinsinden)
  const utcTimestamp = date.getTime();

  // UTC datetime nesnesi
  const utcDatetime = new Date(utcTimestamp);

  return {
    utcTimestamp: utcTimestamp,
    utcDatetime: utcDatetime,
    formattedUTC: utcDatetime.toUTCString(),
    isoUTC: utcDatetime.toISOString()
  };
}

/*
Bu fonksiyon şunları yapar:

Verilen ISO 8601 formatındaki string'i bir JavaScript Date nesnesine çevirir.
Oluşturulan tarihin geçerli olup olmadığını kontrol eder.
UTC timestamp'ini (Unix zamanı, milisaniye cinsinden) hesaplar.
UTC datetime nesnesini oluşturur.
Bir nesne döndürür, bu nesne şunları içerir:

utcTimestamp: UTC zaman damgası (milisaniye cinsinden)
utcDatetime: UTC datetime nesnesi
formattedUTC: İnsan tarafından okunabilir UTC string formatı
isoUTC: ISO 8601 formatında UTC string


Bu fonksiyonu şu şekilde kullanabilirsiniz:

KOD BLOGU BASLAR:

// Önce parseTimestamp fonksiyonunu kullanarak bir tarih parse edelim
const parsedDate = parseTimestamp("2023-08-15 14:30:00");

// Şimdi bu tarihi UTC'ye dönüştürelim
const utcResult = convertToUTC(parsedDate);

console.log(utcResult.utcTimestamp); // Örnek: 1692108600000
console.log(utcResult.utcDatetime); // Örnek: 2023-08-15T14:30:00.000Z (Date nesnesi)
console.log(utcResult.formattedUTC); // Örnek: "Tue, 15 Aug 2023 14:30:00 GMT"
console.log(utcResult.isoUTC); // Örnek: "2023-08-15T14:30:00.000Z"

KOD BLOGU BITTI:

Bu fonksiyon, parseTimestamp fonksiyonunun döndürdüğü her türlü ISO 8601 formatındaki tarihi alabilir ve onu UTC zaman damgasına ve datetime nesnesine dönüştürür. Ayrıca, insan tarafından okunabilir bir format ve ISO 8601 UTC formatı da sağlar. Bu, farklı ihtiyaçlarınız için esneklik sağlar.

*/


// // Google People API'yi kullanmak için OAuth2 kütüphanesini ekleyin
// // Kütüphane Kimliği: 1B7FSrk5Zi6L1rSxxTDgDEUsPzlukDsi4KGuTMorsTQHhGBzBkMun4iDF
var CLIENT_ID = 'YOUR_CLIENT_ID_HERE';
var CLIENT_SECRET = 'YOUR_CLIENT_SECRET_HERE';
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
  var email = "test@mail.com"; // Test etmek istediğiniz e-posta adresi
  Logger.log(getPersonInfo(email));
}
