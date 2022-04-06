var request = require("request");

var client_id = "8536b313f38f4155a21defafccc3de68";
var client_secret = "2fc41b3c1d6e488b80098033135a9ef5";

var authOptions = {
  url: "https://accounts.spotify.com/api/token",
  headers: {
    Authorization:
      "Basic " + new Buffer(client_id + ":" + client_secret).toString("base64"),
  },
  form: {
    grant_type: "client_credentials",
  },
  json: true,
};

request.post(authOptions, function (error, response, body) {
  if (!error && response.statusCode === 200) {
    var token = body.access_token;
    console.log(token);
  }
});
