import streamlit as st
import replicate
import os
from PIL import Image

# 1. تنظیمات زبان (دوزبانه: ترکی و انگلیسی)
translations = {
    "English": {
        "title": "🏠 EvVision-AI",
        "subtitle": "Instant AI Virtual Staging for Turkish Real Estate",
        "sidebar_header": "Design Settings",
        "lang_select": "Choose Language",
        "upload_label": "Upload a photo of an empty room",
        "button": "Generate Design ✨",
        "loading": "Designing in luxury style...",
        "success": "Render Complete!",
        "input_caption": "Empty Unit",
        "output_caption": "AI Proposed Interior",
        "style_label": "Select Style",
        "styles": ["Modern Istanbul", "Luxury Marble", "Minimalist White", "Classic Ottoman"]
    },
    "Türkçe": {
        "title": "🏠 EvVision-AI",
        "subtitle": "Gayrimenkul Satışları İçin Yapay Zeka Destekli Sanal Dekorasyon",
        "sidebar_header": "Tasarım Ayarları",
        "lang_select": "Dil Seçin",
        "upload_label": "Boş oda fotoğrafı yükleyin",
        "button": "Tasarımı Oluştur ✨",
        "loading": "Lüks tarzda tasarlanıyor...",
        "success": "Render Tamamlandı!",
        "input_caption": "Boş Ünite",
        "output_caption": "AI Önerilen Tasarım",
        "style_label": "Tarz Seçin",
        "styles": ["Modern İstanbul", "Lüks Mermer", "Minimalist Beyaz", "Klasik Osmanlı"]
    }
}

# 2. تنظیمات صفحه
st.set_page_config(page_title="EvVision-AI | PropTech Turkey", layout="wide")

# 3. مدیریت زبان در سایدبار
lang = st.sidebar.selectbox("🌐 Language / Dil", ["Türkçe", "English"])
t = translations[lang]

# 4. تنظیم امنیتی توکن (از Secrets استریم‌لایت)
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
selected_style = st.sidebar.selectbox(t["style_label"], t["styles"])

uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption=t["input_caption"], use_container_width=True)
        
    if st.button(t["button"]):
        with st.spinner(t["loading"]):
            try:
                # بهینه‌سازی پرامپت برای بازار ترکیه
                prompt_details = f"{selected_style} interior design, high-end materials, realistic lighting, 8k, architectural photography"
                
                # فراخوانی مدل
                output = replicate.run(
                    "jagadeeshr-t/interior-ai:76604a39c3816481cc23f39",
                    input={
                        "image": uploaded_file,
                        "prompt": prompt_details,
                        "n_prompt": "low quality, distorted, changing walls, extra windows, blurry",
                    }
                )
                
                with col2:
                    st.image(output[0], caption=t["output_caption"], use_container_width=True)
                    st.success(t["success"])
                    
                    # امکان دانلود تصویر خروجی
                    st.download_button(
                        label="Download Render",
                        data=output[0],
                        file_name="evvision_render.png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error(f"Error: {e}")

# فوتر ساده
st.divider()
st.caption("EvVision-AI - Developed for Turkey PropTech Market 2026")
