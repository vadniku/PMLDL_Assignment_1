# PMLDL Assignment 1: MLOps Pipeline (Iris)

Полностью автоматизированный MLOps-пайплайн из трёх стадий:

1. **Data Engineering** — загрузка, очистка, удаление выбросов, split
2. **Model Engineering** — обучение RandomForest + логирование в MLflow
3. **Deployment** — FastAPI + Streamlit в **отдельных Docker-контейнерах**

Пайплайн автоматически запускается **каждые 5 минут** через Apache Airflow.

---

## Структура репозитория

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
├── models                  # сюда сохраняется model.joblib
├── notebooks
├── services
│   └── airflow
│       ├── dags
│       │   └── ml_pipeline_dag.py
│       └── logs
├── requirements.txt
└── README.md
```

---

## Быстрый старт (ручной запуск)

### 1. Клонируйте репозиторий и создайте окружение

```bash
git clone <your-repo-url>
cd pmldl-mlops-assignment

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Запустите Stage 1 и Stage 2

```bash
python code/datasets/data_processing.py
python code/models/train_model.py
```

После этого в папке `models/` появятся файлы:
- `model.joblib`
- `feature_names.joblib`

### 3. Запустите Deployment (Docker)

```bash
cd code/deployment
docker compose up --build -d
```

### 4. Откройте сервисы

| Сервис       | URL                          | Описание                  |
|--------------|------------------------------|---------------------------|
| **API**      | http://localhost:8000        | FastAPI                   |
| **Swagger**  | http://localhost:8000/docs   | Интерактивная документация|
| **App**      | http://localhost:8501        | Streamlit веб-приложение  |

### 5. Остановка контейнеров

```bash
cd code/deployment
docker compose down
```

---

## Автоматизация через Airflow

1. Установите Apache Airflow (или используйте Docker-образ Airflow).
2. Скопируйте файл `services/airflow/dags/ml_pipeline_dag.py` в папку `dags` вашего Airflow.
3. Убедитесь, что:
   - Проект доступен из контейнера/процесса Airflow
   - Docker доступен (для task Deployment)
4. DAG называется `mlops_iris_pipeline` и запускается каждые 5 минут.

Если один прогон занимает больше времени — измените `schedule_interval` на `*/10 * * * *` или `*/15 * * * *`.

---

## Примечания

- Датасет: **Iris** (не запрещён заданием).
- Модель: `RandomForestClassifier` (простая и достаточная).
- API и приложение работают в **разных** Docker-контейнерах и общаются через Docker-сеть.
- Модель не обязательно пушить в GitHub — она генерируется при запуске пайплайна.
- Для демонстрации TA достаточно показать:
  1. Запуск пайплайна
  2. Работающее Streamlit-приложение с предсказаниями
  3. Документацию API (`/docs`)

---

## Требования задания — выполнены

- [x] Data Engineering stage
- [x] Model Engineering stage (MLflow)
- [x] Deployment (отдельные Docker-контейнеры + FastAPI + Streamlit)
- [x] Автоматизация (Airflow, каждые 5 минут)
- [x] Логичная структура репозитория
