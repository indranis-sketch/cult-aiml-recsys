import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as plt_sns
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.data.processing import load_netflix_data

def run_eda():
    dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset'))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'output'))
    os.makedirs(output_dir, exist_ok=True)
    
    print("Loading data... (This might take a minute depending on the dataset size)")
    movies, ratings = load_netflix_data(dataset_dir)
    
    print("Generating EDA plots...")
    # Set seaborn style
    plt_sns.set_theme(style="whitegrid")
    
    # 1. Rating Distribution
    print("1. Plotting Rating Distribution...")
    plt.figure(figsize=(8, 5))
    rating_counts = ratings['Rating'].value_counts().sort_index()
    plt_sns.barplot(x=rating_counts.index, y=rating_counts.values, palette="viridis")
    plt.title("Distribution of Ratings")
    plt.xlabel("Rating (Stars)")
    plt.ylabel("Count")
    plt.savefig(os.path.join(output_dir, 'rating_distribution.png'))
    plt.close()
    
    # 2. Content Popularity (Ratings per Movie)
    print("2. Plotting Content Popularity...")
    plt.figure(figsize=(10, 5))
    movie_counts = ratings['MovieID'].value_counts()
    plt.plot(movie_counts.values)
    plt.title("Movie Popularity (Long Tail Distribution)")
    plt.xlabel("Movies (sorted by popularity)")
    plt.ylabel("Number of Ratings")
    plt.fill_between(range(len(movie_counts)), movie_counts.values, alpha=0.3)
    plt.savefig(os.path.join(output_dir, 'content_popularity.png'))
    plt.close()
    
    # 3. User Activity (Ratings per User)
    print("3. Plotting User Activity...")
    plt.figure(figsize=(10, 5))
    user_counts = ratings['UserID'].value_counts()
    plt.plot(user_counts.values)
    plt.title("User Activity (Long Tail Distribution)")
    plt.xlabel("Users (sorted by activity)")
    plt.ylabel("Number of Ratings")
    plt.fill_between(range(len(user_counts)), user_counts.values, alpha=0.3)
    plt.savefig(os.path.join(output_dir, 'user_activity.png'))
    plt.close()
    
    # 4. Data Sparsity
    print("4. Calculating Sparsity...")
    num_users = ratings['UserID'].nunique()
    num_movies = len(movies)  # use total movies list for full sparsity calc
    num_ratings = len(ratings)
    
    # Avoid division by zero if dataset is malformed or extremely small
    if num_users > 0 and num_movies > 0:
        total_possible = num_users * num_movies
        sparsity = 1.0 - (num_ratings / total_possible)
    else:
        sparsity = 0.0
    
    with open(os.path.join(output_dir, 'eda_summary.txt'), 'w') as f:
        f.write("--- EDA Summary ---\n")
        f.write(f"Total Users: {num_users}\n")
        f.write(f"Total Movies: {num_movies}\n")
        f.write(f"Total Ratings: {num_ratings}\n")
        f.write(f"Sparsity: {sparsity * 100:.4f}%\n")
        
    print(f"\n✅ EDA Complete! All charts and the summary have been saved to the {output_dir} folder.")

if __name__ == "__main__":
    run_eda()
