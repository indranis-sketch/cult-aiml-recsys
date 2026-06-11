import pandas as pd
import numpy as np
from collections import defaultdict

class RecommendationGenerator:
    def __init__(self, movies_df, user_ids, movie_ids, predicted_scores):
        """
        Initialize the generator with movies metadata and predicted scores.
        """
        self.movies_df = movies_df
        self.user_ids = user_ids
        self.movie_ids = movie_ids
        self.predicted_scores = predicted_scores
        
    def get_recommendations(self, user_id, top_k=10):
        """
        Generate Top-K recommendations for a specific user ID.
        """
        if user_id not in self.user_ids:
            return []
            
        u_idx = np.where(self.user_ids == user_id)[0][0]
        user_scores = self.predicted_scores[u_idx]
        
        # Get top-k indices
        top_indices = np.argsort(user_scores)[::-1][:top_k]
        
        recommendations = []
        for rank, idx in enumerate(top_indices, start=1):
            m_id = self.movie_ids[idx]
            score = user_scores[idx]
            
            # Fetch movie details
            if m_id in self.movies_df.index:
                title = self.movies_df.loc[m_id, 'Title']
                year = self.movies_df.loc[m_id, 'Year']
            else:
                title = "Unknown"
                year = "Unknown"
                
            recommendations.append({
                'Rank': rank,
                'MovieID': m_id,
                'Title': title,
                'Year': year,
                'PredictedScore': round(score, 4)
            })
            
        return recommendations

def analyze_recommendation_quality(recommendations):
    """
    Provide basic analysis of a set of recommendations.
    """
    print(f"--- Top {len(recommendations)} Recommendations ---")
    for r in recommendations:
        print(f"{r['Rank']}. {r['Title']} ({r['Year']}) - Score: {r['PredictedScore']}")
