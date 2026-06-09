from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class AnalyticsMetric(Base):
    __tablename__ = "analytics_metrics"

    id = Column(Integer, primary_key=True, index=True)
    model_accuracy = Column(Float, nullable=True)
    mae = Column(Float, nullable=True)
    rmse = Column(Float, nullable=True)
    mape = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
