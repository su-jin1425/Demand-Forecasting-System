import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pickle
from ml.base import BasePredictor

class SARIMAXPredictor(BasePredictor):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model = None
        self.result = None
        self.last_date = None

    def train(self, df: pd.DataFrame, date_col: str, target_col: str):
        df = df.sort_values(date_col).set_index(date_col)
        self.last_date = df.index.max()
        # Simple ARIMA(1,1,1) for demonstration
        self.model = SARIMAX(df[target_col], order=(1, 1, 1))
        self.result = self.model.fit(disp=False)

    def predict(self, periods: int) -> pd.DataFrame:
        forecast = self.result.get_forecast(steps=periods)
        dates = pd.date_range(start=self.last_date + pd.Timedelta(days=1), periods=periods, freq='D')
        
        df_pred = pd.DataFrame({
            'prediction_date': dates,
            'forecast_value': forecast.predicted_mean.values,
            'lower_bound': forecast.conf_int().iloc[:, 0].values,
            'upper_bound': forecast.conf_int().iloc[:, 1].values
        })
        return df_pred

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump({'result': self.result, 'last_date': self.last_date}, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            data = pickle.load(f)
            self.result = data['result']
            self.last_date = data['last_date']
