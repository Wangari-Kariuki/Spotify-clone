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
import os
from dotenv import load_dotenv
from pyngrok import ngrok
import urllib.parse

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Validate credentials are loaded
if not CLIENT_ID or not CLIENT_SECRET:
    st.error("❌ ERROR: CLIENT_ID or CLIENT_SECRET not found in .env file!")
    st.stop()

st.set_page_config(page_title='SpotiPan recomender', page_icon=None)
st.title('🎵 Spotify Recommendation System')

# Initialize session state
if 'ngrok_tunnel' not in st.session_state:
    st.session_state.ngrok_tunnel = ngrok.connect(8501)
if 'redirect_url' not in st.session_state:
    st.session_state.redirect_url = f'{st.session_state.ngrok_tunnel.public_url}/callback'
if 'sp' not in st.session_state:
    st.session_state.sp = None
if 'auth_manager' not in st.session_state:
    st.session_state.auth_manager = None

REDIRECT_URL = st.session_state.redirect_url

# Display the ngrok URL
st.info(f"🔗 **Redirect URL:** `{REDIRECT_URL}`\n\n**IMPORTANT:** Update this in your Spotify Dashboard settings and then come back here!")

# Initialize SpotifyOAuth (keep it in session state)
if st.session_state.auth_manager is None:
    st.session_state.auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        scope='user-top-read user-read-private',
        cache_path='.spotifyoauthcache',
        show_dialog=True
    )

auth_manager = st.session_state.auth_manager

# Check for OAuth callback and handle it
query_params = st.query_params
if 'code' in query_params and st.session_state.sp is None:
    auth_code = query_params['code']
    try:
        st.write("🔐 Exchanging authorization code for token...")
        token = auth_manager.get_access_token(auth_code, as_dict=True)
        st.write(f"✅ Got access token!")
        st.session_state.sp = spotipy.Spotify(auth=token['access_token'])
        st.success("✅ Successfully authenticated with Spotify!")
        st.balloons()
        # Clear query params
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"❌ Authentication failed: {e}")

# If not authenticated yet, show login button
if st.session_state.sp is None:
    st.write('Get personalized song recommendations based on your top tracks')
    
    # Generate authorization URL
    auth_url = auth_manager.get_authorize_url()
    st.markdown(f"### Step 1: Click the button below to authorize with Spotify")
    st.markdown(f"[🔐 Authorize with Spotify]({auth_url})")
    st.write("After authorizing, you'll be redirected back here automatically.")
    st.stop()

from recommender import load_songs, recommend_songs, convert_spotify_to_songs

# Use the authenticated Spotify client from session state
sp = st.session_state.sp

st.write('Get personalized song recommendations based on your top tracks')

# Fetch user's top tracks
try:
    st.write("🔄 Fetching your top tracks...")
    top_tracks = sp.current_user_top_tracks(limit=20, time_range='short_term')
    st.write(f"✅ Fetched {len(top_tracks['items'])} top tracks")
    
    track_ids = [track['id'] for track in top_tracks['items']]
    st.write(f"Track IDs: {track_ids[:3]}...")  # Debug output
    
    # Fetch audio features with error handling
    try:
        st.write("📊 Fetching audio features...")
        audio_features = sp.audio_features(track_ids)
        st.write(f"✅ Fetched audio features for {len(audio_features)} tracks")
    except Exception as audio_err:
        st.error(f"❌ Failed to fetch audio features: {audio_err}")
        st.error("💡 Try re-authorizing the app or clearing the cache.")
        st.stop()
    
    # Convert Spotify data to our song format
    st.write("🔄 Converting tracks to song format...")
    user_songs = convert_spotify_to_songs(top_tracks, audio_features)
    st.write(f"✅ Converted {len(user_songs)} tracks")
    
    # Show user's top tracks
    st.subheader('📊 Your Top Tracks')
    for i, song in enumerate(user_songs[:5], 1):
        st.write(f"{i}. **{song['title']}** by {song['artist']} ({song['genre']}, {song['mood']})")
    
    # Create user profile from their top tracks
    avg_energy = sum(s['energy'] for s in user_songs) / len(user_songs)
    avg_valence = sum(s['valence'] for s in user_songs) / len(user_songs)
    
    # Most common mood and genre
    moods = [s['mood'] for s in user_songs]
    genres = [s['genre'] for s in user_songs]
    favorite_mood = max(set(moods), key=moods.count)
    favorite_genre = max(set(genres), key=genres.count)
    
    user_prefs = {
        'genre': favorite_genre,
        'mood': favorite_mood,
        'energy': avg_energy,
        'likes_acoustic': avg_valence > 0.6
    }
    
    st.subheader('👤 Your Profile')
    st.write(f"**Favorite Genre:** {user_prefs['genre']}")
    st.write(f"**Favorite Mood:** {user_prefs['mood']}")
    st.write(f"**Energy Level:** {user_prefs['energy']:.2f}/1.0")
    st.write(f"**Likes Acoustic:** {'Yes' if user_prefs['likes_acoustic'] else 'No'}")
    
    # Load all songs from CSV for recommendations
    all_songs = load_songs("data/songs.csv")
    
    # Get recommendations
    recommendations = recommend_songs(user_prefs, all_songs, k=10)
    
    st.subheader('⭐ Recommended Songs for You')
    for i, (song, score, explanation) in enumerate(recommendations, 1):
        st.write(f"**{i}. {song['title']}** by {song['artist']}")
        st.write(f"Score: {score:.2f}/1.0")
        st.write(f"💡 {explanation}")
        st.divider()
        
except Exception as e:
    import traceback
    st.error(f"❌ Error: {str(e)}")
    st.error(traceback.format_exc())
    st.info("⚠️ Make sure you've authorized the app in your browser and updated Spotify Dashboard with the ngrok URL above.")






