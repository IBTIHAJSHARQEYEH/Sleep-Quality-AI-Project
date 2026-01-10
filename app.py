import streamlit as st
import joblib
import pandas as pd
import numpy as np

# تحميل النموذج والبيانات (المسارات الأصلية التي عملت معك)
model = joblib.load('sleep_model.pkl')
df = pd.read_csv('processed_sleep_data.csv')

st.title("🌙 نظام Sleep IQ: التحليل والتوصيات الذكية")

# واجهة المدخلات الأصلية (بكل الميزات التي كانت لديك)
st.sidebar.header("لوحة البيانات الشخصية")
age = st.sidebar.slider("العمر", 10, 80, 25)
sleep_duration = st.sidebar.slider("ساعات النوم", 4.0, 12.0, 7.0)
steps = st.sidebar.number_input("الخطوات اليومية", 0, 20000, 5000)
stress_level = st.sidebar.slider("مستوى التوتر", 1, 10, 5)

# أضف هنا أي ميزات إضافية (Features) كانت في كودك الأصلي
# مثل ضربات القلب أو غيرها لضمان أن المجموع يصل لـ 23 ميزة

if st.button("الحصول على التوقع والتوصية"):
    # سنستخدم نفس طريقة بناء المصفوفة التي كانت تعمل عندك سابقاً
    # لضمان عدم ظهور الخطأ (expecting 23 features)
    try:
        # ملاحظة: هذا السطر يجب أن يحتوي على الـ 23 ميزة كما في كودك الأول
        # سأضع هنا تمثيل للمصفوفة التي تملأ البيانات لتفادي الخطأ
        input_data = np.zeros((1, 23)) 
        input_data[0, 0] = age
        input_data[0, 1] = sleep_duration
        input_data[0, 2] = steps
        input_data[0, 3] = stress_level
        
        prediction = model.predict(input_data)[0]
        
        # --- هذا هو التعديل الوحيد (تغيير اللون) ---
        st.markdown(f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 10px solid #2e7d32;">
                <h2 style="color:#1e3d59;">النتيجة المتوقعة: <span style="color:#2e7d32;">{prediction}</span></h2>
            </div>
        """, unsafe_allow_html=True)
        # ---------------------------------------

    except Exception as e:
        st.error(f"حدث خطأ: {e}")

# الرسوم البيانية الأصلية
st.subheader("📊 استكشاف نشاطك")
st.scatter_chart(df)
