import streamlit as st
import pandas as pd
import joblib

# 1. تحميل الموديل والبيانات (الأساس الرياضي لابتهاج)
model = joblib.load('sleep_model.pkl')
data = pd.read_csv('processed_sleep_data.csv')

st.title("🌙 نظام Sleep IQ: التحليل الشامل لـ 23 مؤشر")

# 2. القائمة الجانبية: المدخلات
st.sidebar.header("📊 مدخلاتك الشخصية")
age = st.sidebar.slider("العمر", 18, 80, 20)
sleep_dur = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
stress = st.sidebar.slider("مستوى التوتر", 1, 10, 5)
steps = st.sidebar.slider("النشاط البدني (الخطوات)", 0, 15000, 5000)
heart_rate = st.sidebar.slider("معدل ضربات القلب", 60, 100, 72)

# القوائم المنسدلة للخصائص الفئوية (Categorical)
occupation = st.sidebar.selectbox("المهنة", [
    'Software Engineer', 'Doctor', 'Engineer', 'Nurse', 'Lawyer', 'Teacher', 'Scientist', 'Manager'
])
bmi_cat = st.sidebar.selectbox("فئة الوزن (BMI)", ['Normal', 'Overweight', 'Obese'])

# 3. بناء الجدول الرياضي (The 23 Feature Table)
# وظيفة ابتهاج: تصفير المتجه وتعبئته بالقيم الحالية
input_row = {col: 0 for col in model.feature_names_in_}

input_row.update({
    'Age': age,
    'Sleep Duration': sleep_dur,
    'Stress Level': stress,
    'Physical Activity Level': steps,
    'Heart Rate': heart_rate
})

# تفعيل المهنة المختارة (One-Hot Encoding)
if f'Occupation_{occupation}' in input_row:
    input_row[f'Occupation_{occupation}'] = 1

# تفعيل فئة الوزن المختارة
if f'BMI Category_{bmi_cat}' in input_row:
    input_row[f'BMI Category_{bmi_cat}'] = 1

input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# --- إظهار الجدول الذي طلبتهِ يا ابتهاج ليتأكد الموديل من الـ 23 ميزة ---
st.subheader("📋 جدول الخصائص المرسل للموديل (The Input Vector)")
st.write(input_df) # هذا الأمر سيظهر الجدول الذي كان يظهر سابقاً

# 4. النتيجة النهائية والتفاعل
if st.button("تحليل جودة النوم 🚀"):
    probs = model.predict_proba(input_df)[0]
    score = round(probs[1] * 10, 2)
    
    # تحويل الرقم إلى فئات نصية ملونة
    if score >= 8.0:
        status, color = "ممتازة جداً 🌟", "green"
    elif score >= 5.0:
        status, color = "متوسطة ✅", "blue"
    else:
        status, color = "منخفضة ⚠️", "red"

    st.markdown(f"### الحالة المتوقعة: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
    st.metric("مؤشر جودة النوم الحقيقي", f"{score} / 10")
