import streamlit as st

st.set_page_config(
    page_title="Sri Lanka Climate Explorer",
    page_icon="🌦️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 700;
    background: -webkit-linear-gradient(45deg, #56CCF2, #2F80ED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}

.hero-sub {
    color: #A0AEC0;
    font-size: 1.15rem;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

.hero-banner {
    background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    gap: 30px;
}

.banner-emoji {
    font-size: 6rem;
    line-height: 1;
}

.card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 28px 20px;
    text-align: center;
    height: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.card-icon {
    font-size: 2.8rem;
    margin-bottom: 12px;
}

.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #E2E8F0;
    margin-bottom: 8px;
}

.card-desc {
    font-size: 0.88rem;
    color: #A0AEC0;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<div class="hero-banner">
    <div class="banner-emoji">🌦️</div>
    <div>
        <div class="hero-title">Sri Lankan Climate Explorer</div>
        <div class="hero-sub">
            Explore weather patterns, predict apparent temperature,<br>
            and discover climate zones across 30 Sri Lankan cities.
        </div>
        <strong style="color:#E2E8F0;">👈 Use the sidebar to navigate between pages.</strong>
    </div>
</div>
""", unsafe_allow_html=True)

##Cards

st.markdown("### What can you do here?")
st.markdown('<div style="margin-top: 16px;"></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📊</div>
        <div class="card-title">Data Explorer</div>
        <div class="card-desc">Select a city and year to explore temperature and rainfall trends with summary statistics.</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🌡️</div>
        <div class="card-title">Apparent Temp Predictor</div>
        <div class="card-desc">Predict how hot it actually feels using a Random Forest model trained on Sri Lankan weather data.</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🗺️</div>
        <div class="card-title">City Clustering</div>
        <div class="card-desc">Discover which climate zone your city belongs to using K-Means clustering.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ----------------------------------------------------------
# DATASET QUICK STATS
# ----------------------------------------------------------

import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("data/SriLanka_Weather_Dataset_V1.csv")

df = load_data()

st.markdown("### Dataset at a Glance")
s1, s2, s3, s4 = st.columns(4)
s1.metric("Total Records", f"{len(df):,}")
s2.metric("Cities Covered", f"{df['city'].nunique()}")
s3.metric("Years of Data", f"{pd.to_datetime(df['time']).dt.year.nunique()}")
s4.metric("Weather Variables", "14")

st.markdown("---")
