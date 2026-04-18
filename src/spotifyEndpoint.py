import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://localhost:8888/callback",
    scope="user-top-read user-read-recently-played user-library-read"
))

top_tracks = sp.current_user_top_tracks(limit=10)

for item in top_tracks["items"]:
    print(item["name"])

# Use an actual track ID from the API response
track_id = top_tracks["items"][0]["id"]
features = sp.audio_features(track_id)
print(features)

#use the API to pull playlist tracks , then run auio features on each track D to build a dataset
#spotipy - a python libary for spotify web API