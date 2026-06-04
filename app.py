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
Sistem penyimpanan bahan kimia kompatibel adalah suatu metode penataan, pengelompokan, dan penempatan zat-zat kimia di dalam ruang penyimpanan atau laboratorium yang didasarkan sepenuhnya pada sifat fisika dan karakteristik kimia masing-masing bahan. Sistem ini secara spesifik menjauhkan zat-zat yang jika bercampur dapat memicu reaksi berbahaya. Di dalam dunia sains dan industri, metode ini menggantikan sistem penyimpanan konvensional berbasis urutan alfabetis. Penyimpanan berbasis alfabetis dinilai sangat berbahaya karena sering kali menempatkan dua zat yang saling reaktif secara berdampingan, seperti menempatkan asam kuat tepat di sebelah basa kuat atau bahan organik di samping oksidator. Fondasi utama dari sistem kompatibel ini adalah analisis mendalam terhadap dokumen Safety Data Sheet (SDS) atau Lembar Data Keselamatan Bahan yang menyertai setiap zat kimia.

### 2. Fungsi Utama
Fungsi utama dari sistem penyimpanan kompatibel adalah sebagai benteng pertahanan pertama dalam mengendalikan risiko bahaya di area penyimpanan. Secara teknis, sistem ini berfungsi untuk mengisolasi potensi bahaya dengan cara mengelompokkan bahan kimia ke dalam kategori spesifikasi yang sejenis, seperti kelompok mudah terbakar (flammable), korosif, oksidator, beracun (toxic), dan reaktif terhadap air. Selain itu, fungsi penataan ini juga mempermudah pengawasan masa kedaluwarsa zat serta mempercepat proses audit inventaris berkala. Dengan pengelompokan yang sistematis, pengelola laboratorium dapat dengan mudah mengenali letak bahan, memastikan bahwa setiap zat disimpan dalam kondisi lingkungan (suhu dan kelembapan) yang tepat, serta mengidentifikasi potensi kerusakan wadah secara lebih dini sebelum menimbulkan dampak yang lebih luas.

### 3. Manfaat
Penerapan sistem penyimpanan bahan kimia berdasarkan kompatibilitas memberikan keuntungan yang luas bagi institusi, yang dapat dijabarkan ke dalam beberapa poin krusial berikut:Mencegah Kecelakaan Kerja Fatal: Melindungi laboran, peneliti, dan petugas gudang dari risiko cedera parah akibat ledakan spontan, kebakaran, maupun keracunan akibat paparan gas toksik.Meminimalkan Efek Domino Saat Bencana: Mencegah terjadinya eskalasi atau pembesaran skala bencana saat terjadi gempa bumi atau kebakaran eksternal, karena botol-botol kimia yang pecah tidak akan memicu reaksi berantai baru.Melindungi Aset dan Fasilitas Fisik: Menjaga gedung, infrastruktur ruangan, serta instrumen laboratorium yang bernilai tinggi dari kerusakan fatal akibat kebakaran atau korosi yang disebabkan oleh uap asam/basa.Memperpanjang Masa Simpan Bahan Kimia: Menghindari kontaminasi silang antar-uap zat kimia di dalam ruangan, sehingga kualitas dan efektivitas senyawa kimia tetap terjaga dengan baik dalam jangka panjang.Meningkatkan Efisiensi Tata Kelola Inventaris: Mempercepat proses pencarian, pengambilan, dan pengembalian zat kimia karena setiap bahan telah terpetakan secara sistematis berdasarkan kelompoknya.Mempermudah Penanggulangan Situasi Darurat: Membantu tim pemadam kebakaran atau tim K3 dalam memetakan area risiko saat terjadi kebocoran, sehingga proses evakuasi dan netralisasi zat dapat dilakukan secara cepat dan tepat.Menjamin Kepatuhan Hukum dan Regulasi: Memastikan laboratorium atau industri memenuhi standar baku keselamatan kerja nasional maupun internasional, seperti audit ISO atau akreditasi laboratorium.

### 4. Alasan Penerapan
Alasan mendasar mengapa sistem penyimpanan kompatibel bersifat wajib dan tidak dapat ditawar adalah karena sifat alami bahan kimia yang tidak pernah stabil secara absolut. Banyak senyawa kimia yang memiliki kecenderungan kuat untuk bereaksi hebat secara spontan ketika bersentuhan dengan senyawa dari kelompok lain. Sebagai contoh, interaksi antara cairan mudah terbakar dengan zat oksidator dapat menyulut api instan tanpa memerlukan sumber percikan eksternal. Begitu pula dengan bahan reaktif air seperti logam natrium yang akan meledak jika terkena kelembapan udara atau percikan air. Tanpa adanya sistem pemisahan yang terstruktur, probabilitas terjadinya kecelakaan kerja akibat kelalaian manusia (human error), seperti botol tersenggol atau kebocoran wadah, akan selalu mengancam keselamatan jiwa dan keberlangsungan operasional.

### 5. Prinsip Pemisahan
Dalam mengeksekusi sistem ini, terdapat prinsip pemisahan fisik (segregation) yang harus dipatuhi secara ketat. Pemisahan tidak boleh sekadar berupa pemberian jarak di atas rak yang sama, melainkan harus menggunakan sekat fisik yang tidak dapat ditembus, lemari penyimpanan khusus (seperti flammable cabinet), atau bahkan penempatan di ruangan yang berbeda. Tantangan tersendiri muncul ketika suatu zat memiliki bahaya ganda (multiple hazards), contohnya zat yang bersifat korosif sekaligus mudah terbakar. Dalam kondisi kompleks seperti ini, aturan yang berlaku adalah memprioritaskan pemisahan berdasarkan sifat bahaya yang paling dominan atau risiko yang paling ekstrem, yang kemudian wajib didukung dengan penggunaan wadah penampung sekunder (secondary containment) berupa baki antikorosi untuk mengurung tumpahan sekecil apa pun.

### 6. Fasilitas dan Administrasi
Kesempurnaan sistem penyimpanan ini tidak hanya bertumpu pada pengelompokan zat, melainkan juga harus didukung oleh kualitas fasilitas fisik dan manajemen administrasi yang disiplin. Rak penyimpanan harus terbuat dari material yang tahan terhadap paparan kimia, tidak boleh menempatkan bahan kimia berbahaya langsung di atas lantai, dan dilarang keras menyimpan botol kimia di atas ketinggian mata manusia demi menghindari cipratan pada wajah saat pengambilan. Dari sisi administrasi, manajemen pelabelan yang jelas menggunakan simbol bahaya standar global (Globally Harmonized System/GHS), pencantuman tanggal penerimaan bahan, serta tanggal pertama kali wadah dibuka menjadi instrumen vital yang memastikan bahwa seluruh rantai pengawasan bahan kimia berjalan dengan sempurna dan sesuai dengan regulasi keselamatan kerja internasional.
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
