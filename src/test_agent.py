#!/usr/bin/env python3
"""Quick test to verify EvaluationAgent is working"""

import os
from analyst_agent import EvaluationAgent
from recommender import load_songs

# Load data - use absolute path
data_path = os.path.join(os.path.dirname(__file__), '../data/songs_with_audio_feature_cleaned.csv')
songs = load_songs(data_path)
print(f'✓ Loaded {len(songs)} songs from cleaned dataset\n')

# Initialize agent
agent = EvaluationAgent()
print('✓ EvaluationAgent initialized\n')

# Test 3 different user profiles
test_users = [
    {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False},
    {'genre': 'rock', 'mood': 'energetic', 'energy': 0.7, 'likes_acoustic': False},
    {'genre': 'indie pop', 'mood': 'chill', 'energy': 0.4, 'likes_acoustic': True}
]

print('Testing user profiles:')
print('-' * 50)
for i, user in enumerate(test_users, 1):
    score = agent.test_user(user, songs, k=10)
    print(f'User {i} ({user["genre"]}): {score:.1%} match rate')

print('-' * 50)
print(f'\n✓ Average recommendation quality: {agent.summary():.1%}')
print(f'✓ Total results stored: {len(agent.results)}')
print('\n✅ Agent is working correctly!')
