import streamlit as st
import pandas as pd
import plotly.express as px


#Lod Data

@st.cache_data
def load_data():
    df = pd.read_csv("data/SriLanka_Weather_Dataset_V1.csv")
    df["time"] = pd.to_datetime(df["time"])
    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    return df

df = load_data()


#Header
st.title("📊 Data Explorer")
st.markdown("Explore temperature and rainfall trends for any city and year.")


#Sidebar
st.sidebar.header("Filters")

cities = sorted(df["city"].unique())
selected_city = st.sidebar.selectbox("Select City", cities)

years = sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

#Filter Data
filtered = df[
    (df["city"] == selected_city) &
    (df["year"] == selected_year)
].copy()

if filtered.empty:
    st.warning("No data found for this selection.")
    st.stop()

##Summary Statistics
st.subheader(f"Summary Statistics — {selected_city}, {selected_year}")

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# Row 1
row1_col1.metric("Avg. Temp", f"{filtered['temperature_2m_mean'].mean():.1f}°C")
row1_col2.metric("Total Rain", f"{filtered['rain_sum'].sum():.1f} mm")

# Row 2
row2_col1.metric("Avg. Wind Speed", f"{filtered['windspeed_10m_max'].mean():.1f} km/h")
row2_col2.metric("Avg. Solar Radiation", f"{filtered['shortwave_radiation_sum'].mean():.1f} MJ/m²")

st.markdown("---")


## Temparature Trend
st.subheader("Temperature Trend")


fig_temp = px.line(
    filtered,
    x="time",
    y="temperature_2m_mean",
    title=f"Daily Mean Temperature — {selected_city} ({selected_year})",
    labels={"time": "Date", "temperature_2m_mean": "Temperature (°C)"},
    color_discrete_sequence=["#e74c3c"]
)
fig_temp.update_traces(line_width=1.5)
fig_temp.update_layout(hovermode="x unified")
st.plotly_chart(fig_temp, use_container_width=True)

st.caption("""
Each point is the daily average temperature. 
Peaks indicate hotter periods.
""")

st.markdown("---")

#Precipitation Trend
st.subheader("Rainfall Trend")


fig_rain = px.bar(
    filtered,
    x="time",
    y="rain_sum",
    title=f"Daily Rainfall — {selected_city} ({selected_year})",
    labels={"time": "Date", "rain_sum": "Rainfall (mm)"},
    color_discrete_sequence=["#2980b9"]
)
fig_rain.update_layout(hovermode="x unified")
st.plotly_chart(fig_rain, use_container_width=True)

st.caption("""
Each bar shows the total rainfall for that day. 
Tall bars indicate heavy rain events, typically during monsoon seasons.
""")

st.markdown("---")

##Monthly Summary for selected city.
st.subheader("Monthly Summary (Overall)")


months_dict = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

selected_month_name = st.selectbox(
    "Select Month",
    ["Select a month..."] + list(months_dict.values())
)

if selected_month_name != "Select a month...":
    month_num = [k for k, v in months_dict.items() if v == selected_month_name][0]

    month_df = df[
        (df["city"] == selected_city) &
        (df["month"] == month_num)
    ]

    if not month_df.empty:
        avg_temp = month_df["temperature_2m_mean"].mean()
        monthly_totals = month_df.groupby("year")["rain_sum"].sum()
        avg_monthly_rain = monthly_totals.mean()
        if avg_monthly_rain < 50:
            rain_label = "Low Rainfall"
        elif avg_monthly_rain < 150:
            rain_label = "Moderate Rainfall"
        elif avg_monthly_rain < 300:
            rain_label = "High Rainfall"
        else:
            rain_label = "Very Heavy Rainfall"
        avg_wind = month_df["windspeed_10m_max"].mean()



        col1, col2, col3 = st.columns(3)

        col1.metric("Average Temparature", f"{avg_temp:.1f}°C")
        col2.metric("Average Rain", f"{avg_monthly_rain:.1f} mm")
        col3.metric("Average Wind", f"{avg_wind:.1f} km/h")
        st.info(f"Rainfall Level: **{rain_label}**")
      

st.markdown("---")

# Full data table
with st.expander("🔍 View Raw Data"):
    display_cols = [
        "time", "temperature_2m_mean", "rain_sum",
        "windspeed_10m_max", "shortwave_radiation_sum",
        "et0_fao_evapotranspiration"
    ]
    st.dataframe(filtered[display_cols].reset_index(drop=True))


