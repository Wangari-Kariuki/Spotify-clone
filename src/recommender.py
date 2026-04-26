
#st.write("spotfy-clone")
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k songs ranked by matching the user's preferences."""
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate a concise explanation for why a song matches the user's taste."""
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file with audio features.
    Supports both old format (with genre/mood) and new format (raw audio features).
    Automatically infers genre and mood from audio features if not present.
    
    Required by src/main.py
    """
    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Handle new format: songs_with_audio_feature.csv
            # Map column names from Spotify API format to our format
            if 'track_id' in row:
                song_id = row['track_id']
                title = row['track_name']
                artist = row['artist_names']
            else:
                # Handle old format: songs.csv
                song_id = row['id']
                title = row['title']
                artist = row['artist']
            
            # Parse audio features
            energy = float(row['energy'])
            valence = float(row['valence'])
            danceability = float(row['danceability'])
            acousticness = float(row['acousticness'])
            tempo = float(row.get('tempo', row.get('tempo_bpm', 120)))
            
            # Infer genre and mood from audio features, or use existing values
            audio_features = {
                'energy': energy,
                'valence': valence,
                'danceability': danceability,
                'acousticness': acousticness,
                'tempo': tempo
            }
            
            if 'genre' in row and row['genre']:
                genre = row['genre']
            else:
                genre = _infer_genre(audio_features)
            
            if 'mood' in row and row['mood']:
                mood = row['mood']
            else:
                mood = _infer_mood(audio_features)
            
            song = {
                'id': song_id,
                'title': title,
                'artist': artist,
                'genre': genre,
                'mood': mood,
                'energy': energy,
                'tempo_bpm': tempo,
                'valence': valence,
                'danceability': danceability,
                'acousticness': acousticness,
            }
            songs.append(song)
    
    print(f"Successfully loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> float:
    """
    Calculate a score (0.0-1.0) for how well a song matches user preferences.
    
    Scoring formula:
    FINAL_SCORE = (0.35 × genre_match) + (0.25 × mood_match) + (0.25 × energy_match) + (0.15 × acoustic_match)
    """
    # Genre match (35% weight)
    genre_score = _calculate_genre_match(user_prefs['genre'], song['genre'])
    
    # Mood match (25% weight)
    mood_score = _calculate_mood_match(user_prefs['mood'], song['mood'])
    
    # Energy match (25% weight) - default to 0.5 (neutral) if not specified
    energy_score = _calculate_energy_match(user_prefs.get('energy', 0.5), song['energy'])
    
    # Acoustic match (15% weight)
    acoustic_score = _calculate_acoustic_match(user_prefs.get('likes_acoustic', False), song['acousticness'])
    
    # Combine weighted scores
    final_score = (0.35 * genre_score) + (0.25 * mood_score) + (0.25 * energy_score) + (0.15 * acoustic_score)
    
    return final_score


def _calculate_genre_match(user_genre: str, song_genre: str) -> float:
    """
    Calculate genre similarity score.
    - Exact match: 1.0
    - Similar styles (pop ≈ indie-pop): 0.7
    - Otherwise: 0.0
    """
    if user_genre == song_genre:
        return 1.0
    
    # Define genre families for similarity
    similar_genres = {
        'pop': {'indie pop', 'pop'},
        'indie pop': {'pop', 'indie pop', 'indie'},
        'indie': {'indie pop', 'indie'},
        'rock': {'rock'},
        'lofi': {'lofi'},
        'ambient': {'ambient'},
        'jazz': {'jazz'},
        'synthwave': {'synthwave', 'electronic'},
        'electronic': {'synthwave', 'electronic'},
        'hip-hop': {'hip-hop'},
        'country': {'country'},
        'classical': {'classical'},
        'reggae': {'reggae'},
        'blues': {'blues'},
        'disco': {'disco'},
    }
    
    user_family = similar_genres.get(user_genre.lower(), {user_genre})
    if song_genre.lower() in user_family:
        return 0.7
    
    return 0.0


def _calculate_mood_match(user_mood: str, song_mood: str) -> float:
    """
    Calculate mood similarity score.
    - Exact match: 1.0
    - Adjacent moods (happy ≈ energetic): 0.6
    - Otherwise: 0.0
    """
    if user_mood == song_mood:
        return 1.0
    
    # Define mood adjacencies
    adjacent_moods = {
        'happy': {'happy', 'energetic'},
        'energetic': {'happy', 'energetic'},
        'chill': {'chill', 'relaxed', 'focused'},
        'relaxed': {'chill', 'relaxed'},
        'focused': {'chill', 'focused'},
        'intense': {'intense', 'energetic'},
        'moody': {'moody', 'dark'},
        'dark': {'moody', 'dark'},
        'sad': {'sad', 'melancholic'},
        'melancholic': {'sad', 'melancholic'},
        'romantic': {'romantic', 'happy'},
    }
    
    user_adjacent = adjacent_moods.get(user_mood.lower(), {user_mood})
    if song_mood.lower() in user_adjacent:
        return 0.6
    
    return 0.0


def _calculate_energy_match(user_energy: float, song_energy: float) -> float:
    """
    Calculate energy match score based on distance from target energy.
    - Distance ≤ 0.1: 1.0
    - Distance ≤ 0.3: 0.7
    - Distance ≤ 0.5: 0.4
    - Otherwise: 0.0
    """
    distance = abs(song_energy - user_energy)
    
    if distance <= 0.1:
        return 1.0
    elif distance <= 0.3:
        return 0.7
    elif distance <= 0.5:
        return 0.4
    else:
        return 0.0


def _calculate_acoustic_match(likes_acoustic: bool, song_acousticness: float) -> float:
    """
    Calculate acoustic match score based on user preference.
    """
    if likes_acoustic:
        # User likes acoustic: prefer high acousticness
        if song_acousticness >= 0.6:
            return 1.0
        elif song_acousticness >= 0.3:
            return 0.6
        else:
            return 0.2
    else:
        # User does not like acoustic: prefer low acousticness
        if song_acousticness <= 0.4:
            return 1.0
        elif song_acousticness <= 0.7:
            return 0.6
        else:
            return 0.2
def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Scores all songs and returns top-k ranked by score.
    
    Expected return format: (song_dict, score, explanation)
    """
    # Score all songs
    scored_songs = []
    for song in songs:
        score = score_song(user_prefs, song)
        explanation = _explain_recommendation(user_prefs, song, score)
        scored_songs.append((song, score, explanation))
    
    # Sort by score (descending) and return top-k
    ranked_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
    return ranked_songs[:k]


