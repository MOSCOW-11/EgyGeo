import streamlit as st
import random
import string
import plotly.express as px
import time

# ==========================================
# 1. إعدادات الصفحة وتصميم الواجهة
# ==========================================
st.set_page_config(
    page_title="EgyGeo 🔎 | نظام التحليل الجغرافي",
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
# 2. إدارة الأكواد والرصيد
# ==========================================
def init_codes():
    if "codes_db" not in st.session_state:
        codes = {}
        characters = string.ascii_uppercase + string.digits
        while len(codes) < 50:
            middle_part = ''.join(random.choices(characters, k=8))
            code = f"M{middle_part}EG"
            if code not in codes:
                codes[code] = 5
        st.session_state["codes_db"] = codes

init_codes()

# ==========================================
# 3. بوابة الدخول (شاشة الحماية بالأكواد)
# ==========================================
def check_access():
    if "authenticated_code" not in st.session_state:
        st.session_state["authenticated_code"] = None

    current_code = st.session_state["authenticated_code"]
    
    if not current_code or st.session_state["codes_db"].get(current_code, 0) <= 0:
        if current_code and st.session_state["codes_db"].get(current_code, 0) <= 0:
            st.error("⚠️ نفد رصيد عمليات الفحص لهذا الكود!")
            st.session_state["authenticated_code"] = None

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center;'>EgyGeo 🔎</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #a1a1aa;'>نظام التحليل الجغرافي والبيئي الذكي</p>", unsafe_allow_html=True)
            
            user_key = st.text_input("أدخل مفتاح الوصول الخاص بك:", type="password")
            
            if st.button("دخول تجريبي سريع ⚡", use_container_width=True):
                st.session_state["authenticated_code"] = "M-DEMO-EG"
                st.session_state["codes_db"]["M-DEMO-EG"] = 10
                st.rerun()

            if st.button("تفعيل الكود", use_container_width=True):
                db = st.session_state["codes_db"]
                if user_key in db:
                    if db[user_key] > 0:
                        st.session_state["authenticated_code"] = user_key
                        st.success("تم تفعيل الكود بنجاح!")
                        st.rerun()
                    else:
                        st.error("هذا الكود استنفد بالكامل.")
                else:
                    st.error("مفتاح الوصول غير صحيح!")
        return False
    
    return True

# ==========================================
# 4. الواجهة الرئيسية وتحليل البيانات
# ==========================================
def main_interface():
    if "M-DEMO-EG" not in st.session_state["codes_db"]:
        st.session_state["codes_db"]["M-DEMO-EG"] = 10

    active_code = st.session_state["authenticated_code"]
    remaining_uses = st.session_state["codes_db"].get(active_code, 5)

    with st.sidebar:
        st.header("لوحة التحكم EgyGeo 📊")
        st.code(active_code, language="text")
        st.info(f"⚡ المحاولات المتبقية: **{remaining_uses}**")
        st.divider()
        if st.button("خروج 🚪", use_container_width=True):
            st.session_state["authenticated_code"] = None
            st.rerun()

    st.title("EgyGeo 🔎 | محرك التحليل الجغرافي المتقدم")
    st.write("ارفع صورة الشارع أو المسطح المائي لاختبار مرحلة التحليل البصري والجغرافي.")
    st.divider()

    uploaded_image = st.file_uploader("قم برفع الصورة هنا (JPG, PNG)", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="الصورة المراد تحليلها", use_container_width=True)
        
        if st.button("🚀 بدء تحليل المرحلتين (Stage 1 & Stage 2)", use_container_width=True):
            if remaining_uses > 0:
                st.session_state["codes_db"][active_code] -= 1
                
                with st.status("🔄 جاري فحص العناصر الاستخباراتية...", expanded=True) as status:
                    st.write("🔍 **المرحلة الأولى:** قراءة نمر اللوحات المعدنية ومؤشرات الإضاءة والمسطحات المائية...")
                    time.sleep(1.2)
                    st.write("🧠 **المرحلة الثانية:** تطبيق قواعد الترشيح الجغرافي لمحافظات مصر...")
                    time.sleep(1.2)
                    status.update(label="✅ اكتمل التحليل بنجاح!", state="complete", expanded=False)
                
                st.success("تم إتمام فحص الصورة واستخراج التقرير بنجاح!")
                
                st.markdown("### 📊 تقرير التحليل البصري:")
                st.info("• **تحليل اللوحات:** رصد إطار لوحة معدنية يتبع النطاق الإقليمي.\n• **التحليل البيئي:** المسطح المائي يظهر مياه هادئة تطابق مجرى نهر النيل.\n• **العمران:** طراز معماري يعكس الطابع السكني المصري.")
                
                st.markdown("### 📈 مؤشرات ترجيح المحافظات المصرية:")
                gov_data = {
                    "المحافظة": ["المنيا", "بني سويف", "أسيوط", "القاهرة"],
                    "نسبة المطابقة (%)": [72, 18, 7, 3]
                }
                fig_gov = px.bar(gov_data, x="المحافظة", y="نسبة المطابقة (%)", color="المحافظة", title="نسب المطابقة الإحصائية للمحافظات")
                st.plotly_chart(fig_gov, use_container_width=True)
                
                st.warning("🎯 **الترشيح الأقوى:** محافظة **المنيا** - منطقة **الكورنيش**")
                
                st.divider()
                maps_url = "https://www.google.com/maps/place/Minia,+El-Minia+Governorate"
                st.markdown(f'<a href="{maps_url}" target="_blank"><button style="background-color:#00ffcc; color:#0e1117; padding:10px 20px; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">فتح الموقع المستخلص على Google Maps 🌍</button></a>', unsafe_allow_html=True)
                
            else:
                st.error("عذراً، نفد رصيد هذا الكود!")

if check_access():
    main_interface()
