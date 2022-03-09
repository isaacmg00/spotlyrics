$.ajax({
  method: "POST",
  url: "https://accounts.spotify.com/api/token",
  data: {
    grant_type: "authorization_code",
    code: code,
    redirect_uri: myurl,
    client_secret: mysecret,
    client_id: myid,
  },
  success: function (result) {
    // handle result...
  },
});
