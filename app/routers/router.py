from fastapi import APIRouter
from routers.plant_disease_detection import router as plant_disease_detection_router

router = APIRouter()
router.include_router(plant_disease_detection_router)
