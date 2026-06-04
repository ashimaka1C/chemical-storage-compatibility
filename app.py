import streamlit as st
import json

# ========================
# LOAD DATA
# ========================
@st.cache_data
def load_data():
    try:
        with open("chemical_data.json", "r") as f:
            return json.load(f)
    except:
        return {}

chemical_db = load_data()

# ========================
# VALIDASI DATA
# ========================
if not chemical_db:
    st.error("❌ Database bahan kimia kosong atau gagal dimuat!")
    st.stop()

# ========================
# INISIALISASI SESSION STATE (AMAN)
# ========================
if "chem1" not in st.session_state:
    st.session_state["chem1"] = list(chemical_db.keys())[0]

if "chem2" not in st.session_state:
    st.session_state["chem2"] = list(chemical_db.keys())[0]

# ========================
# UI PILIHAN BAHAN
# ========================
st.title("🧪 Chemical Compatibility Checker")

col1, col2 = st.columns(2)

with col1:
    chem1 = st.selectbox(
        "Pilih Bahan 1",
        options=list(chemical_db.keys()),
        key="chem1"
    )

with col2:
    chem2 = st.selectbox(
        "Pilih Bahan 2",
        options=list(chemical_db.keys()),
        key="chem2"
    )

# ========================
# LOGIKA CEK KOMPATIBILITAS
# ========================
if chem1 and chem2:
    data1 = chemical_db.get(chem1, {})
    data2 = chemical_db.get(chem2, {})

    st.subheader("🔍 Hasil Analisis")

    if data1 == data2:
        st.success("✅ Bahan kompatibel (indikasi awal sama)")
    else:
        st.warning("⚠️ Perlu pengecekan lanjutan (berbeda sifat)")

# ========================
# DEBUG (opsional)
# ========================
# st.write(st.session_state)
