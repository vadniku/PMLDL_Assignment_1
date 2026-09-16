"""
Streamlit Web Application
Communicates with the FastAPI model service
"""

import streamlit as st
import requests

st.set_page_config(
    page_title="Iris Classifier",
    page_icon="🌸",
    layout="centered"
)

st.title("🌸 Iris Flower Classifier")
st.markdown("Введите параметры цветка и получите предсказание вида с помощью модели Random Forest.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    sepal_length = st.number_input(
        "Sepal length (cm)",
        min_value=4.0,
        max_value=8.0,
        value=5.1,
        step=0.1,
        help="Длина чашелистика"
    )
    petal_length = st.number_input(
        "Petal length (cm)",
        min_value=1.0,
        max_value=7.0,
        value=1.4,
        step=0.1,
        help="Длина лепестка"
    )

with col2:
    sepal_width = st.number_input(
        "Sepal width (cm)",
        min_value=2.0,
        max_value=4.5,
        value=3.5,
        step=0.1,
        help="Ширина чашелистика"
    )
    petal_width = st.number_input(
        "Petal width (cm)",
        min_value=0.1,
        max_value=2.5,
        value=0.2,
        step=0.1,
        help="Ширина лепестка"
    )

st.divider()

if st.button("🔮 Предсказать", type="primary", use_container_width=True):
    payload = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width
    }

    # Inside Docker network the service is called "api"
    api_url = "http://api:8000/predict"

    try:
        with st.spinner("Отправляем запрос к модели..."):
            response = requests.post(api_url, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()
            st.success(f"**Предсказанный вид:** {result['class_name'].upper()} (код {result['prediction']})")

            st.subheader("Вероятности классов")
            probs = result["probabilities"]
            st.progress(probs["setosa"], text=f"Setosa: {probs['setosa']:.1%}")
            st.progress(probs["versicolor"], text=f"Versicolor: {probs['versicolor']:.1%}")
            st.progress(probs["virginica"], text=f"Virginica: {probs['virginica']:.1%}")
        else:
            st.error(f"Ошибка API (код {response.status_code}): {response.text}")
    except requests.exceptions.ConnectionError:
        st.error(
            "Не удалось подключиться к API.\n\n"
            "Убедитесь, что контейнеры запущены:\n"
            "`docker-compose up --build -d`"
        )
    except Exception as e:
        st.error(f"Произошла ошибка: {e}")

st.markdown("---")
st.caption("MLOps Assignment 1 | FastAPI + Streamlit + Docker")
