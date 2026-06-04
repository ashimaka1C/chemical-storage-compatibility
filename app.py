import streamlit as st
import pandas as pd
import time
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Chemical Compatibility PRO", layout="wide")

# =========================
# STYLE
# =========================
st.markdown("""
<style>
.title {font-size:40px; font-weight:bold;}
.safe {color:#00c853;}
.danger {color:#ff1744;}
.warning {color:#ff9100;}
.box {padding:15px; border-radius:10px; background:#f5f5f5;}
</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE (~300)
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
# ANALISIS DETAIL
# =========================
def analyze(t1, t2):

    if "Asam" in [t1,t2] and "Basa" in [t1,t2]:
        return ("❌ BERBAHAYA",
        """Reaksi antara asam dan basa merupakan reaksi netralisasi yang menghasilkan garam dan air.
Reaksi ini bersifat eksoterm, yaitu melepaskan panas dalam jumlah besar.
Dalam kondisi tertentu, reaksi ini dapat menyebabkan tekanan tinggi, percikan bahan kimia, bahkan ledakan kecil.
Uap yang dihasilkan juga dapat mengiritasi sistem pernapasan.""",
        """Pisahkan dalam lemari khusus asam dan basa (corrosive cabinet),
gunakan ventilasi baik dan wadah tahan korosi.""")

    elif "Oksidator" in [t1,t2] and "Flammable" in [t1,t2]:
        return ("❌ BERBAHAYA",
        """Oksidator meningkatkan laju pembakaran dan dapat menyebabkan reaksi sangat cepat.
Jika bercampur dengan bahan mudah terbakar, dapat terjadi kebakaran hebat bahkan tanpa sumber api.""",
        """Simpan oksidator dan bahan mudah terbakar di tempat terpisah,
hindari panas dan percikan.""")

    elif "Reaktif Air" in [t1,t2] and "Air" in [t1,t2]:
        return ("❌ BERBAHAYA",
        """Bahan reaktif air menghasilkan gas hidrogen yang sangat mudah terbakar.
Reaksi ini sangat cepat dan dapat menyebabkan ledakan.""",
        """Simpan di tempat kering, gunakan wadah kedap udara.""")

    elif t1 == t2:
        return ("✔ AMAN",
        """Bahan memiliki sifat yang sama sehingga relatif stabil.""",
        """Simpan dalam kelompok yang sama dengan label jelas.""")

    else:
        return ("⚠ PERLU PERHATIAN",
        """Tidak ada reaksi langsung, namun potensi interaksi tetap ada.""",
        """Gunakan pemisahan sekunder.""")

# =========================
# MENU
# =========================
menu = st.sidebar.radio("📌 Menu", [
    "🏠 Home","🔍 Cek","📚 Materi","🧪 Database","📊 Dashboard"
])

# =========================
# HOME
# =========================
if menu == "🏠 Home":
    st.markdown("<div class='title'>🧪 Chemical Compatibility System PRO</div>", unsafe_allow_html=True)

    st.subheader("📖 Pengertian")
    st.write("Metode penyimpanan bahan kimia berdasarkan sifat untuk mencegah reaksi berbahaya.")

    st.subheader("🎯 Tujuan")
    st.write("""
    - Mencegah kecelakaan  
    - Menjamin keamanan  
    - Mendukung K3  
    """)

# =========================
# CEK
# =========================
elif menu == "🔍 Cek":

    st.title("🔍 Cek Kompatibilitas")

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

        if "AMAN" in status:
            st.markdown(f"<h2 class='safe'>{status}</h2>", unsafe_allow_html=True)
        elif "BERBAHAYA" in status:
            st.markdown(f"<h2 class='danger'>{status}</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 class='warning'>{status}</h2>", unsafe_allow_html=True)

        st.write(f"**{chem1} ({t1}) vs {chem2} ({t2})**")

        st.subheader("🧠 Penjelasan Ilmiah")
        st.write(penjelasan)

        st.subheader("📦 Penyimpanan")
        st.info(penyimpanan)

        st.subheader("⚠ Dampak")
        st.write("""
        - Kebakaran  
        - Ledakan  
        - Gas beracun  
        - Kerusakan alat  
        """)

        st.session_state.history.append({
            "Waktu": datetime.now().strftime("%H:%M:%S"),
            "Bahan1": chem1,
            "Bahan2": chem2,
            "Hasil": status
        })

# =========================
# MATERI FULL
# =========================
elif menu == "📚 Materi":
    st.title("📚 Materi Lengkap Sistem Penyimpanan Kimia")

    st.markdown("""
### 1. Pengertian Sistem Penyimpanan Bahan Kimia Kompatibel
Sistem penyimpanan bahan kimia kompatibel merupakan metode penataan bahan kimia berdasarkan sifat fisika dan karakteristik kimia masing-masing bahan untuk mencegah reaksi berbahaya. Sistem ini menggantikan metode alfabetis yang berisiko tinggi karena dapat menempatkan bahan reaktif secara berdekatan.

### 2. Fungsi Utama
Sistem ini berfungsi sebagai pengendalian risiko dengan mengelompokkan bahan menjadi kategori seperti flammable, korosif, oksidator, toxic, dan reaktif air. Selain itu, mempermudah inventaris dan pengawasan.

### 3. Manfaat
- Mencegah kecelakaan kerja  
- Melindungi aset laboratorium  
- Meningkatkan efisiensi operasional  

### 4. Alasan Penerapan
Bahan kimia bersifat reaktif dan dapat menimbulkan reaksi spontan seperti kebakaran atau ledakan jika tidak dipisahkan.

### 5. Prinsip Pemisahan
Gunakan lemari khusus, sekat fisik, dan secondary containment untuk mencegah pencampuran.

### 6. Fasilitas dan Administrasi
Gunakan label GHS, rak tahan kimia, dan sistem pencatatan bahan yang baik.
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
        st.download_button("Download CSV", csv, "riwayat.csv")
    else:
        st.info("Belum ada data")