def _explain_recommendation(user_prefs: Dict, song: Dict, score: float) -> str:
    """
    Generate a human-readable explanation for why this song was recommended.
    """
    matched_attributes = []
    
    # Check which attributes matched
    if song['genre'] == user_prefs['genre']:
        matched_attributes.append('genre')
    if song['mood'] == user_prefs['mood']:
        matched_attributes.append('mood')
    
    energy_dist = abs(song['energy'] - user_prefs.get('energy',0.5))
    if energy_dist <= 0.1:
        matched_attributes.append('energy')
    
    # Energy descriptor
    if song['energy'] >= 0.7:
        energy_desc = 'high'
    elif song['energy'] >= 0.4:
        energy_desc = 'moderate'
    else:
        energy_desc = 'low'
    
    matches_str = ', '.join(matched_attributes) if matched_attributes else 'some attributes'
    
    explanation = f"This {song['genre']} song has {song['mood']} vibes with {energy_desc} energy. Matches: {matches_str}. Score: {score:.2f}"
    return explanation


def convert_spotify_to_songs(top_tracks: List[Dict], audio_features: List[Dict]) -> List[Dict]:
    """
    Convert Spotify API data (top tracks + audio features) into our song format.
    
    Args:
        top_tracks: Spotify API response from current_user_top_tracks()
        audio_features: Spotify API response from audio_features()
    
    Returns:
        List of songs in our expected format
    """
    songs = []
    
    for track, features in zip(top_tracks['items'], audio_features):
        if features is None:  # Skip if features couldn't be retrieved
            continue
        
        # Infer mood and genre from audio features
        mood = _infer_mood(features)
        genre = _infer_genre(features)
        
        song = {
            'id': len(songs),  # Create a simple ID
            'title': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'genre': genre,
            'mood': mood,
            'energy': features.get('energy', 0.5),
            'tempo_bpm': features.get('tempo', 120),
            'valence': features.get('valence', 0.5),
            'danceability': features.get('danceability', 0.5),
            'acousticness': features.get('acousticness', 0.5),
        }
        songs.append(song)
    
    return songs


def _infer_mood(features: Dict) -> str:
    """
    Infer mood from Spotify audio features.
    Uses energy and valence to determine mood.
    """
    energy = features.get('energy', 0.5)
    valence = features.get('valence', 0.5)
    acousticness = features.get('acousticness', 0.5)
    
    if energy > 0.7 and valence > 0.6:
        return 'happy'
    elif energy > 0.7:
        return 'energetic'
    elif energy < 0.4 and acousticness > 0.6:
        return 'chill'
    elif energy < 0.4:
        return 'relaxed'
    elif valence < 0.3:
        return 'sad'
    else:
        return 'focused'


def _infer_genre(features: Dict) -> str:
    """
    Infer genre from Spotify audio features.
    Uses danceability, acousticness, and energy.
    """
    danceability = features.get('danceability', 0.5)
    acousticness = features.get('acousticness', 0.5)
    energy = features.get('energy', 0.5)
    
    if acousticness > 0.6:
        return 'folk'
    elif danceability > 0.7 and energy > 0.7:
        return 'pop'
    elif energy > 0.8:
        return 'rock'
    elif danceability > 0.7:
        return 'disco'
    elif energy < 0.4 and acousticness < 0.3:
        return 'lofi'
    else:
        return 'indie pop'
