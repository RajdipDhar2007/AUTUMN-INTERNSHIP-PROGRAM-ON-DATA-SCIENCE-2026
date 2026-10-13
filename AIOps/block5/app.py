from pathlib import Path

import joblib
import numpy as np
import streamlit as st

MODEL_PATH = Path("/models/iris_model.joblib")
CLASS_NAMES = ["Setosa", "Versicolor", "Virginica"]

st.set_page_config(page_title="Iris Classifier", page_icon="🌸")

st.title("Iris Flower Classifier")
st.write("Enter the flower measurements and predict its species.")

if not MODEL_PATH.exists():
    st.error("Model not found. Run the training service first.")
    st.stop()


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()

sepal_length = st.slider("Sepal length (cm)", 4.0, 8.0, 5.1)
sepal_width = st.slider("Sepal width (cm)", 2.0, 4.5, 3.5)
petal_length = st.slider("Petal length (cm)", 1.0, 7.0, 1.4)
petal_width = st.slider("Petal width (cm)", 0.1, 2.5, 0.2)

features = np.array(
    [[sepal_length, sepal_width, petal_length, petal_width]]
)

if st.button("Predict"):
    prediction = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]

    st.success(f"Predicted species: {CLASS_NAMES[prediction]}")
    st.write("Class probabilities")

    for name, probability in zip(CLASS_NAMES, probabilities):
        st.write(f"{name}: {probability:.1%}")