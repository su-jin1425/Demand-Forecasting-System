import pandas as pd
import xgboost as xgb
import pickle
import numpy as np
from ml.base import BasePredictor

class XGBoostPredictor(BasePredictor):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model = xgb.XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1)
        self.feature_cols = []
        self.last_date = None
        self.last_row = None

    def train(self, df: pd.DataFrame, date_col: str, target_col: str):
        self.feature_cols = [c for c in df.columns if c not in [date_col, target_col]]
        X = df[self.feature_cols]
        y = df[target_col]
        self.model.fit(X, y)
        self.last_date = df[date_col].max()
        self.last_row = df.iloc[-1].copy()

    def predict(self, periods: int) -> pd.DataFrame:
        predictions = []
        dates = pd.date_range(start=self.last_date + pd.Timedelta(days=1), periods=periods, freq='D')
        
        # This is a naive autoregressive prediction for demonstration.
        # In a real scenario, we'd recursively construct features for future dates.
        current_features = self.last_row[self.feature_cols].to_frame().T
        
        for date in dates:
            pred = self.model.predict(current_features)[0]
            predictions.append({
                'prediction_date': date,
                'forecast_value': float(pred),
                'lower_bound': float(pred * 0.9), # Mock confidence intervals
                'upper_bound': float(pred * 1.1)
            })
            
        return pd.DataFrame(predictions)

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump({
                'model': self.model,
                'feature_cols': self.feature_cols,
                'last_date': self.last_date,
                'last_row': self.last_row
            }, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            data = pickle.load(f)
            self.model = data['model']
            self.feature_cols = data['feature_cols']
            self.last_date = data['last_date']
            self.last_row = data['last_row']
