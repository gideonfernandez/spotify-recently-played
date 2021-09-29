import json
import requests
from secrets import spotify_user_id, playlist_id, refresh_token, base_64

class Refresh:

    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):
        # Request a new access token
        TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"

        response = requests.post(TOKEN_ENDPOINT,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": self.refresh_token},
                                 headers={"Authorization": "Basic " + self.base_64})

        response_json = response.json()

        return response_json["access_token"]

class SpotifyListenHistory:
    def __init__(self):
        self.user_id = spotify_user_id
        self.playlist_id = playlist_id
        self.tracks = ""
        self.spotify_access_token = ""

    def find_recently_played(self):
        print("START: Looking at your listen history")

        PLAYER_ENDPOINT = "https://api.spotify.com/v1/me/player/recently-played"

        response = requests.get(PLAYER_ENDPOINT,
                                headers={
                                        "Content-Type": "application/json",
                                        "Authorization": "Bearer {}".format(self.spotify_access_token)},
                                params={"limit": 50})

        response_json = response.json()

        # To check that this function is working
        for i in response_json["items"]:
            self.tracks += i["track"]["uri"] + ","
            print(i['track']['name'] + ' - ' + i['track']['artists'][0]['name'])
        self.tracks = self.tracks[:-1]
        self.replace_songs()

        print("SUCCESS: All recently played songs found!")

    def replace_songs(self):
        print("START: Update recently played playlist")

        REPLACE_PLAYLIST_ENDPOINT = "https://api.spotify.com/v1/playlists/{}/tracks".format(self.playlist_id)

        response = requests.put(REPLACE_PLAYLIST_ENDPOINT,
                                headers={
                                        "Content-Type": "application/json",
                                        "Authorization": "Bearer {}".format(self.spotify_access_token)},
                                params={"uris": self.tracks})

        print("SUCCESS: Recently played playlist updated.")

    def start(self):
        print("START: Token refresh")
        refreshCaller = Refresh()
        self.spotify_access_token = refreshCaller.refresh()
        self.find_recently_played()
        print("SUCCESS: Token refreshed!")

initiate = SpotifyListenHistory()
initiate.start()