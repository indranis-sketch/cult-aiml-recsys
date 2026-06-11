import numpy as np
from sklearn.decomposition import TruncatedSVD

def train_svd(sparse_matrix, n_components=50, random_state=42):
    """
    Train a Singular Value Decomposition (SVD) model on the sparse user-item matrix.
    """
    svd = TruncatedSVD(n_components=n_components, random_state=random_state)
    user_factors = svd.fit_transform(sparse_matrix)
    item_factors = svd.components_
    
    return user_factors, item_factors

def predict_svd(user_factors, item_factors):
    """
    Predict ratings by taking the dot product of user and item factors.
    """
    return np.dot(user_factors, item_factors)
