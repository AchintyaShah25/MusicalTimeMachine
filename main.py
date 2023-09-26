from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
redirect = "http://example.com"
S_CLIENT_ID = "3b52e6b93bcb423fac08689af2bcc0e5"
S_CLIENT_SECRET = "ffc1020731e6484c919c2fbad7d9a77d"
S_USER_ID = "31rrivhkol6cadxdxsywqt36rpea"
user_date = input("What date Hot100 Would you like? YYYY-MM-DD\n")
year = user_date.split("-")[0]
response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date}/")
response = response.text
soup = BeautifulSoup(response, "html.parser")
all_songs = [song_titles.getText().strip() for song_titles in soup.find_all(name="h3", class_="a-no-trucate")]
artists_name = [artists.getText().strip() for artists in soup.find_all(name="span", class_="a-no-trucate")]
all_artists = [singer for singer in artists_name]
song_artist = {}

for keys in all_songs:
    for value in artists_name:
        song_artist[keys] = value
        artists_name.remove(value)
        break
uri_li = []
spotify_credentials = SpotifyOAuth(client_id=S_CLIENT_ID, client_secret=S_CLIENT_SECRET,redirect_uri=redirect, scope="playlist-modify-private")
access_token = spotify_credentials.get_cached_token()
ACCESS_TOKEN = access_token["access_token"]
spotify = spotipy.Spotify(ACCESS_TOKEN)
for songs in all_songs:
    res = spotify.search(q=f"track:{songs} year:{year}", type="track")
    try:
        uri_li.append(res["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"'{songs}' not found")
playlist_name = f"{user_date} Billboard Hot 100 playlist"
desc = "Python generated top 100 songs of a particular day"
playlist = spotify.user_playlist_create(user=S_USER_ID, name=playlist_name, description=desc, public=False)
playlist_id = playlist["id"]
spotify.user_playlist_add_tracks(user=S_USER_ID, playlist_id=playlist_id,tracks=uri_li)
