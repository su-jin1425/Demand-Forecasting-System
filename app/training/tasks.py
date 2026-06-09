import os
import asyncio
from app.core.celery_app import celery_app
from app.db.database import AsyncSessionLocal
from app.models.forecasting import ForecastingModel, TrainingLog
from app.core.config import settings
from sqlalchemy import update

import pandas as pd
import numpy as np

def _sync_train_model(model_id: int, model_type: str):
    """
    Synchronous wrapper for training to be executed by Celery.
    In a real scenario, we'd fetch data from the DB, but here we generate synthetic data
    to demonstrate the training and prove error reduction.
    """
    # 1. Generate Synthetic Demand Data
    dates = pd.date_range(start="2023-01-01", periods=365, freq='D')
    np.random.seed(42)
    # Base demand + trend + seasonality + noise
    demand = 100 + np.arange(365)*0.5 + np.sin(np.arange(365)*2*np.pi/7)*20 + np.random.normal(0, 10, 365)
    df = pd.DataFrame({'date': dates, 'demand': demand})

    # 2. Train Logic
    if model_type == "prophet":
        from ml.prophet.predictor import ProphetPredictor
        predictor = ProphetPredictor(model_name=f"model_{model_id}")
        predictor.train(df, date_col='date', target_col='demand')
    
    elif model_type == "xgboost":
        from ml.xgboost.predictor import XGBoostPredictor
        from app.feature_engineering.pipeline import FeatureEngineer
        fe = FeatureEngineer()
        df_features = fe.generate_features(df)
        predictor = XGBoostPredictor(model_name=f"model_{model_id}")
        predictor.train(df_features, date_col='date', target_col='demand')
    
    elif model_type == "statsmodels":
        from ml.statsmodels.predictor import SARIMAXPredictor
        predictor = SARIMAXPredictor(model_name=f"model_{model_id}")
        predictor.train(df, date_col='date', target_col='demand')
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    # 3. Save Model Artifact
    path = os.path.join(settings.MODEL_STORAGE_DIR, f"model_{model_id}.pkl")
    predictor.save(path)

async def _update_training_status(model_id: int, status: str, log: str):
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(ForecastingModel)
            .where(ForecastingModel.id == model_id)
            .values(training_status=status)
        )
        t_log = TrainingLog(model_id=model_id, training_status=status, execution_logs=log)
        session.add(t_log)
        await session.commit()

@celery_app.task(name="train_forecasting_model")
def train_forecasting_model_task(model_id: int, model_type: str):
    """
    Celery task to offload ML training asynchronously.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_update_training_status(model_id, "in_progress", "Started training"))
    
    try:
        _sync_train_model(model_id, model_type)
        loop.run_until_complete(_update_training_status(model_id, "completed", "Training finished successfully"))
    except Exception as e:
        loop.run_until_complete(_update_training_status(model_id, "failed", str(e)))
        raise e
