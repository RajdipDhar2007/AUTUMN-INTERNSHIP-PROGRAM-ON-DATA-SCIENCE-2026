import streamlit as st

st.set_page_config(page_title="Travel Blog", page_icon="🌍", layout="wide")

# Coloured headers via markdown + HTML
st.markdown("""
<style>
    .header-europe  { color: #ff1493; font-size: 2rem; font-weight: 700; margin-bottom: 4px; }
    .header-asia    { color: #27ae60; font-size: 2rem; font-weight: 700; margin-bottom: 4px; }
    .header-tips    { color: #2980b9; font-size: 2rem; font-weight: 700; margin-bottom: 4px; }
    .subheader-text { color: #8e44ad; font-size: 1.3rem; font-weight: 600; margin-bottom: 2px; }
</style>
""", unsafe_allow_html=True)

# code for sidebar navigation and info
with st.sidebar:
    st.title("🗺️ Navigate")
    st.markdown("Jump to a section:")
    st.markdown("- 🟠 [Europe](#europe)")
    st.markdown("- 🟢 [Asia](#asia)")
    st.markdown("- 🔵 [Travel Tips](#travel-tips)")

    st.divider()

    st.subheader("About")
    st.markdown("A personal travel journal covering the best spots across continents.")

    st.divider()

    st.subheader("Stats")
    # layout for metrics
    col1, col2 = st.columns(2)
    col1.metric("Countries", "12")
    col2.metric("Cities", "28")

    st.divider()
    st.caption("© 2026 My Travel Blog")

# Main title
st.title("🌍 Travel Blog")
st.markdown("Welcome to my travel journal — a collection of places, stories, and memories from around the world.")

st.divider()

# Europe
st.markdown('<p class="header-europe">Europe</p>', unsafe_allow_html=True)

st.markdown('<p class="subheader-text">Paris, France</p>', unsafe_allow_html=True)
st.markdown("""
The city of lights never disappoints. From the **Eiffel Tower** to hidden *patisseries* in Le Marais,
Paris is a feast for the senses. Must-try: a warm croissant at dawn by the Seine.
""")

st.markdown('<p class="subheader-text">Santorini, Greece</p>', unsafe_allow_html=True)
st.markdown("""
Perched on volcanic cliffs, Santorini offers **breathtaking sunsets** and *whitewashed villages*.
The town of Oia is especially magical in the golden hour.
""")

st.divider()

# Asia
st.markdown('<p class="header-asia">Asia</p>', unsafe_allow_html=True)

st.markdown('<p class="subheader-text">Kyoto, Japan</p>', unsafe_allow_html=True)
st.markdown("""
Ancient temples, bamboo groves, and tea ceremonies — Kyoto is Japan's *cultural soul*.
Visit **Arashiyama** in autumn for a riot of red and orange foliage.
""")

st.markdown('<p class="subheader-text">Bali, Indonesia</p>', unsafe_allow_html=True)
st.markdown("""
Between rice terraces and ocean surf, Bali strikes a rare balance of **adventure and tranquility**.
Don't miss the sacred **Tanah Lot** temple at sunset.
""")

st.divider()

# Tips
st.markdown('<p class="header-tips">Travel Tips</p>', unsafe_allow_html=True)
st.markdown("""
- **Pack light** — you'll thank yourself later  
- Always carry *local currency* for small vendors  
- Learn a few phrases in the **local language**  
- Eat where the locals eat — skip the tourist menus  
""")