from sklearn.base import BaseEstimator, TransformerMixin
from .onepara_func import onepara
import numpy as np


class OnePara(BaseEstimator, TransformerMixin):
    def __init__(self):
        """No settings required"""

    def fit(self, X: np.ndarray, y: np.ndarray = None):
        """Do nothing and return the estimator unchanged"""
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        return onepara(X)
