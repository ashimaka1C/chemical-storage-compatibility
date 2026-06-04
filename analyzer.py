"""
Modul analisis kompatibilitas bahan kimia FCOT
"""

def analyze_compatibility(t1, t2):
    """
    Menganalisis kompatibilitas dua bahan kimia
    
    Parameters:
    t1, t2: Kategori FCOT (Flammable, Corrosive, Oxidizer, Toxic, Safe)
    
    Returns:
    Tuple: (status, penjelasan, penyimpanan)
    """
    
    categories = [t1, t2]
    
    # Kombinasi berbahaya tinggi
    if "Flammable" in categories and "Oxidizer" in categories:
        return (
            "❌ BERBAHAYA",
            "Kombinasi Flammable + Oxidizer sangat berbahaya! Flammable akan mempercepat pembakaran, Oxidizer akan meningkatkan intensitas api → ledakan atau kebakaran besar.",
            "🚨 PISAHKAN KETAT! Jangan simpan di area yang sama. Gunakan cabinet terpisah dan jauh dari sumber panas/api."
        )
    
    elif "Corrosive" in categories and "Toxic" in categories:
        return (
            "❌ BERBAHAYA",
            "Corrosive dapat merusak wadah → Toxic bocor. Kombinasi ini sangat bahaya untuk lingkungan kerja.",
            "🚨 Gunakan SECONDARY CONTAINMENT (wadah berlapis). Simpan di ventilasi khusus dengan monitoring ketat."
        )
    
    elif "Oxidizer" in categories and "Toxic" in categories:
        return (
            "❌ BERBAHAYA",
            "Oxidizer mempercepat reaksi → gas beracun meningkat drastis. Inhalasi dapat fatal.",
            "🚨 PISAHKAN KETAT! Gunakan fume hood khusus dan ventilasi eksternal ke luar gedung."
        )
    
    # Kombinasi perlu perhatian
    elif "Flammable" in categories and "Toxic" in categories:
        return (
            "⚠️ PERLU PERHATIAN",
            "Kombinasi ini memiliki risiko ganda: kebakaran + gas beracun. Jika terbakar, asap akan sangat beracun.",
            "⚠️ Ventilasi SANGAT BAIK diperlukan. Simpan dalam wadah tertutup rapat. Jauh dari sumber panas. Siapkan alat pemadam api khusus."
        )
    
    elif "Corrosive" in categories and "Flammable" in categories:
        return (
            "⚠️ PERLU PERHATIAN",
            "Corrosive dapat merusak/bocor dari wadah → Flammable tumpah → api. Risiko sedang-tinggi.",
            "⚠️ Gunakan WADAH TAHAN KOROSI. Simpan terpisah. Area dengan ventilasi baik dan jauh dari api."
        )
    
    elif "Corrosive" in categories and "Oxidizer" in categories:
        return (
            "⚠️ PERLU PERHATIAN",
            "Kedua zat reaktif. Oxidizer + asam dapat menciptakan reaksi eksplosif.",
            "⚠️ Simpan TERPISAH dengan minimal 2 meter jarak. Gunakan wadah tahan korosi/asam."
        )
    
    # Kombinasi aman
    elif t1 == t2 and t1 != "Safe":
        return (
            "✅ RELATIF AMAN",
            f"Kedua bahan termasuk kategori {t1} yang sama. Sifat kimia serupa sehingga kompatibel.",
            f"📦 Dapat disimpan bersama dalam area penyimpanan {t1}. Tetap perhatikan ventilasi dan suhu ruang."
        )
    
    elif t1 == "Safe" or t2 == "Safe":
        return (
            "✅ AMAN",
            "Salah satu atau kedua bahan adalah kategori Safe (tidak berbahaya). Kombinasi aman.",
            "📦 Dapat disimpan bersama di lokasi penyimpanan normal. Perhatikan regulasi penyimpanan umum."
        )
    
    # Kombinasi default
    else:
        return (
            "⚠️ PERLU PERHATIAN",
            f"Kombinasi {t1} dan {t2}. Meski tidak seserius kombinasi lain, tetap ada potensi interaksi. Perlu monitoring.",
            "⚠️ Simpan TERPISAH (minimal 1 meter). Gunakan SECONDARY CONTAINMENT untuk precaution. Pastikan label jelas."
        )


def get_compatibility_score(t1, t2):
    """
    Memberikan skor kompatibilitas 1-10 (10 = paling aman)
    """
    categories = [t1, t2]
    
    if "Flammable" in categories and "Oxidizer" in categories:
        return 1
    elif "Corrosive" in categories and "Toxic" in categories:
        return 2
    elif "Oxidizer" in categories and "Toxic" in categories:
        return 2
    elif "Flammable" in categories and "Toxic" in categories:
        return 4
    elif "Corrosive" in categories and "Flammable" in categories:
        return 5
    elif "Corrosive" in categories and "Oxidizer" in categories:
        return 5
    elif t1 == t2 and t1 != "Safe":
        return 8
    elif t1 == "Safe" or t2 == "Safe":
        return 10
    else:
        return 6
