import streamlit as st
import replicate
import os

# 1. تنظیمات صفحه
st.set_page_config(page_title="EvVision-AI", layout="wide", page_icon="🏠")

# 2. دیکشنری ترجمه‌ها
translations = {
    "Türkçe": {
        "title": "🏠 EvVision-AI",
        "style_label": "Tasarım Tarزını Seçin",
        "styles": ["Modern Luxury", "Scandinavian", "Minimalist", "Classic Turkish", "Industrial"],
        "button": "Tasarımı Oluştur ✨",
        "upload_msg": "Boş oda fotoğrafı yükleyin",
        "error_msg": "Bir hata oluştu: ",
        "success_msg": "Tasarım Hazır!"
    },
    "English": {
        "title": "🏠 EvVision-AI",
        "style_label": "Select Interior Style",
        "styles": ["Modern Luxury", "Scandinavian", "Minimalist", "Classic Turkish", "Industrial"],
        "button": "Generate Design ✨",
        "upload_msg": "Upload an empty room photo",
        "error_msg": "An error occurred: ",
        "success_msg": "Design Completed!"
    }
}

# 3. سایدبار و انتخاب زبان
lang = st.sidebar.selectbox("🌐 Language / Dil", ["English", "Türkçe"])
t = translations[lang]

st.sidebar.divider()
st.sidebar.header("Design Menu")
selected_style = st.sidebar.radio(t["style_label"], t["styles"])

# 4. تنظیم توکن Replicate
# اول در Secrets چک می‌کند، اگر نبود از متغیر سیستم می‌خواند
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.sidebar.warning("⚠️ API Token not found in Secrets. Please add it.")

# 5. بدنه اصلی برنامه
st.title(t["title"])
uploaded_file = st.file_uploader(t["upload_msg"], type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption="Original", use_container_width=True)

    if st.button(t["button"]):
        with st.spinner("AI is reimagining your space..."):
            try:
                # فراخوانی مدل جدید و پایدارتر
                # این نسخه مدل تست شده و خروجی با کیفیتی دارد
                output = replicate.run(
                    "lucataco/interior-design:76604a39c3816481cc23f39d05e0cbf6e728f87c5411a0d010545656967340fb",
                    input={
                        "image": uploaded_file,
                        "prompt": f"a professional high-quality photo of a {selected_style} room, realistic lighting, highly detailed, 8k uhd, architectural photography",
                        "guidance_scale": 7.5,
                        "num_inference_steps": 25
                    }
                )

                with col2:
                    # بررسی نوع خروجی برای نمایش درست تصویر
                    if isinstance(output, list):
                        res_image = output[1] if len(output) > 1 else output[0]
                    else:
                        res_image = output
                    
                    st.image(res_image, caption="AI Generated Design", use_container_width=True)
                    st.success(t["success_msg"])
                    
            except Exception as e:
                st.error(f"{t['error_msg']} {str(e)}")
                st.info("Tip: Check if your Replicate API token has enough credits.")

# فوتر
st.divider()
st.caption("EvVision-AI - 2026 PropTech Solution")
