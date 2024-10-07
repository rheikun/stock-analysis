import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Fungsi untuk memuat model
def load_model(model_path):
    return joblib.load(model_path)

# Fungsi untuk membaca data dari CSV

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce')
    df.columns = df.columns.str.strip()  # Menghapus whitespace dari nama kolom
    
    # Format semua kolom numerik menjadi string dengan 3 angka di belakang koma
    cols_to_format = ['Terakhir', 'Pembukaan', 'Tertinggi', 'Terendah', 'Vol.', 'Perubahan%']
    df[cols_to_format] = df[cols_to_format].applymap(lambda x: f"{x:.3f}")

    return df

# Path ke file CSV yang telah dibersihkan
file_path = './saham_cleaned_formatted.csv'
all_data = load_data(file_path)

# Judul aplikasi
st.title("Analisis Saham dengan Model Regresi")

# Pemilihan saham
selected_stock = st.selectbox("Pilih Saham untuk dianalisis:", options=all_data['Code'].unique())

# Filter data berdasarkan saham yang dipilih
stock_data = all_data[all_data['Code'] == selected_stock]

# Tampilkan beberapa data terbaru
st.write("Data terbaru untuk:", selected_stock)
st.write(stock_data.head())

# Memuat model regresi
model = load_model('./linear_regression_model.pkl')

# Input fitur untuk prediksi (pastikan 4 fitur digunakan)
input_features = stock_data[['Pembukaan', 'Tertinggi', 'Terendah', 'Vol.']].astype(float).values
predictions = model.predict(input_features)

# Tambahkan kolom prediksi ke DataFrame
stock_data['Prediksi'] = predictions

# Slider untuk prediksi harga di masa depan
years = st.slider("Prediksi untuk berapa tahun ke depan?", 1, 10, 5)

# Asumsi pertumbuhan market cap dan volume per tahun
def predict_future_price(stock_data, years):
    future_data = stock_data.copy()
    future_data['Pembukaan'] = future_data['Pembukaan'].astype(float) * (1 + 0.05 * years)  # Asumsi kenaikan 5% per tahun
    future_data['Tertinggi'] = future_data['Tertinggi'].astype(float) * (1 + 0.05 * years)
    future_data['Terendah'] = future_data['Terendah'].astype(float) * (1 + 0.05 * years)
    future_data['Vol.'] = future_data['Vol.'].astype(float) * (1 + 0.02 * years)  # Asumsi kenaikan 2% per tahun
    
    # Melakukan prediksi dengan data yang disesuaikan
    future_input_features = future_data[['Pembukaan', 'Tertinggi', 'Terendah', 'Vol.']].astype(float).values
    future_predictions = model.predict(future_input_features)
    
    return future_predictions

# Membuat prediksi untuk beberapa tahun ke depan
future_predictions = predict_future_price(stock_data, years)

# Ambil prediksi pertama dari future_predictions_text untuk ringkasan
predictions_summary = f"Harga saham {selected_stock} dalam {years} tahun ke depan adalah {future_predictions[0]:.3f}"

# Tampilkan hasil dalam satu kalimat
st.write(predictions_summary)
