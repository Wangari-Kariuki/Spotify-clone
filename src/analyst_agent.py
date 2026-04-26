import recommender


class EvaluationAgent:
    """
    Evaluates recommendation quality by testing user profiles
    and calculating how many recommendations match user preferences.
    """
    
    def __init__(self):
        self.recommender = recommender
        self.results = []  # ✅ Fixed: self.results (plural)
    
    def test_user(self, user_profile, songs, k=5):
        """
        Test a user profile by getting recommendations and evaluating them.
        
        Args:
            user_profile: User preferences dict
            songs: List of available songs
            k: Number of recommendations to get
        """
        # ✅ Fixed: Call recommend_songs correctly
        recs = recommender.recommend_songs(user_profile, songs, k=k)
        
        # recs is [(song, score, explanation), ...]
        # Extract just the songs and the cores of each song to compare that to the user pref
        rec_songs = [song for song, _, _ in recs]
        
        score = self.evaluate(user_profile, rec_songs)
        self.results.append(score)
        return score
    
    def evaluate(self, user, recs):
        """
        Calculate how many recommendations match user's favorite genre.
        
        Args:
            user: User profile with 'genre' key
            recs: List of recommended songs
            
        Returns:
            Percentage of recommendations that match user's genre (0.0-1.0)
        """
        if not recs:
            return 0.0
        
        total = 0
        # ✅ Fixed: Loop completes before returning
        for song in recs:
            if song["genre"] == user["genre"]:
                total += 1
        
        # ✅ Fixed: Return AFTER loop (calculates all songs)
        return total / len(recs)
    
    def summary(self):
        """
        Get average evaluation score across all tested users.
        
        Returns:
            Average score (0.0-1.0)
        """
        if not self.results:
            return 0.0
        
        # ✅ Fixed: self.results (not self.returns)
        return sum(self.results) / len(self.results)