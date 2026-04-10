import streamlit as st
import replicate
import os

# تنظیمات ظاهری و هویتی اپلیکیشن
st.set_page_config(page_title="EvVision-AI | PropTech Solution", layout="wide", page_icon="🏗️")

# سیستم چندزبانه برای بازارهای عمان و ترکیه
translations = {
    "English": {
        "header": "🏗️ AI Construction Visualizer",
        "sub": "Transform raw construction sites into finished luxury spaces.",
        "upload": "Upload site photo (Raw/Construction)",
        "style": "Target Finishing Style",
        "btn": "Render Final View ✨",
        "processing": "Analyzing structure and applying materials..."
    },
    "Arabic": {
        "header": "🏗️ مصور الإنشاءات بالذكاء الاصطناعي",
        "sub": "حول مواقع البناء الخام إلى مساحات فاخرة جاهزة.",
        "upload": "تحميل صورة الموقع (قيد الإنشاء)",
        "style": "نمط التشطيب المستهدف",
        "btn": "عرض النتيجة النهائية ✨",
        "processing": "تحليل الهيكل وتطبيق المواد..."
    },
    "Turkish": {
        "header": "🏗️ Yapay Zeka İnşaat Görselleştirici",
        "sub": "İnşaat halindeki alanları bitmiş lüks mekanlara dönüştürün.",
        "upload": "Saha fotoğrafı yükleyin (Kaba İnşaat)",
        "style": "Hedef Tasarım Tarzı",
        "btn": "Son Görünümü Oluştur ✨",
        "processing": "Yapı analiz ediliyor ve malzemeler uygulanıyor..."
    }
}

lang = st.sidebar.selectbox("🌐 Select Market / Language", ["English", "Arabic", "Turkish"])
t = translations[lang]

# مدیریت کلید API
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Missing REPLICATE_API_TOKEN in Secrets!")
    st.stop()

st.title(t["header"])
st.markdown(f"*{t['sub']}*")

uploaded_file = st.file_uploader(t["upload"], type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption="Site Condition (Raw)", use_container_width=True)
        selected_style = st.selectbox(t["style"], ["Ultra Modern", "Classic Luxury", "Industrial Office", "Minimalist Residential"])

    if st.button(t["btn"]):
        with st.spinner(t["processing"]):
            try:
                # استفاده از ControlNet برای حفظ دقیق خطوط معماری
                # این مدل برای عکس‌های شلوغ کارگاهی عالی عمل می‌کند
                output = replicate.run(
                    "jagilley/controlnet-hough:854e96fc0574160c90d3c5d6e19276c93685477d57572d422030616b54238e8",
                    input={
                        "image": uploaded_file,
                        "prompt": f"a professional interior design photo of a {selected_style} room, finished walls, high-end flooring, cinematic lighting, architectural render, 8k",
                        "n_prompt": "people, construction tools, ladders, boxes, messy, unfinished, blurry, distorted, text",
                        "num_samples": "1",
                        "image_resolution": "768",
                        "ddim_steps": 25,
                        "scale": 9
                    }
                )
                
                with col2:
                    # مدل ControlNet معمولاً دو خروجی می‌دهد: نقشه خطوط و رندر نهایی
                    final_image = output[1] if isinstance(output, list) and len(output) > 1 else output[0]
                    st.image(final_image, caption="AI Transformation", use_container_width=True)
                    st.success("Visualization Ready!")
                    
                    # امکان دانلود برای ارائه به مشتری
                    st.download_button("Download Render", final_image, file_name="render.png")
            
            except Exception as e:
                st.error(f"Render Error: {e}")

st.divider()
st.caption("EvVision-AI - Professional PropTech Solution 2026")
