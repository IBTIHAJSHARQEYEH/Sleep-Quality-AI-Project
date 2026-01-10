import streamlit as st
import joblib
import pandas as pd
import numpy as np

# إعدادات الصفحة لتظهر بشكل احترافي
st.set_page_config(page_title="Sleep IQ: نظام التحليل الذكي", page_icon="🌙")

# تنسيق العناوين والألوان باستخدام CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 25px;
        font-weight: bold;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# تحميل النموذج والبيانات (بدون مسارات Colab)
try:
    model = joblib.load('sleep_model.pkl')
    df = pd.read_csv('processed_sleep_data.csv')
except:
    st.error("⚠️ خطأ: تأكد من وجود ملفات sleep_model.pkl و processed_sleep_data.csv في المستودع.")

st.title("🌙 نظام Sleep IQ: التحليل والتوصيات الذكية")

# واجهة المدخلات في الجانب (Sidebar)
st.sidebar.header("📋 لوحة البيانات الشخصية")
age = st.sidebar.slider("العمر", 10, 80, 25)
sleep_duration = st.sidebar.slider("ساعات النوم", 4.0, 12.0, 7.0)
steps = st.sidebar.number_input("الخطوات اليومية", 0, 20000, 5000)
stress_level = st.sidebar.slider("مستوى التوتر (1-10)", 1, 10, 5)

# زر التوقع
if st.button("🚀 الحصول على التوقع والتوصية"):
    # تجهيز البيانات للتنبؤ
    input_data = np.array([[age, sleep_duration, steps, stress_level]])
    
    # إجراء التنبؤ
    prediction = model.predict(input_data)[0]
    
    st.subheader("📊 تحليل جودة النوم")
    
    if prediction == 1:
        # عرض النتيجة باللون الأخضر
        st.success(f"✨ النتيجة: جودة نومك ممتازة! (التقييم: {prediction})")
        st.balloons()
        st.markdown('<div style="color: #155724; background-color: #d4edda; border-color: #c3e6cb; padding: 15px; border-radius: 5px;">✅ استمر على هذا المنوال، عاداتك الصحية تنعكس إيجاباً على نومك.</div>', unsafe_allow_html=True)
    else:
        # عرض النتيجة باللون الأصفر/البرتقالي
        st.warning(f"⚠️ النتيجة: جودة النوم تحتاج إلى تحسين. (التقييم: {prediction})")
        st.markdown('<div style="color: #856404; background-color: #fff3cd; border-color: #ffeeba; padding: 15px; border-radius: 5px;">💡 نصيحة: حاول تقليل التوتر قبل النوم بـ 30 دقيقة والالتزام بموعد ثابت للنوم.</div>', unsafe_allow_html=True)

# عرض رسم بياني بسيط للتوضيح
st.divider()
st.subheader("📈 استكشاف نشاطك")
st.scatter_chart(df[['Steps', 'Sleep Duration']])
