import time
import json
import os
import subprocess
import requests
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import pickle
import base64

# load .env credentials
load_dotenv()

# clear the terminal when the program starts
os.system('cls' if os.name == 'nt' else 'clear')

# create spotipy instance to connect with user account and get information about current playback
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                                               client_secret=os.getenv(
    'CLIENT_SECRET'),
    redirect_uri="http://localhost:8888/",
    scope="user-read-playback-state"))

track_name = sp.current_playback()['item']['name']
track_artist = sp.current_playback()['item']['artists'][0]['name']
track_id = sp.current_playback()['item']['id']
art_image_url = sp.current_playback()['item']['album']['images'][0]['url']
art_image_directory = art_image_url.split("image/")
substr = art_image_directory[1]

# url to retrieve lyrics with timestamps
base_url = "https://spclient.wg.spotify.com/color-lyrics/v2/track/" + \
    str(track_id) + "/image/https%3A%2F%2Fi.scdn.co%2Fimage%2F" + \
    str(substr) + "?format=json&vocalRemoval=false&market=from_token"

BEARER_TOKEN = ''

# after the bearer token expires, retrieve a new one valid for 1hr


def REFRESH_BEARER_TOKEN():
    return subprocess.getoutput('python get_cookie.py')

# return true if a song is currently playing, false otherwise


def IS_PLAYING():
    return sp.current_playback()['is_playing']

# converting to b64 to avoid storing user tokens in plaintext


def ENCODE_TOKEN(bearer_token):
    token_bytes = base64.b64encode(bearer_token.encode('ascii'))
    b64_token = token_bytes.decode('ascii')
    return b64_token


def DECODE_TOKEN(bearer_token):
    return base64.b64decode(bearer_token).decode('UTF-8')


def GET_BEARER_TOKEN():
    file = open('bearer_token.dat', 'rb')
    b64_token = pickle.load(file)
    file.close()
    return DECODE_TOKEN(b64_token)


def DUMP_TOKEN(bearer_token):
    file = open('bearer_token.dat', 'wb')
    encoded = ENCODE_TOKEN(bearer_token)
    pickle.dump(encoded, file)
    file.close()

# get the current playback information (artist, song title)


def NOW_PLAYING(sp):
    print("Now Playing: ", sp.current_playback()[
          'item']['artists'][0]['name'], "-", sp.current_playback()['item']['name'])
    print()

# retrieves the lyrics for the songs, timestamps for each line, and the current bar of the song playing


def GET_LYRIC_DATA():
    result = []
    track_id = sp.current_playback()['item']['id']
    art_image_url = sp.current_playback()['item']['album']['images'][0]['url']
    art_image_directory = art_image_url.split("image/")
    substr = art_image_directory[1]

    base_url = "https://spclient.wg.spotify.com/color-lyrics/v2/track/" + \
        str(track_id) + "/image/https%3A%2F%2Fi.scdn.co%2Fimage%2F" + \
        str(substr) + "?format=json&vocalRemoval=false&market=from_token"

    BEARER_TOKEN = GET_BEARER_TOKEN()

    headers = {
        "Host": "spclient.wg.spotify.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
        "Accept": "application/json",
        "Accept-Language": "en",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://open.spotify.com/",
        "authorization": "Bearer " + BEARER_TOKEN,
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
    try:
        response = requests.get(base_url, headers=headers)
        RESP_CODE = response.status_code
        if(RESP_CODE != 200):
            raise PermissionError("401 unauthorized/token has expired")

        LYRICS_JSON = response.json()
        NUM_LINES = len(LYRICS_JSON['lyrics']['lines'])
        DUMP_TOKEN(BEARER_TOKEN)

    except (PermissionError):
        updated_token = REFRESH_BEARER_TOKEN()
        headers = {
            "Host": "spclient.wg.spotify.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
            "Accept": "application/json",
            "Accept-Language": "en",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://open.spotify.com/",
            "authorization": "Bearer " + updated_token,
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
        try:
            response = requests.get(base_url, headers=headers)
            LYRICS_JSON = response.json()
            NUM_LINES = len(LYRICS_JSON['lyrics']['lines'])
            DUMP_TOKEN(updated_token)

        except:
            NOW_PLAYING(sp)
            print("No lyrics found for this track.")
            exit()

    NOW_PLAYING(sp)
    lyrics = []
    ms_timestamp = []

    for line in range(0, NUM_LINES):
        line_one_based = line+1
        lyrics.append(LYRICS_JSON['lyrics']['lines'][line]['words'])
        ms_timestamp.append(
            LYRICS_JSON['lyrics']['lines'][line]['startTimeMs'])

    current_progress = sp.current_playback()['progress_ms']
    current_line = 0
    for i in range(0, len(ms_timestamp)-1):
        if((current_progress >= int(ms_timestamp[i])) and (current_progress <= int(ms_timestamp[i+1]))
           ):
            current_line = i
            break

    result.append(ms_timestamp)
    result.append(current_line)
    result.append(lyrics)
    return result

# when called, start the interactive cli session printing lyrics line by line and checking if a song gets changed


def PRINT_INTERACTIVE_LYRICS(data):
    track_id = sp.current_playback()['item']['id']
    ms_timestamp = data[0]
    current_line = data[1]
    lyrics = data[2]
    starttime = time.time()
    while True:
        track_id2 = sp.current_playback()['item']['id']
        if(track_id != track_id2):
            print("song has changed")
            os.system('cls' if os.name == 'nt' else 'clear')
            song_changed = True
            new_track_id = sp.current_playback()['item']['id']
            track_id = new_track_id
            break

        current_progress = sp.current_playback()['progress_ms']
        if(current_progress >= int(ms_timestamp[current_line])):
            printed = False
            print(lyrics[current_line])
            current_line += 1

        is_playing = sp.current_playback()['is_playing']
        if(not(is_playing) and not printed):
            print("Playback Paused")
            printed = True

        time.sleep(0.5 - ((time.time() - starttime) % 0.5))


# main function call to handle song changes and rewinds/forwards
while(True):
    data = GET_LYRIC_DATA()
    PRINT_INTERACTIVE_LYRICS(data)
