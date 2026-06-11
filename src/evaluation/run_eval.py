import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.data.processing import load_netflix_data, prepare_train_test_split
from src.models.baselines import build_user_item_matrix, get_top_n_recommendations_from_scores
from src.models.matrix_factorization import train_svd, predict_svd
from src.evaluation.metrics import calculate_rmse, calculate_map_at_k
from collections import defaultdict
import numpy as np

def run_evaluation():
    dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset'))
    movies, ratings = load_netflix_data(dataset_dir)
    
    print("Splitting data...")
    train_df, test_df = prepare_train_test_split(ratings, test_size=0.2)
    
    print("Building Sparse Matrix...")
    train_mat, user_id_to_idx, movie_id_to_idx, user_ids, movie_ids = build_user_item_matrix(train_df)
    
    print("Training SVD Model...")
    user_factors, item_factors = train_svd(train_mat, n_components=5)
    
    print("Predicting with SVD...")
    predicted_scores = predict_svd(user_factors, item_factors)
    
    # Calculate RMSE on test set
    y_true = []
    y_pred = []
    actual_interactions = defaultdict(list)
    
    for row in test_df.itertuples():
        uid = row.UserID
        iid = row.MovieID
        r = row.Rating
        actual_interactions[uid].append((iid, r))
        
        if uid in user_id_to_idx and iid in movie_id_to_idx:
            u_idx = user_id_to_idx[uid]
            i_idx = movie_id_to_idx[iid]
            y_true.append(r)
            y_pred.append(predicted_scores[u_idx, i_idx])
            
    if y_true:
        rmse_val = calculate_rmse(y_true, y_pred)
        print(f"SVD RMSE: {rmse_val:.4f}")
    
    # Calculate MAP@10
    top_n_recs = get_top_n_recommendations_from_scores(user_ids, movie_ids, predicted_scores, n=10)
    predicted_recommendations = {uid: [iid for (iid, est) in user_ratings] for uid, user_ratings in top_n_recs.items()}
    
    map_at_10 = calculate_map_at_k(actual_interactions, predicted_recommendations, k=10)
    print(f"SVD MAP@10: {map_at_10:.4f}")

if __name__ == "__main__":
    run_evaluation()
