import streamlit as st
import replicate
import os

# 1. تنظیمات اولیه و زبان
translations = {
    "English": {"title": "🏠 EvVision-AI", "button": "Generate Design ✨", "loading": "Processing..."},
    "Türkçe": {"title": "🏠 EvVision-AI", "button": "Tasarımı Oluştur ✨", "loading": "Tasarım hazırlanıyor..."}
}

st.set_page_config(page_title="EvVision-AI", layout="wide")
lang = st.sidebar.selectbox("🌐 Language", ["Türkçe", "English"])
t = translations[lang]

# 2. بررسی توکن
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("API Token missing in Secrets!")
    st.stop()

# 3. رابط کاربری
st.title(t["title"])
uploaded_file = st.file_uploader("Upload Room Photo", type=["jpg", "png"])

if uploaded_file and st.button(t["button"]):
    with st.spinner(t["loading"]):
        try:
            # استفاده از مدل پایدار و عمومی
            output = replicate.run(
                "lucataco/controlnet-depth:985e133e8a5a54452a2333",
                input={
                    "image": uploaded_file,
                    "prompt": "modern luxury interior design, turkish style, marble, high quality",
                }
            )
            st.image(output[0], caption="Result", use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
