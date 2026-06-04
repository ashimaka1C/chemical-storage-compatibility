import streamlit as st
import pandas as pd
import time
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Chemical Compatibility Pro", layout="wide")

# =========================
# DATABASE (AUTO GENERATE ~300)
# =========================
base_chemicals = {
    "HCl - Asam Klorida": "Asam",
    "H2SO4 - Asam Sulfat": "Asam",
    "HNO3 - Asam Nitrat": "Asam",
    "CH3COOH - Asam Asetat": "Asam",
    "NaOH - Natrium Hidroksida": "Basa",
    "KOH - Kalium Hidroksida": "Basa",
    "NH3 - Amonia": "Basa",
    "KMnO4 - Kalium Permanganat": "Oksidator",
    "H2O2 - Hidrogen Peroksida": "Oksidator",
    "Etanol - Alkohol": "Flammable",
    "Benzena - Benzene": "Flammable",
    "Aseton - Acetone": "Flammable",
    "Na - Natrium": "Reaktif Air",
    "K - Kalium": "Reaktif Air",
    "H2O - Air": "Air",
    "Hg - Merkuri": "Toxic",
    "Pb - Timbal": "Toxic",
    "NaCl - Natrium Klorida": "Inert"
}

# Duplicate untuk simulasi 300+
chemical_db = {}
for i in range(15):  # 15x lipat
    for k, v in base_chemicals.items():
        chemical_db[f"{k} ({i})"] = v

# =========================
# SESSION
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# LOGIKA
# =========================
def analyze(t1, t2):

    if "Asam" in [t1,t2] and "Basa" in [t1,t2]:
        return "❌ BERBAHAYA", "Reaksi netralisasi menghasilkan panas tinggi (eksoterm).", "Pisahkan dalam lemari asam & basa"
    
    if "Oksidator" in [t1,t2] and "Flammable" in [t1,t2]:
        return "❌ BERBAHAYA", "Dapat memicu kebakaran/ledakan.", "Jauhkan oksidator dari bahan organik"
    
    if "Reaktif Air" in [t1,t2] and "Air" in [t1,t2]:
        return "❌ BERBAHAYA", "Reaksi eksplosif dengan air.", "Simpan di tempat kering"
    
    if t1 == t2:
        return "✔ AMAN", "Stabil dalam kategori yang sama.", "Simpan dalam satu kelompok"
    
    return "⚠ PERLU PERHATIAN", "Potensi interaksi tidak langsung.", "Gunakan pemisahan sekunder"

# =========================
# MENU
# =========================
menu = st.sidebar.radio("Menu", [
    "🏠 Home",
    "🔍 Cek",
    "📚 Materi",
    "🧪 Database",
    "📊 Dashboard"
])

# =========================
# HOME
# =========================
if menu == "🏠 Home":
    st.title("🧪 Chemical Compatibility System PRO")

    st.subheader("📖 Pengertian")
    st.write("Kompatibilitas penyimpanan adalah kemampuan bahan kimia disimpan bersama tanpa reaksi berbahaya.")

    st.subheader("🎯 Tujuan")
    st.write("""
    - Mencegah kecelakaan
    - Menentukan keamanan penyimpanan
    - Mendukung K3 laboratorium
    """)

# =========================
# CEK
# =========================
elif menu == "🔍 Cek":

    st.title("🔍 Cek Kompatibilitas")

    c1, c2 = st.columns(2)

    with c1:
        chem1 = st.selectbox("Bahan 1", list(chemical_db.keys()))
    with c2:
        chem2 = st.selectbox("Bahan 2", list(chemical_db.keys()))

    if st.button("Cek Sekarang"):

        # ANIMASI
        with st.spinner("🔬 Menganalisis reaksi kimia..."):
            time.sleep(2)

        t1 = chemical_db[chem1]
        t2 = chemical_db[chem2]

        status, penjelasan, penyimpanan = analyze(t1, t2)

        st.subheader("Hasil")
        st.markdown(f"### {status}")

        st.write(f"**{chem1} ({t1})** vs **{chem2} ({t2})**")

        st.subheader("🧠 Penjelasan")
        st.write(penjelasan)

        st.subheader("📦 Penyimpanan")
        st.info(penyimpanan)

        # AI tambahan
        st.subheader("🤖 AI Insight")
        st.write("Sistem menyarankan pemisahan berdasarkan kategori bahaya untuk menghindari reaksi tidak terkontrol.")

        # SIMPAN
        st.session_state.history.append({
            "Waktu": datetime.now().strftime("%H:%M:%S"),
            "Bahan1": chem1,
            "Bahan2": chem2,
            "Hasil": status
        })

# =========================
# MATERI
# =========================
elif menu == "📚 Materi":
    st.title("📚 Materi")

    st.write("""
    Prinsip:
    - Asam vs Basa → reaksi panas
    - Oksidator vs Organik → kebakaran
    - Air vs logam aktif → ledakan
    """)

# =========================
# DATABASE
# =========================
elif menu == "🧪 Database":
    df = pd.DataFrame(list(chemical_db.items()), columns=["Bahan","Kategori"])
    st.dataframe(df)

# =========================
# DASHBOARD
# =========================
elif menu == "📊 Dashboard":

    st.title("📊 Riwayat")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)

        st.bar_chart(df["Hasil"].value_counts())

        # DOWNLOAD
        csv = df.to_csv(index=False)
        st.download_button("Download Data", csv, "riwayat.csv")
    else:
        st.info("Belum ada data")
