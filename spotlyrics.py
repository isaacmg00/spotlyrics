import json
import os

import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


os.system('cls' if os.name == 'nt' else 'clear')
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8536b313f38f4155a21defafccc3de68",
                                               client_secret="2fc41b3c1d6e488b80098033135a9ef5",
                                               redirect_uri="http://localhost:8888/",
                                               scope="user-read-playback-state"))

# exec(open("get_cookie.py").read())

track_name = sp.current_playback()['item']['name']
track_artist = sp.current_playback()['item']['artists'][0]['name']


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
    "authorization": "Bearer BQAe2_dXjE1HOPR_o40GzepdR_5QfZm5_D5KYjyKDGKDPsY5QP32wlRutYzAUg5bGdSSEbmZj2utrQNT609sSQVOwHpC7y706tI0SExzTdwBzwZWCM_mWmDM1p9I9GL_It6TX9SQ41cgC9c1bx3Y-yXN8omqAAZt_mQI3tdf8JgF6AtgFR-i6lz-whdo1e5t4WFeVNlRO3gRTaEII6EJSwLO0MuKW1uoc-hUYg-jE9lq2vTIe_sCr2ckYrWWqU2UHCtER0w-DnA8NOav3FqBlra3DeOZEIpU6ftPveNz",
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
# print(LYRICS_JSON)

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

# os.system('cls' if os.name == 'nt' else 'clear')

while(True):
    current_progress = sp.current_playback()['progress_ms']
    if(current_progress >= int(ms_timestamp[current_line])):
        print(str(current_line+1) + "-" + str(lyrics[current_line]))
        current_line += 1

    is_playing = sp.current_playback()['is_playing']
    if(not(is_playing)):
        print("song paused")
