from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class ForecastingDataset(Base):
    __tablename__ = "forecasting_datasets"

    id = Column(Integer, primary_key=True, index=True)
    dataset_name = Column(String, index=True, nullable=False)
    dataset_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FeatureStore(Base):
    __tablename__ = "feature_store"

    id = Column(Integer, primary_key=True, index=True)
    feature_name = Column(String, index=True, nullable=False)
    feature_value = Column(String, nullable=False)
    feature_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
