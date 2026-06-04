import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from database import get_chemical_database, get_ghs_images
from analyzer import analyze_compatibility

st.set_page_config(page_title="FCOT Chemical System PRO", page_icon="🧪", layout="wide")

st.markdown("""
<style>
.main-title {font-size:48px; font-weight:bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
.section-title {font-size:28px; font-weight:bold; color:#2c3e50; border-bottom: 3px solid #667eea; padding-bottom:10px;}
.status-card {padding:20px; border-radius:10px; font-weight:bold; font-size:18px; text-align:center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
.safe {background: linear-gradient(135deg, #00c853 0%, #00a040 100%); color: white;}
.danger {background: linear-gradient(135deg, #ff1744 0%, #d01e3c 100%); color: white;}
.warning {background: linear-gradient(135deg, #ff9100 0%, #e67e22 100%); color: white;}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []

st.sidebar.markdown("<div style='text-align:center; padding:20px 0;'><h1 style='font-size:32px; margin:0;'>🧪</h1><h2 style='color:#667eea;'>FCOT PRO</h2></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio("📌 MENU", ["🏠 Home", "🔍 Cek", "📊 Dashboard", "❤️ Favorit", "📚 Panduan", "🧪 Database", "⚙️ Pengaturan"])

if menu == "🏠 Home":
    st.markdown("<div class='main-title'>🧪 FCOT CHEMICAL SYSTEM PRO</div>", unsafe_allow_html=True)
    st.markdown("Sistem analisis keamanan bahan kimia berbasis FCOT dan GHS.")
    
elif menu == "🔍 Cek":
    st.markdown("<h2 class='section-title'>🔍 Cek Kompatibilitas</h2>", unsafe_allow_html=True)
    
    chemical_db = get_chemical_database()
    ghs_images = get_ghs_images()
    
    col1, col2 = st.columns(2)
    with col1:
        chem1 = st.selectbox("Bahan 1", list(chemical_db.keys()))
    with col2:
        chem2 = st.selectbox("Bahan 2", list(chemical_db.keys()))
    
    if st.button("✅ Cek Sekarang"):
        with st.spinner("🔬 Menganalisis..."):
            import time
            time.sleep(1)
        
        t1 = chemical_db[chem1]
        t2 = chemical_db[chem2]
        status, penjelasan, penyimpanan = analyze_compatibility(t1, t2)
        
        status_class = "safe" if "AMAN" in status else ("danger" if "BERBAHAYA" in status else "warning")
        st.markdown(f"<div class='status-card {status_class}'>{status}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(ghs_images.get(t1, ""), width=120)
            st.write(f"**{chem1}** ({t1})")
        with col2:
            st.image(ghs_images.get(t2, ""), width=120)
            st.write(f"**{chem2}** ({t2})")
        
        st.markdown("### 🧠 Penjelasan")
        st.info(penjelasan)
        st.markdown("### 📦 Penyimpanan")
        st.warning(penyimpanan)
        
        record = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Bahan 1": chem1,
            "Bahan 2": chem2,
            "Hasil": status.replace("❌ ", "").replace("⚠️ ", "").replace("✅ ", "")
        }
        st.session_state.history.append(record)
        
        if st.button("❤️ Tambah Favorit"):
            fav = f"{chem1} + {chem2}"
            if fav not in st.session_state.favorites:
                st.session_state.favorites.append(fav)
                st.success("✅ Ditambahkan ke favorit!")

elif menu == "📊 Dashboard":
    st.markdown("<h2 class='section-title'>📊 Dashboard</h2>", unsafe_allow_html=True)
    
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", len(df))
        col2.metric("Aman", len(df[df["Hasil"].str.contains("AMAN", na=False)]))
        col3.metric("Berbahaya", len(df[df["Hasil"].str.contains("BERBAHAYA", na=False)]))
        
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button("📥 Download CSV", csv, f"fcot_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    else:
        st.info("Belum ada data")

elif menu == "❤️ Favorit":
    st.markdown("<h2 class='section-title'>❤️ Favorit</h2>", unsafe_allow_html=True)
    if st.session_state.favorites:
        for i, fav in enumerate(st.session_state.favorites):
            col1, col2 = st.columns([4, 1])
            col1.write(f"{i+1}. {fav}")
            if col2.button("❌", key=f"del_{i}"):
                st.session_state.favorites.pop(i)
                st.rerun()
    else:
        st.info("Tidak ada favorit")

elif menu == "📚 Panduan":
    st.markdown("<h2 class='section-title'>📚 FCOT & GHS</h2>", unsafe_allow_html=True)
    st.markdown("""
    **FCOT:**
    - 🔥 Flammable (Mudah Terbakar)
    - 🧪 Corrosive (Korosif)
    - ⚡ Oxidizer (Pengoksidasi)
    - ☠️ Toxic (Beracun)
    
    **GHS Icons:**
    - GHS02: Flammable
    - GHS05: Corrosive
    - GHS03: Oxidizing
    - GHS06: Acute Toxicity
    """)

elif menu == "🧪 Database":
    st.markdown("<h2 class='section-title'>🧪 Database</h2>", unsafe_allow_html=True)
    chemical_db = get_chemical_database()
    db_list = [{"Nama": name, "Kategori": category} for name, category in chemical_db.items()]
    df_db = pd.DataFrame(db_list)
    st.dataframe(df_db, use_container_width=True)

elif menu == "⚙️ Pengaturan":
    st.markdown("<h2 class='section-title'>⚙️ Pengaturan</h2>", unsafe_allow_html=True)
    with st.expander("Data & Privasi"):
        if st.button("🗑️ Hapus Semua Data"):
            st.session_state.history = []
            st.session_state.favorites = []
            st.success("✅ Data dihapus!")
    with st.expander("Tentang"):
        st.write("**FCOT Chemical System PRO v2.0** - Aplikasi manajemen keamanan bahan kimia")
