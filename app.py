import streamlit as st
import replicate
import os

# 1. تنظیمات ظاهر و زبان
st.set_page_config(page_title="EvVision-AI", layout="wide")

translations = {
    "Türkçe": {
        "title": "🏠 EvVision-AI",
        "style_label": "Tasarım Tarzını Seçin",
        "styles": ["Modern", "Minimalist", "Industrial", "Scandinavian", "Luxury"],
        "button": "Tasarımı Oluştur ✨",
        "upload_msg": "Boş oda fotoğrafı yükleyin"
    },
    "English": {
        "title": "🏠 EvVision-AI",
        "style_label": "Select Design Style",
        "styles": ["Modern", "Minimalist", "Industrial", "Scandinavian", "Luxury"],
        "button": "Generate Design ✨",
        "upload_msg": "Upload empty room photo"
    }
}

# 2. سایدبار (منوی سمت چپ)
lang = st.sidebar.selectbox("🌐 Language", ["Türkçe", "English"])
t = translations[lang]

st.sidebar.header(t["title"])
selected_style = st.sidebar.selectbox(t["style_label"], t["styles"])

# 3. بررسی توکن
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("API Token missing in Secrets!")
    st.stop()

# 4. بدنه اصلی
st.title(t["title"])
uploaded_file = st.file_uploader(t["upload_msg"], type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="Original", use_container_width=True)

    if st.button(t["button"]):
        with st.spinner("AI is designing..."):
            try:
                # این مدل مخصوص دکوراسیون داخلیه و احتمال ارورش خیلی کمه
                output = replicate.run(
                    "adirik/interior-design:76604a39c3816481cc23f39d05e0cbf6e728f87c5411a0d010545656967340fb",
                    input={
                        "image": uploaded_file,
                        "prompt": f"a professional photo of a {selected_style} room, high quality, realistic lighting",
                        "guidance_scale": 7.5,
                        "num_inference_steps": 25
                    }
                )
                with col2:
                    st.image(output[1], caption="AI Design", use_container_width=True)
                    st.success("Done!")
            except Exception as e:
                st.error(f"خطای جدید: {e}")

st.divider()
st.caption("EvVision-AI 2026")
