import streamlit as st
import replicate
import os
from PIL import Image

# 1. تنظیمات زبان و استایل‌ها
translations = {
    "English": {
        "title": "🏠 EvVision-AI",
        "subtitle": "Professional AI Staging for Properties",
        "sidebar_header": "Design Menu",
        "upload_label": "Upload Empty Room Photo",
        "button": "Generate Design ✨",
        "loading": "Architect AI is working...",
        "style_label": "Select Interior Style",
        "styles": ["Modern Luxury", "Scandinavian", "Minimalist", "Classic Turkish", "Industrial"]
    },
    "Türkçe": {
        "title": "🏠 EvVision-AI",
        "subtitle": "Gayrimenkul İçin Profesyonel Yapay Zeka Tasarımı",
        "sidebar_header": "Tasarım Menüsü",
        "upload_label": "Boş Oda Fotoğrafı Yükleyin",
        "button": "Tasarımı Oluştur ✨",
        "loading": "Yapay Zeka tasarlıyor...",
        "style_label": "İç Mekan Tarzı Seçin",
        "styles": ["Modern Lüks", "İskandinav", "Minimalist", "Klasik Türk", "Endüstriyel"]
    }
}

# 2. پیکربندی صفحه
st.set_page_config(page_title="EvVision-AI", layout="wide")

# 3. انتخاب زبان در سایدبار
lang = st.sidebar.selectbox("🌐 Language / Dil", ["Türkçe", "English"])
t = translations[lang]

# 4. تنظیم توکن از Secrets
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("API Token missing in Streamlit Secrets!")
    st.stop()

# 5. بخش سایدبار (سمت چپ) برای تنظیمات
st.sidebar.header(t["sidebar_header"])
selected_style = st.sidebar.radio(t["style_label"], t["styles"])

# 6. بدنه اصلی برنامه
st.title(t["title"])
st.subheader(t["subtitle"])

uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption="Original", use_container_width=True)
        
    if st.button(t["button"]):
        with st.spinner(t["loading"]):
            try:
                # استفاده از مدل پایدار و جدید برای حل ارور 422
                output = replicate.run(
                    "lucataco/controlnet-depth:985e133e8a5a54452a2333",
                    input={
                        "image": uploaded_file,
                        "prompt": f"a high quality photo of a {selected_style} interior, realistic furniture, professional lighting, 8k",
                        "n_prompt": "low quality, blurry, distorted, messy, extra windows, change walls",
                        "num_inference_steps": 30
                    }
                )
                
                with col2:
                    st.image(output[0], caption="AI Design", use_container_width=True)
                    st.success("Success!")
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("EvVision-AI - 2026 PropTech Solution")
