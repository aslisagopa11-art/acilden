import streamlit as st
import google.generativeai as genai
import json

# 1. Sayfa Ayarları
st.set_page_config(
    page_title="Gemlik Gayrimenkul Ekspertiz",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TASARIM CSS ---
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #1e3a8a; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. API Kontrolü
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("Lütfen API Anahtarını Ayarlayın!")
        st.stop()
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")

# 3. SOL MENÜ (FORM YAPISI - GARANTİ ÇALIŞIR)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1040/1040993.png", width=80)
    st.title("Mülk Detayları")
    
    # FORM BAŞLANGICI
    with st.form(key='emlak_formu'):
        mahalle = st.selectbox("Mahalle", ["Cumhuriyet (Manastır)", "Dr. Ziya Kaya", "Eşref Dinçer", "Hamidiye", "Kumla", "Kurşunlu", "Osmaniye", "Umurbey"])
        emlak_tipi = st.selectbox("Emlak Tipi", ["Daire", "Villa", "Müstakil", "Yazlık", "Arsa"])
        oda_sayisi = st.selectbox("Oda Sayısı", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
        
        c1, c2 = st.columns(2)
        with c1: m2 = st.number_input("Net m²", 30, 1000, 110)
        with c2: bina_yasi = st.number_input("Bina Yaşı", 0, 50, 5)
        
        # FORM GÖNDERME BUTONU
        submit_button = st.form_submit_button(label='🚀 ANALİZİ BAŞLAT')

    st.markdown("---")
    st.caption("© 2025 Gemlik Emlak")

# 4. ANA EKRAN VE HESAPLAMA
st.title("Gemlik Gayrimenkul Ekspertiz Robotu")
st.markdown("Gemlik bölgesindeki güncel piyasa verileri ve yapay zeka analizi.")
st.divider()

# EĞER BUTONA BASILDIYSA BURASI ÇALIŞIR
if submit_button:
    with st.spinner('Yapay zeka verileri işliyor...'):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Sen Bursa Gemlik bölgesinde uzman bir emlakçısın.
            MÜLK: {mahalle}, {bina_yasi} yaşında, {m2} m2, {oda_sayisi}, {emlak_tipi}.
            
            GÖREV: SADECE aşağıdaki JSON formatında çıktı ver (Yorumsuz):
            {{
                "acil_fiyat": "X.XXX.XXX TL",
                "piyasa_fiyat": "X.XXX.XXX TL",
                "tok_fiyat": "X.XXX.XXX TL",
                "yorum": "Mülk hakkında 3 cümlelik uzman yorumu."
            }}
            """
            
            response = model.generate_content(prompt)
            text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(text)
            
            # SONUÇLARI GÖSTER
            col1, col2, col3 = st.columns(3)
            col1.metric("🔥 Acil Satış", data['acil_fiyat'], "Hızlı Nakit")
            col2.metric("⚖️ Piyasa Değeri", data['piyasa_fiyat'], "Ortalama")
            col3.metric("💎 Tok Satıcı", data['tok_fiyat'], "Yüksek Hedef")
            
            st.success("✅ Analiz Tamamlandı")
            st.info(f"**Uzman Yorumu:** {data['yorum']}")
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
            st.warning("Lütfen sayfayı yenileyip tekrar deneyin.")

else:
    st.info("👈 Lütfen sol taraftan bilgileri seçip butona basın.")
