import streamlit as st
import replicate
import os
import requests
from PIL import Image
from io import BytesIO

# 1. تنظیمات اولیه و هویت برند
st.set_page_config(page_title="EvVision-AI | PropTech Solutions", layout="wide", page_icon="🏗️")

# سیستم ترجمه برای بازارهای هدف (عمان، ترکیه و بین‌الملل)
translations = {
    "English": {
        "header": "🏗️ AI Construction Visualizer",
        "sub": "Transform raw sites into finished luxury spaces.",
        "upload": "Upload site photo (Raw/Construction)",
        "style": "Target Design Style",
        "btn": "Render Professional View ✨",
        "processing": "Analyzing architecture and applying materials...",
        "success": "Visualization Ready!",
        "error_422": "Version mismatch detected. Re-fetching latest AI engine..."
    },
    "Arabic": {
        "header": "🏗️ مصور الإنشاءات بالذكاء الاصطناعي",
        "sub": "حول مواقع البناء الخام إلى مساحات فاخرة.",
        "upload": "تحميل صورة الموقع (قيد الإنشاء)",
        "style": "نمط التصميم المستهدف",
        "btn": "عرض النتيجة النهائية ✨",
        "processing": "تحليل الهيكل وتطبيق المواد...",
        "success": "العرض جاهز!",
        "error_422": "تم اكتشاف عدم تطابق في الإصدار. جارٍ تحديث المحرك..."
    },
    "Turkish": {
        "header": "🏗️ Yapay Zeka İnşaat Görselleştirici",
        "sub": "Kaba inşaatları bitmiş lüks mekanlara dönüştürün.",
        "upload": "Saha fotoğrafı yükleyin (İnşaat Hali)",
        "style": "Hedef Tasarım Tarzı",
        "btn": "Görünümü Oluştur ✨",
        "processing": "Yapı analiz ediliyor و malzemeler uygulanıyor...",
        "success": "Görselleştirme Hazır!",
        "error_422": "Sürüm hatası algılandı. Güncel motor çekiliyor..."
    }
}

# انتخاب زبان در سایدبار
lang = st.sidebar.selectbox("🌐 Market / Language", ["English", "Arabic", "Turkish"])
t = translations[lang]

# 2. مدیریت توکن امنیتی
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.sidebar.error("⚠️ API Token missing in Streamlit Secrets!")
    st.stop()

# 3. رابط کاربری اصلی
st.title(t["header"])
st.markdown(f"#### {t['sub']}")

uploaded_file = st.file_uploader(t["upload"], type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption="Original Site Condition", use_container_width=True)
        selected_style = st.selectbox(t["style"], 
                                    ["Modern Luxury", "Scandinavian Business", "Minimalist Residential", "Classic Industrial"])

    if st.button(t["btn"]):
        with st.spinner(t["processing"]):
            try:
                # راهکار حل دائمی ارور 422: گرفتن پویا (Dynamic) آخرین ورژن مدل
                model = replicate.models.get("jagilley/controlnet-hough")
                latest_version = model.versions.list()[0].id
                
                # اجرای پردازش تصویر با مدل ControlNet برای حفظ ساختار معماری
                output = replicate.run(
                    f"jagilley/controlnet-hough:{latest_version}",
                    input={
                        "image": uploaded_file,
                        "prompt": f"a professional high-quality interior design photo of a {selected_style} room, finished walls, premium materials, realistic cinematic lighting, 8k, architectural digest style",
                        "n_prompt": "people, workers, ladders, construction tools, boxes, messy, dirt, low quality, text, watermark, blurry",
                        "image_resolution": "768",
                        "ddim_steps": 30,
                        "scale": 9,
                        "a_prompt": "high quality, extremely detailed, photorealistic"
                    }
                )
                
                with col2:
                    # استخراج تصویر نهایی (معمولاً ایندکس 1 در این مدل خروجی اصلی است)
                    result_url = output[1] if isinstance(output, list) and len(output) > 1 else output[0]
                    st.image(result_url, caption=f"AI Finished Concept: {selected_style}", use_container_width=True)
                    st.success(t["success"])
                    
                    # قابلیت دانلود برای ارائه به کارفرما
                    response = requests.get(result_url)
                    st.download_button(label="Download Full Render", 
                                     data=BytesIO(response.content), 
                                     file_name="evvision_render.png", 
                                     mime="image/png")
            
            except Exception as e:
                if "422" in str(e):
                    st.error(t["error_422"])
                else:
                    st.error(f"Technical Error: {e}")
                    st.info("Ensure your Replicate billing is active and the API token is correct.")

st.divider()
st.caption("EvVision-AI | Advanced PropTech Solution for Construction Visualization 2026")
