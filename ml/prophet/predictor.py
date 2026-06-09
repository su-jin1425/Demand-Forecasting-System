import pandas as pd
from prophet import Prophet
import pickle
from ml.base import BasePredictor

class ProphetPredictor(BasePredictor):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model = Prophet(yearly_seasonality=True, weekly_seasonality=True)

    def train(self, df: pd.DataFrame, date_col: str, target_col: str):
        train_df = df[[date_col, target_col]].rename(columns={date_col: "ds", target_col: "y"})
        self.model.fit(train_df)

    def predict(self, periods: int) -> pd.DataFrame:
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
            columns={'ds': 'prediction_date', 'yhat': 'forecast_value', 'yhat_lower': 'lower_bound', 'yhat_upper': 'upper_bound'}
        )

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            self.model = pickle.load(f)
