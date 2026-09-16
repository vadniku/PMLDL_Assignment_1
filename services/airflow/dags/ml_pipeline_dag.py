"""
Airflow DAG: Full MLOps Pipeline
Runs every 5 minutes:
1. Data Engineering
2. Model Engineering
3. Deployment (docker-compose)
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import sys
from pathlib import Path

# Make project modules importable
# Adjust this path depending on how you mount the project into Airflow
PROJECT_ROOT = Path(__file__).resolve().parents[3]  # services/airflow/dags -> project root
sys.path.insert(0, str(PROJECT_ROOT))

default_args = {
    "owner": "student",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="mlops_iris_pipeline",
    default_args=default_args,
    description="Automated MLOps pipeline: Data → Model → Deploy",
    schedule_interval="*/5 * * * *",  # every 5 minutes
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["mlops", "iris", "assignment"],
) as dag:

    # Task 1: Data Engineering
    data_engineering = BashOperator(
        task_id="data_engineering",
        bash_command=f"cd {PROJECT_ROOT} && python code/datasets/data_processing.py",
    )

    # Task 2: Model Engineering
    model_engineering = BashOperator(
        task_id="model_engineering",
        bash_command=f"cd {PROJECT_ROOT} && python code/models/train_model.py",
    )

    # Task 3: Deployment
    deployment = BashOperator(
        task_id="deployment",
        bash_command=f"cd {PROJECT_ROOT}/code/deployment && docker compose up --build -d",
    )

    data_engineering >> model_engineering >> deployment
