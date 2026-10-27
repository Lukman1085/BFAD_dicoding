# Proyek Analisis Data: E-Commerce Public Dataset

Proyek ini merupakan submission akhir untuk kelas **Belajar Fundamental Analisis Data** di Dicoding. Fokus utama proyek ini adalah menganalisis data transaksi e-commerce (Olist) guna mengidentifikasi waktu puncak transaksi dan melakukan segmentasi pelanggan di wilayah São Paulo menggunakan metode RFM (Recency, Frequency, Monetary) serta analisis Geospasial.

## Deskripsi Berkas

### 1. Berkas Utama
- **`notebook.ipynb`**: Berkas Jupyter Notebook yang berisi seluruh tahapan analisis data end-to-end, mulai dari Data Wrangling (Gathering, Assessing, Cleaning), Exploratory Data Analysis (EDA), hingga Visualisasi, implementasi RFM Analysis, dan analisis Geospasial.
- **`requirements.txt`**: Berkas yang berisi daftar library Python beserta versinya yang dibutuhkan untuk menjalankan proyek ini (seperti pandas, matplotlib, seaborn, dan streamlit).
- **`url.txt`**: Berkas teks sederhana yang berisi tautan publik aplikasi dashboard Streamlit yang telah di-deploy ke cloud.
- **`README.md`**: Berkas dokumentasi ini yang memberikan panduan dan informasi umum mengenai proyek.

### 2. Direktori `dashboard/`
- **`dashboard.py`**: Skrip Python utama yang menggunakan library Streamlit untuk membangun dan merender antarmuka pengguna (UI) dashboard interaktif.
- **`main_data.csv`**: Dataset hasil pembersihan dan penggabungan (merge) dari Jupyter Notebook yang siap digunakan oleh dashboard agar proses muat data lebih cepat.

### 3. Direktori `data/` (E-Commerce Public Dataset)
Direktori ini berisi kumpulan raw data (data mentah) dalam format CSV:
- **`customers_dataset.csv`**: Berisi informasi demografi pelanggan seperti ID pelanggan unik, kode pos, kota, dan negara bagian (state).
- **`geolocation_dataset.csv`**: Berisi informasi pemetaan geografis berupa koordinat latitude dan longitude berdasarkan awalan kode pos wilayah di Brasil.
- **`order_items_dataset.csv`**: Berisi detail item dari setiap pesanan, mencakup ID produk, ID penjual, batas waktu pengiriman, harga barang, dan ongkos kirim.
- **`order_payments_dataset.csv`**: Berisi riwayat transaksi pembayaran pesanan, mencakup tipe pembayaran (kartu kredit, dll.), jumlah cicilan, dan total nilai yang dibayarkan.
- **`order_reviews_dataset.csv`**: Berisi data ulasan pelanggan terhadap pesanan mereka, mencakup skor (1-5), judul ulasan, pesan ulasan, dan tanggal ulasan dibuat.
- **`orders_dataset.csv`**: Berisi informasi inti dari setiap transaksi, mencakup status pesanan (delivered, canceled, dll.) serta berbagai rekaman waktu (waktu pembelian, persetujuan, pengiriman kurir, hingga diterima pelanggan).
- **`products_dataset.csv`**: Berisi metadata katalog produk seperti kategori produk, panjang nama, panjang deskripsi, jumlah foto, berat, dan dimensi produk.
- **`sellers_dataset.csv`**: Berisi informasi demografi penjual yang bermitra dengan e-commerce, mencakup ID penjual, kode pos, kota, dan negara bagian asal.
- **`product_category_name_translation.csv`**: Tabel kamus sederhana untuk menerjemahkan nama kategori produk dari bahasa Portugis ke bahasa Inggris.

## Setup Environment

### Menggunakan Built-in Python venv
```bash
python -m venv .venv
.venv\Scripts\activate      # Untuk Windows
source .venv/bin/activate   # Untuk Mac/Linux
pip install -r requirements.txt
```

### Menggunakan Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Run Dashboard
streamlit run dashboard/dashboard.py