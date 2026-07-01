from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import JSONResponse
from app.services.plant_disease_detection import predictor
from http import HTTPStatus
from app.schemas.plant_disease_detection import PredictionResponse, ModelName

router = APIRouter()

@router.post(
  "/plant_disease_detection/predict", 
  response_model=PredictionResponse,
  status_code=HTTPStatus.ACCEPTED,)
async def predict(
  image: UploadFile = File(...),
  model: ModelName = Query(ModelName.efficientnet)
):
  return predictor.predict(
    image.file,
    model
  )