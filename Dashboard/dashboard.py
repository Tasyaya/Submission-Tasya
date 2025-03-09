import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Tren Penyewaan Sepeda", layout="wide")

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv('https://raw.githubusercontent.com/FatwaAlFajar/submission-main/refs/heads/main/data/day.csv')
    return day_df

# Membaca data
day_df = load_data()
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['year'] = day_df['dteday'].dt.year

# Sidebar untuk filter tahun terlebih dahulu
with st.sidebar:
    st.image("https://raw.githubusercontent.com/FatwaAlFajar/submission-main/main/Picture/rental%20sepeda.png", use_container_width=True)
    selected_year = st.selectbox("Pilih Tahun", options=sorted(day_df['year'].unique()))
    
    # Filter data berdasarkan tahun
    filtered_year_data = day_df[day_df['year'] == selected_year]
    
    # Pilihan musim setelah memilih tahun
    season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
    available_seasons = filtered_year_data['season'].unique()
    selected_season = st.selectbox("Pilih Musim", options=sorted(available_seasons), format_func=lambda x: season_mapping[x])
    
    # Pilihan bulan berdasarkan musim
    season_months = {
        1: [3, 4, 5],  # Musim Semi: Maret, April, Mei
        2: [6, 7, 8],  # Musim Panas: Juni, Juli, Agustus
        3: [9, 10, 11],  # Musim Gugur: September, Oktober, November
        4: [12, 1, 2]  # Musim Dingin: Desember, Januari, Februari
    }
    available_months = [m for m in season_months[selected_season] if m in filtered_year_data['dteday'].dt.month.unique()]
    month_names = {1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"}
    selected_month = st.selectbox("Pilih Bulan", options=sorted(available_months), format_func=lambda x: month_names[x])

# Filter data berdasarkan musim dan bulan
filtered_data = filtered_year_data[(filtered_year_data['season'] == selected_season) & (filtered_year_data['dteday'].dt.month == selected_month)]

# Judul Dashboard
st.title("📊 Dashboard Tren Penyewaan Sepeda")

# **Analisis Tren Penggunaan Sepeda per Bulan**
st.subheader(f"Tren Penggunaan Sepeda - {season_mapping[selected_season]} {selected_year}, {month_names[selected_month]}")
monthly_trend = filtered_data.groupby('dteday')['cnt'].mean()

fig, ax = plt.subplots()
sns.lineplot(x=monthly_trend.index, y=monthly_trend.values, marker='o', ax=ax)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Tren Penyewaan Sepeda per Hari dalam Bulan yang Dipilih")
st.pyplot(fig)

# **Perbedaan Penggunaan Sepeda antara Hari Kerja dan Hari Libur**
st.subheader(f"Perbedaan Penggunaan Sepeda antara Hari Kerja dan Hari Libur - {season_mapping[selected_season]} {selected_year}, {month_names[selected_month]}")
workday_usage = filtered_data.groupby('workingday')['cnt'].mean()

fig, ax = plt.subplots()
sns.barplot(x=['Hari Libur', 'Hari Kerja'], y=workday_usage.values, palette=['red', 'blue'], ax=ax)
ax.set_xlabel("Jenis Hari")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Perbandingan Penyewaan Sepeda")
st.pyplot(fig)

# **Kesimpulan Strategi Pemasaran**
if workday_usage[1] > workday_usage[0]:
    st.success("🚴‍♂️ Strategi: Fokus pemasaran pada hari kerja karena penyewaan lebih tinggi.")
else:
    st.success("🎉 Strategi: Fokus pemasaran pada akhir pekan karena penyewaan lebih tinggi.")