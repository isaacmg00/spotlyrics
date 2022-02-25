import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8536b313f38f4155a21defafccc3de68",
                                               client_secret="2fc41b3c1d6e488b80098033135a9ef5",
                                               redirect_uri="http://localhost:8888/auth",
                                               scope="streaming"))

# print(sp.auth_manager.scope)
# print(sp.track(track_id='USUYG1291802'))
# https://api.musixmatch.com/ws/1.1/artist.get?artist_id=118&apikey=ae9aa98c34e0bb6029ae6bcef2e9b4a7

BASE_URL = "https://spclient.wg.spotify.com/color-lyrics/v2/track/1i1fxkWeaMmKEB4T7zqbzK/image/https%3A%2F%2Fi.scdn.co%2Fimage%2Fab67616d0000b273df7cddc2d32ef9df762d5a30?format=json&vocalRemoval=false&market=from_token"

headers = {
    "Host": "spclient.wg.spotify.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Accept": "application/json",
    "Accept-Language": "en",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://open.spotify.com/",
    "authorization": "Bearer BQAuJC81Dl2FdG0oF4aFsBkBSDAg1HF5FiUOBSpO9unopJhEQlEXX2SnLr8nVpmuP9P3nvSl6NK_GplMFSgduv_brO3jakxSMGnpStqNkjpZ-NhDXSZ9N4CDyWeP1F6uHub8oL4s-F5ASO6jP49wyatc4wadRCWmQzdnwAIwWXn6gA0GgsK7MDMp7nGwklSq414Ie6KKgfKQJEksWuDox8D5cj2s5CtlUfDsq0zd13JkbEnlFjAW4K-DqzYvklthCSWUGwcoH8zTTT_2KWKefH5DfpFygNl-DNCTdvBk",
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

response = requests.get(BASE_URL, headers=headers)
print(response.text["lines"])
