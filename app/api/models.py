from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.database import get_db
from app.models.forecasting import ForecastingModel
from app.schemas.forecasting import ModelCreate, ModelResponse
from app.training.tasks import train_forecasting_model_task
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/train", response_model=ModelResponse, status_code=202)
async def train_model(
    model_in: ModelCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if model_in.model_type not in ["prophet", "xgboost", "statsmodels"]:
        raise HTTPException(status_code=400, detail="Invalid model type. Must be prophet, xgboost, or statsmodels.")
    
    # Create model record
    db_model = ForecastingModel(model_name=model_in.model_name, model_type=model_in.model_type)
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)

    # Offload training to Celery
    train_forecasting_model_task.delay(db_model.id, db_model.model_type)

    return db_model

@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(ForecastingModel).filter(ForecastingModel.id == model_id))
    model = result.scalars().first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model
