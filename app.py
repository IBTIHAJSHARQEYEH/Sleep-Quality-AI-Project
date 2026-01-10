import streamlit as st
import pandas as pd
import joblib

# 1. تحميل الملفات الأساسية
model = joblib.load('sleep_model.pkl')
data = pd.read_csv('processed_sleep_data.csv')

st.title("🌙 نظام Sleep IQ المطور")

# 2. إضافة قائمة المهن (Occupations) كما تظهر في بياناتك
st.sidebar.header("📝 البيانات المهنية والشخصية")
occupation = st.sidebar.selectbox("ما هي مهنتك؟", [
    'Software Engineer', 'Doctor', 'Engineer', 'Nurse', 'Manager', 
    'Sales Representative', 'Lawyer', 'Teacher', 'Scientist', 'Accountant'
])

# المدخلات الأساسية التي تؤثر على الرقم
sleep_dur = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
stress = st.sidebar.slider("مستوى التوتر", 1, 10, 5)
steps = st.sidebar.slider("النشاط البدني (الخطوات)", 0, 15000, 5000)

# 3. بناء الـ 23 فيتشر رياضياً (وظيفة ابتهاج)
input_row = {col: 0 for col in model.feature_names_in_} # تصفير كل القيم أولاً
input_row.update({
    'Sleep Duration': sleep_dur,
    'Stress Level': stress,
    'Daily Steps': steps,
    f'Occupation_{occupation}': 1 # تفعيل المهنة المختارة فقط بوضع رقم 1
})
input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# 4. التنبؤ والتقييم النصي
if st.button("تحليل جودة النوم 🚀"):
    probs = model.predict_proba(input_df)[0]
    score = round(probs[1] * 10, 2)
    
    # تحويل الرقم إلى كلمات (ممتازة، متوسطة، إلخ)
    if score >= 8.0:
        status, color = "ممتازة جداً 🌟", "green"
    elif score >= 5.0:
        status, color = "متوسطة / مستقرة ✅", "blue"
    else:
        status, color = "منخفضة / تحتاج تحسين ⚠️", "red"

    st.markdown(f"### النتيجة: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
    st.metric("مؤشر جودة النوم", f"{score} / 10")
