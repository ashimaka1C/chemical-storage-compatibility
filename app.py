import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from database import get_chemical_database, get_ghs_images
from analyzer import analyze_compatibility
from utils import get_safety_color, format_timestamp

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="FCOT Chemical System PRO",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# CUSTOM STYLING
# =========================
st.markdown("""
<style>
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Titles */
    .main-title {
        font-size: 48px;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .section-title {
        font-size: 28px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 20px;
        margin-bottom: 15px;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
    }
    
    /* Status Cards */
    .status-card {
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .safe {
        background: linear-gradient(135deg, #00c853 0%, #00a040 100%);
        color: white;
    }
    
    .danger {
        background: linear-gradient(135deg, #ff1744 0%, #d01e3c 100%);
        color: white;
    }
    
    .warning {
        background: linear-gradient(135deg, #ff9100 0%, #e67e22 100%);
        color: white;
    }
    
    /* Info Boxes */
    .info-box {
        background: #e3f2fd;
        border-left: 5px solid #2196F3;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Chart Container */
    .chart-container {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 10px;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #667eea;
        margin: 10px 0;
    }
    
    .metric-label {
        color: #666;
        font-size: 14px;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Table Styling */
    .stDataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Chemical Card */
    .chemical-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px;
    }
    
    .chemical-name {
        font-weight: bold;
        color: #2c3e50;
        margin-top: 10px;
    }
    
    .chemical-category {
        color: #667eea;
        font-size: 14px;
        margin-top: 5px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE INITIALIZATION
# =========================
if "history" not in st.session_state:
    st.session_state.history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# =========================
# SIDEBAR MENU
# =========================
st.sidebar.markdown("""
<div style='text-align:center; padding:20px 0;'>
    <h1 style='font-size:32px; margin:0;'>🧪</h1>
    <h2 style='font-size:18px; margin:5px 0; color:#667eea;'>FCOT PRO</h2>
    <p style='font-size:12px; color:#666; margin:10px 0;'>Chemical Safety System</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📌 MENU UTAMA",
    [
        "🏠 Home",
        "🔍 Cek Kompatibilitas",
        "📊 Dashboard",
        "❤️ Favorit",
        "📚 Panduan",
        "🧪 Database",
        "⚙️ Pengaturan"
    ],
    key="main_menu"
)

st.sidebar.markdown("---")

# Sidebar Info
with st.sidebar.expander("ℹ️ Informasi Aplikasi"):
    st.write("""
    **FCOT Chemical System PRO** adalah sistem analisis keamanan bahan kimia 
    berbasis standar FCOT dan GHS.
    
    - **FCOT**: Flammable, Corrosive, Oxidizer, Toxic
    - **GHS**: Globally Harmonized System
    
    Aplikasi ini membantu mengidentifikasi risiko kombinasi bahan kimia 
    dan memberikan rekomendasi penyimpanan yang aman.
    """)

# =========================
# PAGES
# =========================

