import streamlit as st
import pandas as pd
import time
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="FCOT Chemical System", layout="wide")

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
# DATABASE FCOT
# =========================
base = {
"HCl - Asam Klorida":"Corrosive",
"H2SO4 - Asam Sulfat":"Corrosive",
"HNO3 - Asam Nitrat":"Oxidizer",

"NaOH - Natrium Hidroksida":"Corrosive",
"KOH - Kalium Hidroksida":"Corrosive",

"KMnO4 - Kalium Permanganat":"Oxidizer",
"H2O2 - Hidrogen Peroksida":"Oxidizer",

"Etanol - Alkohol":"Flammable",
"Benzena - Benzene":"Flammable",
"Aseton - Acetone":"Flammable",

"Hg - Merkuri":"Toxic",
"Pb - Timbal":"Toxic",

"NaCl - Natrium Klorida":"Safe"
}

chemical_db = {}
for i in range(20):
    for k,v in base.items():
        chemical_db[f"{k} ({i})"] = v

# =========================
# GHS IMAGE
# =========================
ghs_images = {
"Flammable":"https://upload.wikimedia.org/wikipedia/commons/6/6c/GHS-pictogram-flamme.svg",
"Corrosive":"https://upload.wikimedia.org/wikipedia/commons/5/5a/GHS-pictogram-acid.svg",
"Oxidizer":"https://upload.wikimedia.org/wikipedia/commons/1/1c/GHS-pictogram-rondflam.svg",
"Toxic":"https://upload.wikimedia.org/wikipedia/commons/3/3b/GHS-pictogram-skull.svg"
}

# =========================
# SESSION
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# ANALISIS FCOT
# =========================
def analyze(t1, t2):

    if "Flammable" in [t1,t2] and "Oxidizer" in [t1,t2]:
        return ("❌ BERBAHAYA",
        "Flammable + Oxidizer → kebakaran atau ledakan besar.",
        "Pisahkan di lemari khusus.")

    elif "Corrosive" in [t1,t2] and "Toxic" in [t1,t2]:
        return ("❌ BERBAHAYA",
        "Korosif dapat merusak wadah → toxic bocor.",
        "Gunakan secondary containment.")

    elif "Oxidizer" in [t1,t2] and "Toxic" in [t1,t2]:
        return ("❌ BERBAHAYA",
        "Mempercepat pembentukan gas beracun.",
        "Pisahkan ketat.")

    elif "Flammable" in [t1,t2] and "Toxic" in [t1,t2]:
        return ("⚠ PERLU PERHATIAN",
        "Kebakaran + gas beracun.",
        "Ventilasi baik.")

    elif "Corrosive" in [t1,t2] and "Flammable" in [t1,t2]:
        return ("⚠ PERLU PERHATIAN",
        "Korosi → kebocoran bahan flammable.",
        "Gunakan wadah tahan korosi.")

    elif t1 == t2:
        return ("✔ AMAN",
        "Kategori sama → relatif stabil.",
        "Simpan bersama.")

    else:
        return ("⚠ PERLU PERHATIAN",
        "Tidak reaktif langsung tapi tetap berisiko.",
        "Pisahkan sekunder.")

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
    st.markdown("<div class='title'>🧪 FCOT Chemical Storage System</div>", unsafe_allow_html=True)

    st.write("Sistem penyimpanan bahan kimia berbasis FCOT dan standar GHS.")

# =========================
# CEK
# =========================
elif menu == "🔍 Cek":

    st.title("🔍 Cek Kompatibilitas FCOT + GHS")

    c1,c2 = st.columns(2)
    with c1:
        chem1 = st.selectbox("Bahan 1", list(chemical_db.keys()))
    with c2:
        chem2 = st.selectbox("Bahan 2", list(chemical_db.keys()))

    if st.button("Cek Sekarang"):

        with st.spinner("🔬 Menganalisis..."):
            time.sleep(1.5)

        t1 = chemical_db[chem1]
        t2 = chemical_db[chem2]

        status, penjelasan, penyimpanan = analyze(t1,t2)

        if "AMAN" in status:
            st.markdown(f"<h2 class='safe'>{status}</h2>", unsafe_allow_html=True)
        elif "BERBAHAYA" in status:
            st.markdown(f"<h2 class='danger'>{status}</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 class='warning'>{status}</h2>", unsafe_allow_html=True)

        # GHS IMAGE DISPLAY
        col1, col2 = st.columns(2)

        with col1:
            st.image(ghs_images.get(t1, ""), width=120)
            st.write(f"{chem1} ({t1})")

        with col2:
            st.image(ghs_images.get(t2, ""), width=120)
            st.write(f"{chem2} ({t2})")

        st.subheader("🧠 Penjelasan")
        st.write(penjelasan)

        st.subheader("📦 Penyimpanan")
        st.info(penyimpanan)

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

    st.title("📚 Sistem FCOT & GHS")

    st.markdown("""
### FCOT
- Flammable  
- Corrosive  
- Oxidizer  
- Toxic  

### Simbol GHS
- GHS02 🔥 Flammable  
- GHS05 🧪 Corrosive  
- GHS03 ⚡ Oxidizer  
- GHS06 ☠️ Toxic  

Digunakan secara global dalam K3 laboratorium.
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
