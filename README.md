# Spotlyrics

Spotlyrics connects to your Spotify account and delivers real-time, line-by-line lyrics for the current playback song. 

### Requirements
* Spotify account (free or premium)
* Spotify API credentials ([get started here](https://developer.spotify.com/documentation/web-api/tutorials/getting-started))
* A web browser currently logged into your account on the [Spotify Web Player](https://open.spotify.com/)

### Installation (manual)
```shell
git clone https://github.com/isaacmg00/spotlyrics
pip install -r requirements.txt
```
### *IN PROGRESS* Installation (pip)
```shell
# not currently on PyPI
# pip install spotlyrics
```
### Setup API Credentials for Spotlyrics
Once you have created a developer account, paste the `CLIENT_ID` & `CLIENT_SECRET` into a newly created .env file.

In the spotlyrics directory:
```shell
touch .env
echo CLIENT_ID="\"<YOUR CLIENT_ID>"\" >> .env
echo CLIENT_SECRET="\"<YOUR CLIENT_SECRET>"\" >> .env
```
### Usage
In the spotlyrics directory, run `python spotlyrics.py` to start the interactive cli session. 

#### Known issues: 
* rewinding a playing song will freeze the program
* forwarding a playing song is not smooth
* when playing a song with no lyrics, spotlyrics will crash

#### TODO:
* add flag to print lyrics for the song and exit
* create pip package
