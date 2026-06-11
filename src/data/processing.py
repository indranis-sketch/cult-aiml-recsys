import pandas as pd
import os
from sklearn.model_selection import train_test_split

def load_netflix_data(dataset_dir):
    """
    Loads the movie_titles.csv and combined_data_1.txt into Pandas DataFrames.
    """
    movie_titles_path = os.path.join(dataset_dir, 'movie_titles.csv')
    combined_data_path = os.path.join(dataset_dir, 'combined_data_1.txt')
    
    print(f"Loading movies from {movie_titles_path}...")
    movies_df = pd.read_csv(movie_titles_path, sep=',', encoding='iso-8859-1', 
                            header=None, names=['MovieID', 'Year', 'Title'], on_bad_lines='skip')
    movies_df.set_index('MovieID', inplace=True)
    
    print(f"Loading ratings from {combined_data_path}...")
    data = []
    current_movie_id = None
    
    if not os.path.exists(combined_data_path):
        raise FileNotFoundError(f"Ratings file not found at {combined_data_path}")
        
    with open(combined_data_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.endswith(':'):
                current_movie_id = int(line[:-1])
            else:
                user_id, rating, date = line.split(',')
                data.append([current_movie_id, int(user_id), int(rating), date])
                
    ratings_df = pd.DataFrame(data, columns=['MovieID', 'UserID', 'Rating', 'Date'])
    
    return movies_df, ratings_df

def prepare_train_test_split(ratings_df, test_size=0.2, random_state=42):
    """
    Splits the ratings dataframe into training and testing sets.
    """
    train_df, test_df = train_test_split(ratings_df, test_size=test_size, random_state=random_state)
    return train_df, test_df

if __name__ == "__main__":
    # Test loading
    dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset'))
    movies, ratings = load_netflix_data(dataset_dir)
    print("Movies Head:\n", movies.head())
    print("\nRatings Head:\n", ratings.head())
