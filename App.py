import streamlit as st
import google.generativeai as genai
from PIL import Image
import plotly.express as px
import json

# ==========================================
# 1. إعدادات الصفحة والواجهة
# ==========================================
st.set_page_config(
    page_title="EgyGeo 🔎 | نظام التحليل الجغرافي الذكي",
    page_icon="👁️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1, h2, h3 { color: #00ffcc; text-shadow: 0px 0px 10px rgba(0, 255, 204, 0.3); }
    .stButton>button { background-color: #00ffcc; color: #0e1117; font-weight: bold; border-radius: 8px; border: none; }
    .stButton>button:hover { background-color: #00b386; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إدخال مفتاح الـ API والتحقق
# ==========================================
st.sidebar.header("🔑 إعدادات الاتصال")
api_key = st.sidebar.text_input("أدخل مفتاح Google Gemini API:", type="password")

if not api_key:
    st.title("EgyGeo 🔎 | نظام التحليل الجغرافي المصري")
    st.warning("⚠️ يرجى إدخال مفتاح الـ API في القائمة الجانبية لتشغيل محرك الذكاء الاصطناعي الحقيقي.")
    st.info("💡 يمكنك جلب مفتاح مجاني بسهولة من موقع Google AI Studio.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# ==========================================
# 3. الواجهة الرئيسية وتحليل الصور الحقيقي
# ==========================================
st.title("EgyGeo 🔎 | محرك التحليل الجغرافي المتقدم (Live AI)")
st.write("ارفع صورة الشارع أو المعلم المصري لتطبيق مرحلتي التحليل البصري واستخراج الموقع الجغرافي بدقة.")
st.divider()

uploaded_image = st.file_uploader("قم برفع الصورة الحقيقية هنا (JPG, PNG)", type=["jpg", "png", "jpeg"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="الصورة المراد تحليلها", use_container_width=True)
    
    if st.button("🚀 بدء تحليل المرحلتين بالذكاء الاصطناعي", use_container_width=True):
        
        prompt = """
        Act as an elite Egyptian OSINT, computer vision, and geolocation expert. We are running a two-stage analysis pipeline.

        STAGE 1 INSTRUCTIONS (Visual Feature Extraction):
        Analyze the provided image strictly as a computer vision expert. Extract and describe everything visible:
        - Any vehicle license plates (letters and numbers if visible).
        - Any water bodies (are there waves meaning Mediterranean? light ripples meaning Red Sea? calm water meaning Nile River? or still pure water meaning a lake?).
        - Building styles, architecture, vegetation, road conditions, and lighting/shadows.

        STAGE 2 INSTRUCTIONS (Egyptian Geolocation & Mapping):
        Using the extracted visual data, apply comprehensive Egyptian mapping rules:
        - EGYPTIAN LICENSE PLATES CODES: Cairo (3 letters, 3 numbers), Giza (2 letters, 4 numbers), Regional (3 letters, 4 numbers like ن for Minia, س for Alexandria, ر for الشرقية, etc., and ط for Canal/Sinai).
        - ENVIRONMENTAL RULES: Waves = Mediterranean, Ripples = Red Sea, Calm river = Nile, Pure enclosed water = Lakes.

        Return your final analysis STRICTLY as a valid JSON object without any extra markdown formatting or backticks, with these exact keys:
        - "governorate": The most likely Egyptian governorate in Arabic.
        - "city": The most likely city or neighborhood in Arabic.
        - "confidence_score": An integer representing confidence percentage.
        - "details": A detailed explanation in Arabic of how the visual features mapped to this location.
        - "google_maps_query": A specific search query for Google Maps based on the location.
        - "top_governorates": A dictionary containing 3 alternative Egyptian governorates and their probability percentages summing up to 100 (e.g. {"المنيا": 70, "بني سويف": 20, "أسيوط": 10}).
        """

        with st.spinner("🔄 جارِ معالجة الصورة عبر محرك Gemini 2.5-Flash..."):
            try:
                response = model.generate_content([prompt, image])
                raw_text = response.text.replace("```json", "").replace("```", "").strip()
                result = json.loads(raw_text)
                
                st.success("✅ تم تحليل الصورة بنجاح بواسطة الذكاء الاصطناعي الحقيقي!")
                
                st.markdown("### 📊 تقرير التحليل البصري الاستخباراتي:")
                st.info(result.get("details", "لا توجد تفاصيل متاحة."))
                
                gov = result.get("governorate", "غير محدد")
                city = result.get("city", "غير محدد")
                conf = result.get("confidence_score", 0)
                
                st.metric(label="🎯 المحافظة المستخلصة", value=gov, delta=f"نسبة ثقة: {conf}%")
                st.write(f"**المدينة / المنطقة المقترحة:** {city}")
                
                st.markdown("### 📈 مؤشرات ترجيح المحافظات المصرية:")
                top_govs = result.get("top_governorates", {gov: conf})
                
                gov_names = list(top_govs.keys())
                gov_probs = list(top_govs.values())
                
                fig_gov = px.bar(
                    x=gov_names, 
                    y=gov_probs, 
                    labels={'x': 'المحافظة', 'y': 'نسبة المطابقة (%)'},
                    color=gov_names, 
                    title="تحليل احتمالية التوزيع الجغرافي"
                )
                st.plotly_chart(fig_gov, use_container_width=True)
                
                st.divider()
                
                maps_query = result.get("google_maps_query", "Egypt")
                maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
                st.markdown(f'<a href="{maps_url}" target="_blank"><button style="background-color:#00ffcc; color:#0e1117; padding:10px 20px; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">فتح الموقع المستخلص على Google Maps 🌍</button></a>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"حدث خطأ أثناء تحليل الصورة بواسطة الذكاء الاصطناعي: {e}")
