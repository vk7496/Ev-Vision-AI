import streamlit as st
import replicate
import os
from PIL import Image

# 1. تنظیمات دوزبانه و استایل‌های دکوراسیون
translations = {
    "English": {
        "title": "🏠 EvVision-AI",
        "subtitle": "Instant AI Virtual Staging",
        "sidebar_header": "Design Settings",
        "upload_label": "Upload a photo of an empty room",
        "button": "Generate Design ✨",
        "loading": "Designing your space...",
        "style_label": "Choose Interior Style",
        "styles": ["Modern Luxury", "Scandinavian", "Minimalist", "Classic Turkish", "Industrial"]
    },
    "Türkçe": {
        "title": "🏠 EvVision-AI",
        "subtitle": "Yapay Zeka Destekli Sanal Dekorasyon",
        "sidebar_header": "Tasarım Ayarları",
        "upload_label": "Boş bir oda fotoğrafı yükleyin",
        "button": "Tasarımı Oluştur ✨",
        "loading": "Tasarımınız hazırlanıyor...",
        "style_label": "İç Mekan Tarzı Seçin",
        "styles": ["Modern Lüks", "İskandinav", "Minimalist", "Klasik Türk", "Endüstriyel"]
    }
}

# 2. تنظیمات صفحه
st.set_page_config(page_title="EvVision-AI | PropTech", layout="wide")

# 3. مدیریت زبان
lang = st.sidebar.selectbox("🌐 Language / Dil", ["Türkçe", "English"])
t = translations[lang]

# 4. فراخوانی امن توکن از Secrets
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ API Token missing in Streamlit Secrets!")
    st.stop()

# 5. بخش انتخاب سبک در سایدبار (سمت چپ)
st.sidebar.divider()
st.sidebar.header(t["sidebar_header"])
selected_style = st.sidebar.radio(t["style_label"], t["styles"])

# 6. رابط کاربری اصلی
st.title(t["title"])
st.subheader(t["subtitle"])

uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption="Original Photo", use_container_width=True)
        
    if st.button(t["button"]):
        with st.spinner(t["loading"]):
            try:
                # استفاده از یک مدل بسیار پایدار و عمومی برای رفع ارور 422
                # این مدل (ControlNet Depth) ساختار اتاق را کاملا حفظ می‌کند
                output = replicate.run(
                    "lucataco/controlnet-depth:985e133e8a5a54452a2333",
                    input={
                        "image": uploaded_file,
                        "prompt": f"a professional photo of a {selected_style} interior, highly detailed, realistic lighting, 8k, interior design magazine style",
                        "n_prompt": "low quality, blurry, distorted, change walls, extra windows, messy",
                        "num_inference_steps": 30
                    }
                )
                
                with col2:
                    st.image(output[0], caption="AI Proposed Design", use_container_width=True)
                    st.success("Done!")
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("EvVision-AI - 2026 PropTech Solution for Turkey Market")
