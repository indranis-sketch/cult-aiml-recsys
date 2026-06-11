import random
import datetime

def generate_mock_data():
    # 1. Generate movie_titles.csv
    movies = [
        "The Matrix", "Inception", "Interstellar", "The Dark Knight",
        "Pulp Fiction", "Forrest Gump", "The Shawshank Redemption",
        "The Godfather", "Toy Story", "Gladiator"
    ]
    
    with open('movie_titles.csv', 'w', encoding='iso-8859-1') as f:
        for i, title in enumerate(movies, start=1):
            year = random.randint(1990, 2010)
            f.write(f"{i},{year},{title}\n")
            
    # 2. Generate combined_data_1.txt (Ratings)
    user_ids = [random.randint(1000000, 2000000) for _ in range(50)]
    
    with open('combined_data_1.txt', 'w') as f:
        for movie_id in range(1, len(movies) + 1):
            f.write(f"{movie_id}:\n")
            # Generate random number of ratings for this movie
            num_ratings = random.randint(5, 20)
            for _ in range(num_ratings):
                user_id = random.choice(user_ids)
                rating = random.randint(1, 5)
                # Generate random date around 2005
                days_offset = random.randint(0, 365)
                date_str = (datetime.date(2005, 1, 1) + datetime.timedelta(days=days_offset)).strftime("%Y-%m-%d")
                f.write(f"{user_id},{rating},{date_str}\n")

if __name__ == "__main__":
    generate_mock_data()
    print("Mock Netflix Prize dataset generated successfully!")
