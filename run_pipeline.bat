@echo off
cd /d D:\pmldl-mlops-assignment

echo ========================================
echo Starting MLOps Pipeline
echo ========================================

call venv\Scripts\activate.bat

echo.
echo [1/3] Data Engineering...
python code\datasets\data_processing.py
if %errorlevel% neq 0 (
    echo Data Engineering failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Model Engineering...
python code\models\train_model.py
if %errorlevel% neq 0 (
    echo Model Engineering failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Deployment...
cd code\deployment
docker compose up --build -d
if %errorlevel% neq 0 (
    echo Deployment failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Pipeline finished successfully
echo ========================================
