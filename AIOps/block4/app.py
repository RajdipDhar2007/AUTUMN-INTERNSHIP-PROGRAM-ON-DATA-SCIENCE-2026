# app.py
import pickle
import streamlit as st
import numpy as np

# Load model
with open("iris_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Iris Flower Classifier")
st.write("This app predicts the type of Iris flower 🌸")

# Input features
sepal_length = st.slider("Sepal length (cm)", 4.0, 8.0, 5.0)
sepal_width = st.slider("Sepal width (cm)", 2.0, 4.5, 3.0)
petal_length = st.slider("Petal length (cm)", 1.0, 7.0, 4.0)
petal_width = st.slider("Petal width (cm)", 0.1, 2.5, 1.0)

features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

# Prediction
if st.button("Predict"):
    prediction = model.predict(features)
    iris_types = ["Setosa", "Versicolor", "Virginica"]
    st.success(f"Predicted Iris type: {iris_types[prediction[0]]}")