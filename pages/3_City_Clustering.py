import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
import plotly.express as px


#Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/SriLanka_Weather_Dataset_V1.csv")
    df["time"] = pd.to_datetime(df["time"])
    df["month"] = df["time"].dt.month
    df["year"] = df["time"].dt.year
    return df

@st.cache_data
def build_city_profiles(df):
    features = [
        "temperature_2m_mean",
        "rain_sum",
        "windspeed_10m_max",
        "et0_fao_evapotranspiration",
        "shortwave_radiation_sum"
    ]

    city_profiles = df.groupby("city")[features].mean().reset_index()

    elevation_lookup = df.groupby("city")["elevation"].first().reset_index()
    city_profiles = city_profiles.merge(elevation_lookup, on="city")

    coords = df.groupby("city")[["latitude", "longitude"]].first().reset_index()
    city_profiles = city_profiles.merge(coords, on="city")

    return city_profiles

@st.cache_data
def run_kmeans(city_profiles, k):
    features = [
        "temperature_2m_mean",
        "rain_sum",
        "windspeed_10m_max",
        "et0_fao_evapotranspiration",
        "shortwave_radiation_sum",
        "elevation"
    ]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(city_profiles[features])

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    return labels, X_scaled

df = load_data()
city_profiles = build_city_profiles(df)


# Clustering-kmeans

k = 4
labels, X_scaled = run_kmeans(city_profiles, k)
city_profiles["cluster"] = labels

cluster_names_k4 = {
    0: "Cool Highland Climate",
    1: "Warm Wet Lowland Climate",
    2: "Hot Dry Climate",
    3: "Coastal Humid Climate"
}

city_profiles["cluster_name"] = city_profiles["cluster"].map(cluster_names_k4)


## Title
st.title("🗺️Climate Zone Clustering")
st.caption("Explore climate zones across Sri Lanka using K-Means clustering")

#Sidebar
cluster_options = sorted(city_profiles["cluster_name"].unique())
selected_cluster = st.sidebar.selectbox("Select Climate Zone", cluster_options)


cluster_df = city_profiles[city_profiles["cluster_name"] == selected_cluster]
cluster_id = cluster_df["cluster"].iloc[0]
cities_in_cluster = cluster_df["city"].tolist()



st.markdown(f"## {selected_cluster}")

st.info("""
Cities in this cluster share similar characteristics.
""")

st.write("**Cities:**", ", ".join(cities_in_cluster))

#Summary Statistics
cluster_full_df = df[df["city"].isin(cities_in_cluster)]

st.subheader("Cluster Summary")

col1, col2, col3 = st.columns(3)

# Avg Temp
col1.metric(
    "Avg. Temparature",
    f"{cluster_full_df['temperature_2m_mean'].mean():.1f}°C"
)

#Avg annual rain(2023 is discarded since it only has observations of first 6 months.)
filtered_df = cluster_full_df[cluster_full_df["year"] != 2023]

yearly_rain = (
    filtered_df
    .groupby(["city", "year"])["rain_sum"]
    .sum()
    .reset_index()
)
avg_annual_rain = yearly_rain.groupby("city")["rain_sum"].mean().mean()


col2.metric(
    "Avg. Annual Rain",
    f"{avg_annual_rain:.0f} mm"
)

# Avg Wind
col3.metric(
    "Avg. Wind Speed",
    f"{cluster_full_df['windspeed_10m_max'].mean():.1f} km/h"
)

st.caption("Average total rainfall per year (excluding incomplete year 2023).")


#map
st.subheader("Cluster Map")

m = folium.Map(location=[7.8, 80.7], zoom_start=7)

for _, row in city_profiles.iterrows():
    if row["cluster"] == cluster_id:
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=8,
            color="#FF6B6B",
            fill=True,
            fill_color="#FF6B6B",
            fill_opacity=0.9,
            popup=row["city"]
        ).add_to(m)
    else:
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            color="gray",
            fill=True,
            fill_color="gray",
            fill_opacity=0.4
        ).add_to(m)

st_folium(m, width=700)

st.markdown("---")

##PCA

st.subheader("Cluster Separation (PCA)")

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

city_profiles["PC1"] = X_pca[:, 0]
city_profiles["PC2"] = X_pca[:, 1]

fig_pca = px.scatter(
    city_profiles,
    x="PC1",
    y="PC2",
    color="cluster_name",
    hover_name="city"
)

fig_pca.update_traces(marker=dict(size=10, opacity=0.8))

st.plotly_chart(fig_pca, use_container_width=True)
