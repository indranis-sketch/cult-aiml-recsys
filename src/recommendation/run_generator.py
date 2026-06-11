import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.data.processing import load_netflix_data, prepare_train_test_split
from src.models.baselines import build_user_item_matrix
from src.models.matrix_factorization import train_svd, predict_svd
from src.recommendation.generator import RecommendationGenerator, analyze_recommendation_quality
import random

def test_generator():
    dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset'))
    movies, ratings = load_netflix_data(dataset_dir)
    
    print("Preparing Matrix Factorization model...")
    train_df, _ = prepare_train_test_split(ratings, test_size=0.2)
    train_mat, user_id_to_idx, movie_id_to_idx, user_ids, movie_ids = build_user_item_matrix(train_df)
    
    user_factors, item_factors = train_svd(train_mat, n_components=5)
    predicted_scores = predict_svd(user_factors, item_factors)
    
    # Initialize the generator
    generator = RecommendationGenerator(movies, user_ids, movie_ids, predicted_scores)
    
    # Pick a random user
    random_user = random.choice(user_ids)
    print(f"\nGenerating recommendations for User ID: {random_user}")
    
    recs = generator.get_recommendations(random_user, top_k=10)
    analyze_recommendation_quality(recs)

if __name__ == "__main__":
    test_generator()
