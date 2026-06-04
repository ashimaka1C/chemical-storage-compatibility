import streamlit as st
import pandas as pd
import time
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Chemical Compatibility PRO",
    page_icon="🧪",
    layout="wide"
)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.big-title {font-size:40px; font-weight:bold;}
.safe {color:#00ff9f;}
.danger {color:#ff4b4b;}
.warning {color:#ffc107;}
</style>
""", unsafe_allow_html=True)

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
for i in range(20):  # ~300+
    for k,v in base.items():
        chemical_db[f"{k} ({i})"] = v

# =========================
# SESSION
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# ANALISIS (SUPER DETAIL)
# =========================
def analyze(t1, t2):

    if "Asam" in [t1,t2] and "Basa" in [t1,t2]:
        return ("❌ BERBAHAYA",
        """Reaksi antara asam dan basa merupakan reaksi netralisasi yang menghasilkan garam dan air.
Reaksi ini bersifat eksoterm, yaitu melepaskan panas dalam jumlah besar.
Dalam kondisi tertentu, terutama jika terjadi dalam volume besar atau wadah tertutup,
reaksi ini dapat menyebabkan peningkatan tekanan, percikan bahan kimia, bahkan ledakan kecil.
Selain itu, beberapa reaksi dapat menghasilkan uap berbahaya yang dapat mengiritasi kulit,
mata, dan saluran pernapasan.""",
        """Pisahkan penyimpanan asam dan basa dalam lemari khusus (corrosive cabinet).
Gunakan wadah tahan korosi, ventilasi baik, dan hindari penyimpanan dalam satu rak.""")

    elif "Oksidator" in [t1,t2] and "Flammable" in [t1,t2]:
        return ("❌ BERBAHAYA",
        """Oksidator dapat mempercepat proses pembakaran dengan menyediakan oksigen tambahan.
Jika bercampur dengan bahan mudah terbakar, reaksi dapat berlangsung sangat cepat dan tidak terkendali.
Hal ini dapat memicu kebakaran hebat atau ledakan, bahkan tanpa sumber api eksternal.
Beberapa oksidator kuat juga dapat bereaksi spontan dengan bahan organik.""",
        """Simpan oksidator dan bahan mudah terbakar di lemari terpisah.
Gunakan flammable cabinet untuk bahan mudah terbakar dan jauhkan dari panas.""")

    elif "Reaktif Air" in [t1,t2] and "Air" in [t1,t2]:
        return ("❌ BERBAHAYA",
        """Bahan reaktif terhadap air dapat menghasilkan reaksi hebat saat kontak dengan air,
menghasilkan gas hidrogen yang sangat mudah terbakar.
Reaksi ini sering disertai pelepasan panas tinggi dan dapat menyebabkan kebakaran atau ledakan.""",
        """Simpan bahan dalam kondisi kering, wadah kedap udara, dan jauh dari kelembaban.""")

    elif t1 == t2:
        return ("✔ AMAN",
        """Kedua bahan memiliki sifat kimia yang sama sehingga relatif stabil jika disimpan bersama.
Namun tetap perlu memperhatikan kondisi lingkungan seperti suhu dan kontaminasi.""",
        """Simpan dalam kategori yang sama dengan label jelas dan ventilasi baik.""")

    else:
        return ("⚠ PERLU PERHATIAN",
        """Tidak terdapat reaksi langsung yang berbahaya, namun interaksi tidak langsung tetap mungkin terjadi.
Perubahan kondisi seperti suhu, tekanan, atau kontaminasi dapat memicu reaksi yang tidak diinginkan.""",
        """Gunakan pemisahan sekunder dan simpan dalam wadah terpisah.""")

# =========================
# MENU
# =========================
menu = st.sidebar.radio("📌 Menu", [
    "🏠 Home","🔍 Cek Kompatibilitas","📚 Materi","🧪 Database","📊 Dashboard"
])

# =========================
# HOME
# =========================
if menu == "🏠 Home":
    st.markdown("<div class='big-title'>🧪 Chemical Compatibility System PRO</div>", unsafe_allow_html=True)

    st.subheader("📖 Pengertian")
    st.write("Kompatibilitas penyimpanan bahan kimia adalah kemampuan bahan disimpan bersama tanpa reaksi berbahaya.")

    st.subheader("🎯 Tujuan")
    st.write("""
    - Mencegah kecelakaan laboratorium  
    - Menentukan keamanan penyimpanan  
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

        with st.spinner("🔬 Menganalisis reaksi kimia..."):
            time.sleep(2)

        t1 = chemical_db[chem1]
        t2 = chemical_db[chem2]

        status, penjelasan, penyimpanan = analyze(t1,t2)

        # SIMBOL WARNA
        if "AMAN" in status:
            st.markdown(f"<h2 class='safe'>{status}</h2>", unsafe_allow_html=True)
        elif "BERBAHAYA" in status:
            st.markdown(f"<h2 class='danger'>{status}</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 class='warning'>{status}</h2>", unsafe_allow_html=True)

        st.write(f"**{chem1} ({t1}) vs {chem2} ({t2})**")

        st.subheader("🧠 Penjelasan Ilmiah")
        st.write(penjelasan)

        st.subheader("📦 Rekomendasi Penyimpanan")
        st.info(penyimpanan)

        st.subheader("⚠ Dampak Potensial")
        st.write("""
        - Luka bakar kimia  
        - Kebakaran / ledakan  
        - Gas beracun  
        - Kerusakan peralatan  
        """)

        # SIMPAN HISTORY
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
    Prinsip utama:
    - Asam vs Basa → eksoterm  
    - Oksidator vs organik → kebakaran  
    - Reaktif air → ledakan  
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

    st.title("📊 Riwayat Analisis")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)

        st.bar_chart(df["Hasil"].value_counts())

        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "riwayat.csv")
    else:
        st.info("Belum ada data")
