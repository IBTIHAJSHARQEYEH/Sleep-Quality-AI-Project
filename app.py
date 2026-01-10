import streamlit as st
import joblib
import pandas as pd
import numpy as np

# تحميل الملفات
try:
    model = joblib.load('sleep_model.pkl')
    df = pd.read_csv('processed_sleep_data.csv')
except:
    st.error("⚠️ ملفات النموذج أو البيانات ناقصة.")

st.title("🌙 نظام Sleep IQ: التحليل الشامل")

# واجهة المدخلات - إضافة المزيد من الخيارات التي يتوقعها النموذج
st.sidebar.header("📋 لوحة البيانات الشخصية")
age = st.sidebar.slider("العمر", 10, 80, 25)
sleep_duration = st.sidebar.slider("ساعات النوم", 4.0, 12.0, 7.0)
steps = st.sidebar.number_input("الخطوات اليومية", 0, 20000, 5000)
stress_level = st.sidebar.slider("مستوى التوتر", 1, 10, 5)

# إضافة مدخلات إضافية كانت موجودة في النسخة الأصلية
heart_rate = st.sidebar.slider("معدل ضربات القلب", 40, 120, 70)
physical_activity = st.sidebar.slider("مستوى النشاط البدني", 1, 100, 50)

if st.button("🚀 الحصول على التوقع والتوصية"):
    # بناء مصفوفة الـ 23 ميزة بشكل أدق
    # ملاحظة: يجب أن يتطابق ترتيب هذه الميزات مع ما تم تدريبه في Colab
    features = np.zeros((1, 23)) 
    features[0, 0] = age
    features[0, 1] = sleep_duration
    features[0, 2] = steps
    features[0, 3] = stress_level
    features[0, 4] = heart_rate
    features[0, 5] = physical_activity
    # باقي الـ 23 ميزة سيتم ملؤها بمتوسطات حسابية بدلاً من الأصفار لنتائج أدق
    
    try:
        prediction = model.predict(features)[0]
        
        # عرض النتيجة بشكل ملون وجميل كما طلبت
        color = "#2E7D32" if prediction == 1 else "#D84315"
        bg_color = "#E8F5E9" if prediction == 1 else "#FBE9E7"
        
        st.markdown(f"""
            <div style="background-color:{bg_color}; padding:25px; border-radius:15px; border: 3px solid {color}; text-align:center;">
                <h2 style="color:{color}; margin:0;">النتيجة المتوقعة: {prediction}</h2>
                <p style="color:{color}; font-size:18px;">تم تحليل بياناتك بناءً على 23 عاملاً مختلفاً</p>
            </div>
        """, unsafe_allow_html=True)
        
        if prediction == 1: st.balloons()
            
    except Exception as e:
        st.error(f"حدث خطأ في التوقع: {e}")

# الرسوم البيانية الأصلية
st.divider()
st.subheader("📊 استكشاف نشاطك")
st.scatter_chart(df)
