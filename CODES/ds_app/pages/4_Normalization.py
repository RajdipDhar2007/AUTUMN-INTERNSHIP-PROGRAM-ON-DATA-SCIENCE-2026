import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

st.set_page_config(page_title="Normalization", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
    .page-title { color: #e74c3c; font-size: 2rem; font-weight: 800; }
    .section    { color: #8e44ad; font-size: 1.4rem; font-weight: 700; }
    .desc-box {
        background: #f5eef8;
        border-left: 5px solid #8e44ad;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 14px;
        color: #333;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚖️ Normalization")
    st.markdown("Scale numeric features so models train fairly. Choose a scaler and select which columns to scale.")
    st.markdown("---")
    st.markdown("**Scalers:**")
    st.markdown("""
- **Min-Max** → scales to [0, 1]
- **Standard** → mean=0, std=1
- **Robust** → uses median/IQR, ignores outliers
""")
    st.markdown("---")
    st.caption("DS Toolkit · Page 4 of 5")

st.markdown('<p class="page-title">⚖️ Normalization</p>', unsafe_allow_html=True)
st.markdown("Scale your numeric features before feeding them into a machine learning model.")
st.divider()

if "df_clean" not in st.session_state:
    st.warning("⚠️ No data found. Please complete **Page 1 → Upload** first.")
    st.stop()

df = st.session_state["df_clean"].copy()
num_cols = df.select_dtypes(include="number").columns.tolist()

if not num_cols:
    st.error("No numeric columns found in the dataset.")
    st.stop()

# Scaler choice 
st.markdown('<p class="section">1 · Choose a Scaler</p>', unsafe_allow_html=True)

scaler_choice = st.radio("Scaling method", ["Min-Max Scaler", "Standard Scaler (Z-score)", "Robust Scaler"], horizontal=True)

descriptions = {
    "Min-Max Scaler":             "Scales each feature to a [0, 1] range. Sensitive to outliers. Best when you know the bounds of your data.",
    "Standard Scaler (Z-score)":  "Transforms features to have mean=0 and std=1. Good for algorithms that assume normally distributed data (e.g. logistic regression, SVM).",
    "Robust Scaler":              "Uses median and IQR instead of mean/std. Robust to outliers — great for real-world messy data.",
}
st.markdown(f'<div class="desc-box">ℹ️ {descriptions[scaler_choice]}</div>', unsafe_allow_html=True)

st.divider()

# Column selection
st.markdown('<p class="section">2 · Select Columns to Scale</p>', unsafe_allow_html=True)

cols_to_scale = st.multiselect("Numeric columns to normalize", num_cols, default=num_cols)

if not cols_to_scale:
    st.info("Select at least one column above.")
    st.stop()

# Before / After preview
st.markdown('<p class="section">3 · Before vs After Preview</p>', unsafe_allow_html=True)

scalers = {
    "Min-Max Scaler":            MinMaxScaler(),
    "Standard Scaler (Z-score)": StandardScaler(),
    "Robust Scaler":             RobustScaler(),
}
scaler = scalers[scaler_choice]

df_scaled = df.copy()
df_scaled[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Before scaling**")
    st.dataframe(df[cols_to_scale].describe().T[["mean", "std", "min", "max"]].style.format("{:.3f}"),
                 use_container_width=True)
with col2:
    st.markdown("**After scaling**")
    st.dataframe(df_scaled[cols_to_scale].describe().T[["mean", "std", "min", "max"]].style.format("{:.3f}"),
                 use_container_width=True)

st.divider()

# Distribution comparison 
st.markdown('<p class="section">4 · Distribution Comparison</p>', unsafe_allow_html=True)

viz_col = st.selectbox("Column to visualise", cols_to_scale)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(df[viz_col].dropna(), bins=30, color="#2980b9", edgecolor="white", alpha=0.85)
axes[0].set_title(f"Before — {viz_col}")
axes[0].set_xlabel("Value")

axes[1].hist(df_scaled[viz_col].dropna(), bins=30, color="#27ae60", edgecolor="white", alpha=0.85)
axes[1].set_title(f"After ({scaler_choice}) — {viz_col}")
axes[1].set_xlabel("Scaled Value")

plt.tight_layout()
st.pyplot(fig)
plt.close()

st.divider()

#Save 
if st.button("💾 Save Scaled Dataset for Classification", type="primary"):
    st.session_state["df_normalized"] = df_scaled
    st.success("✅ Scaled dataset saved! Head to **Page 5 → Classification**.")

st.dataframe(df_scaled.head(10), use_container_width=True)
st.download_button("⬇️ Download Scaled CSV", df_scaled.to_csv(index=False), "scaled_data.csv", "text/csv")
