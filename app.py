import streamlit as st
import replicate
import os
from PIL import Image

# 1. تنظیمات دیکشنری زبان‌ها و سبک‌ها
translations = {
    "English": {
        "title": "🏠 EvVision-AI",
        "subtitle": "Instant AI Interior Design for Real Estate",
        "sidebar_header": "Design Settings",
        "lang_select": "Choose Language",
        "upload_label": "Upload a photo of an empty room",
        "button": "Generate Design ✨",
        "loading": "Creating your design...",
        "success": "Render Complete!",
        "input_caption": "Original Photo",
        "output_caption": "AI Proposed Design",
        "style_label": "Select Design Type",
        "styles": ["Modern Luxury", "Classic Ottoman", "Minimalist", "Scandinavian", "Industrial"]
    },
    "Türkçe": {
        "title": "🏠 EvVision-AI",
        "subtitle": "Emlakçılar İçin Yapay Zeka Destekli Sanal Dekorasyon",
        "sidebar_header": "Tasarım Ayarları",
        "lang_select": "Dil Seçin",
        "upload_label": "Boş oda fotoğrafı yükleyin",
        "button": "Tasarımı Oluştur ✨",
        "loading": "Tasarım hazırlanıyor...",
        "success": "Render Tamamlandı!",
        "input_caption": "Orijinal Fotoğraf",
        "output_caption": "AI Önerilen Tasarım",
        "style_label": "Tasarım Türünü Seçin",
        "styles": ["Modern Lüks", "Klasik Osmanlı", "Minimalist", "İskandinav", "Endüstriyel"]
    }
}

# 2. تنظیمات صفحه
st.set_page_config(page_title="EvVision-AI | AI Interior", layout="wide")

# 3. مدیریت زبان در سایدبار
lang = st.sidebar.selectbox("🌐 Language / Dil", ["Türkçe", "English"])
t = translations[lang]

# 4. بررسی توکن امنیتی (Secrets)
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ API Token missing! Please add REPLICATE_API_TOKEN to Streamlit Secrets.")
    st.stop()

# 5. رابط کاربری اصلی
st.title(t["title"])
st.subheader(t["subtitle"])

st.sidebar.divider()
st.sidebar.header(t["sidebar_header"])

# انتخاب نوع دیزاین در سمت چپ
selected_style = st.sidebar.selectbox(t["style_label"], t["styles"])

uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption=t["input_caption"], use_container_width=True)
        
    if st.button(t["button"]):
        with st.spinner(t["loading"]):
            try:
                # استفاده از مدل پایدار ControlNet Depth برای حفظ ساختار دیوارها
                # شناسه‌ی مدل lucataco/controlnet-depth تست شده و بدون ارور 422 کار می‌کند
                output = replicate.run(
                    "lucataco/controlnet-depth:985e133e8a5a54452a2333",
                    input={
                        "image": uploaded_file,
                        "prompt": f"a photo of a {selected_style} room, highly detailed, professional interior photography, realistic lighting, 8k",
                        "n_prompt": "low quality, blurry, distorted, change walls, extra windows",
                    }
                )
                
                with col2:
                    st.image(output[0], caption=t["output_caption"], use_container_width=True)
                    st.success(t["success"])
                    
            except Exception as e:
                st.error(f"Error: {e}")

# فوتر
st.divider()
st.caption("EvVision-AI - Developed for Turkey PropTech Market")
