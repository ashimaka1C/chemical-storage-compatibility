"""
Utility functions untuk FCOT Chemical System
"""
from datetime import datetime

def get_safety_color(status):
    """
    Mengembalikan warna untuk setiap status keamanan
    """
    if "AMAN" in status.upper():
        return "#00c853"
    elif "BERBAHAYA" in status.upper():
        return "#ff1744"
    else:
        return "#ff9100"


def format_timestamp(dt):
    """
    Format timestamp untuk display
    """
    if isinstance(dt, str):
        return dt
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def get_category_emoji(category):
    """
    Mengembalikan emoji untuk kategori FCOT
    """
    emojis = {
        "Flammable": "🔥",
        "Corrosive": "🧪",
        "Oxidizer": "⚡",
        "Toxic": "☠️",
        "Safe": "✅"
    }
    return emojis.get(category, "❓")
