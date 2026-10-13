import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, ConfusionMatrixDisplay)
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Classification", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    .page-title { color: #e74c3c; font-size: 2rem; font-weight: 800; }
    .section    { color: #c0392b; font-size: 1.4rem; font-weight: 700; }
    .metric-card {
        background: #fef9f0;
        border-left: 5px solid #e67e22;
        border-radius: 8px;
        padding: 16px 20px;
        text-align: center;
    }
    .metric-num   { font-size: 2.2rem; font-weight: 800; color: #c0392b; }
    .metric-label { font-size: 13px; color: #777; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🤖 Classification")
    st.markdown("Pick a target column and a model, then train and evaluate.")
    st.markdown("---")
    st.markdown("**Available models:**")
    st.markdown("""
- Logistic Regression
- Decision Tree
- Random Forest
""")
    st.markdown("---")
    st.caption("DS Toolkit · Page 5 of 5")

st.markdown('<p class="page-title">🤖 Classification</p>', unsafe_allow_html=True)
st.markdown("Select a target column, choose a model, and evaluate its performance.")
st.divider()

if "df_normalized" not in st.session_state:
    st.warning("⚠️ No data found. Please complete earlier pages first.")
    st.stop()

df = st.session_state["df_normalized"].copy()

# 1. Setup 
st.markdown('<p class="section">1 · Configure the Model</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    target_col = st.selectbox("🎯 Target column (label)", df.columns.tolist())

with col2:
    model_choice = st.selectbox("🤖 Model", ["Logistic Regression", "Decision Tree", "Random Forest"])

with col3:
    test_size = st.slider("Test set size (%)", 10, 40, 20)

# Feature columns (all except target)
feature_cols = [c for c in df.columns if c != target_col]
num_features = df[feature_cols].select_dtypes(include="number").columns.tolist()

st.markdown(f"**Features available:** {len(num_features)} numeric columns will be used for training.")

if not num_features:
    st.error("No numeric feature columns found. Please clean/encode your data first.")
    st.stop()

selected_features = st.multiselect("Select feature columns", num_features, default=num_features)

if not selected_features:
    st.info("Select at least one feature column.")
    st.stop()

st.divider()

# 2. Model params
st.markdown('<p class="section">2 · Model Hyperparameters</p>', unsafe_allow_html=True)

params = {}
if model_choice == "Logistic Regression":
    col1, col2 = st.columns(2)
    params["max_iter"] = col1.slider("Max iterations", 100, 1000, 200, step=50)
    params["C"]        = col2.slider("Regularisation (C)", 0.01, 10.0, 1.0)

elif model_choice == "Decision Tree":
    col1, col2 = st.columns(2)
    params["max_depth"]    = col1.slider("Max depth", 1, 20, 5)
    params["min_samples_split"] = col2.slider("Min samples split", 2, 20, 2)

elif model_choice == "Random Forest":
    col1, col2, col3 = st.columns(3)
    params["n_estimators"] = col1.slider("No. of trees", 10, 200, 100, step=10)
    params["max_depth"]    = col2.slider("Max depth", 1, 20, 5)
    params["random_state"] = 42

st.divider()

# 3. Train
if st.button("🚀 Train Model", type="primary"):

    # Prepare X, y
    X = df[selected_features].dropna()
    y = df.loc[X.index, target_col]

    # Encode target if categorical
    le = LabelEncoder()
    y_enc = le.fit_transform(y.astype(str))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=test_size / 100, random_state=42, stratify=y_enc if len(np.unique(y_enc)) > 1 else None
    )

    # Build model
    if model_choice == "Logistic Regression":
        model = LogisticRegression(**params)
    elif model_choice == "Decision Tree":
        model = DecisionTreeClassifier(**params, random_state=42)
    else:
        model = RandomForestClassifier(**params)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc    = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=[str(c) for c in le.classes_], output_dict=True)
    cm     = confusion_matrix(y_test, y_pred)

    # Results 
    st.markdown('<p class="section">3 · Results</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-card"><div class="metric-num">{acc*100:.1f}%</div><div class="metric-label">Accuracy</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="metric-num">{len(X_train)}</div><div class="metric-label">Train Samples</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="metric-num">{len(X_test)}</div><div class="metric-label">Test Samples</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card"><div class="metric-num">{len(le.classes_)}</div><div class="metric-label">Classes</div></div>', unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    # Confusion matrix
    with col1:
        st.markdown("**Confusion Matrix**")
        fig, ax = plt.subplots(figsize=(5, 4))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
        disp.plot(ax=ax, colorbar=False, cmap="Blues")
        ax.set_title("Confusion Matrix")
        st.pyplot(fig)
        plt.close()

    # Classification report
    with col2:
        st.markdown("**Classification Report**")
        report_df = pd.DataFrame(report).T.iloc[:-3]  # drop avg rows
        st.dataframe(
            report_df[["precision", "recall", "f1-score", "support"]].style.format({
                "precision": "{:.2f}", "recall": "{:.2f}", "f1-score": "{:.2f}", "support": "{:.0f}"
            }), use_container_width=True
        )

    st.divider()

    # Feature importance
    if model_choice in ["Decision Tree", "Random Forest"]:
        st.markdown('<p class="section">4 · Feature Importance</p>', unsafe_allow_html=True)
        importances = model.feature_importances_
        fi_df = pd.DataFrame({"Feature": selected_features, "Importance": importances})
        fi_df = fi_df.sort_values("Importance", ascending=True)

        fig, ax = plt.subplots(figsize=(8, max(3, len(selected_features) * 0.4)))
        bars = ax.barh(fi_df["Feature"], fi_df["Importance"], color="#c0392b", edgecolor="white")
        ax.set_xlabel("Importance")
        ax.set_title(f"Feature Importance — {model_choice}")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    elif model_choice == "Logistic Regression":
        st.markdown('<p class="section">4 · Feature Coefficients</p>', unsafe_allow_html=True)
        if model.coef_.shape[0] == 1:
            coefs = model.coef_[0]
        else:
            coefs = np.abs(model.coef_).mean(axis=0)

        coef_df = pd.DataFrame({"Feature": selected_features, "Coefficient": coefs})
        coef_df = coef_df.sort_values("Coefficient", ascending=True)

        fig, ax = plt.subplots(figsize=(8, max(3, len(selected_features) * 0.4)))
        colors = ["#c0392b" if v >= 0 else "#2980b9" for v in coef_df["Coefficient"]]
        ax.barh(coef_df["Feature"], coef_df["Coefficient"], color=colors, edgecolor="white")
        ax.axvline(0, color="black", linewidth=0.8)
        ax.set_title("Logistic Regression Coefficients")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.divider()

    # Prediction on full dataset
    st.markdown('<p class="section">5 · Predictions on Dataset</p>', unsafe_allow_html=True)
    full_X = df[selected_features].dropna()
    full_preds = le.inverse_transform(model.predict(full_X))
    result_df = df.loc[full_X.index, [target_col] + selected_features].copy()
    result_df["Predicted"] = full_preds
    result_df["Correct"]   = result_df[target_col].astype(str) == result_df["Predicted"].astype(str)
    st.dataframe(result_df.head(30), use_container_width=True)
    st.download_button("⬇️ Download Predictions CSV", result_df.to_csv(index=False), "predictions.csv", "text/csv")
