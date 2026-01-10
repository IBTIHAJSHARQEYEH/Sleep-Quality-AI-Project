import streamlit as st
import joblib
import pandas as pd
import numpy as np

# إعدادات الصفحة
st.set_page_config(page_title="Sleep IQ: التحليل الذكي", page_icon="🌙")

# تنسيق الألوان
st.markdown("""
    <style>
    .result-text {
        font-size: 24px;
        font-weight: bold;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# تحميل الملفات
try:
    model = joblib.load('sleep_model.pkl')
    # قمنا بإزالة محاولة رسم الرسم البياني المعقد لتجنب أخطاء أسماء الأعمدة
except:
    st.error("تأكد من وجود الملفات المطلوبة في المستودع.")

st.title("🌙 نظام Sleep IQ: التحليل الذكي")

# المدخلات
st.sidebar.header("📋 بياناتك")
age = st.sidebar.slider("العمر", 10, 80, 25)
sleep_duration = st.sidebar.slider("ساعات النوم", 4.0, 12.0, 7.0)
steps = st.sidebar.number_input("الخطوات اليومية", 0, 20000, 5000)
stress_level = st.sidebar.slider("مستوى التوتر (1-10)", 1, 10, 5)

if st.button("🚀 الحصول على التوقع"):
    input_data = np.array([[age, sleep_duration, steps, stress_level]])
    prediction = model.predict(input_data)[0]
    
    st.subheader("📊 النتيجة النهائية:")
    
    if prediction == 1:
        # لون أخضر للنتيجة الجيدة
        st.balloons()
        st.success(f"### ✨ جودة نومك ممتازة! (التقييم: {prediction})")
        st.info("💡 نصيحة: حافظ على هذا المستوى الرائع من النشاط البدني.")
    else:
        # لون برتقالي للتنبيه
        st.warning(f"### ⚠️ جودة نومك تحتاج لتحسين. (التقييم: {prediction})")
        st.info("💡 نصيحة: حاول تحسين عدد خطواتك اليومية وتقليل ساعات استخدام الهاتف قبل النوم.")
