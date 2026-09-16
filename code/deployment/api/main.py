"""
FastAPI Model Serving
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import numpy as np
from pathlib import Path

app = FastAPI(
    title="Iris Classifier API",
    description="Predict Iris species from flower measurements",
    version="1.0.0"
)

# Paths inside container
MODEL_PATH = Path("/app/models/model.joblib")
FEATURES_PATH = Path("/app/models/feature_names.joblib")

model = None
feature_names = None

@app.on_event("startup")
def load_model():
    global model, feature_names
    model = joblib.load(MODEL_PATH)
    feature_names = joblib.load(FEATURES_PATH)
    print(f"Model loaded. Features: {feature_names}")


class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., example=5.1, description="Sepal length in cm")
    sepal_width: float = Field(..., example=3.5, description="Sepal width in cm")
    petal_length: float = Field(..., example=1.4, description="Petal length in cm")
    petal_width: float = Field(..., example=0.2, description="Petal width in cm")


@app.get("/")
def root():
    return {
        "message": "Iris Classifier API is running",
        "endpoints": {
            "docs": "/docs",
            "predict": "POST /predict"
        }
    }


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
def predict(features: IrisFeatures):
    data = np.array([[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width
    ]])
    prediction = int(model.predict(data)[0])
    probabilities = model.predict_proba(data)[0].tolist()

    class_names = ["setosa", "versicolor", "virginica"]
    return {
        "prediction": prediction,
        "class_name": class_names[prediction],
        "probabilities": {
            "setosa": round(probabilities[0], 4),
            "versicolor": round(probabilities[1], 4),
            "virginica": round(probabilities[2], 4)
        }
    }
