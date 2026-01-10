import streamlit as st
import joblib
import pandas as pd
import numpy as np

# تحميل النموذج والبيانات
try:
    model = joblib.load('sleep_model.pkl')
    df = pd.read_csv('processed_sleep_data.csv')
except:
    st.error("⚠️ تأكد من وجود ملفات sleep_model.pkl و processed_sleep_data.csv في المستودع.")

st.title("🌙 نظام Sleep IQ: التحليل والتوصيات الذكية")

# واجهة المدخلات الجانبية
st.sidebar.header("لوحة البيانات الشخصية")
age = st.sidebar.slider("العمر", 10, 80, 25)
sleep_duration = st.sidebar.slider("ساعات النوم", 4.0, 12.0, 7.0)
steps = st.sidebar.number_input("الخطوات اليومية", 0, 20000, 5000)
stress_level = st.sidebar.slider("مستوى التوتر", 1, 10, 5)

# القسم الخاص بالتنبؤ
st.subheader("🎯 تحليل جودة النوم")
if st.button("الحصول على التوقع والتوصية"):
    # تجهيز البيانات لتطابق ما يحتاجه نموذجك (23 ميزة)
    # سننشئ مصفوفة تحتوي على 23 ميزة تعتمد على مدخلاتك الأساسية
    features = np.zeros((1, 23)) 
    features[0, 0] = age
    features[0, 1] = sleep_duration
    features[0, 2] = steps
    features[0, 3] = stress_level
    
    try:
        prediction = model.predict(features)[0]
        
        # عرض النتيجة بلون مميز (أزرق غامق وخلفية خفيفة) لتكون واضحة جداً
        st.markdown(f"""
            <div style="background-color:#e1f5fe; padding:20px; border-radius:10px; border: 2px solid #01579b;">
                <h2 style="color:#01579b; text-align:center; margin:0;">
                    النتيجة المتوقعة: {prediction}
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"يرجى التأكد من مطابقة مدخلات النموذج: {e}")

# عرض الرسم البياني الذي كان يظهر سابقاً
st.divider()
st.subheader("📊 استكشاف نشاطك")
st.write("العلاقة بين خطواتك وجودة النوم:")
st.scatter_chart(df)
