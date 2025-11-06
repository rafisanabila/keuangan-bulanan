import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Keuangan Bulanan", layout="wide")

# === FILE DATA ===
file_income = "pemasukan.csv"
file_expense = "pengeluaran.csv"

# === LOAD DATA ===
if os.path.exists(file_income):
    income = pd.read_csv(file_income)
else:
    income = pd.DataFrame(columns=["Tanggal", "Sumber", "Jumlah (Rp)"])

if os.path.exists(file_expense):
    expense = pd.read_csv(file_expense)
else:
    expense = pd.DataFrame(columns=["Tanggal", "Pengeluaran", "Jumlah (Rp)"])

# Pastikan tanggal berupa angka
for df in [income, expense]:
    if len(df) > 0:
        df["Tanggal"] = df["Tanggal"].astype(int)
        df.sort_values(by="Tanggal", inplace=True)

st.title("📊 Aplikasi Pencatatan Keuangan Harian")

# ==============================
# INPUT PEMASUKAN
# ==============================
st.subheader("💰 Input Pemasukan")

with st.form("input_pemasukan"):
    tgl_in = st.text_input("Tanggal pemasukan:")
    sumber = st.text_input("Sumber pemasukan (misal: gaji, freelance, transfer):")
    jml_in = st.number_input("Jumlah (Rp):", min_value=0.0, step=1000.0)
    add_in = st.form_submit_button("Tambahkan Pemasukan")

if add_in and tgl_in and sumber and jml_in > 0:
    income.loc[len(income)] = [tgl_in, sumber, jml_in]
    income.to_csv(file_income, index=False)
    st.success("✅ Pemasukan berhasil ditambahkan!")

st.dataframe(income, use_container_width=True)

# Hapus pemasukan
if len(income) > 0:
    idx_in = st.selectbox("Hapus pemasukan:", income.index, format_func=lambda x: f"{income.loc[x,'Tanggal']} - {income.loc[x,'Sumber']} (Rp {income.loc[x,'Jumlah (Rp)']:,.0f})")
    if st.button("Hapus pemasukan ini"):
        income = income.drop(idx_in)
        income.to_csv(file_income, index=False)
        st.success("✅ Pemasukan dihapus!")

# ==============================
# INPUT PENGELUARAN
# ==============================
st.subheader("📝 Input Pengeluaran")

with st.form("input_pengeluaran"):
    tgl_out = st.text_input("Tanggal pengeluaran:")
    nama_out = st.text_input("Nama pengeluaran:")
    jml_out = st.number_input("Jumlah pengeluaran (Rp):", min_value=0.0, step=1000.0)
    add_out = st.form_submit_button("Tambahkan Pengeluaran")

if add_out and tgl_out and nama_out and jml_out > 0:
    expense.loc[len(expense)] = [tgl_out, nama_out, jml_out]
    expense.to_csv(file_expense, index=False)
    st.success("✅ Pengeluaran berhasil ditambahkan!")

st.dataframe(expense, use_container_width=True)

# Hapus pengeluaran
if len(expense) > 0:
    idx_out = st.selectbox("Hapus pengeluaran:", expense.index, format_func=lambda x: f"{expense.loc[x,'Tanggal']} - {expense.loc[x,'Pengeluaran']} (Rp {expense.loc[x,'Jumlah (Rp)']:,.0f})")
    if st.button("Hapus pengeluaran ini"):
        expense = expense.drop(idx_out)
        expense.to_csv(file_expense, index=False)
        st.success("✅ Pengeluaran dihapus!")

# ==============================
# RINGKASAN
# ==============================
if len(income) > 0 and len(expense) > 0:
    total_in = income["Jumlah (Rp)"].sum()
    total_out = expense["Jumlah (Rp)"].sum()
    persentase = (total_out / total_in) * 100

    biggest = expense.loc[expense["Jumlah (Rp)"].idxmax()]

    st.subheader("📌 Ringkasan Bulanan")
    st.write(f"**Total Pemasukan:** Rp {total_in:,.0f}")
    st.write(f"**Total Pengeluaran:** Rp {total_out:,.0f}")
    st.write(f"**Pengeluaran Terbesar:** {biggest['Pengeluaran']} (Tanggal {biggest['Tanggal']}) = Rp {biggest['Jumlah (Rp)']:,.0f}")
    st.write(f"**Persentase Pengeluaran terhadap Pemasukan:** {persentase:.2f}%")

    # Gabung data untuk grafik
    g_income = income.groupby("Tanggal")["Jumlah (Rp)"].sum()
    g_expense = expense.groupby("Tanggal")["Jumlah (Rp)"].sum()

    st.subheader("📈 Grafik Pemasukan vs Pengeluaran")
    st.line_chart(pd.DataFrame({"Pemasukan": g_income, "Pengeluaran": g_expense}).fillna(0))

else:
    st.info("Masukkan minimal 1 pemasukan dan pengeluaran.")

