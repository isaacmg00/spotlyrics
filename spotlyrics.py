import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import json

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8536b313f38f4155a21defafccc3de68",
                                               client_secret="2fc41b3c1d6e488b80098033135a9ef5",
                                               redirect_uri="http://localhost:8888/auth",
                                               scope="user-read-playback-state"))

track_id = sp.current_playback()['item']['id']
art_image_url = sp.current_playback()['item']['album']['images'][0]['url']
art_image_directory = art_image_url.split("image/")
substr = art_image_directory[1]

base_url = "https://spclient.wg.spotify.com/color-lyrics/v2/track/" + \
    str(track_id) + "/image/https%3A%2F%2Fi.scdn.co%2Fimage%2F" + \
    str(substr) + "?format=json&vocalRemoval=false&market=from_token"

headers = {
    "Host": "spclient.wg.spotify.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Accept": "application/json",
    "Accept-Language": "en",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://open.spotify.com/",
    "authorization": "Bearer BQCJVaoj8tlQegIxO7My4VKqSa4JnAAnHYL8IJeY5uTKuVdPF4nZbsJaRHI1k8ojLmXxntQs4LwWGKrGfGx6n-h9m04QnSOUR93gImejJ8cnNECCB7wZVMjo188Iy8vC3mA3_W3YeZnQ_e_xUMiBare_yNQL7Vnn_m5EkM5BgvG2J8hr_5OFMYHM6MNHqaF77MFLXNhHx2CBRu5UdhhPCG91362dSsO4qcaUDdIHfW11RlGx2I7VGfzC3Fwe-uI53rHgp9CG0q7jm_dTqEmMBGAAjDhUdRAXbyMb8eHIyc4TVZxAc4upb-e6Eb6aSbGUjYY21w",
    "app-platform": "WebPlayer",
    "spotify-app-version": "1.1.81.4.gf0a51a16",
    "Origin": "https://open.spotify.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
}

response = requests.get(base_url, headers=headers)
LYRICS_JSON = response.json()
print(LYRICS_JSON)

NUM_LINES = len(LYRICS_JSON['lyrics']['lines'])


print("Number of Lines in the song: " + str(NUM_LINES))
for line in range(0, NUM_LINES):
    line_one_based = line+1
    print("line " + str(line_one_based) + ": " +
          str(LYRICS_JSON['lyrics']['lines'][line]['words']))

is_playing = sp.current_playback()['is_playing']

while(True):
    is_playing = sp.current_playback()['is_playing']
    print(sp.current_playback()['progress_ms'])

    if(not(is_playing)):
        print("song paused")