# HOME PAGE
if menu == "🏠 Home":
    st.markdown("<div class='main-title'>🧪 FCOT CHEMICAL SYSTEM PRO</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <h3>🎯 Selamat Datang di FCOT Chemical System PRO</h3>
        <p>Sistem manajemen keamanan bahan kimia yang komprehensif dan mudah digunakan.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size:32px;'>🔍</div>
            <div class='metric-label'>CEK KOMPATIBILITAS</div>
            <p style='margin-top:10px; color:#666;'>Analisis keamanan kombinasi bahan kimia secara real-time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size:32px;'>📊</div>
            <div class='metric-label'>DASHBOARD ANALYTICS</div>
            <p style='margin-top:10px; color:#666;'>Visualisasi data dan insight keamanan bahan kimia</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size:32px;'>📚</div>
            <div class='metric-label'>PANDUAN LENGKAP</div>
            <p style='margin-top:10px; color:#666;'>Materi edukasi tentang FCOT dan GHS</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features
    st.markdown("<h2 class='section-title'>✨ Fitur Utama</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Analisis Cepat
        - Cek kompatibilitas dalam hitungan detik
        - Database 250+ bahan kimia
        - Rekomendasi penyimpanan otomatis
        
        ### 📈 Data Analytics
        - Dashboard komprehensif
        - Grafik dan visualisasi
        - Laporan trend analisis
        """)
    
    with col2:
        st.markdown("""
        ### 🛡️ Keamanan Tingkat Lanjut
        - Standar GHS terintegrasi
        - Alert sistem real-time
        - Panduan penanganan lengkap
        
        ### ❤️ Favorit & Histori
        - Simpan analisis favorit
        - Riwayat lengkap
        - Export data mudah
        """)

# CHECK COMPATIBILITY PAGE
elif menu == "🔍 Cek Kompatibilitas":
    st.markdown("<h2 class='section-title'>🔍 Cek Kompatibilitas Bahan Kimia</h2>", unsafe_allow_html=True)
    
    chemical_db = get_chemical_database()
    ghs_images = get_ghs_images()
    
    # Input Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Bahan Kimia 1** 🧪")
        chem1 = st.selectbox(
            "Pilih bahan pertama",
            list(chemical_db.keys()),
            key="chem1",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("**Bahan Kimia 2** 🧪")
        chem2 = st.selectbox(
            "Pilih bahan kedua",
            list(chemical_db.keys()),
            key="chem2",
            label_visibility="collapsed"
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        check_btn = st.button("✅ Cek Sekarang", use_container_width=True)
    with col2:
        swap_btn = st.button("🔄 Tukar", use_container_width=True)
    with col3:
        clear_btn = st.button("🗑️ Reset", use_container_width=True)
    
    if swap_btn:
        st.session_state.chem1, st.session_state.chem2 = st.session_state.chem2, st.session_state.chem1
        st.rerun()
    
    if clear_btn:
        st.session_state.chem1 = None
        st.session_state.chem2 = None
        st.rerun()
    
    if check_btn:
        with st.spinner("🔬 Menganalisis kombinasi bahan kimia..."):
            import time
            time.sleep(1)
        
        t1 = chemical_db[chem1]
        t2 = chemical_db[chem2]
        
        status, penjelasan, penyimpanan = analyze_compatibility(t1, t2)
        
        # Status Display
        status_class = "safe" if "AMAN" in status else ("danger" if "BERBAHAYA" in status else "warning")
        
        st.markdown(f"""
        <div class='status-card {status_class}'>
            {status}
        </div>
        """, unsafe_allow_html=True)
        
        # Chemical Display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='chemical-card'>
            """, unsafe_allow_html=True)
            st.image(ghs_images.get(t1, ""), width=120, use_column_width=False)
            st.markdown(f"""
                <div class='chemical-name'>{chem1}</div>
                <div class='chemical-category'>{t1}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='chemical-card'>
            """, unsafe_allow_html=True)
            st.image(ghs_images.get(t2, ""), width=120, use_container_width=False)
            st.markdown(f"""
                <div class='chemical-name'>{chem2}</div>
                <div class='chemical-category'>{t2}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Explanation Section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🧠 Penjelasan")
            st.info(penjelasan)
        
        with col2:
            st.markdown("### 📦 Rekomendasi Penyimpanan")
            st.warning(penyimpanan)
        
        # Save to History
        record = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Bahan 1": chem1,
            "Bahan 2": chem2,
            "Kategori 1": t1,
            "Kategori 2": t2,
            "Hasil": status.replace("❌ ", "").replace("⚠ ", "").replace("✔ ", "").replace("BERBAHAYA", "Berbahaya").replace("PERLU PERHATIAN", "Perlu Perhatian").replace("AMAN", "Aman"),
        }
        st.session_state.history.append(record)
        
        # Add to Favorites Button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❤️ Tambah ke Favorit"):
                fav = f"{chem1} + {chem2}"
                if fav not in st.session_state.favorites:
                    st.session_state.favorites.append(fav)
                    st.success("✅ Ditambahkan ke favorit!")
                else:
                    st.info("Sudah ada di favorit")
        
        with col2:
            if st.button("📋 Copy Hasil"):
                st.info(f"""
                Bahan 1: {chem1} ({t1})
                Bahan 2: {chem2} ({t2})
                Status: {status}
                """)

# DASHBOARD PAGE
elif menu == "📊 Dashboard":
    st.markdown("<h2 class='section-title'>📊 Dashboard Analytics</h2>", unsafe_allow_html=True)
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class='metric-card'>
                <div class='metric-value'>""" + str(len(df)) + """</div>
                <div class='metric-label'>Total Analisis</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            bahaya_count = len(df[df["Hasil"].str.contains("Berbahaya", na=False)])
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#ff1744;'>{bahaya_count}</div>
                <div class='metric-label'>Berbahaya</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            aman_count = len(df[df["Hasil"].str.contains("Aman", na=False)])
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#00c853;'>{aman_count}</div>
                <div class='metric-label'>Aman</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            perhatian_count = len(df[df["Hasil"].str.contains("Perlu Perhatian", na=False)])
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value' style='color:#ff9100;'>{perhatian_count}</div>
                <div class='metric-label'>Perlu Perhatian</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 class='section-title'>📈 Distribusi Hasil Analisis</h3>", unsafe_allow_html=True)
            result_counts = df["Hasil"].value_counts()
            colors = {"Berbahaya": "#ff1744", "Aman": "#00c853", "Perlu Perhatian": "#ff9100"}
            fig = px.pie(
                values=result_counts.values,
                names=result_counts.index,
                color_discrete_map=colors,
                hole=0.3
            )
            fig.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<h3 class='section-title'>🧪 Kategori Bahan Paling Dianalisis</h3>", unsafe_allow_html=True)
            all_cats = pd.concat([df["Kategori 1"], df["Kategori 2"]])
            cat_counts = all_cats.value_counts().head(6)
            fig = px.bar(
                x=cat_counts.index,
                y=cat_counts.values,
                labels={"x": "Kategori", "y": "Jumlah"},
                color=cat_counts.values,
                color_continuous_scale="Viridis"
            )
            fig.update_layout(height=400, xaxis_title="Kategori Bahan Kimia", yaxis_title="Frekuensi")
            st.plotly_chart(fig, use_container_width=True)
        
        # History Table
        st.markdown("<h3 class='section-title'>📋 Riwayat Analisis Lengkap</h3>", unsafe_allow_html=True)
        
        # Sort options
        col1, col2 = st.columns([3, 1])
        with col1:
            filter_result = st.multiselect(
                "Filter berdasarkan hasil",
                ["Berbahaya", "Aman", "Perlu Perhatian"],
                default=["Berbahaya", "Aman", "Perlu Perhatian"]
            )
        with col2:
            sort_order = st.radio("Urutan", ["Terbaru", "Terlama"], horizontal=True)
        
        filtered_df = df[df["Hasil"].isin(filter_result)].copy()
        if sort_order == "Terbaru":
            filtered_df = filtered_df.iloc[::-1]
        
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Export Options
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"fcot_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_data = df.to_json(orient="records", indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"fcot_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col3:
            if st.button("🗑️ Hapus Semua Histori"):
                st.session_state.history = []
                st.success("Histori dihapus!")
                st.rerun()
    
    else:
        st.info("📭 Belum ada data analisis. Mulai dengan melakukan pengecekan kompatibilitas!")

# FAVORITES PAGE
elif menu == "❤️ Favorit":
    st.markdown("<h2 class='section-title'>❤️ Favorit Analisis</h2>", unsafe_allow_html=True)
    
    if st.session_state.favorites:
        st.success(f"Total {len(st.session_state.favorites)} favorit tersimpan")
        
        for i, fav in enumerate(st.session_state.favorites):
            col1, col2, col3 = st.columns([4, 1, 1])
            
            with col1:
                st.markdown(f"**{i+1}. {fav}**")
            
            with col2:
                if st.button("🔄 Analisis", key=f"analyze_{i}"):
                    chem1, chem2 = fav.split(" + ")
                    st.session_state.chem1 = chem1
                    st.session_state.chem2 = chem2
                    st.switch_page("pages/check.py") if "pages/check.py" in dir() else st.info("Lanjut ke Cek Kompatibilitas")
            
            with col3:
                if st.button("❌", key=f"delete_{i}"):
                    st.session_state.favorites.pop(i)
                    st.rerun()
        
        if st.button("🗑️ Hapus Semua Favorit"):
            st.session_state.favorites = []
            st.rerun()
    
    else:
        st.info("📭 Tidak ada favorit. Tambahkan favorit saat menganalisis!")

# PANDUAN PAGE
elif menu == "📚 Panduan":
    st.markdown("<h2 class='section-title'>📚 Panduan FCOT & GHS</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["FCOT", "GHS", "Penyimpanan", "FAQ"])
    
    with tab1:
        st.markdown("""
        ## 🔥 FCOT (Chemical Categories)
        
        ### **F - Flammable (Mudah Terbakar)**
        - Zat yang mudah terbakar atau menghasilkan api
        - Contoh: Etanol, Benzena, Aseton
        - Penyimpanan: Wadah anti api, jauh dari sumber panas
        - Hazard: 🔥
        
        ### **C - Corrosive (Korosif)**
        - Zat yang dapat merusak atau membakar kulit
        - Contoh: HCl, H2SO4, NaOH
        - Penyimpanan: Wadah tahan korosi, jauh dari basa/asam
        - Hazard: 🧪
        
        ### **O - Oxidizer (Pengoksidasi)**
        - Zat yang mempercepat pembakaran
        - Contoh: KMnO4, H2O2, HNO3
        - Penyimpanan: Terpisah dari bahan mudah terbakar
        - Hazard: ⚡
        
        ### **T - Toxic (Beracun)**
        - Zat yang berbahaya bagi kesehatan
        - Contoh: Hg, Pb, Sianida
        - Penyimpanan: Dalam wadah tertutup, area terventilasi
        - Hazard: ☠️
        """)
    
    with tab2:
        st.markdown("""
        ## 🌍 GHS (Globally Harmonized System)
        
        Sistem standar internasional untuk klasifikasi dan pelabelan bahan kimia.
        
        ### **GHS02 - Flammable** 🔥
        - Zat mudah terbakar
        - Precautionary: Jauhkan dari panas, percikan, nyala api
        
        ### **GHS05 - Corrosive** 🧪
        - Zat korosif untuk kulit/mata
        - Precautionary: Gunakan sarung tangan, kacamata
        
        ### **GHS03 - Oxidizing** ⚡
        - Zat pengoksidasi
        - Precautionary: Terpisah dari zat mudah terbakar
        
        ### **GHS06 - Acute Toxicity** ☠️
        - Zat beracun
        - Precautionary: Hindari kontak langsung
        """)
    
    with tab3:
        st.markdown("""
        ## 📦 Panduan Penyimpanan Bahan Kimia
        
        ### **Prinsip Umum:**
        1. **Pisahkan Kategori**: Flammable, Oxidizer, Corrosive, Toxic
        2. **Ventilasi Baik**: Hindari penumpukan uap
        3. **Suhu Kontrol**: Jauh dari sumber panas
        4. **Wadah Tepat**: Sesuai jenis zat
        5. **Labeling Jelas**: Identifikasi mudah
        
        ### **Kombinasi Aman:**
        - ✅ Flammable + Flammable
        - ✅ Corrosive + Corrosive
        - ✅ Toxic + Toxic (dengan secondary containment)
        
        ### **Kombinasi Berbahaya:**
        - ❌ Flammable + Oxidizer = Ledakan
        - ❌ Corrosive + Toxic = Gas berbahaya
        - ❌ Oxidizer + Toxic = Reaksi eksplosif
        """)
    
    with tab4:
        st.markdown("""
        ## ❓ Pertanyaan Umum
        
        **Q: Apakah bahan yang sama kategori selalu aman?**
        A: Tidak selalu. Kompatibilitas tergantung pada sifat kimia spesifik.
        
        **Q: Berapa jarak pisah untuk penyimpanan?**
        A: Minimal 1-2 meter untuk kategori berbeda, tergantung regulasi lokal.
        
        **Q: Apa yang harus dilakukan jika ada kombinasi berbahaya?**
        A: Pisahkan segera, gunakan secondary containment, dan pastikan ventilasi.
        
        **Q: Bagaimana jika tidak punya wadah tahan korosi?**
        A: Gunakan secondary containment (wadah luar yang tahan) sebagai alternatif.
        
        **Q: Berapa lama bahan kimia bisa disimpan?**
        A: Tergantung jenis dan kondisi penyimpanan (lihat tanggal expired).
        """)

# DATABASE PAGE
elif menu == "🧪 Database":
    st.markdown("<h2 class='section-title'>🧪 Database Bahan Kimia</h2>", unsafe_allow_html=True)
    
    chemical_db = get_chemical_database()
    ghs_images = get_ghs_images()
    
    # Create DataFrame
    db_list = []
    for name, category in chemical_db.items():
        db_list.append({
            "Nama Bahan": name.split(" (")[0],
            "Kategori": category,
            "Kode": name.split(" (")[1].rstrip(")") if " (" in name else ""
        })
    
    df_db = pd.DataFrame(db_list)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search = st.text_input("🔍 Cari bahan kimia", placeholder="Cth: HCl, Etanol...")
    
    with col2:
        categories = st.multiselect(
            "📂 Filter kategori",
            df_db["Kategori"].unique(),
            default=df_db["Kategori"].unique()
        )
    
    with col3:
        sort_by = st.selectbox("📊 Urutkan", ["Nama A-Z", "Kategori", "Kode"])
    
    # Apply filters
    filtered_df = df_db[df_db["Kategori"].isin(categories)].copy()
    
    if search:
        filtered_df = filtered_df[
            filtered_df["Nama Bahan"].str.contains(search, case=False, na=False)
        ]
    
    if sort_by == "Nama A-Z":
        filtered_df = filtered_df.sort_values("Nama Bahan")
    elif sort_by == "Kategori":
        filtered_df = filtered_df.sort_values("Kategori")
    
    st.info(f"📊 Menampilkan {len(filtered_df)} dari {len(df_db)} bahan kimia")
    
    # Display as cards or table
    view_type = st.radio("📋 Tampilan", ["Tabel", "Kartu"], horizontal=True)
    
    if view_type == "Tabel":
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    else:
        cols = st.columns(3)
        for idx, row in filtered_df.iterrows():
            with cols[idx % 3]:
                category = row["Kategori"]
                st.markdown(f"""
                <div class='chemical-card'>
                    <img src='{ghs_images.get(category, "")}' width=80>
                    <div class='chemical-name'>{row['Nama Bahan']}</div>
                    <div class='chemical-category'>{category}</div>
                    <div style='font-size:12px; color:#999; margin-top:5px;'>Kode: {row['Kode']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Statistics
    st.markdown("---")
    st.markdown("<h3 class='section-title'>📊 Statistik Database</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Bahan", len(df_db))
    
    flammable_count = len(df_db[df_db["Kategori"] == "Flammable"])
    with col2:
        st.metric("🔥 Flammable", flammable_count)
    
    corrosive_count = len(df_db[df_db["Kategori"] == "Corrosive"])
    with col3:
        st.metric("🧪 Corrosive", corrosive_count)
    
    oxidizer_count = len(df_db[df_db["Kategori"] == "Oxidizer"])
    with col4:
        st.metric("⚡ Oxidizer", oxidizer_count)
    
    toxic_count = len(df_db[df_db["Kategori"] == "Toxic"])
    with col5:
        st.metric("☠️ Toxic", toxic_count)

# SETTINGS PAGE
elif menu == "⚙️ Pengaturan":
    st.markdown("<h2 class='section-title'>⚙️ Pengaturan Aplikasi</h2>", unsafe_allow_html=True)
    
    with st.expander("🎨 Tema & Display"):
        st.info("Tema sedang menggunakan default Streamlit. Tema custom akan tersedia di versi mendatang.")
    
    with st.expander("📊 Data & Privasi"):
        st.write("Data histori disimpan dalam session state browser Anda (tidak dikirim ke server).")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Semua Data"):
                if st.session_state.history:
                    json_data = json.dumps(st.session_state.history, indent=2, ensure_ascii=False)
                    st.download_button(
                        "Download JSON",
                        json_data,
                        f"fcot_backup_{datetime.now().strftime('%Y%m%d')}.json",
                        "application/json"
                    )
        
        with col2:
            if st.button("🗑️ Hapus Semua Data Lokal"):
                st.session_state.history = []
                st.session_state.favorites = []
                st.success("✅ Semua data lokal dihapus!")
    
    with st.expander("ℹ️ Tentang"):
        st.markdown("""
        **FCOT Chemical System PRO v2.0**
        
        Aplikasi manajemen keamanan bahan kimia berbasis FCOT dan GHS.
        
        **Fitur:**
        - ✅ Analisis kompatibilitas real-time
        - ✅ Database 250+ bahan kimia
        - ✅ Dashboard analytics komprehensif
        - ✅ Panduan lengkap
        - ✅ Export/Import data
        
        **Teknologi:**
        - Python 3.9+
        - Streamlit
        - Plotly
        - Pandas
        
        **Disclaimer:**
        Aplikasi ini untuk tujuan edukasi. Untuk operasi industri, 
        konsultasi dengan ahli keselamatan profesional.
        """)
    
    with st.expander("📞 Kontak & Support"):
        st.markdown("""
        **Butuh Bantuan?**
        
        - 📧 Email: support@fcotpro.local
        - 🌐 Website: www.fcotpro.local
        - 📱 WhatsApp: +62-xxx-xxxx-xxxx
        
        **Report Bug:**
        Laporkan bug atau fitur yang ingin ditambahkan di GitHub Issues.
        """)
