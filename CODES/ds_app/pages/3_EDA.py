import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .page-title { color: #e74c3c; font-size: 2rem; font-weight: 800; }
    .section    { color: #e67e22; font-size: 1.4rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📊 EDA")
    st.markdown("Explore distributions, correlations, and relationships in your cleaned data.")
    st.markdown("---")
    st.caption("DS Toolkit · Page 3 of 5")

st.markdown('<p class="page-title">📊 Exploratory Data Analysis</p>', unsafe_allow_html=True)
st.markdown("Visualise and understand patterns in your dataset.")
st.divider()

if "df_clean" not in st.session_state:
    st.warning("⚠️ No data found. Please complete **Page 1 → Upload** first.")
    st.stop()

df = st.session_state["df_clean"]
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

# 1. Distribution
st.markdown('<p class="section">1 · Distribution of Numeric Columns</p>', unsafe_allow_html=True)

if num_cols:
    col1, col2 = st.columns([1, 3])
    with col1:
        dist_col  = st.selectbox("Column", num_cols, key="dist_col")
        plot_type = st.radio("Plot type", ["Histogram", "Box Plot", "KDE"], key="dist_type")
        bins      = st.slider("Bins (histogram)", 5, 100, 20) if plot_type == "Histogram" else None
    with col2:
        fig, ax = plt.subplots(figsize=(8, 4))
        if plot_type == "Histogram":
            ax.hist(df[dist_col].dropna(), bins=bins, color="#2980b9", edgecolor="white", alpha=0.85)
            ax.set_title(f"Histogram — {dist_col}")
        elif plot_type == "Box Plot":
            ax.boxplot(df[dist_col].dropna(), vert=False, patch_artist=True,
                       boxprops=dict(facecolor="#2980b9", color="#1a5276"),
                       medianprops=dict(color="white", linewidth=2))
            ax.set_title(f"Box Plot — {dist_col}")
        else:
            df[dist_col].dropna().plot(kind="kde", ax=ax, color="#e74c3c", linewidth=2)
            ax.set_title(f"KDE — {dist_col}")
        ax.set_xlabel(dist_col)
        st.pyplot(fig)
        plt.close()
else:
    st.info("No numeric columns available.")

st.divider()

# 2. Categorical Value Counts 
st.markdown('<p class="section">2 · Categorical Column Value Counts</p>', unsafe_allow_html=True)

if cat_cols:
    col1, col2 = st.columns([1, 3])
    with col1:
        cat_col   = st.selectbox("Column", cat_cols, key="cat_col")
        top_n     = st.slider("Top N categories", 3, 20, 10)
        bar_color = st.color_picker("Bar colour", "#27ae60")
    with col2:
        vc = df[cat_col].value_counts().head(top_n)
        fig, ax = plt.subplots(figsize=(8, 4))
        vc.plot(kind="bar", ax=ax, color=bar_color, edgecolor="white")
        ax.set_title(f"Top {top_n} — {cat_col}")
        ax.set_xlabel(cat_col)
        ax.set_ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)
        plt.close()
else:
    st.info("No categorical columns found.")

st.divider()

# 3. Correlation Heatmap 
st.markdown('<p class="section">3 · Correlation Heatmap</p>', unsafe_allow_html=True)

if len(num_cols) >= 2:
    selected_num = st.multiselect("Select columns for heatmap", num_cols, default=num_cols[:min(8, len(num_cols))])
    if len(selected_num) >= 2:
        fig, ax = plt.subplots(figsize=(max(6, len(selected_num)), max(4, len(selected_num) - 1)))
        corr = df[selected_num].corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
                    linewidths=0.5, square=True, cbar_kws={"shrink": 0.8})
        ax.set_title("Correlation Matrix")
        st.pyplot(fig)
        plt.close()
    else:
        st.info("Select at least 2 columns.")
else:
    st.info("Need at least 2 numeric columns for a heatmap.")

st.divider()

# 4. Scatter Plot
st.markdown('<p class="section">4 · Scatter Plot</p>', unsafe_allow_html=True)

if len(num_cols) >= 2:
    col1, col2, col3 = st.columns(3)
    with col1:
        x_col = st.selectbox("X axis", num_cols, key="sc_x")
    with col2:
        y_col = st.selectbox("Y axis", num_cols, index=min(1, len(num_cols)-1), key="sc_y")
    with col3:
        hue_col = st.selectbox("Colour by (optional)", ["None"] + cat_cols, key="sc_hue")

    fig, ax = plt.subplots(figsize=(8, 5))
    if hue_col != "None":
        categories = df[hue_col].unique()
        palette = sns.color_palette("tab10", len(categories))
        for i, cat in enumerate(categories):
            subset = df[df[hue_col] == cat]
            ax.scatter(subset[x_col], subset[y_col], label=str(cat), color=palette[i], alpha=0.7, s=40)
        ax.legend(title=hue_col, bbox_to_anchor=(1, 1))
    else:
        ax.scatter(df[x_col], df[y_col], color="#8e44ad", alpha=0.6, s=40)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(f"{x_col} vs {y_col}")
    st.pyplot(fig)
    plt.close()

st.divider()

# 5. Missing Value Heatmap
st.markdown('<p class="section">5 · Missing Values Map</p>', unsafe_allow_html=True)

missing_total = df.isnull().sum().sum()
if missing_total > 0:
    fig, ax = plt.subplots(figsize=(min(16, df.shape[1]), 4))
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap="viridis", ax=ax)
    ax.set_title("Missing Values (yellow = missing)")
    st.pyplot(fig)
    plt.close()
else:
    st.success("✅ No missing values — nothing to map.")
