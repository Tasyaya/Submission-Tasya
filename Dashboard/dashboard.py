import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv('https://raw.githubusercontent.com/Tasyaya/Submission-Tasya/refs/heads/main/Data/day.csv')
    hour_df = pd.read_csv('https://raw.githubusercontent.com/Tasyaya/Submission-Tasya/refs/heads/main/Data/hour.csv')
    return day_df, hour_df

day_df, hour_df = load_data()
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Sidebar untuk filter rentang waktu
with st.sidebar:
    st.image("https://raw.github.com/Tasyaya/Submission-Tasya/blob/main/picture/sepeda.jpg", use_container_width=True)
    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

# 🎯 Filter data berdasarkan rentang waktu
filtered_data = day_df[(day_df['dteday'] >= pd.Timestamp(start_date)) & (day_df['dteday'] <= pd.Timestamp(end_date))]
filtered_hour = hour_df[(hour_df['dteday'] >= pd.Timestamp(start_date)) & (hour_df['dteday'] <= pd.Timestamp(end_date))]

# Judul Dashboard
st.title("📊 Dashboard Data Penyewaan Sepeda")

# ✅ Menampilkan data yang sudah difilter
st.write("### Data Harian (Setelah Difilter):")
st.dataframe(filtered_data.head())

st.write("### Data Per Jam:")
st.dataframe(filtered_hour.head())

# **Menampilkan Jam dan Tanggal dengan Penyewaan Terbanyak dan Tersedikit**
data_terbanyak = filtered_hour.loc[filtered_hour['cnt'].idxmax()]
jam_terbanyak = data_terbanyak['hr']
tanggal_terbanyak = data_terbanyak['dteday'].strftime('%d %B %Y')
jumlah_terbanyak = data_terbanyak['cnt']

data_tersedikit = filtered_hour.loc[filtered_hour['cnt'].idxmin()]
jam_tersedikit = data_tersedikit['hr']
tanggal_tersedikit = data_tersedikit['dteday'].strftime('%d %B %Y')
jumlah_tersedikit = data_tersedikit['cnt']

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="🚀 Penyewaan Terbanyak",
        value=f"{jumlah_terbanyak} penyewaan",
        delta=f"Jam ke-{jam_terbanyak} pada {tanggal_terbanyak} 🔼"
    )

with col2:
    st.metric(
        label="🐢 Penyewaan Tersedikit",
        value=f"{jumlah_tersedikit} penyewaan",
        delta=f"Jam ke-{jam_tersedikit} pada {tanggal_tersedikit} 🔽"
    )

# **Plot Rata-rata Penyewaan Sepeda Berdasarkan Musim**
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots()
    sns.barplot(x='season', y='cnt', data=filtered_data, estimator='mean', palette='coolwarm', ax=ax)
    ax.set_xticklabels(['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    st.pyplot(fig)

with col2:
    st.image("https://raw.githubusercontent.com/FatwaAlFajar/submission-main/main/Picture/493394_650-Photoroom.png", caption="Musim Penyewaan", use_container_width=True)

# **Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda**
st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots()
    sns.barplot(x='weathersit', y='cnt', data=filtered_data, estimator='mean', palette='Set2', ax=ax)
    ax.set_xticklabels(['Cerah', 'Berkabut', 'Hujan Ringan', 'Hujan Lebat'])
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    st.pyplot(fig)

with col2:
    st.image("https://raw.githubusercontent.com/FatwaAlFajar/submission-main/main/Picture/png-clipart-weather-forecasting-rain-meteorology-cloud-weather-cloud-weather-forecasting-Photoroom.png", caption="Cuaca dan Penyewaan", use_container_width=True)

# **Visualisasi Penyewaan Sepeda Per Jam**
st.subheader("Penyewaan Sepeda Per Jam")
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots()
    sns.lineplot(x='hr', y='cnt', data=filtered_hour, marker='o', ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

with col2:
    st.image("https://raw.githubusercontent.com/FatwaAlFajar/submission-main/main/Picture/pngtree-clock-vector-icon-png-image_3723571-Photoroom.png", caption="Jam Penyewaan", use_container_width=True)