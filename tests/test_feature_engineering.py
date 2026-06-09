import pytest
import pandas as pd
from app.feature_engineering.pipeline import FeatureEngineer

def test_feature_engineering_reduces_error():
    # Synthetic data
    dates = pd.date_range(start="2023-01-01", periods=30, freq='D')
    df = pd.DataFrame({'date': dates, 'demand': range(30)})
    
    fe = FeatureEngineer(date_column='date', target_column='demand')
    df_features = fe.generate_features(df)
    
    # Assertions
    assert 'lag_1' in df_features.columns
    assert 'lag_7' in df_features.columns
    assert 'rolling_mean_7' in df_features.columns
    assert 'is_weekend' in df_features.columns
    # Ensure NaNs are dropped
    assert not df_features.isnull().values.any()
