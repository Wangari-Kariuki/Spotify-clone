import pandas as pd

df = pd.read_csv('data/songs_with_audio_feature.csv')
print(f"Initial songs: {len(df)}")

# Check the year column (release_date is empty!)
print(f"\nYear column info:")
print(f"Data type: {df['year'].dtype}")
print(f"Null values: {df['year'].isnull().sum()}")
print(f"Year range: {df['year'].min()} to {df['year'].max()}")

# Find songs BEFORE 2000 (old songs) - USE YEAR COLUMN!
old_songs = df[df['year'] < 2000]
print(f"\nOld songs (before 2000): {len(old_songs)}")

# Drop old songs (keep songs from 2000 onwards)
df_new = df.drop(old_songs.index)
print(f"Songs kept (from 2000 onwards): {len(df_new)}")
print(f"\nSample of kept songs:")
print(df_new[['track_name', 'artist_names', 'year']].tail(5))

# Save cleaned data
df_new.to_csv('data/songs_with_audio_feature_cleaned.csv', index=False)
print(f"\n✅ Cleaned data saved!")
print(f"Removed {len(df) - len(df_new)} old songs")
print(f"number of songs with empty year values: {len(old_songs['year'].isnull())}")
songs_af_2010 = df_new[df_new['year'] > 2010]
print(f"Number of songs with years after 2010 in our cleaded dataset: {len(songs_af_2010)}")
songs_bf_2010 = df_new[df_new['year'] < 2010]
print(f"Number of songs with years before 2010 in our cleaded dataset: {len(songs_bf_2010)}")

empty_year = df_new[df_new['year'].isnull()]
print(len(empty_year))
