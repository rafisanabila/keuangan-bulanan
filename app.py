import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Aplikasi Keuangan Bulanan", layout="wide")

# -----------------------------
# Fungsi Load dan Simpan CSV
# -----------------------------
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

    return pemasukan, pengeluaran

def save_data(pemasukan, pengeluaran):
    pemasukan.to_csv("pemasukan.csv", index=False)
    pengeluaran.to_csv("pengeluaran.csv", index=False)

# Load data awal
pemasukan, pengeluaran = load_data()

st.title("📊 Aplikasi Keuangan Bulanan")


# =============================
# ⬆️ INPUT PEMASUKAN
# =============================
st.header("➕ Tambah Pemasukan")
with st.form("form_pemasukan"):
    tgl_in = st.date_input("Tanggal")
    sumber_in = st.text_input("Sumber Pemasukan")
    jumlah_in = st.number_input("Jumlah (Rp)", step=1000, min_value=0)
    simpan_in = st.form_submit_button("Simpan")

if simpan_in:
    pemasukan.loc[len(pemasukan)] = [tgl_in, sumber_in, jumlah_in]
    save_data(pemasukan, pengeluaran)
    st.success("✅ Pemasukan berhasil disimpan")


# =============================
# ⬇️ INPUT PENGELUARAN
# =============================
st.header("➖ Tambah Pengeluaran")
with st.form("form_pengeluaran"):
    tgl_out = st.date_input("Tanggal ")
    nama_out = st.text_input("Nama Pengeluaran")
    jumlah_out = st.number_input("Jumlah (Rp)", step=1000, min_value=0)
    kategori_out = st.text_input("Kategori (Makan, Transport, dll)")
    simpan_out = st.form_submit_button("Simpan")

if simpan_out:
    pengeluaran.loc[len(pengeluaran)] = [tgl_out, nama_out, jumlah_out, kategori_out]
    save_data(pemasukan, pengeluaran)
    st.success("✅ Pengeluaran berhasil disimpan")


# =============================
# 🗑 HAPUS DATA
# =============================
st.header("🗑 Hapus Data")
tab1, tab2 = st.tabs(["Hapus Pemasukan", "Hapus Pengeluaran"])

with tab1:
    if len(pemasukan) > 0:
        pilihan = st.selectbox("Pilih data pemasukan yang ingin dihapus:", pemasukan.index)
        if st.button("Hapus Pemasukan"):
            pemasukan = pemasukan.drop(pilihan)
            save_data(pemasukan, pengeluaran)
            st.experimental_rerun()
    else:
        st.info("Belum ada data pemasukan.")

with tab2:
    if len(pengeluaran) > 0:
        pilihan2 = st.selectbox("Pilih data pengeluaran yang ingin dihapus:", pengeluaran.index)
        if st.button("Hapus Pengeluaran"):
            pengeluaran = pengeluaran.drop(pilihan2)
            save_data(pemasukan, pengeluaran)
            st.experimental_rerun()
    else:
        st.info("Belum ada data pengeluaran.")


# =============================
# 📄 TAMPIL DATA
# =============================
st.header("📄 Data Pemasukan")
st.dataframe(pemasukan)

st.header("📄 Data Pengeluaran")
st.dataframe(pengeluaran)


# =============================
# 🧾 RINGKASAN
# =============================
total_in = pemasukan["Jumlah (Rp)"].sum()
total_out = pengeluaran["Jumlah (Rp)"].sum()
saldo = total_in - total_out

st.header("🧾 Ringkasan")
st.write(f"**Total Pemasukan:** Rp {total_in:,.0f}")
st.write(f"**Total Pengeluaran:** Rp {total_out:,.0f}")
st.write(f"**Saldo Akhir:** **Rp {saldo:,.0f}**")


# =============================
# 📊 GRAFIK
# =============================
st.header("📈 Grafik Pengeluaran per Kategori")
if len(pengeluaran) > 0:
    kategori_sum = pengeluaran.groupby("Kategori")["Jumlah (Rp)"].sum()
    st.bar_chart(kategori_sum)
else:
    st.info("Tambahkan pengeluaran untuk melihat grafik.")


st.header("📉 Grafik Pemasukan vs Pengeluaran")
total_df = pd.DataFrame({
    "Keterangan": ["Pemasukan", "Pengeluaran"],
    "Jumlah (Rp)": [total_in, total_out]
})
st.bar_chart(total_df.set_index("Keterangan"))
