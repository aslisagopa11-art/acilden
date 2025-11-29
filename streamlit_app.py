import streamlit as st
import google.generativeai as genai
import json

# 1. Sayfa Ayarları (Geniş Ekran)
st.set_page_config(
    page_title="Gemlik Emlak Değerleme",
    page_icon="🏠",
    layout="wide"
)

# 2. API Anahtarını Al (Streamlit Secrets'tan)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Lütfen Streamlit panelinden API anahtarını (GEMINI_API_KEY) ayarlayın.")
    st.stop()

# 3. Sol Menü (Sidebar) - Kullanıcı Girişleri
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1040/1040993.png", width=100)
    st.title("Mülk Bilgileri")
    
    mahalle = st.selectbox(
        "Mahalle Seçiniz",
        ["Cumhuriyet (Manastır)", "Dr. Ziya Kaya", "Eşref Dinçer", "Hamidiye", "Kumla", "Kurşunlu", "Osmaniye", "Umurbey"]
    )
    
    emlak_tipi = st.selectbox("Emlak Tipi", ["Daire", "Villa", "Müstakil", "Yazlık", "Arsa"])
    oda_sayisi = st.selectbox("Oda Sayısı", ["1+1", "2+1", "3+1", "4+1", "5+1", "Dubleks"])
    m2 = st.number_input("Net Metrekare (m2)", min_value=30, max_value=1000, value=110)
    bina_yasi = st.number_input("Bina Yaşı", min_value=0, max_value=50, value=5)
    
    hesapla_btn = st.button("🔍 Fiyatı Analiz Et", type="primary")
    
    st.markdown("---")
    st.caption("© 2025 Gemlik Emlak | Rasim Kılıç")

# 4. Ana Ekran (Sağ Taraf)
st.title("🏡 Gemlik Gayrimenkul Ekspertiz Robotu")
st.markdown("Gemlik bölgesindeki güncel piyasa verileri ve yapay zeka analizi ile mülkünüzün gerçek değerini öğrenin.")
st.divider()

if hesapla_btn:
    with st.spinner('Yapay Zeka bölgeyi analiz ediyor, emsalleri tarıyor... Lütfen bekleyin.'):
        try:
            # Yapay Zekaya Gidecek Emir (Prompt)
            prompt = f"""
            Sen Gemlik bölgesinde 20 yıllık deneyime sahip uzman bir emlak danışmanısın (Rasim Kılıç).
            Aşağıdaki mülk için Sahibinden.com, Hepsiemlak ve Zingat verilerini simüle ederek bir değerleme yap.
            
            Mülk Bilgileri:
            - Bölge: Gemlik, {mahalle} Mahallesi
            - Tip: {emlak_tipi}
            - Özellikler: {oda_sayisi}, {m2} m2, {bina_yasi} yaşında.
            
            Lütfen cevabı SADECE aşağıdaki JSON formatında ver (Başka yazı yazma):
            {{
                "acil_satis": "X.XXX.XXX TL",
                "piyasa_degeri": "X.XXX.XXX TL",
                "tok_satici": "X.XXX.XXX TL",
                "yorum": "Buraya mülkün konumu, avantajları ve piyasa durumu hakkında detaylı, profesyonel bir yorum yaz."
            }}
            """
            
            # Modeli Çalıştır
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            # Gelen veriyi temizle ve JSON'a çevir
            text_response = response.text.replace("```json", "").replace("```", "")
            data = json.loads(text_response)
            
            # 5. Sonuçları Göster (3'lü Kart Yapısı)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.error("Acil Satış Fiyatı")
                st.metric(label="1-7 Gün İçinde Nakit", value=data["acil_satis"], delta="- %15 Fırsat")
            
            with col2:
                st.info("Gerçek Piyasa Değeri")
                st.metric(label="Ortalama İşlem Süresi", value=data["piyasa_degeri"], delta="Piyasa Ortalaması")
                
            with col3:
                st.warning("Tok Satıcı Fiyatı")
                st.metric(label="Bekleme Süresi Yüksek", value=data["tok_satici"], delta="+ %10 Kâr Hedefi")
            
            st.divider()
            
            # 6. Uzman Yorumu ve Rapor
            st.subheader("📋 Yapay Zeka Ekspertiz Raporu")
            st.info(data["yorum"])
            
            st.success("Bu rapor, bölge verileri ve yapay zeka tahminleri ile oluşturulmuştur. Kesin sonuç için yerinde inceleme gerekir.")
            
        except Exception as e:
            st.error(f"Bir hata oluştu. Lütfen tekrar deneyin. Hata: {str(e)}")

else:
    # Başlangıçta boş durmasın diye bilgi mesajı
    st.info("👈 Sol taraftaki menüden mülk bilgilerini girip 'Fiyatı Analiz Et' butonuna basınız.")
