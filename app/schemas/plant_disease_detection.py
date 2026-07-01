from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class ModelName(str, Enum):
  cnn = "cnn"
  resnet = "resnet"
  mobilenet = "mobilenet"
  efficientnet = "efficientnet"

class PredictionResponse(BaseModel):
  model: str
  class_name: str
  confidence: float
  inference_time: float
  is_healthy: bool
  explanation: dict | None