import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Deteksi Tongkat Tunanetra", layout="wide")
st.title("👨‍🦯 Dashboard Deteksi Tongkat Tunanetra (GPS Nyata)")

# Koordinat acuan (misalnya Madiun)
base_lat = -7.6291
base_lng = 111.5235

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar - Controls
st.sidebar.header("⚙️ Kontrol")
auto_refresh = st.sidebar.checkbox("Auto Refresh (2 detik)", value=False)
if st.sidebar.button("Reset Data"):
    st.session_state.history = []

# Generate data untuk 1 titik GPS tanpa manipulasi
lat = base_lat  # Tidak ada manipulasi, hanya koordinat dasar
lng = base_lng  # Tidak ada manipulasi, hanya koordinat dasar
obstacle_detected = False  # Bisa disesuaikan jika diperlukan deteksi obstacle dari perangkat keras

# Menyimpan data posisi GPS dalam history
st.session_state.history.append({
    "lat": lat,
    "lng": lng,
    "obstacle": obstacle_detected
})

# Convert to DataFrame
df = pd.DataFrame(st.session_state.history)

# Rename 'lng' to 'lon' for st.map
df = df.rename(columns={"lng": "lon"})

# Sidebar - Filter obstacle
show_obstacle_only = st.sidebar.checkbox("Tampilkan Hanya Obstacle", value=False)
if show_obstacle_only:
    df_display = df[df["obstacle"] == True]
else:
    df_display = df

# Tampilkan data
st.subheader("📋 Data Deteksi")
st.dataframe(df_display)

# Tampilkan peta
if not df_display.empty:
    st.subheader("🗺️ Peta Deteksi")
    st.map(df_display[["lat", "lon"]])
else:
    st.warning("Tidak ada data yang ditampilkan!")

# Ringkasan obstacle
n_obstacles = df["obstacle"].sum()
st.info(f"🚧 Jumlah obstacle terdeteksi: {n_obstacles}")

# Line chart
if len(df) > 1:
    st.subheader("📈 Pergerakan Latitude / Longitude")
    st.line_chart(df[["lat", "lon"]])

# Auto-refresh
if auto_refresh:
    time.sleep(2)
    st.experimental_rerun()
