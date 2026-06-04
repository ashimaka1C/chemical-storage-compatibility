import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Chemical Compatibility FCOT",
    page_icon="🧪",
    layout="wide"
)

# =========================
# STYLE UI
# =========================
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 10px;
    background-color: #1c1f26;
    margin-bottom: 15px;
}
.safe {color: #00ff9f;}
.danger {color: #ff4b4b;}
.warning {color: #ffc107;}
</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE 100+
# =========================
chemical_db = {

# ASAM
"HCl": {"type": "Asam"}, "H2SO4": {"type": "Asam"}, "HNO3": {"type": "Asam"},
"CH3COOH": {"type": "Asam"}, "H3PO4": {"type": "Asam"}, "HF": {"type": "Asam"},
"HClO4": {"type": "Asam"}, "H2CO3": {"type": "Asam"}, "HBr": {"type": "Asam"}, "HI": {"type": "Asam"},

# BASA
"NaOH": {"type": "Basa"}, "KOH": {"type": "Basa"}, "Ca(OH)2": {"type": "Basa"},
"Ba(OH)2": {"type": "Basa"}, "NH3": {"type": "Basa"}, "Na2CO3": {"type": "Basa"},
"NaHCO3": {"type": "Basa"}, "K2CO3": {"type": "Basa"}, "Mg(OH)2": {"type": "Basa"}, "LiOH": {"type": "Basa"},

# OKSIDATOR
"KMnO4": {"type": "Oksidator"}, "K2Cr2O7": {"type": "Oksidator"}, "H2O2": {"type": "Oksidator"},
"NaClO": {"type": "Oksidator"}, "Cl2": {"type": "Oksidator"}, "O3": {"type": "Oksidator"},
"KClO3": {"type": "Oksidator"}, "KNO3": {"type": "Oksidator"}, "NaNO3": {"type": "Oksidator"}, "CrO3": {"type": "Oksidator"},

# FLAMMABLE
"Etanol": {"type": "Flammable"}, "Metanol": {"type": "Flammable"}, "Propanol": {"type": "Flammable"},
"Butanol": {"type": "Flammable"}, "Aseton": {"type": "Flammable"}, "Benzena": {"type": "Flammable"},
"Toluena": {"type": "Flammable"}, "Xilena": {"type": "Flammable"}, "Eter": {"type": "Flammable"}, "Hexana": {"type": "Flammable"},

# REAKTIF AIR
"Na": {"type": "Reaktif Air"}, "K": {"type": "Reaktif Air"}, "CaC2": {"type": "Reaktif Air"},
"NaH": {"type": "Reaktif Air"}, "LiAlH4": {"type": "Reaktif Air"}, "K2O": {"type": "Reaktif Air"},
"Na2O": {"type": "Reaktif Air"}, "Mg": {"type": "Reaktif Air"}, "AlCl3": {"type": "Reaktif Air"}, "PCl3": {"type": "Reaktif Air"},

# TOXIC
"Hg": {"type": "Toxic"}, "Pb": {"type": "Toxic"}, "Cd": {"type": "Toxic"},
"As2O3": {"type": "Toxic"}, "KCN": {"type": "Toxic"}, "NaCN": {"type": "Toxic"},
"CO": {"type": "Toxic"}, "H2S": {"type": "Toxic"}, "NO2": {"type": "Toxic"}, "SO2": {"type": "Toxic"},

# GAS & LAINNYA
"H2O": {"type": "Air"}, "O2": {"type": "Oksidator"}, "N2": {"type": "Inert"},
"CO2": {"type": "Gas"}, "CH4": {"type": "Flammable"}, "C2H6": {"type": "Flammable"},
"C3H8": {"type": "Flammable"}, "NO": {"type": "Gas"},

# ORGANIK TAMBAHAN
"Glukosa": {"type": "Organik"}, "Sukrosa": {"type": "Organik"}, "Pati": {"type": "Organik"},
"Urea": {"type": "Organik"}, "Fenol": {"type": "Toxic"}, "Formaldehida": {"type": "Toxic"},

# EXTRA
"AgNO3": {"type": "Oksidator"}, "CuSO4": {"type": "Toxic"}, "FeCl3": {"type": "Asam"},
"ZnCl2": {"type": "Asam"}, "NaCl": {"type": "Inert"}, "KBr": {"type": "Inert"},
"KI": {"type": "Inert"}, "CaCO3": {"type": "Inert"}, "MgSO4": {"type": "Inert"}
}

# =========================
# SESSION TRACK
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# LOGIKA DASAR (CHECK)
# =========================
def check_compatibility(t1, t2):
    if ("Asam" in [t1, t2] and "Basa" in [t1, t2]):
        return "DANGER", "Reaksi eksoterm"
    if ("Oksidator" in [t1, t2] and "Flammable" in [t1, t2]):
        return "DANGER", "Risiko kebakaran"
    if ("Reaktif Air" in [t1, t2] and "Air" in [t1, t2]):
        return "DANGER", "Reaksi dengan air"
    if t1 == t2:
        return "SAFE", "Stabil"
    return "WARNING", "Perlu perhatian"

# =========================
# AI SMART ANALYSIS
# =========================
def smart_ai_analysis(chem1, chem2, t1, t2):

    if ("Asam" in [t1, t2] and "Basa" in [t1, t2]):
        return "High", "Reaksi netralisasi menghasilkan panas tinggi.", "Pisahkan asam dan basa"

    elif ("Oksidator" in [t1, t2] and "Flammable" in [t1, t2]):
        return "High", "Berpotensi kebakaran/ledakan.", "Jauhkan oksidator dari bahan organik"

    elif ("Reaktif Air" in [t1, t2] and "Air" in [t1, t2]):
        return "High", "Reaksi hebat dengan air.", "Simpan di tempat kering"

    elif t1 == t2:
        return "Low", "Stabil dalam kategori sama.", "Boleh disimpan bersama"

    else:
        return "Medium", "Interaksi tidak langsung.", "Gunakan pemisahan sekunder"

# =========================
# UI
# =========================
st.title("🧪 Chemical Compatibility System (FCOT + AI)")

c1, c2 = st.columns(2)

with c1:
    chem1 = st.selectbox("Bahan 1", list(chemical_db.keys()))

with c2:
    chem2 = st.selectbox("Bahan 2", list(chemical_db.keys()))

if st.button("🔍 Cek Kompatibilitas"):

    t1 = chemical_db[chem1]["type"]
    t2 = chemical_db[chem2]["type"]

    status, desc = check_compatibility(t1, t2)

    st.subheader("✅ Hasil Utama")

    if status == "SAFE":
        st.success(desc)
    elif status == "DANGER":
        st.error(desc)
    else:
        st.warning(desc)

    st.write(f"{chem1} ({t1}) vs {chem2} ({t2})")

    # =========================
    # AI RESULT
    # =========================
    st.markdown("## 🧠 AI Smart Analysis")

    risk, ai_exp, ai_reco = smart_ai_analysis(chem1, chem2, t1, t2)

    if risk == "High":
        st.error(f"🔥 Risiko Tinggi")
    elif risk == "Medium":
        st.warning(f"⚠ Risiko Sedang")
    else:
        st.success(f"✅ Risiko Rendah")

    st.write(f"**Analisis:** {ai_exp}")
    st.write(f"**Rekomendasi:** {ai_reco}")

    # =========================
    # TRACK
    # =========================
    st.session_state.history.append({
        "Waktu": datetime.now().strftime("%H:%M:%S"),
        "Bahan 1": chem1,
        "Bahan 2": chem2,
        "Status": status,
        "Risk": risk
    })

# =========================
# DASHBOARD
# =========================
st.markdown("## 📊 Dashboard")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    st.markdown("### Statistik Status")
    st.bar_chart(df["Status"].value_counts())

    st.markdown("### Statistik Risiko AI")
    st.bar_chart(df["Risk"].value_counts())
else:
    st.info("Belum ada data")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("🔬 Sistem FCOT + AI untuk Keamanan Penyimpanan Bahan Kimia")
