import streamlit as st
from recommender import load_songs, recommend_songs

# Page configuration
st.set_page_config(page_title='🎵 Music Recommender', layout='wide')
st.title('🎵 Music Recommender System')

# Fetch data from database
@st.cache_data
def fetch_data():
    """Load songs from CSV file."""
    return load_songs("data/songs_with_audio_feature.csv")

songs = fetch_data()
st.sidebar.success(f"✅ Loaded {len(songs)} songs")

# Ask users to enter their song preferences
st.sidebar.header("Your Music Preferences")

# Genre preference
available_genres = sorted(list(set([song['genre'] for song in songs])))
selected_genre = st.sidebar.selectbox(
    "📀 Favorite Genre",
    available_genres,
    help="Select your preferred music genre"
)

# Mood preference
available_moods = sorted(list(set([song['mood'] for song in songs])))
selected_mood = st.sidebar.selectbox(
    "😊 Favorite Mood",
    available_moods,
    help="Select the mood you prefer"
)

# Energy level preference
energy_level = st.sidebar.slider(
    "⚡ Energy Level",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.1,
    help="0 = Low energy (chill), 1 = High energy (energetic)"
)

# Acoustic preference
likes_acoustic = st.sidebar.checkbox(
    "🎸 I like acoustic songs",
    value=False
)

# Create user preferences dictionary
user_prefs = {
    'genre': selected_genre,
    'mood': selected_mood,
    'energy': energy_level,
    'likes_acoustic': likes_acoustic
}

# Display user profile
st.sidebar.markdown("---")
st.sidebar.subheader("Your Profile")
st.sidebar.write(f"**Genre:** {selected_genre}")
st.sidebar.write(f"**Mood:** {selected_mood}")
st.sidebar.write(f"**Energy:** {energy_level:.1f}/1.0")
st.sidebar.write(f"**Acoustic:** {'Yes ✓' if likes_acoustic else 'No ✗'}")

# Display all available songs in expandable section
with st.sidebar.expander("📚 Browse All Songs"):
    st.subheader("All Available Songs")
    for i, song in enumerate(songs[:20], 1):  # Show first 20
        st.write(f"**{i}. {song['title']}** by {song['artist']}")
        st.caption(f"Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']:.2f}")
    if len(songs) > 20:
        st.caption(f"... and {len(songs) - 20} more songs")

# Throw suggestions to user
st.markdown("---")
st.subheader("⭐ Recommended Songs For You")

# Get number of recommendations
num_recommendations = st.slider(
    "How many recommendations would you like?",
    min_value=1,
    max_value=20,
    value=10
)

# Get recommendations
recommendations = recommend_songs(user_prefs, songs, k=num_recommendations)

if recommendations:
    # Display recommendations in columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        for i, (song, score, explanation) in enumerate(recommendations, 1):
            with st.container():
                st.markdown(f"### {i}. {song['title']}")
                st.write(f"**Artist:** {song['artist']}")
                st.write(f"**Genre:** {song['genre']} | **Mood:** {song['mood']}")
                
                # Display score as progress bar
                st.progress(score, text=f"Match Score: {score:.1%}")
                st.caption(f"💡 {explanation}")
                st.divider()
    
    with col2:
        st.markdown("### 📊 Recommendation Stats")
        avg_score = sum(r[1] for r in recommendations) / len(recommendations)
        st.metric("Average Match Score", f"{avg_score:.1%}")
        st.metric("Total Recommendations", len(recommendations))
else:
    st.warning("No recommendations found. Try adjusting your preferences!")