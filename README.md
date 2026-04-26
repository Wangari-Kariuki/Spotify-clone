# 🎵 Music Recommender Simulation

## Project Summary

This music recommender system provides personalized song recommendations based on user taste profiles. 

**Key Features:**
- **Multi-user support**: Process recommendations for multiple users simultaneously
- **Weighted scoring algorithm**: Combines genre (35%), mood (25%), energy (25%), and acoustic (15%) preferences
- **Robust preference handling**: Gracefully handles missing or incomplete user preferences
- **Edge case testing**: Includes adversarial user profiles to validate scoring logic reliability
- **Interactive web interface**: Streamlit app for real-time recommendations
- **Large song catalog**: 1000+ songs with full Spotify audio feature data
- **Automatic feature inference**: Intelligently infers genre and mood from raw audio features

The system evaluates songs against user preferences and returns ranked recommendations with scoring explanations.

---

## Project Structure

```
src/
├── app.py                 # 🎨 Streamlit web app (main interactive interface)
├── main.py               # 🔧 Command-line demo with 12 predefined users
├── recommender.py        # 🧠 Core recommendation engine
└── spotipan.py          # (Legacy Spotify OAuth integration)

data/
├── songs_with_audio_feature.csv    # 📊 1000+ songs with Spotify audio features
└── songs.csv                        # 📝 Original 10-song dataset (legacy)

tests/
└── test_recommender.py   # ✅ Test suite for the recommender

requirements.txt          # 📦 Python dependencies
README.md                # 📖 This file
model_card.md            # 🏷️ Model documentation and reflection
```

### Key Files

- **`src/app.py`** - Interactive Streamlit web application for real-time recommendations
- **`src/recommender.py`** - Core recommendation engine with scoring and matching logic
- **`data/songs_with_audio_feature.csv`** - Song dataset from Spotify (1000+ songs with full audio features)

---

## How The System Works
Music recommender --> Evaluation agent --> Simulated users --> Metrics --> Weakness analysis

## How the evaluation agent works:
Environement: Recommendtion sytem
Goal: Measure recommendation quality and robustness 

Actions: Submit user preferences, change  preferences, gie feedback

Percepts: returned reccomendations, scores, rankings

The evaluation agent has five modules : User persona generator - creates synthetic users like high energy lofi listener,sad mood  lofi listener, genre flexibe explorer
*Action planner*: Choose what preference query to send
*System Interface*: calls your recommender function/API
*Judge/Scoring module* : evaluates whether returned songs align with expectted preferences
*Memory + reporter*: Stores results across many tests and summarizes failure cases 
### Song Features

Each song in the system includes:
- **track_id** - Unique Spotify identifier
- **title** - Song name
- **artist** - Artist name(s)
- **genre** - Music genre (inferred from audio features)
- **mood** - Emotional mood (inferred from audio features)
- **energy** - Spotify energy (0.0-1.0)
- **valence** - Musical positiveness (0.0-1.0)
- **danceability** - How danceable (0.0-1.0)
- **acousticness** - Acoustic qualities (0.0-1.0)
- **tempo_bpm** - Tempo in beats per minute

### User Profile

User preferences are represented as:
- **favorite_genre** - Preferred music genre
- **favorite_mood** - Preferred emotional mood
- **target_energy** - Desired energy level (0.0-1.0)
- **likes_acoustic** - Preference for acoustic songs (boolean)

### Recommendation Algorithm

The system uses **content-based filtering** with a weighted scoring formula:

**FINAL_SCORE = (0.35 × genre_match) + (0.25 × mood_match) + (0.25 × energy_match) + (0.15 × acoustic_match)**

#### Scoring Components:

**Genre Match (35% weight)**
- Exact match: 1.0
- Similar styles (e.g., pop ≈ indie-pop): 0.7
- Otherwise: 0.0

**Mood Match (25% weight)**
- Exact match: 1.0
- Adjacent moods (e.g., happy ≈ energetic): 0.6
- Otherwise: 0.0

**Energy Match (25% weight)**
- Distance ≤ 0.1: 1.0
- Distance ≤ 0.3: 0.7
- Distance ≤ 0.5: 0.4
- Otherwise: 0.0

