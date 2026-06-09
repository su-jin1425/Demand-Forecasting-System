from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class ForecastingModel(Base):
    __tablename__ = "forecasting_models"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True, nullable=False)
    model_type = Column(String, nullable=False)
    training_status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    predictions = relationship("ForecastPrediction", back_populates="model")
    logs = relationship("TrainingLog", back_populates="model")


class ForecastPrediction(Base):
    __tablename__ = "forecast_predictions"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("forecasting_models.id"), nullable=False)
    prediction_date = Column(DateTime(timezone=True), nullable=False)
    forecast_value = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    model = relationship("ForecastingModel", back_populates="predictions")


class TrainingLog(Base):
    __tablename__ = "training_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("forecasting_models.id"), nullable=False)
    training_status = Column(String, nullable=False)
    execution_logs = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    model = relationship("ForecastingModel", back_populates="logs")
