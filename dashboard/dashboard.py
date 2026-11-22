from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Dashboard E-Commerce", page_icon="🛒", layout="wide")

BASE_DIR = Path(__file__).parent
BLUE, RED = "#2E86AB", "#E4572E"


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    sales = pd.read_csv(BASE_DIR / "sales_main.csv", parse_dates=["order_purchase_timestamp"])
    delivery = pd.read_csv(BASE_DIR / "delivery_main.csv", parse_dates=["order_purchase_timestamp"])

    delivery["is_late"] = delivery["delay_days"] > 0
    delivery["delay_group"] = pd.cut(
        delivery["delay_days"],
        bins=[-np.inf, 0, 3, 7, np.inf],
        labels=["Tepat waktu", "Telat 1-3 hari", "Telat 4-7 hari", "Telat >7 hari"],
    )
    return sales, delivery


sales_df, delivery_df = load_data()

# ---------------------------------------------------------------------------
# Sidebar (filter)
# ---------------------------------------------------------------------------
st.sidebar.header("Filter")

min_date = sales_df["order_purchase_timestamp"].min().date()
max_date = sales_df["order_purchase_timestamp"].max().date()

date_range = st.sidebar.date_input(
    "Rentang tanggal pembelian",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if len(date_range) != 2:
    st.info("Pilih tanggal awal dan tanggal akhir dulu ya.")
    st.stop()
start_date, end_date = date_range

top_n = st.sidebar.slider("Jumlah kategori teratas", min_value=5, max_value=15, value=10)
min_orders = st.sidebar.slider(
    "Minimum pesanan per state",
    min_value=1, max_value=500, value=100,
    help="State dengan pesanan sedikit bikin persentase keterlambatan kurang stabil.",
)

sales_f = sales_df[
    sales_df["order_purchase_timestamp"].dt.date.between(start_date, end_date)
]
delivery_f = delivery_df[
    delivery_df["order_purchase_timestamp"].dt.date.between(start_date, end_date)
]

if sales_f.empty or delivery_f.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
    st.stop()

# ---------------------------------------------------------------------------
# Header + ringkasan
# ---------------------------------------------------------------------------
st.title("🛒 Dashboard Analisis E-Commerce")
st.caption(f"Periode: {start_date:%d %b %Y} – {end_date:%d %b %Y} (hanya pesanan berstatus delivered)")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"R$ {sales_f['price'].sum():,.0f}")
c2.metric("Total Pesanan", f"{sales_f['order_id'].nunique():,}")
c3.metric("Rata-rata Review", f"{delivery_f['review_score'].mean():.2f}")
c4.metric("Pesanan Terlambat", f"{delivery_f['is_late'].mean() * 100:.2f}%")

tab1, tab2 = st.tabs(["Pertanyaan 1: Revenue Kategori", "Pertanyaan 2: Keterlambatan & Review"])

# ---------------------------------------------------------------------------
# Tab 1: revenue per kategori
# ---------------------------------------------------------------------------
with tab1:
    category_revenue = (
        sales_f.groupby("product_category_name_english")["price"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"product_category_name_english": "category", "price": "revenue"})
    )
    category_revenue["contribution_pct"] = (
        category_revenue["revenue"] / category_revenue["revenue"].sum() * 100
    )

    top_df = category_revenue.head(top_n)
    bottom_df = category_revenue.tail(5)

    st.subheader("Kategori produk dengan revenue tertinggi dan terendah")
    st.metric(
        "Kontribusi 5 kategori teratas terhadap total revenue",
        f"{category_revenue.head(5)['contribution_pct'].sum():.2f}%",
    )

    col_a, col_b = st.columns(2)
    with col_a:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(data=top_df, x="revenue", y="category", color=BLUE, ax=ax)
        ax.set_title(f"Top {top_n} Kategori dengan Revenue Tertinggi")
        ax.set_xlabel("Revenue (R$)")
        ax.set_ylabel(None)
        st.pyplot(fig)
    with col_b:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(data=bottom_df, x="revenue", y="category", color=RED, ax=ax)
        ax.set_title("5 Kategori dengan Revenue Terendah")
        ax.set_xlabel("Revenue (R$)")
        ax.set_ylabel(None)
        st.pyplot(fig)

    with st.expander("Lihat tabel revenue semua kategori"):
        st.dataframe(category_revenue.round(2))

# ---------------------------------------------------------------------------
# Tab 2: keterlambatan vs review
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Pengaruh keterlambatan pengiriman terhadap review score")

    review_by_late = (
        delivery_f.groupby("is_late")["review_score"].mean().reset_index()
    )
    review_by_late["status"] = review_by_late["is_late"].map({False: "Tepat waktu", True: "Terlambat"})

    state_late = (
        delivery_f.groupby("customer_state")
        .agg(total_orders=("order_id", "count"), late_rate=("is_late", "mean"))
        .reset_index()
    )
    state_late["late_rate"] *= 100
    state_late = state_late[state_late["total_orders"] >= min_orders]
    state_late = state_late.sort_values("late_rate", ascending=False).head(10)

    col_a, col_b = st.columns(2)
    with col_a:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(
            data=review_by_late, x="status", y="review_score", hue="status",
            palette={"Tepat waktu": BLUE, "Terlambat": RED}, legend=False, ax=ax,
        )
        ax.set_title("Rata-rata Review Score: Tepat Waktu vs Terlambat")
        ax.set_xlabel(None)
        ax.set_ylabel("Rata-rata review score")
        ax.set_ylim(0, 5)
        st.pyplot(fig)
    with col_b:
        if state_late.empty:
            st.info("Tidak ada state yang memenuhi minimum pesanan. Turunkan nilainya di sidebar.")
        else:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(data=state_late, x="late_rate", y="customer_state", color=RED, ax=ax)
            ax.set_title("10 State dengan Persentase Keterlambatan Tertinggi")
            ax.set_xlabel("% pesanan terlambat")
            ax.set_ylabel(None)
            st.pyplot(fig)

    st.subheader("Analisis lanjutan: lama keterlambatan vs review score")
    delay_summary = (
        delivery_f.groupby("delay_group", observed=True)
        .agg(total_orders=("order_id", "count"), avg_review=("review_score", "mean"))
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(10, 4.5))
    sns.barplot(data=delay_summary, x="delay_group", y="avg_review", color=BLUE, ax=ax)
    ax.set_xlabel(None)
    ax.set_ylabel("Rata-rata review score")
    ax.set_ylim(0, 5)
    for i, row in delay_summary.iterrows():
        ax.text(i, row["avg_review"] + 0.05, f"{row['avg_review']:.2f}", ha="center")
    st.pyplot(fig)

st.caption("Sumber data: E-Commerce Public Dataset (Olist).")