**Acoustic Match (15% weight)**
- User likes acoustic + song acousticness ≥ 0.6: 1.0
- User dislikes acoustic + song acousticness ≤ 0.4: 1.0
- Partial matches: 0.6 or 0.2

#### Feature Inference

When loading songs without explicit genre/mood, the system infers them from audio features:

**Mood Inference:**
- High energy (>0.7) + high valence (>0.6) → Happy
- High energy (>0.7) → Energetic
- Low energy (<0.4) + high acousticness (>0.6) → Chill
- Low energy (<0.4) → Relaxed
- Low valence (<0.3) → Sad
- Default → Focused

**Genre Inference:**
- High acousticness (>0.6) → Folk
- High danceability (>0.7) + high energy (>0.7) → Pop
- Very high energy (>0.8) → Rock
- High danceability (>0.7) → Disco
- Low energy (<0.4) + low acousticness (<0.3) → LoFi
- Default → Indie Pop

---

## Testing & Edge Cases

To validate the scoring algorithm's robustness, the system includes **8 adversarial and edge case user profiles** designed to reveal potential issues:

| Test Profile | Edge Case | Purpose |
|--------------|-----------|---------|
| Contradictory Bob | High energy + chill mood | Tests handling of conflicting preference signals |
| Neutral Nancy | All middle-ground values | Validates neutral preference ranking |
| Maximalist Max / Minimalist Min | Boundary values (1.0 / 0.0) | Ensures scoring doesn't break at extremes |
| Obscure Ollie | Niche/non-existent genre | Tests graceful handling of unknown genres |
| Minimal Mike | Missing energy field | Validates robustness with incomplete data |
| Mismatched Mary | Metal genre + relaxed mood | Tests feature dominance when preferences conflict |
| Acoustic Alex | Extreme acoustic preference | Evaluates acoustic weighting impact |

**Bug Fix:** The scoring function now handles missing `energy` preferences by defaulting to 0.5 (neutral), making the system more resilient to incomplete user profiles.



## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv myenv
   source myenv/bin/activate      # Mac or Linux
   myenv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the interactive Streamlit app:

   ```bash
   streamlit run src/app.py
   ```

   The app opens at `http://localhost:8501` and provides an interactive UI to:
   - Browse available songs
   - Adjust your music preferences (genre, mood, energy, acoustic preference)
   - Get personalized song recommendations with match scores and explanations
   - View recommendation statistics

### Alternative: Run Command-Line Demo

To run the original command-line demo with 12 predefined users:

```bash
python -m src.main
```

This generates recommendations for 4 standard profiles and 8 edge case profiles, displaying:
- User preferences summary
- Top 5 recommended songs per user
- Match scores (0.0-1.0) for each song
- Detailed explanations for each recommendation

---

## Recent Updates

### System Changes

**Data Source Upgrade:**
- Migrated from `data/songs.csv` (10 songs) to `data/songs_with_audio_feature.csv` (1000+ songs)
- New dataset includes raw Spotify audio features: energy, valence, danceability, acousticness, tempo, and more
- The `load_songs()` function now automatically infers **genre** and **mood** from audio features using intelligent heuristics

**Audio Feature Inference Logic:**
- **Mood** inference from energy + valence:
  - High energy + high valence → Happy
  - High energy → Energetic
  - Low energy + high acousticness → Chill
  - Low energy → Relaxed
  - Low valence → Sad
  - Default → Focused

- **Genre** inference from danceability + acousticness + energy:
  - High acousticness → Folk
  - High danceability + high energy → Pop
  - Very high energy → Rock
  - High danceability → Disco
  - Low energy + low acousticness → LoFi
  - Default → Indie Pop

**Interactive Web App:**
- Replaced command-line interface with **Streamlit-based web application** (`src/app.py`)
- Features include:
  - **Sidebar controls** for user preference input (genre, mood, energy slider, acoustic checkbox)
  - **Song browser** showing all 1000+ available songs
  - **Interactive recommendation display** with match scores as progress bars
  - **Recommendation statistics** (average match score, total recommendations)
  - **Adjustable recommendation count** (1-20 songs)
  - **Real-time matching** based on user preference changes

**Backward Compatibility:**
- The original `src/main.py` command-line demo still works
- `load_songs()` handles both old and new CSV formats seamlessly
- Existing scoring and recommendation logic unchanged

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

