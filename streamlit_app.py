import streamlit as st
import google.generativeai as genai
import json

# 1. Sayfa Ayarları (Geniş ve Şık)
st.set_page_config(
    page_title="Gemlik Gayrimenkul Ekspertiz",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TASARIM İÇİN CSS (Lüks Kartlar ve Gölgeler) ---
st.markdown("""
<style>
    /* Ana Arkaplan */
    .main { background-color: #f8f9fa; }
    h1 { color: #1e3a8a; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Fiyat Kartları Tasarımı */
    .metric-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }
    .metric-label {
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        margin: 10px 0;
    }
    .metric-sub {
        font-size: 12px;
        padding: 5px 10px;
        border-radius: 20px;
        display: inline-block;
    }
    
    /* Renk Temaları */
    .card-red { border-top: 5px solid #ef4444; }
    .text-red { color: #ef4444; }
    .bg-red-light { background-color: #fee2e2; color: #991b1b; }
    
    .card-blue { border-top: 5px solid #3b82f6; }
    .text-blue { color: #3b82f6; }
    .bg-blue-light { background-color: #dbeafe; color: #1e40af; }
    
    .card-purple { border-top: 5px solid #a855f7; }
    .text-purple { color: #a855f7; }
    .bg-purple-light { background-color: #f3e8ff; color: #6b21a8; }
    
    /* Buton Tasarımı */
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
        border: none;
    }
    .stButton>button:hover { background-color: #1d4ed8; }
</style>
""", unsafe_allow_html=True)

# 2. API Anahtarını Kontrol Et
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ API Anahtarı Bulunamadı! Lütfen Streamlit Secrets ayarlarını kontrol edin.")
    st.stop()

# 3. Sol Menü (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1040/1040993.png", width=80)
    st.title("Mülk Detayları")
    
    mahalle = st.selectbox("Mahalle", ["Cumhuriyet (Manastır)", "Dr. Ziya Kaya", "Eşref Dinçer", "Hamidiye", "Kumla", "Kurşunlu", "Osmaniye", "Umurbey"])
    emlak_tipi = st.selectbox("Emlak Tipi", ["Daire", "Villa", "Müstakil", "Yazlık", "Arsa"])
    oda_sayisi = st.selectbox("Oda Sayısı", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
    col1, col2 = st.columns(2)
    with col1: m2 = st.number_input("Net m²", value=110)
    with col2: bina_yasi = st.number_input("Bina Yaşı", value=5)
        
    hesapla_btn = st.button("🚀 ANALİZİ BAŞLAT")
    st.markdown("---")
    st.caption("© 2025 Gemlik Emlak | Rasim Kılıç")

# 4. Ana Ekran
st.title("Gemlik Gayrimenkul Ekspertiz Robotu")
st.markdown("Gemlik bölgesindeki güncel piyasa verileri ve yapay zeka analizi ile mülkünüzün gerçek değerini öğrenin.")
st.divider()

# 5. Hesaplama
