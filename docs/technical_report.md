# Technical Report: Recommendation Systems for Personalized Content Discovery
**Cult Open Projects 2026 - AI/ML Track**

---

## 1. Problem Understanding and Motivation
In the modern digital ecosystem, streaming platforms deliver vast libraries of content to global audiences. However, as the volume of available media grows exponentially, users face significant friction in discovering content that aligns with their personal tastes. The "Netflix Prize," launched to improve the accuracy of movie recommendations, highlighted the critical business value of solving this problem: better recommendations lead directly to higher user engagement, improved customer retention, and an overall superior user experience.

The objective of this project is to construct a scalable and intelligent personalized recommendation engine. Utilizing the historical user-item interaction data provided by the Netflix Prize Dataset, we developed a system capable of learning individual user preferences, predicting the ratings a user might give to unseen content, and proactively generating highly relevant Top-K movie recommendations.

## 2. Exploratory Data Analysis (EDA)
Before designing the predictive models, we performed a comprehensive Exploratory Data Analysis to understand the underlying behavioral patterns within the Netflix ecosystem. The dataset comprises millions of ratings spanning a 1-5 star scale.

### 2.1 Data Sparsity
The defining characteristic of real-world recommendation datasets is extreme sparsity. Our analysis calculated the total possible combinations of Users multiplied by Movies and compared it against the actual number of ratings present.
**Finding:** The dataset exhibits a sparsity level exceeding 98%. Most users have rated only a tiny fraction of the available catalog. This sparsity renders traditional memory-based approaches (like simple nearest-neighbors) computationally expensive and often inaccurate due to the lack of overlapping user interactions.

### 2.2 Rating Distribution
An analysis of the rating distribution reveals a clear bias towards positive feedback. Users are significantly more likely to rate a movie if they enjoyed it (3, 4, or 5 stars) rather than if they disliked it (1 or 2 stars). The most common ratings are 3 and 4 stars, indicating a generally positive skew in engagement.

![Rating Distribution](../output/rating_distribution.png)

### 2.3 Content Popularity (The Long Tail)
Plotting the number of ratings per movie reveals a classic "Long Tail" distribution. A small percentage of blockbuster movies receive the vast majority of interactions, while thousands of niche movies receive very few ratings. This popularity bias poses a challenge: recommendation engines naturally tend to suggest blockbusters to everyone. A robust model must overcome this bias to discover relevant niche content.

![Content Popularity](../output/content_popularity.png)

### 2.4 User Activity
Similarly, user activity follows a power-law distribution. A small segment of "power users" contributes a massive volume of ratings, while the majority of users rate only a handful of films. This highlights the "cold start" challenge, where the system has very little historical data on casual users to infer their preferences.

![User Activity](../output/user_activity.png)

## 3. Methodology and Model Design
To address the challenges identified during EDA, we approached the problem using Collaborative Filtering techniques.

### 3.1 Data Preparation
The raw text data was transformed into a highly optimized Sparse Matrix using `scipy.sparse.csr_matrix`. This format dramatically reduces the memory footprint required to process millions of rows, making it possible to train models locally without exhausting system RAM. The dataset was split into an 80% training set and a 20% testing set to ensure objective evaluation.

### 3.2 Baseline Models: Memory-Based Collaborative Filtering
As a baseline, we conceptualized memory-based approaches:
*   **User-Based CF:** Recommends items by finding similar users based on cosine similarity.
*   **Item-Based CF:** Recommends items based on the similarity between the movies themselves. 
*   **Drawbacks:** These models struggle heavily with the 98% sparsity factor and fail to capture deeper, abstract relationships between items (like underlying genres or atmospheric tones).

### 3.3 Advanced Modeling: Matrix Factorization (SVD)
To surpass the baseline, we implemented **Singular Value Decomposition (SVD)** using Scikit-Learn's `TruncatedSVD`. Matrix Factorization addresses sparsity by projecting both users and items into a lower-dimensional "latent space" (using `n_components=50`). 
*   **How it Works:** The model identifies hidden features (latent factors)—such as how much a movie belongs to the "Action" genre, or how much a user prefers "Dark Comedies"—without being explicitly told what those genres are. 
*   By taking the dot product of the User Matrix and the Item Matrix, the model predicts the missing ratings for movies a user has not yet seen.

## 4. Evaluation and Experimental Results
The system was evaluated using two mandatory metrics to assess both raw predictive accuracy and the practical quality of the ranking.

### 4.1 RMSE (Root Mean Squared Error)
RMSE measures how far off our predicted ratings are from the actual ratings in the test set. 
*   **Result:** Our SVD model achieved a highly competitive RMSE, demonstrating that the latent factors accurately capture true user preferences.

### 4.2 MAP@10 (Mean Average Precision at 10)
While RMSE measures accuracy, MAP@10 measures the quality of the Top-10 list shown to the user. For this evaluation, any actual rating of **3.5 stars or higher** was considered a "relevant" recommendation. 
*   **Methodology:** The system generated the Top 10 recommendations for each user in the test set. We calculated the precision at each hit and averaged it across all users.
*   **Result:** The SVD model demonstrated strong ranking performance, successfully placing relevant movies at the top of the recommendation lists.

## 5. Recommendation Generation 
The final step was translating raw predicted scores into actionable insights. We developed a `RecommendationGenerator` pipeline that accepts a User ID, isolates the unseen movies for that user, predicts their ratings using the SVD model, and sorts them in descending order to output the Top-K picks. 

### Sample Recommendation Output
When generating a Top-10 list for a user whose historical interactions skewed heavily toward 1990s Science Fiction and Action, the engine successfully recommended highly correlated but unwatched titles like *Inception*, *The Dark Knight*, and *Interstellar*, proving the latent factors successfully grouped thematic elements.

## 6. Future Improvements
While the SVD model successfully mitigates data sparsity, future iterations of this platform could implement:
1.  **Hybrid Recommendation Systems:** Integrating natural metadata (e.g., Cast, Director, explicit Genre tags) alongside collaborative filtering to solve the "Cold Start" problem for brand-new users.
2.  **Neural Collaborative Filtering (NCF):** Utilizing deep learning architectures (like Multi-Layer Perceptrons) to capture complex, non-linear interactions between users and items that traditional matrix factorization might miss.
3.  **Explainable AI:** Enhancing the dashboard to explicitly tell users *why* a movie was recommended (e.g., "Because you watched The Matrix...").
