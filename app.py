import streamlit as st
import pandas as pd

st.set_page_config(page_title="Keuangan Harian", page_icon="📊", layout="centered")

# ============================ LOAD DATA ============================
@st.cache_data
def load_data():
    try:
        pemasukan = pd.read_csv("pemasukan.csv")
    except:
        pemasukan = pd.DataFrame(columns=["Tanggal", "Sumber", "Jumlah (Rp)"])

    try:
        pengeluaran = pd.read_csv("pengeluaran.csv")
    except:
        pengeluaran = pd.DataFrame(columns=["Tanggal", "Nama", "Jumlah (Rp)", "Kategori"])

    # ✅ Pastikan kategori selalu ada (untuk data lama)
    if "Kategori" not in pengeluaran.columns:
        pengeluaran["Kategori"] = "Tanpa Kategori"

    return pemasukan, pengeluaran

pemasukan, pengeluaran = load_data()

# ============================ SAVE ============================
def save():
    pemasukan.to_csv("pemasukan.csv", index=False)
    pengeluaran.to_csv("pengeluaran.csv", index=False)

st.title("📊 Aplikasi Pencatatan Keuangan Harian")

# ============================ INPUT PEMASUKAN ============================
st.header("💰 Input Pemasukan")
with st.form("form_pemasukan"):
    tgl_masuk = st.number_input("Tanggal pemasukan:", min_value=1, max_value=31)
    sumber = st.text_input("Sumber pemasukan (misal: gaji, freelance, transfer)")
    jumlah_masuk = st.number_input("Jumlah (Rp):", min_value=0.0)
    submit_in = st.form_submit_button("Tambah Pemasukan")

if submit_in and jumlah_masuk > 0:
    pemasukan.loc[len(pemasukan)] = [tgl_masuk, sumber, jumlah_masuk]
    save()
    st.success("✅ Pemasukan berhasil ditambahkan!")

# ============================ HAPUS PEMASUKAN ============================
if len(pemasukan) > 0:
    st.subheader("🗑️ Hapus Pemasukan")
    list_in = list(pemasukan.index.astype(str) + " - " + pemasukan["Sumber"] + " (Rp " + pemasukan["Jumlah (Rp)"].astype(str) + ")")
    selected_in = st.selectbox("Pilih pemasukan yang ingin dihapus:", [""] + list_in)
    if selected_in != "":
        if st.button("Hapus Pemasukan"):
            idx = int(selected_in.split(" - ")[0])
            pemasukan.drop(idx, inplace=True)
            pemasukan.reset_index(drop=True, inplace=True)
            save()
            st.success("✅ Berhasil dihapus!")

# ============================ INPUT PENGELUARAN ============================
st.header("📝 Input Pengeluaran")
with st.form("form_pengeluaran"):
    tgl_keluar = st.number_input("Tanggal pengeluaran:", min_value=1, max_value=31)
    nama_keluar = st.text_input("Nama pengeluaran:")
    kategori = st.text_input("Kategori (misal: makanan, transport, skincare, dll.)")
    jumlah_keluar = st.number_input("Jumlah pengeluaran (Rp):", min_value=0.0)
    submit_out = st.form_submit_button("Tambah Pengeluaran")

if submit_out and jumlah_keluar > 0:
    pengeluaran.loc[len(pengeluaran)] = [tgl_keluar, nama_keluar, jumlah_keluar, kategori]
    save()
    st.success("✅ Pengeluaran berhasil ditambahkan!")

# ============================ HAPUS PENGELUARAN ============================
if len(pengeluaran) > 0:
    st.subheader("🗑️ Hapus Pengeluaran")
    list_out = list(
        pengeluaran.index.astype(str) +
        " - " + pengeluaran["Nama"] +
        " (Rp " + pengeluaran["Jumlah (Rp)"].astype(str) + ")"
    )
    selected_out = st.selectbox("Pilih pengeluaran yang ingin dihapus:", [""] + list_out)
    if selected_out != "":
        if st.button("Hapus Pengeluaran"):
            idx = int(selected_out.split(" - ")[0])
            pengeluaran.drop(idx, inplace=True)
            pengeluaran.reset_index(drop=True, inplace=True)
            save()
            st.success("✅ Berhasil dihapus!")

# ============================ RINGKASAN ============================
st.header("📌 Ringkasan Bulanan")

total_in = pemasukan["Jumlah (Rp)"].sum()
total_out = pengeluaran["Jumlah (Rp)"].sum()
persen = (total_out / total_in * 100) if total_in > 0 else 0

st.write(f"**Total Pemasukan:** Rp {total_in:,.0f}")
st.write(f"**Total Pengeluaran:** Rp {total_out:,.0f}")
st.write(f"**Persentase Pengeluaran:** {persen:.2f}%")

# Pengeluaran terbesar
if len(pengeluaran) > 0:
    biggest = pengeluaran.loc[pengeluaran["Jumlah (Rp)"].idxmax()]
   
    st.write(f"🔺 Pengeluaran Terbesar: **{biggest['Nama']}** (Rp {biggest['Jumlah (Rp)']:,.0f}) — *Kategori:* {biggest['Kategori']}")

# ============================ GRAFIK ============================
st.header("📈 Grafik Pemasukan vs Pengeluaran")

g_in = pemasukan.groupby("Tanggal")["Jumlah (Rp)"].sum()
g_out = pengeluaran.groupby("Tanggal")["Jumlah (Rp)"].sum()

df_chart = pd.DataFrame({"Pemasukan": g_in, "Pengeluaran": g_out}).fillna(0)
st.line_chart(df_chart)

# ============================ TABEL ============================
st.subheader("📃 Data Pemasukan")
st.dataframe(pemasukan)

st.subheader("📃 Data Pengeluaran")
st.dataframe(pengeluaran)


