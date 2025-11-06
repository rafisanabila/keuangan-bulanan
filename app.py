import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Keuangan Bulanan", layout="wide")

# === LOAD / INIT DATA ===
file_path = "pengeluaran.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=["Tanggal", "Pengeluaran", "Jumlah (Rp)"])

st.title("📊 Aplikasi Pencatatan Keuangan Bulanan")

# === INPUT PEMASUKAN ===
pemasukan = st.number_input("Masukkan total pemasukan bulan ini (Rp):", min_value=0.0, value=0.0)

# === FORM INPUT PENGELUARAN ===
st.subheader("📝 Input Pengeluaran Harian")

with st.form("input_form"):
    tanggal = st.text_input("Tanggal (misal: 1, 12, 30):")
    nama = st.text_input("Nama Pengeluaran:")
    jumlah = st.number_input("Jumlah (Rp):", min_value=0.0, step=500.0)
    submit = st.form_submit_button("Tambahkan Data")

if submit and tanggal and nama and jumlah > 0:
    df.loc[len(df)] = [tanggal, nama, jumlah]
    df.to_csv(file_path, index=False)
    st.success("✅ Data berhasil ditambahkan!")


# === TAMPILKAN DATA ===
st.subheader("📃 Data Pengeluaran")
st.dataframe(df, use_container_width=True)


# === FITUR HAPUS DATA ===
st.subheader("🧹 Hapus Data Pengeluaran")

if len(df) > 0:
    index_to_delete = st.selectbox("Pilih baris untuk dihapus:", df.index, format_func=lambda x: f"{x}. {df.loc[x,'Tanggal']} - {df.loc[x,'Pengeluaran']} (Rp {df.loc[x,'Jumlah (Rp)']:,.0f})")
    
    if st.button("Hapus Baris Ini"):
        df = df.drop(index_to_delete)
        df.to_csv(file_path, index=False)
        st.success("✅ Baris berhasil dihapus! Silakan refresh halaman.")

    if st.button("Hapus Semua Data ⚠️"):
        df = df.iloc[0:0]
        df.to_csv(file_path, index=False)
        st.warning("⚠️ Semua data telah dihapus!")

# === PERHITUNGAN ===
if len(df) > 0 and pemasukan > 0:

    total_pengeluaran = df["Jumlah (Rp)"].sum()
    pengeluaran_terbesar = df.loc[df["Jumlah (Rp)"].idxmax()]
    persentase = (total_pengeluaran / pemasukan) * 100

    st.subheader("📌 Ringkasan Bulanan")
    st.write(f"**Total Pengeluaran:** Rp {total_pengeluaran:,.0f}")
    st.write(f"**Pengeluaran Terbesar:** {pengeluaran_terbesar['Pengeluaran']} (Tanggal {pengeluaran_terbesar['Tanggal']}) = Rp {pengeluaran_terbesar['Jumlah (Rp)']:,.0f}")
    st.write(f"**Persentase Pengeluaran terhadap Pemasukan:** {persentase:.2f}%")

    # === GRAFIK ===
    st.subheader("📈 Grafik Total Pengeluaran per Tanggal")
    grafik = df.groupby("Tanggal")["Jumlah (Rp)"].sum()
    st.line_chart(grafik)

else:
    st.info("Masukkan pemasukan dan minimal 1 data pengeluaran agar grafik & ringkasan tampil.")
