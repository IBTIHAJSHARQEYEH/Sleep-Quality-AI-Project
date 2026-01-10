import streamlit as st
import joblib
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="Sleep IQ", page_icon="🌙")

# تنسيق مخصص للألوان والخطوط
st.markdown("""
    <style>
    .big-font { font-size:26px !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

# تحميل النموذج
try:
    model = joblib.load('sleep_model.pkl')
except:
    st.error("⚠️ خطأ في تحميل ملف النموذج.")

st.title("🌙 نظام Sleep IQ: التحليل الذكي")

# مدخلات البيانات
st.sidebar.header("📋 بياناتك")
age = st.sidebar.slider("العمر", 10, 80, 25)
sleep_duration = st.sidebar.slider("ساعات النوم", 4.0, 12.0, 7.0)
steps = st.sidebar.number_input("الخطوات اليومية", 0, 20000, 5000)
stress_level = st.sidebar.slider("مستوى التوتر (1-10)", 1, 10, 5)

if st.button("🚀 الحصول على التوقع"):
    # تأكد من إرسال البيانات بنفس الترتيب الذي تدرب عليه النموذج
    input_data = np.array([[age, sleep_duration, steps, stress_level]])
    
    try:
        prediction = model.predict(input_data)[0]
        
        st.divider()
        st.subheader("📊 النتيجة:")

        if prediction == 1:
            # نجاح (لون أخضر)
            st.balloons()
            st.success("✨ جودة نومك ممتازة!")
            st.markdown(f'<p class="big-font" style="color: #2E7D32;">التقييم الرقمي: {prediction}</p>', unsafe_allow_html=True)
            st.info("💡 نصيحة: حافظ على هذا المستوى من النشاط البدني.")
        else:
            # تنبيه (لون برتقالي/أصفر)
            st.warning("⚠️ جودة نومك تحتاج إلى تحسين")
            st.markdown(f'<p class="big-font" style="color: #EF6C00;">التقييم الرقمي: {prediction}</p>', unsafe_allow_html=True)
            st.info("💡 نصيحة: حاول زيادة خطواتك اليومية قليلاً والخلود للنوم في وقت ثابت.")
            
    except Exception as e:
        st.error(f"حدث خطأ أثناء التنبؤ: {e}")
