import base64
import requests

client_id = "8536b313f38f4155a21defafccc3de68"
client_secret = "2fc41b3c1d6e488b80098033135a9ef5"
redirect_uri = "http://localhost:8888/auth"

client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

token_url = "https://accounts.spotify.com/api/token"
method = "POST"
token_data = {
    "grant_type": "authorization_code",
    "code": "AQA11329-BFOSUUy7hzcpAikit9FGks6F-5FbqHzQT2O_aFB_5gpyl5EIHTA5XUnxpxwyoqrRmho6u-pWSNjzlGbGwOs2LTcbcjz17xJuYzS7Z9bvmDFlUqSvN_EEsXYfhwVRNspScfLXdUUncmzBOqYYzl0T05tcop56-5oY78KNtNZcMe72OfUSlcYlVMlupUH23xa5fh-GLZObYE",
    "redirect_uri": "http://localhost:8888/"
}
token_header = {
    "Authorization": f"Basic {client_creds_b64.decode()}"
}

print(token_header)

r = requests.post(token_url, data=token_data, headers=token_header)
print(r.json())
