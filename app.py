import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Chemical Compatibility System", layout="wide")

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
        return "DANGER","Reaksi eksoterm"
    if "Oksidator" in [t1,t2] and "Flammable" in [t1,t2]:
        return "DANGER","Risiko kebakaran"
    if "Reaktif Air" in [t1,t2] and "Air" in [t1,t2]:
        return "DANGER","Reaksi dengan air"
    if t1 == t2:
        return "SAFE","Stabil"
    return "WARNING","Perlu perhatian"

def smart_ai_analysis(t1,t2):
    if "Asam" in [t1,t2] and "Basa" in [t1,t2]:
        return "High","Netralisasi menghasilkan panas tinggi","Pisahkan total"
    if "Oksidator" in [t1,t2] and "Flammable" in [t1,t2]:
        return "High","Potensi kebakaran","Pisahkan jauh"
    if "Reaktif Air" in [t1,t2] and "Air" in [t1,t2]:
        return "High","Reaksi eksplosif","Hindari kontak air"
    if t1 == t2:
        return "Low","Stabil","Simpan bersama"
    return "Medium","Interaksi tidak langsung","Gunakan pemisahan"

# =========================
# SIDEBAR MENU
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
    
    🔬 Fitur:
    - Analisis kompatibilitas
    - AI rekomendasi
    - Dashboard monitoring
    - Materi pembelajaran
    """)

# =========================
# CEK
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

        st.subheader("Hasil")
        st.write(f"{chem1} ({t1}) vs {chem2} ({t2})")

        if status == "SAFE":
            st.success(desc)
        elif status == "DANGER":
            st.error(desc)
        else:
            st.warning(desc)

        st.markdown("## 🧠 AI Analysis")
        risk, exp, reco = smart_ai_analysis(t1,t2)

        st.write(f"**Risk:** {risk}")
        st.write(f"**Analisis:** {exp}")
        st.write(f"**Rekomendasi:** {reco}")

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
    st.write("Kompatibilitas penyimpanan adalah kemampuan bahan kimia untuk disimpan bersama tanpa reaksi berbahaya.")

    st.subheader("2. Prinsip Dasar")
    st.write("""
    - Asam tidak boleh dengan basa
    - Oksidator tidak dengan bahan organik
    - Reaktif air harus kering
    """)

    st.subheader("3. Konsep FCOT")
    st.write("""
    - Flow → alur sistem
    - Check → analisis
    - Organize → pengelompokan
    - Track → monitoring
    """)

    st.subheader("4. Contoh Kasus")
    st.write("HCl + NaOH → reaksi panas (tidak boleh disimpan bersama)")

# =========================
# DATABASE
# =========================
elif menu == "🧪 Database":
    st.title("🧪 Database Bahan Kimia")

    df = pd.DataFrame(list(chemical_db.items()), columns=["Bahan","Kategori"])
    st.dataframe(df)

# =========================
# DASHBOARD
# =========================
elif menu == "📊 Dashboard":
    st.title("📊 Dashboard")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)

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
    st.title("ℹ Tentang Sistem")

    st.write("""
    Website ini dibuat untuk membantu keselamatan laboratorium
    dalam penyimpanan bahan kimia menggunakan pendekatan digital.
    
    Dibangun dengan:
    - Python
    - Streamlit
    - Konsep FCOT
    """)
