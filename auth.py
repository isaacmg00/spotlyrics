import base64
import requests

client_id = "8536b313f38f4155a21defafccc3de68"
client_secret = "2fc41b3c1d6e488b80098033135a9ef5"
redirect_uri = "http://localhost:8888/"

client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

token_url = "https://accounts.spotify.com/api/token"
method = "POST"
token_data = {
    "grant_type": "authorization_code",
    "code": "AQBlrC855IOqrDRMNhParjiATQzptXqNuGUNqnp5-so-rwIZ6L6XrH1yCRny4LmJPRIsNTK21TzCv-phfALiV5jmBZhIoVfnDeu1y1ykbN8Yanix6S0bHO7n9Yh4eEyJDH7PFyMM-aQQGF77wBKDpTWfgSwSZcGXjS74EJHvgj0kzDoFoh7DI4G-ofSnlW6l4heatgs0VddYQxfWwOf6RB_CS_EAVIU",
    "redirect_uri": "http://localhost:8888/"
}

token_header = {
    "Authorization": f"Basic {client_creds_b64.decode()}",
    'Content-Type': 'application/x-www-form-urlencoded',
}

print(token_header)

r = requests.post(token_url, data=token_data, headers=token_header)
print(r.json())
