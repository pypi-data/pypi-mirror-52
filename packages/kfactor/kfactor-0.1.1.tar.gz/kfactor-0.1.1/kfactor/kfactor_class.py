from sklearn.base import BaseEstimator, TransformerMixin
from .kfactor_func import kfactor
import numpy as np


class KFactor(BaseEstimator, TransformerMixin):
    def __init__(self, k: int = 2, algorithm: str = 'COBYLA'):
        """No settings required"""
        self.k = k
        self.algorithm = algorithm

    def fit(self, X: np.ndarray, y: np.ndarray = None):
        """Do nothing and return the estimator unchanged"""
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        C, _, _, _, _ = kfactor(X, k=self.k, algorithm=self.algorithm)
        return C
