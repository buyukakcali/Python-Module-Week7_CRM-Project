function getPersonInfo(email) {
  try {
    var oauthService = getOAuthService();
    if (!oauthService.hasAccess()) {
      var authorizationUrl = oauthService.getAuthorizationUrl();
      Logger.log('Aşağıdaki URL\'yi ziyaret edin ve yetkilendirme işlemini tamamlayın: %s', authorizationUrl);
      return HtmlService.createHtmlOutput('Aşağıdaki URL\'yi ziyaret edin ve yetkilendirme işlemini tamamlayın: <a href="' + authorizationUrl + '" target="_blank">' + authorizationUrl + '</a>');
    }

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

    // Logger.log('Total connections retrieved: ' + connections.length);

    var person = connections.find(function(connection) {
      return connection.emailAddresses &&
             connection.emailAddresses.some(function(emailObj) {
               return emailObj.value.toLowerCase() === email.toLowerCase();
             });
    });

    if (person) {
      var name = person.names ? person.names[0].displayName : "Name not found";
      return {
        fullName: name,
        givenName: person.names ? person.names[0].givenName : "Name not found",
        familyName: person.names ? person.names[0].familyName : "Surname not found"
      };
    } else {
      return "The contact was not found or is not in your contact list.";
    }
  } catch (e) {
    console.error('Error occurred in getPersonInfo function: ' + e.stack);
  }
}

// Fonksiyonu test et
function testGetPersonInfo() {
  try {
    var email = "test@mail.com"; // Test etmek istediğiniz e-posta adresi
    Logger.log(getPersonInfo(email));
  } catch (e) {
    console.error('Error occurred in testGetPersonInfo function: ' + e.stack);
  }
}
