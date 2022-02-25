import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import json

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8536b313f38f4155a21defafccc3de68",
                                               client_secret="2fc41b3c1d6e488b80098033135a9ef5",
                                               redirect_uri="http://localhost:8888/auth",
                                               scope="user-read-playback-state"))

print(sp.current_playback()['item']['album']['images'][0]['url'])
print()
# print(sp.track(track_id='USUYG1291802'))
# https://api.musixmatch.com/ws/1.1/artist.get?artist_id=118&apikey=ae9aa98c34e0bb6029ae6bcef2e9b4a7


track_id = sp.current_playback()['item']['id']
art_image_url = sp.current_playback()['item']['album']['images'][0]['url']
art_image_directory = art_image_url.split("image/")
substr = art_image_directory[1]

base_url = "https://spclient.wg.spotify.com/color-lyrics/v2/track/" + \
    str(track_id) + "/image/https%3A%2F%2Fi.scdn.co%2Fimage%2F" + \
    str(substr) + "?format=json&vocalRemoval=false&market=from_token"
print(base_url)

print(substr)
headers = {
    "Host": "spclient.wg.spotify.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Accept": "application/json",
    "Accept-Language": "en",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://open.spotify.com/",
    "authorization": "Bearer BQBsKS3v-m3pTYRiSFdFAOCabjVgtdZe4zeO9geFAZM5QFetpVOhYNCigC_K294kwDorT6udyy3m3eCA-CbX0W1KjsPkjQF-zfW-CPv3cslI5GhVkRU0Y7UTR0STi4Olm5Zt3ytRGJ9SKEYKonXOxFzlZmYrWEU1ILbxdPt_nWW5_zngzM84gcYyYT2KaitLQHR_UW7-ZZ-41QKfuCuczHZUuDNpnven8SX8Fb2TyxiYgEI9Kpx9qZ8Da82hKbYQlKwamJ6eYBxgOm8ImVIE0jZ0WfvJrO5UdzSUOstI",
    "app-platform": "WebPlayer",
    "spotify-app-version": "1.1.81.4.gf0a51a16",
    "Origin": "https://open.spotify.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"}

response = requests.get(base_url, headers=headers)
LYRICS_JSON = response.json()
# print(LYRICS_JSON)

NUM_LINES = len(LYRICS_JSON['lyrics']['lines'])
print("Number of Lines in the song: " + str(NUM_LINES))

for line in range(0, NUM_LINES):
    line_one_based = line+1
    print("Line: " + str(line_one_based) + " " +
          str(LYRICS_JSON['lyrics']['lines'][line]['words']))
