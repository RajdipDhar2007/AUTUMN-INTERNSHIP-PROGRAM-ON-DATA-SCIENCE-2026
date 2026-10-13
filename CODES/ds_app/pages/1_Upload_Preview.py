import streamlit as st
import pandas as pd
import io 
st.set_page_config(page_title="Upload & Preview", page_icon="📂", layout="wide")

st.markdown("""
<style>
    .page-title { color: #e74c3c; font-size: 2rem; font-weight: 800; }
    .section    { color: #2980b9; font-size: 1.4rem; font-weight: 700; }
    .stat-box {
        background: #eaf4fb;
        border-left: 5px solid #2980b9;
        border-radius: 8px;
        padding: 14px 18px;
        text-align: center;
    }
    .stat-num  { font-size: 2rem; font-weight: 800; color: #1a5276; }
    .stat-label{ font-size: 13px; color: #555; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📂 Upload & Preview")
    st.markdown("Upload a CSV to begin. The data is stored in session state and shared across all pages.")
    st.markdown("---")
    st.markdown("**Supported format:** `.csv`")
    st.caption("DS Toolkit · Page 1 of 5")

st.markdown('<p class="page-title">📂 Upload & Preview</p>', unsafe_allow_html=True)
st.markdown("Upload your CSV dataset to get started. The data will be available across all pages.")
st.divider()

uploaded = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.session_state["df"]            = df
    st.session_state["df_clean"]      = df.copy()
    st.session_state["df_normalized"] = df.copy()
    st.success(f"✅ **{uploaded.name}** loaded successfully!")

    st.divider()
    st.markdown('<p class="section">📐 Dataset Shape</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{df.shape[0]:,}</div><div class="stat-label">Rows</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{df.shape[1]}</div><div class="stat-label">Columns</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{df.isnull().sum().sum()}</div><div class="stat-label">Missing Values</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{df.duplicated().sum()}</div><div class="stat-label">Duplicate Rows</div></div>', unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section">🔍 Data Preview</p>', unsafe_allow_html=True)
        n = st.slider("Rows to preview", 5, min(100, len(df)), 10)
        st.dataframe(df.head(n), use_container_width=True)

    with col2:
        st.markdown('<p class="section">🗂️ Column Info</p>', unsafe_allow_html=True)
        info_df = pd.DataFrame({
            "Column":   df.columns,
            "Dtype":    df.dtypes.values,
            "Non-Null": df.notnull().sum().values,
            "Nulls":    df.isnull().sum().values,
            "Unique":   df.nunique().values,
        })
        st.dataframe(info_df, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown('<p class="section">📈 Descriptive Statistics</p>', unsafe_allow_html=True)
    #stat_val = df.describe().T.style.format("{:.2f}")
    #st.write(pd.DataFrame(stat_val.data), use_container_width=True)
    st.dataframe(df.describe().T.style.format("{:.2f}"), use_container_width=True)

    st.divider()
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Raw Data')
    st.download_button("⬇️ Download Raw Excel", buffer, "raw_data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")    
    #st.download_button("⬇️ Download Raw CSV", df.to_csv(index=False), "raw_data.csv", "text/csv")
else:
    st.info("👆 Upload a CSV file above to begin.")
    st.markdown("**Don't have a dataset?** Try a sample from [Kaggle](https://www.kaggle.com/datasets) or use the Iris / Titanic dataset.")
