import streamlit as st
import joblib
import pandas as pd
import numpy as np

# 1. تحميل النموذج والبيانات الأصليين
try:
    model = joblib.load('sleep_model.pkl')
    df = pd.read_csv('processed_sleep_data.csv')
except:
    st.error("تأكد من وجود ملفات sleep_model.pkl و processed_sleep_data.csv")

# عنوان البرنامج كما في الصورة
st.title("🌙 نظام Sleep IQ: التحليل والتوصيات الذكية")

# 2. واجهة المدخلات الأصلية (Sidebar)
st.sidebar.header("لوحة البيانات الشخصية")
age = st.sidebar.slider("العمر", 10, 80, 25)
sleep_duration = st.sidebar.slider("ساعات النوم", 4.0, 12.0, 7.0)
steps = st.sidebar.number_input("الخطوات اليومية", 0, 20000, 5000)
stress_level = st.sidebar.slider("مستوى التوتر", 1, 10, 5)

# أي ميزات إضافية كانت تظهر في صورتك الأصلية
# (مثلاً معدل ضربات القلب إذا كان موجوداً في كودك الأول)

# 3. تحليل جودة النوم
st.subheader("🎯 تحليل جودة النوم")
if st.button("الحصول على التوقع والتوصية"):
    # تجهيز المدخلات للنموذج (نستخدم الـ 23 ميزة التي يطلبها نموذجك)
    # ملاحظة: استبدل هذا الجزء بطريقة ترتيب الـ 23 ميزة في كودك الأصلي إذا كنت تملكها
    features = np.zeros((1, 23))
    features[0, 0] = age
    features[0, 1] = sleep_duration
    features[0, 2] = steps
    features[0, 3] = stress_level
    
    try:
        prediction = model.predict(features)[0]
        
        # --- تعديل اللون المطلوب ---
        st.markdown(f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-right: 10px solid #2e7d32; direction: rtl;">
                <h2 style="color:#1e3d59; margin:0;">النتيجة المتوقعة: <span style="color:#2e7d32;">{prediction}</span></h2>
            </div>
        """, unsafe_allow_html=True)
        # ---------------------------
        
    except Exception as e:
        st.error(f"حدث خطأ في التنبؤ: {e}")

# 4. الرسوم البيانية الأصلية كما في الصورة
st.divider()
st.subheader("📊 استكشاف نشاطك")
st.write("العلاقة بين خطواتك وجودة النوم:")
# عرض الرسم البياني الأصلي الذي ظهر في صورتك
st.scatter_chart(df)
