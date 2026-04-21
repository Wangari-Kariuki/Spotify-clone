"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os #allows us to retrieve values for enironment variables
CLIENT_ID = os.environ.get('CLIEN_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URL = 'http://localhost:5000'

from .recommender import load_songs, recommend_songs


sp = spotipy.Spotify( 
    #initiaize a spotify class
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        scope = 'user-top-read' 
    )

)

st.set_page_config(page_title='SpotiPan recomender', page_icon=None)
st.title('Recommendation system clone')
st.write('Get suggestions that suite your preferences')

top_tracks = sp.current_user_top_tracks(limit=10, time_range='short_term')
track_ids =  [track['id'] for track in top_tracks['items']]
audio_features = sp.audio_features(track_ids)









def main() -> None:
    songs = load_songs("data/songs.csv") 

    # User profiles - Standard users
    users = {
        "User 1": {"genre": "pop", "mood": "happy", "energy": 0.8},
        # "User 2": {"genre": "high-energy-pop", "mood": "happy", "energy": 0.9},
        # "User 3": {"genre": "lofi", "mood": "chill", "energy": 0.4},
        # "User 4": {"genre": "rock", "mood": "intense", "energy": 1.0},
        
        # # Edge case: Contradictory preferences (high energy + chill mood)
        # "Contradictory Bob": {"genre": "pop", "mood": "chill", "energy": 0.95},
        
        # # Edge case: All neutral preferences (middle ground)
        # "Neutral Nancy": {"genre": "pop", "mood": "happy", "energy": 0.5},
        
        # # Edge case: Extreme values (boundaries)
        # "Maximalist Max": {"genre": "rock", "mood": "intense", "energy": 1.0},
        # "Minimalist Min": {"genre": "lofi", "mood": "chill", "energy": 0.0},
        
        # # Edge case: Niche genre that rarely appears in data
        # "Obscure Ollie": {"genre": "experimental-jazz-fusion", "mood": "thoughtful", "energy": 0.6},
        
        # # Edge case: Missing optional fields (tests robustness)
        # "Minimal Mike": {"genre": "pop", "mood": "happy"},  # No energy specified
        
        # # Edge case: Genre-mood mismatch (heavy metal + relaxed)
        # "Mismatched Mary": {"genre": "metal", "mood": "relaxed", "energy": 0.3},
        
        # # Edge case: Very high acoustic preference
        # "Acoustic Alex": {"genre": "folk", "mood": "chill", "energy": 0.2, "likes_acoustic": True},
    }

    # Get recommendations for each user
    for user_name, user_prefs in users.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n{'='*50}")
        print(f"{user_name} - Preferences: {user_prefs}")
        print(f"{'='*50}")
        print("Top recommendations:\n")
        for rec in recommendations:
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
