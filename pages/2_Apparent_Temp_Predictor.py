import streamlit as st
import pandas as pd
import numpy as np
import joblib


# Load data and model
@st.cache_data
def load_data():
    df = pd.read_csv("data/SriLanka_Weather_Dataset_V1.csv")
    return df

@st.cache_resource
def load_model():
    return joblib.load("models/rf_model.pkl")

df = load_data()
model = load_model()

#elevation lookup
elevation_lookup = df.groupby("city")["elevation"].first().to_dict()

# Get min/max from dataset for slider ranges
temp_min, temp_max = float(df["temperature_2m_mean"].min()), float(df["temperature_2m_mean"].max())
wind_min, wind_max = float(df["windspeed_10m_max"].min()), float(df["windspeed_10m_max"].max())
solar_min, solar_max = float(df["shortwave_radiation_sum"].min()), float(df["shortwave_radiation_sum"].max())
et0_min, et0_max = float(df["et0_fao_evapotranspiration"].min()), float(df["et0_fao_evapotranspiration"].max())

#average values for defaults
temp_default = float(df["temperature_2m_mean"].mean())
wind_default = float(df["windspeed_10m_max"].mean())
solar_default = float(df["shortwave_radiation_sum"].mean())
et0_default = float(df["et0_fao_evapotranspiration"].mean())


st.title("🌡️ Apparent Temperature Predictor")
st.markdown("""
**Apparent temperature** is how hot or cold it actually feels to the human body.
Use the controls below to predict it for any city and weather condition.
""")

st.markdown("---")


#Input Features
st.subheader("Input Weather Conditions")

col1, col2 = st.columns(2)

with col1:
    cities = sorted(df["city"].unique())
    selected_city = st.selectbox("Select City", cities)
    elevation = elevation_lookup[selected_city]
    st.info(f"📍 Elevation of {selected_city}: **{elevation} m**")

    temperature = st.slider(
        "Mean Temperature (°C)",
        min_value=temp_min,
        max_value=temp_max,
        value=temp_default,
        step=0.5
    )

    wind_speed = st.slider(
        "Max Wind Speed (km/h)",
        min_value=wind_min,
        max_value=wind_max,
        value=wind_default,
        step=0.5
    )

with col2:
    solar_radiation = st.slider(
        "Solar Radiation (MJ/m²)",
        min_value=solar_min,
        max_value=solar_max,
        value=solar_default,
        step=0.5
    )

    et0 = st.slider(
        "Evapotranspiration — ET₀ (mm)",
        min_value=et0_min,
        max_value=et0_max,
        value=et0_default,
        step=0.1
    )


#Predictions
st.markdown("---")

input_data = pd.DataFrame([{
    "temperature_2m_mean": temperature,
    "windspeed_10m_max": wind_speed,
    "shortwave_radiation_sum": solar_radiation,
    "elevation": elevation,
    "et0_fao_evapotranspiration": et0
}])

prediction = model.predict(input_data)[0]
diff = prediction - temperature

st.subheader("Prediction Result")

col3, col4, col5 = st.columns(3)

col3.metric("Actual Temperature", f"{temperature:.1f} °C")
col4.metric("Apparent Temperature", f"{prediction:.1f} °C")
col5.metric(
    "Feels Like Difference",
    f"{diff:+.1f} °C",
    delta_color="inverse" if diff < 0 else "normal"
)

# Interpretation

st.markdown("---")
st.subheader("Interpretation")

if diff > 1.5:
    st.warning(f"It feels **hotter** than the actual temperature by {diff:.1f}°C.")
elif diff < -1.5:
    st.info(f"It feels **cooler** than the actual temperature by {abs(diff):.1f}°C.")
else:
    st.success("The apparent temperature is close to the actual temperature.")