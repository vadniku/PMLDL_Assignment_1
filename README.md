# PMLDL Assignment 1: MLOps Pipeline

Fully automated MLOps pipeline for Iris flower classification.

## Overview

This project implements a complete MLOps pipeline with three required stages:

1. **Data Engineering** – load, clean, remove outliers, and split data
2. **Model Engineering** – train a Random Forest model, evaluate it, and log metrics with MLflow
3. **Deployment** – serve the model via FastAPI and provide a Streamlit web interface

The API and the web application run in **separate Docker containers**.  
The entire pipeline can be executed automatically every 5 minutes using a Windows batch script + Task Scheduler.

---

## Project Structure

```
├── code
│   ├── datasets
│   │   └── data_processing.py
│   ├── models
│   │   └── train_model.py
│   └── deployment
│       ├── api
│       │   ├── Dockerfile
│       │   ├── main.py
│       │   └── requirements.txt
│       ├── app
│       │   ├── Dockerfile
│       │   ├── app.py
│       │   └── requirements.txt
│       └── docker-compose.yml
├── data
│   ├── processed
│   └── raw
├── models
├── notebooks
├── requirements.txt
├── run_pipeline.bat
└── README.md
```

---

## Quick Start

### 1. Create virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 2. Run the full pipeline

```bash
run_pipeline.bat
```

This script will sequentially:
- Process the data
- Train the model
- Build and start Docker containers

### 3. Access the services

| Service          | URL                        | Description                    |
|------------------|----------------------------|--------------------------------|
| **API**          | http://localhost:8000      | FastAPI model service          |
| **API Docs**     | http://localhost:8000/docs | Interactive Swagger UI         |
| **Web App**      | http://localhost:8501      | Streamlit prediction interface |

### 4. Stop the containers

```bash
cd code\deployment
docker compose down
```

---

## Pipeline Stages in Detail

### Stage 1: Data Engineering
- Loads the Iris dataset
- Saves raw data to `data/raw/`
- Removes missing values and outliers (IQR method)
- Splits data into train/test (80/20, stratified)
- Saves processed files to `data/processed/`

### Stage 2: Model Engineering
- Trains a `RandomForestClassifier`
- Evaluates the model on the test set
- Logs parameters and metrics to MLflow
- Saves the trained model to `models/model.joblib`

### Stage 3: Deployment
- **API** (FastAPI) – loads the model and exposes `/predict` endpoint
- **Web App** (Streamlit) – provides input fields and displays predictions
- Both services run in separate Docker containers and communicate over a Docker network

---

## Automation

Automation is implemented using:

- `run_pipeline.bat` – sequential execution of all three stages
- Windows Task Scheduler – runs the script every 5 minutes

### How to set up Task Scheduler

1. Open **Task Scheduler**
2. Create a new task
3. Set the trigger to repeat every 5 minutes
4. Set the action to run `run_pipeline.bat`
5. Enable “Run with highest privileges”

---

## Manual Execution (step by step)

```bash
# Stage 1
python code/datasets/data_processing.py

# Stage 2
python code/models/train_model.py

# Stage 3
cd code/deployment
docker compose up --build -d
```

---

## Requirements

- Python 3.10+ (3.11 or 3.12 recommended)
- Docker Desktop
- Windows Task Scheduler (for automation)

---

## Notes

- The model file (`models/model.joblib`) is generated at runtime and does not need to be pushed to GitHub.
- The dataset used is **Iris** (allowed by the assignment).
- API and Streamlit application run in **separate Docker containers** as required by the assignment.
