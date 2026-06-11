import numpy as np
from collections import defaultdict

def calculate_rmse(y_true, y_pred):
    """
    Calculate Root Mean Squared Error (RMSE).
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.sqrt(np.mean((y_true - y_pred)**2))

def calculate_map_at_k(actual_interactions, predicted_recommendations, k=10, threshold=3.5):
    """
    Calculate Mean Average Precision at K (MAP@K).
    
    Args:
        actual_interactions: dict of user_id -> list of tuples (movie_id, actual_rating)
        predicted_recommendations: dict of user_id -> list of recommended movie_ids (ordered)
        k: top K recommendations to consider
        threshold: rating >= threshold is considered relevant
    """
    ap_scores = []
    
    for user_id, actual in actual_interactions.items():
        if user_id not in predicted_recommendations:
            continue
            
        relevant_items = {movie_id for movie_id, rating in actual if rating >= threshold}
        
        if not relevant_items:
            continue
            
        predictions = predicted_recommendations[user_id][:k]
        hits = 0
        sum_precisions = 0
        
        for i, p in enumerate(predictions):
            if p in relevant_items:
                hits += 1
                sum_precisions += hits / (i + 1.0)
                
        ap = sum_precisions / min(len(relevant_items), k)
        ap_scores.append(ap)
        
    if not ap_scores:
        return 0.0
        
    return np.mean(ap_scores)
