from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ModelBase(BaseModel):
    model_name: str
    model_type: str

class ModelCreate(ModelBase):
    pass

class ModelResponse(ModelBase):
    id: int
    training_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class PredictionBase(BaseModel):
    prediction_date: datetime
    forecast_value: float
    confidence_score: Optional[float] = None

class PredictionResponse(PredictionBase):
    id: int
    model_id: int
    created_at: datetime

    class Config:
        from_attributes = True
