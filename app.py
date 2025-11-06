import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Keuangan Harian", layout="wide")

# ============ STYLE =============
st.markdown("""
    <style>
        .title {
            font-size: 38px; font-weight: 900; text-align:center; margin-bottom: 10px;
            background: -webkit-linear-gradient(#ff7eb9, #ff65a3, #7afcff);
            -webkit-background-clip: text; color: transparent;
        }
        .card {
            padding: 18px; border-radius: 14px; color: white; font-weight: bold; 
            text-align:center; box-shadow: 0px 2px 12px rgba(0,0,0,0.15);
        }
        .income { background: linear-gradient(135deg, #5ee7df, #b490ca); }
        .expense { background: linear-gradient(135deg, #ff9a9e, #f6416c); }
        .summary { background: linear-gradient(135deg, #a1c4fd, #c2e9fb); color:#222; }
    </style>
""", unsafe_allow_html=True)

# ============ FILE DATA ==========
income_file = "pemasukan.csv"
expense_file = "pengeluaran.csv"

income_df = pd.read_csv(income_file) if os.path.exists(income_file) else pd.DataFrame(columns=["Tanggal", "Sumber", "Jumlah (Rp)"])
expense_df = pd.read_csv(expense_file) if os.path.exists(expense_file) else pd.DataFrame(columns=["Tanggal", "Nama", "Kategori", "Jumlah (Rp)"])

st.markdown("<p class='title'>📊 Aplikasi Keuangan Harian Estetik</p>", unsafe_allow_html=True)

# ============ INPUT PEMASUKAN ==========
st.header("💰 Input Pemasukan")

col1, col2, col3 = st.columns(3)
with col1:
    t_in = st.number_input("Tanggal:", 1, 31, 1)
with col2:
    sumber = st.text_input("Sumber pemasukan:")
with col3:
    j_in = st.number_input("Jumlah (Rp):", min_value=0.0, step=1000.0, format="%.2f")

if st.button("➕ Tambah Pemasukan"):
    income_df.loc[len(income_df)] = [t_in, sumber, j_in]
    income_df.to_csv(income_file, index=False)
    st.success("✅ Pemasukan ditambahkan!")


# Hapus pemasukan
if len(income_df) > 0:
    remove_in = st.selectbox("🧹 Hapus pemasukan:", income_df.index)
    if st.button("Hapus Data Pemasukan"):
        income_df = income_df.drop(remove_in)
        income_df.to_csv(income_file, index=False)
        st.success("✅ Pemasukan berhasil dihapus!")


# ============ INPUT PENGELUARAN ==========
st.header("📝 Input Pengeluaran")

col1, col2, col3, col4 = st.columns(4)
with col1:
    t_out = st.number_input("Tanggal:", 1, 31, 1, key="tgl_out")
with col2:
    nama_out = st.text_input("Nama pengeluaran:")
with col3:
    kategori = st.text_input("Kategori (bebas):")
with col4:
    j_out = st.number_input("Jumlah (Rp):", min_value=0.0, step=1000.0, format="%.2f", key="j_out")

if st.button("➖ Tambah Pengeluaran"):
    expense_df.loc[len(expense_df)] = [t_out, nama_out, kategori, j_out]
    expense_df.to_csv(expense_file, index=False)
    st.success("✅ Pengeluaran ditambahkan!")

if len(expense_df) > 0:
    remove_out = st.selectbox("🧹 Hapus pengeluaran:", expense_df.index)
    if st.button("Hapus Data Pengeluaran"):
        expense_df = expense_df.drop(remove_out)
        expense_df.to_csv(expense_file, index=False)
        st.success("✅ Pengeluaran berhasil dihapus!")


# ============ RINGKASAN =============
st.header("📌 Ringkasan Bulanan")

total_in = income_df["Jumlah (Rp)"].sum()
total_out = expense_df["Jumlah (Rp)"].sum()

colA, colB, colC = st.columns(3)
with colA:
    st.markdown(f"<div class='card income'>Total Pemasukan<br>Rp {total_in:,.0f}</div>", unsafe_allow_html=True)
with colB:
    st.markdown(f"<div class='card expense'>Total Pengeluaran<br>Rp {total_out:,.0f}</div>", unsafe_allow_html=True)
with colC:
    persen = (total_out / total_in * 100) if total_in > 0 else 0
    st.markdown(f"<div class='card summary'>Pengeluaran vs Pemasukan<br>{persen:.2f}%</div>", unsafe_allow_html=True)

if len(expense_df) > 0:
    biggest = expense_df.loc[expense_df["Jumlah (Rp)"].idxmax()]
    st.write(f"🔺 Pengeluaran Terbesar: **{biggest['Nama']}** (Rp {biggest['Jumlah (Rp)']:,.0f}) — *Kategori:* {biggest['Kategori']}")


# ============ GRAFIK GARIS ==========
st.header("📈 Grafik Pemasukan vs Pengeluaran per Tanggal")

income_df["Tanggal"] = income_df["Tanggal"].astype(int)
expense_df["Tanggal"] = expense_df["Tanggal"].astype(int)

g_in = income_df.groupby("Tanggal")["Jumlah (Rp)"].sum()
g_out = expense_df.groupby("Tanggal")["Jumlah (Rp)"].sum()

index = range(1, 32)
chart_data = pd.DataFrame({"Pemasukan": g_in.reindex(index, fill_value=0),
                           "Pengeluaran": g_out.reindex(index, fill_value=0)})
st.line_chart(chart_data)


# ============ GRAFIK PIE ==========
if len(expense_df) > 0:
    st.header("🥧 Grafik Pengeluaran per Kategori")
    pie = expense_df.groupby("Kategori")["Jumlah (Rp)"].sum()
    st.bar_chart(pie)
