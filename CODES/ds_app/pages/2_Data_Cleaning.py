import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Cleaning", page_icon="🧹", layout="wide")

st.markdown("""
<style>
    .page-title { color: #e74c3c; font-size: 2rem; font-weight: 800; }
    .section    { color: #27ae60; font-size: 1.4rem; font-weight: 700; }
    .subhead    { color: #8e44ad; font-size: 1.1rem; font-weight: 600; }
    .result-box {
        background: #f0faf4;
        border-left: 5px solid #27ae60;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 8px;
        color: #1a1a2e;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🧹 Data Cleaning")
    st.markdown("Clean your dataset step by step. Changes are applied to a working copy and carried forward.")
    st.markdown("---")
    st.caption("DS Toolkit · Page 2 of 5")

st.markdown('<p class="page-title">🧹 Data Cleaning</p>', unsafe_allow_html=True)
st.markdown("Handle missing values, remove duplicates, and drop unwanted columns.")
st.divider()

if "df" not in st.session_state:
    st.warning("⚠️ No data found. Please upload a CSV on **Page 1** first.")
    st.stop()

df = st.session_state["df_clean"].copy()

# Before stats
col1, col2, col3 = st.columns(3)
col1.metric("Rows",           df.shape[0])
col2.metric("Columns",        df.shape[1])
col3.metric("Missing Values", int(df.isnull().sum().sum()))
st.divider()

#1. Drop Duplicates 
st.markdown('<p class="section">1 · Remove Duplicate Rows</p>', unsafe_allow_html=True)
dup_count = int(df.duplicated().sum())
st.markdown(f"Duplicate rows found: **{dup_count}**")
if st.button("🗑️ Drop Duplicates", disabled=(dup_count == 0)):
    df = df.drop_duplicates()
    st.success(f"Dropped {dup_count} duplicate row(s).")

st.divider()

#2. Handle Missing Values 
st.markdown('<p class="section">2 · Handle Missing Values</p>', unsafe_allow_html=True)

missing = df.isnull().sum()
missing = missing[missing > 0]

if missing.empty:
    st.success("✅ No missing values in the dataset.")
else:
    st.dataframe(
        missing.reset_index().rename(columns={"index": "Column", 0: "Missing Count"}),
        use_container_width=True, hide_index=True
    )

    col1, col2 = st.columns(2)
    with col1:
        #statistical techniques to handle missing values in numeric columns
        strategy = st.radio("Strategy for numeric columns", ["Mean", "Median", "Mode", "Drop rows with nulls"])
    with col2:
        #statistical techniques to handle missing values in categorical columns
        cat_strategy = st.radio("Strategy for categorical columns", ["Mode", "Fill with 'Unknown'", "Drop rows with nulls"])

    if st.button("✅ Apply Missing Value Strategy"):
        num_cols = df.select_dtypes(include="number").columns
        cat_cols = df.select_dtypes(exclude="number").columns

        if strategy == "Mean":
            df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
        elif strategy == "Median":
            df[num_cols] = df[num_cols].fillna(df[num_cols].median())
        elif strategy == "Mode":
            df[num_cols] = df[num_cols].fillna(df[num_cols].mode().iloc[0])
        elif strategy == "Drop rows with nulls":
            df = df.dropna(subset=num_cols)

        if cat_strategy == "Mode":
            df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0] if not df[cat_cols].mode().empty else "Unknown")
        elif cat_strategy == "Fill with 'Unknown'":
            df[cat_cols] = df[cat_cols].fillna("Unknown")
        elif cat_strategy == "Drop rows with nulls":
            df = df.dropna(subset=cat_cols)

        st.success("✅ Missing values handled.")

st.divider()

# 3. Drop Columns 
st.markdown('<p class="section">3 · Drop Columns</p>', unsafe_allow_html=True)
cols_to_drop = st.multiselect("Select columns to remove", df.columns.tolist())
if st.button("🗑️ Drop Selected Columns", disabled=(len(cols_to_drop) == 0)):
    df = df.drop(columns=cols_to_drop)
    st.success(f"Dropped: {', '.join(cols_to_drop)}")

st.divider()

#4. Fix Dtypes 
st.markdown('<p class="section">4 · Convert Column Data Types</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    dtype_col = st.selectbox("Column", df.columns)
with col2:
    dtype_target = st.selectbox("Convert to", ["int", "float", "str", "category"])
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Convert"):
        try:
            df[dtype_col] = df[dtype_col].astype(dtype_target)
            st.success(f"Converted **{dtype_col}** → `{dtype_target}`")
        except Exception as e:
            st.error(f"Could not convert: {e}")

st.divider()

# Save & Preview 
st.session_state["df_clean"]      = df
st.session_state["df_normalized"] = df.copy()

st.markdown('<p class="section">✅ Cleaned Dataset Preview</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("Rows",           df.shape[0])
c2.metric("Columns",        df.shape[1])
c3.metric("Missing Values", int(df.isnull().sum().sum()))

st.dataframe(df.head(20), use_container_width=True)
st.download_button("⬇️ Download Cleaned CSV", df.to_csv(index=False), "cleaned_data.csv", "text/csv")
