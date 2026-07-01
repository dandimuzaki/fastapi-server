import tensorflow as tf
import numpy as np
from PIL import Image
import json
import time
from app.schemas.plant_disease_detection import PredictionResponse
from huggingface_hub import hf_hub_download

def download_model(model_name):
  path = hf_hub_download(
    repo_id="dandimuzaki/plant-disease-detection",
    filename=f"artifacts/{model_name}/model.keras"
  )

  model = tf.keras.models.load_model(path)
  return model

class PlantDiseasePredictor:
  def __init__(self):
    self.models = {
      # "cnn": {
      #   "display_name": "Custom CNN",
      #   "model": download_model("custom_cnn"),
      # },
      # "resnet": {
      #   "display_name": "ResNet50",
      #   "model": download_model("resnet50"),
      # },
      # "mobilenet": {
      #   "display_name": "MobileNetV3",
      #   "model": download_model("mobilenetv3"),
      # },
      "efficientnet": {
        "display_name": "EfficientNetB0",
        "model": download_model("efficientnetb0"),
      },
    }

    with open("ml/plant_disease_detection/class_names.json") as f:
      self.class_names = json.load(f)

    with open('ml/plant_disease_detection/explanation.json', 'r', encoding='utf-8') as f:
      self.explanation = json.load(f)

  def preprocess_image(self, file):
    image = Image.open(file).convert("RGB")
    image = image.resize((224,224))

    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])

    return input_arr
    
  def predict(self, image_file, model_name):
    image = self.preprocess_image(image_file)
    model_info = self.models[model_name]

    start = time.time()
    prediction = model_info["model"].predict(image)
    end = time.time()
    inference_time = (end-start)*1000

    predicted_idx = int(np.argmax(prediction))

    class_name = self.class_names[predicted_idx]

    confidence = float(np.max(prediction))

    is_healthy = "healthy" in class_name.lower()

    if is_healthy:
      explanation = {
        **self.explanation.get(str(predicted_idx), {}),
        **self.explanation.get("healthy", {}),
      }
    else:
      explanation = self.explanation.get(str(predicted_idx))

    return PredictionResponse(
      model=model_info["display_name"],
      class_name=class_name,
      confidence=confidence,
      inference_time=inference_time,
      is_healthy=is_healthy,
      explanation=explanation,
    )

predictor = PlantDiseasePredictor()