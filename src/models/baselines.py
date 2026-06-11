import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

def build_user_item_matrix(ratings_df):
    """
    Build a sparse user-item matrix from the ratings dataframe.
    """
    # Create mapping from ID to index
    user_ids = ratings_df['UserID'].unique()
    movie_ids = ratings_df['MovieID'].unique()
    
    user_id_to_idx = {uid: idx for idx, uid in enumerate(user_ids)}
    movie_id_to_idx = {mid: idx for idx, mid in enumerate(movie_ids)}
    
    row_ind = ratings_df['UserID'].map(user_id_to_idx).values
    col_ind = ratings_df['MovieID'].map(movie_id_to_idx).values
    data = ratings_df['Rating'].values
    
    mat = csr_matrix((data, (row_ind, col_ind)), shape=(len(user_ids), len(movie_ids)))
    return mat, user_id_to_idx, movie_id_to_idx, user_ids, movie_ids

def get_top_n_recommendations_from_scores(user_ids, movie_ids, scores, n=10):
    """
    Return the top-N recommendations for each user from a dense score matrix.
    """
    top_n = defaultdict(list)
    for u_idx, uid in enumerate(user_ids):
        # Sort scores for this user in descending order
        user_scores = scores[u_idx]
        top_indices = np.argsort(user_scores)[::-1][:n]
        
        for idx in top_indices:
            top_n[uid].append((movie_ids[idx], user_scores[idx]))
            
    return top_n
