from abc import ABC, abstractmethod
import pandas as pd

class BasePredictor(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None

    @abstractmethod
    def train(self, df: pd.DataFrame, date_col: str, target_col: str):
        pass

    @abstractmethod
    def predict(self, periods: int) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def save(self, path: str):
        pass

    @abstractmethod
    def load(self, path: str):
        pass
