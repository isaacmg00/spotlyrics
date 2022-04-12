import time
import json
import os
import subprocess
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# clear the terminal when the program starts
os.system('cls' if os.name == 'nt' else 'clear')


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8536b313f38f4155a21defafccc3de68",
                                               client_secret="2fc41b3c1d6e488b80098033135a9ef5",
                                               redirect_uri="http://localhost:8888/",
                                               scope="user-read-playback-state"))


try:
    track_name = sp.current_playback()['item']['name']
    track_artist = sp.current_playback()['item']['artists'][0]['name']
except TypeError:
    print("No song is playing, try again.")
    exit()

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
    "authorization": "Bearer BQAVbkHmAT5EPzecYg3N_Vm63xo-7icpW4k5spsPQD3NAXutpxyAlqRiYB5vvU7BZWJqE-NMiqycf7zdEzR01cx4g-2PWeuc25LgF5kKXI3wXndqvnrwzioCIvhIKaJQNIB-UM-ItClC4S_zIlQJUuUIBfaZYXi_nr8zMtTFw5Z62OiPFbSOkflhoL-TifNIMDNtu2SYnT4OLfJ_rxGalxug4q0XlUzeIEnLt3V_nS0X5B0LlBleBlxTnUTDJzzggEPqfnn1p9qSzuwjSGIIYVdehpZ5Q71H3Xu5pDm1",
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
RESP_CODE = response.status_code

try:
    LYRICS_JSON = response.json()
    NUM_LINES = len(LYRICS_JSON['lyrics']['lines'])

except (KeyError, TypeError):
    if(RESP_CODE == 401):
        output = subprocess.getoutput('python  get_cookie.py')
        headers = {
            "Host": "spclient.wg.spotify.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
            "Accept": "application/json",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://open.spotify.com/",
            "authorization": "Bearer " + output,
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

try:
    LYRICS_JSON = response.json()
    code = response.status_code

except:
    print("no lyrics found for this track")
    exit()


NUM_LINES = len(LYRICS_JSON['lyrics']['lines'])

lyrics = []
ms_timestamp = []

for line in range(0, NUM_LINES):
    line_one_based = line+1
    lyrics.append(LYRICS_JSON['lyrics']['lines'][line]['words'])
    ms_timestamp.append(LYRICS_JSON['lyrics']['lines'][line]['startTimeMs'])

is_playing = sp.current_playback()['is_playing']

if(is_playing):
    print("Now Playing: ", track_artist, "-", track_name)
current_progress = sp.current_playback()['progress_ms']
current_line = 0
for i in range(0, len(ms_timestamp)-1):
    if((current_progress >= int(ms_timestamp[i])) and (current_progress <= int(ms_timestamp[i+1]))
       ):
        current_line = i
        break


starttime = time.time()
while True:
    track_id2 = sp.current_playback()['item']['id']
    if(track_id != track_id2):
        print("song has changed")

    current_progress = sp.current_playback()['progress_ms']
    if(current_progress >= int(ms_timestamp[current_line])):
        printed = False
        print(lyrics[current_line])
        current_line += 1

    is_playing = sp.current_playback()['is_playing']
    if(not(is_playing) and not printed):
        print("song paused")
        printed = True

    time.sleep(0.5 - ((time.time() - starttime) % 0.5))
