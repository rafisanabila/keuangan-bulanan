import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Keuangan Bulanan", layout="wide")

# ----------------------
# Fungsi Load Data
# ----------------------
def load_data():
    if os.path.exists("pemasukan.csv"):
        pemasukan = pd.read_csv("pemasukan.csv")
    else:
        pemasukan = pd.DataFrame(columns=["Tanggal", "Sumber", "Jumlah (Rp)"])
        pemasukan.to_csv("pemasukan.csv", index=False)

    if os.path.exists("pengeluaran.csv"):
        pengeluaran = pd.read_csv("pengeluaran.csv")
    else:
        pengeluaran = pd.DataFrame(columns=["Tanggal", "Nama", "Jumlah (Rp)", "Kategori"])
        pengeluaran.to_csv("pengeluaran.csv", index=False)

    # Normalisasi Kolom (mencegah KeyError)
    expected_cols = ["Tanggal", "Nama", "Jumlah (Rp)", "Kategori"]
    for col in expected_cols:
        if col not in pengeluaran.columns:
            pengeluaran[col] = ""

    pengeluaran = pengeluaran[expected_cols]  # pastikan urutan benar

    return pemasukan, pengeluaran


# ----------------------
# Load Data
# ----------------------
pemasukan, pengeluaran = load_data()


st.title("📊 Aplikasi Keuangan Bulanan")


# ----------------------
# Input Pemasukan
# ----------------------
st.header("➕ Tambah Pemasukan")
with st.form("form_pemasukan"):
    tgl_in = st.date_input("Tanggal")
    sumber_in = st.text_input("Sumber Pemasukan")
    jumlah_in = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
    submit_in = st.form_submit_button("Simpan")

if submit_in:
    pemasukan.loc[len(pemasukan)] = [tgl_in, sumber_in, jumlah_in]
    pemasukan.to_csv("pemasukan.csv", index=False)
    st.success("Pemasukan berhasil disimpan ✅")


# ----------------------
# Input Pengeluaran
# ----------------------
st.header("➖ Tambah Pengeluaran")
with st.form("form_pengeluaran"):
    tgl_out = st.date_input("Tanggal")
    nama_out = st.text_input("Nama Pengeluaran")
    jumlah_out = st.number_input("Jumlah (Rp)", min_value=0, step=1000)
    kategori_out = st.text_input("Kategori (misal: Makan, Transport, dll)")
    submit_out = st.form_submit_button("Simpan")

if submit_out:
    pengeluaran.loc[len(pengeluaran)] = [tgl_out, nama_out, jumlah_out, kategori_out]
    pengeluaran.to_csv("pengeluaran.csv", index=False)
    st.success("Pengeluaran berhasil disimpan ✅")


# ----------------------
# Tabel Tampil
# ----------------------
st.header("📄 Data Pemasukan")
st.dataframe(pemasukan)

st.header("📄 Data Pengeluaran")
st.dataframe(pengeluaran)


# ----------------------
# Total Keuangan
# ----------------------
total_pemasukan = pemasukan["Jumlah (Rp)"].sum()
total_pengeluaran = pengeluaran["Jumlah (Rp)"].sum()
saldo = total_pemasukan - total_pengeluaran

st.header("🧾 Ringkasan")
st.write(f"**Total Pemasukan:** Rp {total_pemasukan:,.0f}")
st.write(f"**Total Pengeluaran:** Rp {total_pengeluaran:,.0f}")
st.write(f"**Saldo Akhir:** Rp {saldo:,.0f}")



