"""
Stage 2: Model Engineering
- Feature engineering (simple scaling optional)
- Train RandomForest
- Evaluate + log metrics with MLflow
- Package model to models/model.joblib
"""

import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from pathlib import Path


def train_model():
    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)

    train = pd.read_csv("data/processed/train.csv")
    test = pd.read_csv("data/processed/test.csv")

    feature_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    X_train = train[feature_cols]
    y_train = train["species"]
    X_test = test[feature_cols]
    y_test = test["species"]

    with mlflow.start_run(run_name="iris_random_forest"):
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", 5)
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")

        print("=" * 50)
        print(f"Accuracy on test set: {acc:.4f}")
        print(classification_report(y_test, y_pred, target_names=["setosa", "versicolor", "virginica"]))
        print("=" * 50)

        # Save model and feature names
        model_path = models_dir / "model.joblib"
        joblib.dump(model, model_path)
        joblib.dump(feature_cols, models_dir / "feature_names.joblib")

        print(f"[Model] Saved to {model_path}")
        return str(model_path)


if __name__ == "__main__":
    train_model()
