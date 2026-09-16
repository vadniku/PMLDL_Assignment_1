"""
Stage 1: Data Engineering
- Load raw data (Iris)
- Clean (missing values + outliers)
- Split into train/test
- Save to data/processed/
"""

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from pathlib import Path


def process_data():
    # Create directories
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Load Iris and save as "raw" CSV
    iris = load_iris(as_frame=True)
    df = iris.frame.copy()
    df.columns = [
        c.replace(" (cm)", "").replace(" ", "_") for c in df.columns
    ]
    df = df.rename(columns={"target": "species"})
    df.to_csv(raw_dir / "iris_raw.csv", index=False)
    print(f"[Data] Raw data saved to {raw_dir / 'iris_raw.csv'}")

    # === Cleaning ===
    # Handle missing values (Iris has none, but keep the step)
    df = df.dropna()

    # Remove outliers using IQR method on numeric columns
    numeric_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    Q1 = df[numeric_cols].quantile(0.25)
    Q3 = df[numeric_cols].quantile(0.75)
    IQR = Q3 - Q1
    mask = ~((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).any(axis=1)
    df_clean = df[mask].copy()
    print(f"[Data] After outlier removal: {len(df_clean)} rows (was {len(df)})")

    # Split
    X = df_clean.drop("species", axis=1)
    y = df_clean["species"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    train = X_train.copy()
    train["species"] = y_train.values
    test = X_test.copy()
    test["species"] = y_test.values

    train_path = processed_dir / "train.csv"
    test_path = processed_dir / "test.csv"
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)

    print(f"[Data] Train saved: {train_path}  shape={train.shape}")
    print(f"[Data] Test  saved: {test_path}  shape={test.shape}")
    return str(train_path), str(test_path)


if __name__ == "__main__":
    process_data()
