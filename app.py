import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Chemical Compatibility System",
    page_icon="🧪",
    layout="wide"
)

# =========================
# DATABASE
# =========================
chemical_db = {
"HCl":"Asam","H2SO4":"Asam","HNO3":"Asam","CH3COOH":"Asam",
"NaOH":"Basa","KOH":"Basa","NH3":"Basa",
"KMnO4":"Oksidator","H2O2":"Oksidator",
"Etanol":"Flammable","Benzena":"Flammable","Aseton":"Flammable",
"Na":"Reaktif Air","K":"Reaktif Air",
"H2O":"Air",
"Hg":"Toxic","Pb":"Toxic",
"NaCl":"Inert","CO2":"Gas","CH4":"Flammable"
}

# =========================
# SESSION
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# LOGIKA
# =========================
def check_compatibility(t1, t2):
    if "Asam" in [t1,t2] and "Basa" in [t1,t2]:
        return "DANGER","Reaksi eksoterm (panas tinggi)"
    if "Oksidator" in [t1,t2] and "Flammable" in [t1,t2]:
        return "DANGER","Risiko kebakaran/ledakan"
    if "Reaktif Air" in [t1,t2] and "Air" in [t1,t2]:
        return "DANGER","Reaksi hebat dengan air"
    if t1 == t2:
        return "SAFE","Relatif stabil"
    return "WARNING","Perlu kehati-hatian"

def smart_ai_analysis(t1,t2):
    if "Asam" in [t1,t2] and "Basa" in [t1,t2]:
        return "High","Reaksi netralisasi menghasilkan panas tinggi.","Pisahkan penyimpanan asam dan basa"
    if "Oksidator" in [t1,t2] and "Flammable" in [t1,t2]:
        return "High","Berpotensi kebakaran/ledakan.","Jauhkan oksidator dari bahan organik"
    if "Reaktif Air" in [t1,t2] and "Air" in [t1,t2]:
        return "High","Reaksi eksplosif dengan air.","Simpan di tempat kering"
    if t1 == t2:
        return "Low","Stabil dalam kategori yang sama.","Boleh disimpan bersama"
    return "Medium","Interaksi tidak langsung mungkin terjadi.","Gunakan pemisahan sekunder"

# =========================
# MENU SIDEBAR
# =========================
menu = st.sidebar.radio("📌 Menu", [
    "🏠 Home",
    "🔍 Cek Kompatibilitas",
    "📚 Materi",
    "🧪 Database",
    "📊 Dashboard",
    "ℹ Tentang"
])

# =========================
# HOME
# =========================
if menu == "🏠 Home":
    st.title("🧪 Chemical Storage Compatibility System")

    st.markdown("""
    Sistem ini dirancang untuk membantu analisis kompatibilitas penyimpanan **dua bahan kimia**
    menggunakan konsep **FCOT (Flow, Check, Organize, Track)**.
    """)

    # Pengertian
    st.subheader("📖 Pengertian")
    st.write("""
    Kompatibilitas penyimpanan bahan kimia adalah kemampuan dua atau lebih bahan kimia
    untuk disimpan bersama tanpa menimbulkan reaksi berbahaya seperti ledakan, kebakaran,
    atau pembentukan gas beracun. Pengelolaan yang tepat sangat penting dalam menjaga
    keselamatan kerja di laboratorium dan industri.
    """)

    # Tujuan
    st.subheader("🎯 Tujuan")
    st.write("""
    - Menentukan apakah dua bahan kimia aman disimpan bersama  
    - Mencegah terjadinya reaksi berbahaya  
    - Memberikan rekomendasi penyimpanan sesuai standar K3  
    - Membantu pengelolaan bahan kimia secara sistematis  
    - Meningkatkan keselamatan kerja di laboratorium  
    """)

    # Fitur
    st.subheader("🔬 Fitur Utama")
    st.write("""
    - 🔍 Cek kompatibilitas dua bahan kimia  
    - 🧠 AI analisis risiko  
    - 📊 Dashboard monitoring  
    - 📚 Materi pembelajaran  
    - 🧪 Database bahan kimia  
    """)

# =========================
# CEK KOMPATIBILITAS
# =========================
elif menu == "🔍 Cek Kompatibilitas":
    st.title("🔍 Cek Kompatibilitas")

    c1, c2 = st.columns(2)

    with c1:
        chem1 = st.selectbox("Bahan 1", list(chemical_db.keys()))
    with c2:
        chem2 = st.selectbox("Bahan 2", list(chemical_db.keys()))

    if st.button("Cek"):
        t1 = chemical_db[chem1]
        t2 = chemical_db[chem2]

        status, desc = check_compatibility(t1,t2)

        st.subheader("✅ Hasil Utama")
        st.write(f"{chem1} ({t1}) vs {chem2} ({t2})")

        if status == "SAFE":
            st.success(desc)
        elif status == "DANGER":
            st.error(desc)
        else:
            st.warning(desc)

        # AI
        st.markdown("## 🧠 AI Smart Analysis")
        risk, exp, reco = smart_ai_analysis(t1,t2)

        st.write(f"**Risk Level:** {risk}")
        st.write(f"**Analisis:** {exp}")
        st.write(f"**Rekomendasi:** {reco}")

        # Simpan history
        st.session_state.history.append({
            "Bahan1": chem1,
            "Bahan2": chem2,
            "Status": status,
            "Risk": risk
        })

# =========================
# MATERI
# =========================
elif menu == "📚 Materi":
    st.title("📚 Materi Kompatibilitas Kimia")

    st.subheader("1. Pengertian")
    st.write("Kompatibilitas adalah kemampuan bahan kimia disimpan bersama tanpa reaksi berbahaya.")

    st.subheader("2. Prinsip Dasar")
    st.write("""
    - Asam ≠ Basa  
    - Oksidator ≠ Flammable  
    - Reaktif air ≠ Air  
    """)

    st.subheader("3. Konsep FCOT")
    st.write("""
    Flow → Input pengguna  
    Check → Analisis sistem  
    Organize → Pengelompokan  
    Track → Monitoring  
    """)

    st.subheader("4. Contoh Kasus")
    st.write("HCl + NaOH → Reaksi eksoterm (tidak boleh disimpan bersama)")

# =========================
# DATABASE
# =========================
elif menu == "🧪 Database":
    st.title("🧪 Database Kimia")

    df = pd.DataFrame(list(chemical_db.items()), columns=["Bahan","Kategori"])
    st.dataframe(df, use_container_width=True)

# =========================
# DASHBOARD
# =========================
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard Monitoring")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)

        st.subheader("Statistik Status")
        st.bar_chart(df["Status"].value_counts())

        st.subheader("Statistik Risiko")
        st.bar_chart(df["Risk"].value_counts())
    else:
        st.info("Belum ada data")

# =========================
# TENTANG
# =========================
elif menu == "ℹ Tentang":
    st.title("ℹ Tentang")

    st.write("""
    Website ini dibuat untuk membantu analisis kompatibilitas penyimpanan bahan kimia
    secara digital berbasis konsep FCOT dan AI sederhana.

    Teknologi:
    - Python
    - Streamlit
    - Rule-based + AI logic
    """)
