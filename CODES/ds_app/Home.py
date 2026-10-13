import streamlit as st

st.set_page_config(page_title="DS Toolkit", page_icon="🔬", layout="wide")

st.markdown("""
<style>
    .title      { color: #e74c3c; font-size: 2.4rem; font-weight: 800; }
    .section    { color: #2980b9; font-size: 1.5rem; font-weight: 700; }
    .card {
        background: #f8f9fa;
        border-left: 5px solid #2980b9;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
    .card h4 { margin: 0 0 6px 0; color: #1a1a2e; }
    .card p  { margin: 0; color: #555; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🔬 DS Toolkit")
    st.markdown("---")
    st.markdown("**Pages**")
    st.markdown("""
- 🏠 Home *(you are here)*
- 📂 1 · Upload & Preview
- 🧹 2 · Data Cleaning
- 📊 3 · EDA
- ⚖️ 4 · Normalization
- 🤖 5 · Classification
""")
    st.markdown("---")
    st.info("Upload a CSV on **Page 1** to get started. Your data carries through all pages automatically.")
    st.caption("DS Toolkit · Built with Streamlit")

# Main
st.markdown('<p class="title">🔬 Data Science Toolkit</p>', unsafe_allow_html=True)
st.markdown("A simple end-to-end data science app — upload your CSV and walk through every step of the pipeline.")

st.divider()

st.markdown('<p class="section">📌 Pipeline Overview</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h4>📂 Step 1 · Upload & Preview</h4>
        <p>Upload a CSV file and get an instant preview of shape, columns, data types, and sample rows.</p>
    </div>
    <div class="card">
        <h4>🧹 Step 2 · Data Cleaning</h4>
        <p>Handle missing values, drop duplicate rows, and remove unwanted columns — interactively.</p>
    </div>
    <div class="card">
        <h4>📊 Step 3 · EDA</h4>
        <p>Explore distributions, correlation heatmaps, value counts, and pairplots of your data.</p>
    </div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h4>⚖️ Step 4 · Normalization</h4>
        <p>Scale numeric features using Min-Max, Standard (Z-score), or Robust scaling.</p>
    </div>
    <div class="card">
        <h4>🤖 Step 5 · Classification</h4>
        <p>Pick a target column and run Logistic Regression, Decision Tree, or Random Forest. See accuracy, confusion matrix, and feature importance.</p>
    </div>
    <div class="card">
        <h4>💾 Download Anywhere</h4>
        <p>Every processed dataframe can be downloaded as a CSV at any stage of the pipeline.</p>
    </div>
""", unsafe_allow_html=True)

st.divider()
st.markdown("👉 **Start by navigating to Page 1 → Upload & Preview** in the sidebar.")
