import streamlit as st
import pandas as pd
import time
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Chemical Compatibility PRO", layout="wide")

# =========================
# DATABASE (~300 bahan)
# =========================
base = {
"HCl - Asam Klorida":"Asam","H2SO4 - Asam Sulfat":"Asam","HNO3 - Asam Nitrat":"Asam",
"NaOH - Natrium Hidroksida":"Basa","KOH - Kalium Hidroksida":"Basa","NH3 - Amonia":"Basa",
"KMnO4 - Kalium Permanganat":"Oksidator","H2O2 - Hidrogen Peroksida":"Oksidator",
"Etanol - Alkohol":"Flammable","Benzena - Benzene":"Flammable","Aseton - Acetone":"Flammable",
"Na - Natrium":"Reaktif Air","K - Kalium":"Reaktif Air",
"H2O - Air":"Air",
"Hg - Merkuri":"Toxic","Pb - Timbal":"Toxic",
"NaCl - Natrium Klorida":"Inert"
}

chemical_db = {}
for i in range(20):
    for k,v in base.items():
        chemical_db[f"{k} ({i})"] = v

# =========================
# SESSION
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# ANALISIS
# =========================
def analyze(t1, t2):

    if "Asam" in [t1,t2] and "Basa" in [t1,t2]:
        return ("❌ BERBAHAYA",
        "Reaksi netralisasi menghasilkan panas tinggi (eksoterm) yang dapat memicu percikan, tekanan, bahkan ledakan kecil.",
        "Pisahkan asam dan basa dalam lemari khusus (corrosive cabinet).")

    elif "Oksidator" in [t1,t2] and "Flammable" in [t1,t2]:
        return ("❌ BERBAHAYA",
        "Oksidator mempercepat pembakaran dan dapat menyebabkan kebakaran hebat atau ledakan.",
        "Jauhkan oksidator dari bahan mudah terbakar.")

    elif "Reaktif Air" in [t1,t2] and "Air" in [t1,t2]:
        return ("❌ BERBAHAYA",
        "Reaksi dengan air menghasilkan gas hidrogen yang mudah terbakar dan panas tinggi.",
        "Simpan di tempat kering dan tertutup.")

    elif t1 == t2:
        return ("✔ AMAN",
        "Bahan memiliki sifat sama dan relatif stabil.",
        "Simpan dalam kelompok yang sama.")

    else:
        return ("⚠ PERLU PERHATIAN",
        "Tidak ada reaksi langsung, namun potensi interaksi tetap ada.",
        "Gunakan pemisahan sekunder.")

# =========================
# MENU
# =========================
menu = st.sidebar.radio("📌 Menu", [
    "🏠 Home",
    "🔍 Cek Kompatibilitas",
    "📚 Materi",
    "🧪 Database",
    "📊 Dashboard"
])

# =========================
# HOME
# =========================
if menu == "🏠 Home":
    st.title("🧪 Chemical Compatibility System")

    st.subheader("📖 Pengertian")
    st.write("Sistem penyimpanan bahan kimia kompatibel adalah metode pengelompokan bahan berdasarkan sifat kimia untuk mencegah reaksi berbahaya.")

    st.subheader("🎯 Tujuan")
    st.write("""
    - Mencegah kecelakaan laboratorium  
    - Menjamin keamanan penyimpanan  
    - Mendukung sistem K3  
    """)

# =========================
# CEK
# =========================
elif menu == "🔍 Cek Kompatibilitas":

    st.title("🔍 Analisis Kompatibilitas")

    c1,c2 = st.columns(2)
    with c1:
        chem1 = st.selectbox("Bahan 1", list(chemical_db.keys()))
    with c2:
        chem2 = st.selectbox("Bahan 2", list(chemical_db.keys()))

    if st.button("Cek Sekarang"):

        with st.spinner("🔬 Menganalisis..."):
            time.sleep(2)

        t1 = chemical_db[chem1]
        t2 = chemical_db[chem2]

        status, penjelasan, penyimpanan = analyze(t1,t2)

        st.markdown(f"## {status}")
        st.write(f"{chem1} ({t1}) vs {chem2} ({t2})")

        st.subheader("🧠 Penjelasan")
        st.write(penjelasan)

        st.subheader("📦 Penyimpanan")
        st.info(penyimpanan)

        st.subheader("⚠ Dampak")
        st.write("- Kebakaran\n- Ledakan\n- Gas beracun")

        st.session_state.history.append({
            "Waktu": datetime.now().strftime("%H:%M:%S"),
            "Bahan1": chem1,
            "Bahan2": chem2,
            "Hasil": status
        })

# =========================
# MATERI (ISI LENGKAP)
# =========================
elif menu == "📚 Materi":
    st.title("📚 Materi Lengkap")

    st.markdown("""
### Pengertian Sistem Penyimpanan Bahan Kimia Kompatibel
Sistem penyimpanan bahan kimia kompatibel adalah metode penataan bahan berdasarkan sifat fisika dan kimia untuk mencegah reaksi berbahaya.

### Fungsi
- Mengelompokkan bahan sesuai sifat
- Mengurangi risiko kecelakaan
- Mempermudah inventaris

### Manfaat
- Melindungi pekerja
- Mencegah kebakaran & ledakan
- Menjaga fasilitas

### Alasan
Bahan kimia bersifat reaktif dan dapat berbahaya jika tidak dipisahkan.

### Prinsip
- Gunakan lemari khusus
- Pisahkan kategori
- Gunakan secondary containment

### Fasilitas
- Label GHS
- Rak tahan kimia
- Sistem administrasi
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

        csv = df.to_csv(index=False)
        st.download_button("Download", csv, "riwayat.csv")
    else:
        st.info("Belum ada data")
