# Proyek Analisis Data: E-Commerce Public Dataset

Proyek ini menganalisis E-Commerce Public Dataset (Olist) untuk menjawab dua pertanyaan bisnis, lalu menyajikan hasilnya dalam dashboard interaktif menggunakan Streamlit.

- **Nama:** [isi nama]
- **Email:** [isi email]
- **ID Dicoding:** [isi username]

## Pertanyaan Bisnis

1. Kategori produk apa saja yang menyumbang total revenue tertinggi (top 10) dan terendah (bottom 5) selama periode Januari 2017 – Agustus 2018, dan berapa persen kontribusi 5 kategori teratas terhadap total revenue?
2. Seberapa besar pengaruh keterlambatan pengiriman terhadap rata-rata review score pelanggan, dan di 10 state mana persentase pesanan terlambat paling tinggi selama periode Januari 2017 – Agustus 2018?

## Ringkasan Hasil

- Lima kategori teratas (health_beauty, watches_gifts, bed_bath_table, sports_leisure, computers_accessories) menyumbang 39,88% total revenue.
- Pesanan yang terlambat memiliki rata-rata review score 2,27, jauh di bawah pesanan tepat waktu yang mencapai 4,29.
- State dengan persentase keterlambatan tertinggi: AL (20,87%), MA (17,21%), dan SE (15,11%).
- 18 dari 74 kategori menyumbang 81,29% revenue dan pesanan terlambat (>7 hari) mendapat review rata-rata sekitar 1,7.

Detail analisis, insight, dan rekomendasi action item ada di notebook `Proyek_Analisis_Data.ipynb`.

## Struktur Proyek

```
proyek-analisis-data/
├── dashboard/
│   ├── dashboard.py          # aplikasi Streamlit
│   ├── sales_main.csv        # data hasil cleaning untuk pertanyaan 1
│   ├── delivery_main.csv     # data hasil cleaning untuk pertanyaan 2
│   └── requirements.txt      # daftar library
├── data/                     # dataset mentah (CSV Olist)
├── Proyek_Analisis_Data.ipynb
└── README.md
```

## Dataset

Dataset yang digunakan adalah **E-Commerce Public Dataset** (Brazilian E-Commerce Public Dataset by Olist) yang disediakan pada kriteria submission. Tabel yang dipakai: `customers`, `orders`, `order_items`, `order_reviews`, `products`, dan `product_category_name_translation`.

Data hasil cleaning yang dibaca dashboard (`sales_main.csv` dan `delivery_main.csv`) dihasilkan dari notebook.

## Menjalankan Dashboard

### 1. Siapkan environment (opsional, disarankan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 2. Install library

```bash
pip install -r dashboard/requirements.txt
```

### 3. Jalankan Streamlit

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`. Jika perintah `streamlit` tidak dikenali, gunakan:

```bash
python -m streamlit run dashboard/dashboard.py
```

## Fitur Dashboard

- Filter rentang tanggal pembelian, jumlah kategori teratas, dan minimum pesanan per state.
- Ringkasan metrik: total revenue, total pesanan, rata-rata review score, dan persentase pesanan terlambat.
- Visualisasi revenue per kategori produk (top dan bottom).
- Visualisasi pengaruh keterlambatan terhadap review score, state dengan keterlambatan tertinggi, dan analisis lanjutan berdasarkan lama keterlambatan.

## Menjalankan Notebook

Notebook dapat dijalankan di Google Colab atau di lokal (VSCode/Jupyter). Sesuaikan variabel `DATA_DIR` pada bagian Gathering Data dengan lokasi folder dataset mentah, misalnya `"data/"`.

## Library yang Digunakan

`pandas`, `numpy`, `matplotlib`, `seaborn`, `streamlit`