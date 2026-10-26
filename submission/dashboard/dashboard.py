import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Menyiapkan fungsi helper untuk membuat dataframe RFM
def create_rfm_df(df):
    sp_data = df[(df['customer_city'] == 'sao paulo') & (df['order_status'] == 'delivered')]
    
    if sp_data.empty:
        return pd.DataFrame(columns=['customer_unique_id', 'recency', 'frequency', 'monetary', 'segment'])
        
    recent_date = sp_data['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    
    rfm = sp_data.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (recent_date - x.max()).days,
        'order_id': 'nunique',
        'payment_value': 'sum'
    }).reset_index()
    
    rfm.rename(columns={
        'order_purchase_timestamp': 'recency', 
        'order_id': 'frequency', 
        'payment_value': 'monetary'
    }, inplace=True)
    
    # Menghitung skor RFM dengan 'duplicates=drop' untuk menghindari error saat data sedikit
    rfm['r_score'] = pd.qcut(rfm['recency'], 3, labels=[3, 2, 1], duplicates='drop')
    rfm['f_score'] = rfm['frequency'].apply(lambda x: 3 if x > 2 else (2 if x == 2 else 1))
    rfm['m_score'] = pd.qcut(rfm['monetary'], 3, labels=[1, 2, 3], duplicates='drop')
    
    def segment_customer(row):
        if row['r_score'] == 3 and row['f_score'] >= 2 and row['m_score'] == 3:
            return 'VIP / Champions'
        elif row['f_score'] >= 2:
            return 'Loyal Customers'
        elif row['r_score'] >= 2 and row['m_score'] == 3:
            return 'Potential Loyalists (High Spend)'
        elif row['r_score'] == 1 and row['f_score'] == 1:
            return 'At Risk / Hibernating'
        else:
            return 'Regular Customers'
            
    rfm['segment'] = rfm.apply(segment_customer, axis=1)
    return rfm

# Load data dengan st.cache_data agar lebih cepat
@st.cache_data
def load_data():
    # Mengambil direktori tempat dashboard.py berada
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Menggabungkan direktori tersebut dengan nama file CSV
    csv_path = os.path.join(current_dir, "main_data.csv")
    
    df = pd.read_csv(csv_path)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

all_df = load_data()

# Membuat komponen Sidebar
with st.sidebar:
    st.title("🛍️ E-Commerce Dashboard")
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mendapatkan tanggal minimum dan maksimum
    min_date = all_df["order_purchase_timestamp"].min().date()
    max_date = all_df["order_purchase_timestamp"].max().date()
    
    # Filter rentang waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan input sidebar
main_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                 (all_df["order_purchase_timestamp"].dt.date <= end_date)]

# Judul Utama Dashboard
st.header('Analisis E-Commerce Public Dataset')

# --- SECTION 1: Peta Panas Waktu Transaksi ---
st.subheader('Waktu Transaksi Tertinggi')
time_df = main_df[main_df['order_status'] == 'delivered'].copy()

if not time_df.empty:
    time_df['day_of_week'] = time_df['order_purchase_timestamp'].dt.day_name()
    time_df['hour'] = time_df['order_purchase_timestamp'].dt.hour
    
    heatmap_data = time_df.groupby(['day_of_week', 'hour']).size().unstack(fill_value=0)
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(days_order).fillna(0)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(heatmap_data, cmap='YlGnBu', ax=ax)
    ax.set_xlabel('Jam Transaksi')
    ax.set_ylabel('Hari')
    st.pyplot(fig)
else:
    st.info("Tidak ada data transaksi yang 'delivered' pada rentang waktu ini.")

# --- SECTION 2: Segmentasi Pelanggan RFM ---
st.subheader("Segmentasi RFM Pelanggan (Khusus São Paulo)")
rfm_df = create_rfm_df(main_df)

if not rfm_df.empty:
    segment_counts = rfm_df['segment'].value_counts().reset_index()
    segment_counts.columns = ['segment', 'count']
    
    # Menampilkan metrik sederhana
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pelanggan", rfm_df.shape[0])
    with col2:
        potential = segment_counts[segment_counts['segment'] == 'Potential Loyalists (High Spend)']['count']
        st.metric("Potential Loyalists", potential.values[0] if not potential.empty else 0)
    with col3:
        vip = segment_counts[segment_counts['segment'] == 'VIP / Champions']['count']
        st.metric("VIP / Champions", vip.values[0] if not vip.empty else 0)

    # Bar chart segmentasi
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(x='count', y='segment', data=segment_counts, palette='mako', ax=ax2)
    ax2.set_xlabel('Jumlah Pelanggan')
    ax2.set_ylabel('Segmen')
    st.pyplot(fig2)
else:
    st.info("Tidak ada data pelanggan dari São Paulo pada rentang waktu ini.")

# --- SECTION 3: Distribusi Geografis (Analisis Lanjutan) ---
st.subheader("Distribusi Pelanggan Berdasarkan Negara Bagian")
state_counts = main_df['customer_state'].value_counts().reset_index()
state_counts.columns = ['state', 'count']

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(x='state', y='count', data=state_counts, palette='viridis', ax=ax3)
ax3.set_xlabel('Negara Bagian (State)')
ax3.set_ylabel('Jumlah Pelanggan')
st.pyplot(fig3)

st.caption("Dicoding Data Analytics Final Project")