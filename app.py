import streamlit as st
import replicate
import os
from PIL import Image

# 1. تنظیمات دیکشنری زبان‌ها
translations = {
    "English": {
        "title": "🏠 AI Interior Designer",
        "subtitle": "Transform empty spaces into luxury furnished rooms instantly.",
        "sidebar_header": "Settings",
        "api_label": "Enter Replicate API Token",
        "lang_select": "Choose Language",
        "upload_label": "Upload a photo of an empty room",
        "button": "Generate Design ✨",
        "loading": "Designing in Istanbul Luxury style...",
        "success": "Render Complete!",
        "input_caption": "Current Empty Unit",
        "output_caption": "AI Proposed Design",
        "style_label": "Choose Style",
        "styles": ["Modern", "Classic Ottoman", "Minimalist"]
    },
    "Türkçe": {
        "title": "🏠 Yapay Zeka İç Mimari",
        "subtitle": "Boş alanları anında lüks döşenmiş odalara dönüştürün.",
        "sidebar_header": "Ayarlar",
        "api_label": "Replicate API Token Giriniz",
        "lang_select": "Dil Seçin",
        "upload_label": "Boş bir oda fotoğrafı yükleyin",
        "button": "Tasarımı Oluştur ✨",
        "loading": "İstanbul Lüks tarzında tasarlanıyor...",
        "success": "Render Tamamlandı!",
        "input_caption": "Mevcut Boş Ünite",
        "output_caption": "AI Önerilen Tasarım",
        "style_label": "Tarz Seçin",
        "styles": ["Modern", "Klasik Osmanlı", "Minimalist"]
    }
}

# 2. تنظیمات صفحه
st.set_page_config(page_title="PropTech AI Turkey", layout="wide")

# 3. انتخاب زبان در سایدبار
st.sidebar.title("🌐 Language / Dil")
lang = st.sidebar.selectbox("Select Language", ["English", "Türkçe"])
t = translations[lang]

# 4. محتوای اصلی
st.title(t["title"])
st.subheader(t["subtitle"])

st.sidebar.divider()
st.sidebar.header(t["sidebar_header"])
REPLICATE_API_TOKEN = st.sidebar.text_input(t["api_label"], type="password")
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

selected_style = st.sidebar.selectbox(t["style_label"], t["styles"])

uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption=t["input_caption"], use_container_width=True)
        
    if st.button(t["button"]):
        if not REPLICATE_API_TOKEN:
            st.error("Please enter API Token / Lütfen API Token giriniz.")
        else:
            with st.spinner(t["loading"]):
                try:
                    # تنظیم پرامپت بر اساس سبک انتخابی
                    style_prompt = f"{selected_style} Turkish interior design, high-end materials"
                    
                    output = replicate.run(
                        "jagadeeshr-t/interior-ai:76604a39c3816481cc23f39",
                        input={
                            "image": uploaded_file,
                            "prompt": f"{style_prompt}, luxury, marble floors, 8k, realistic",
                            "n_prompt": "low quality, change walls, distorted",
                        }
                    )
                    
                    with col2:
                        st.image(output[0], caption=t["output_caption"], use_container_width=True)
                        st.success(t["success"])
                except Exception as e:
                    st.error(f"Error: {e}")
