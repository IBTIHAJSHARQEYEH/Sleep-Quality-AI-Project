import streamlit as st
import pandas as pd
import joblib

# 1. تحميل الموديل (الذي يحتوي على الـ 23 فيتشر)
model = joblib.load('sleep_model.pkl')

st.title("🌙 نظام Sleep IQ: التقييم الطبي المتكامل")

# 2. القائمة الجانبية (مدخلات ابتهاج الشخصية)
st.sidebar.header("🩺 القياسات الطبية والشخصية")
gender = st.sidebar.selectbox("الجنس", ["Male", "Female"])
age = st.sidebar.slider("العمر", 18, 80, 25)

# --- إضافة قياسات ضغط الدم (طلب ابتهاج) ---
st.sidebar.markdown("---")
st.sidebar.subheader("💓 ضغط الدم")
systolic = st.sidebar.slider("الضغط الانقباضي (Systolic)", 90, 180, 120)
diastolic = st.sidebar.slider("الضغط الانبساطي (Diastolic)", 60, 110, 80)
st.sidebar.markdown("---")

sleep_dur = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
stress = st.sidebar.slider("مستوى التوتر", 1, 10, 5)
steps = st.sidebar.number_input("عدد الخطوات اليومية", value=5000)
heart_rate = st.sidebar.slider("نبض القلب", 60, 100, 72)

bmi_cat = st.sidebar.selectbox("فئة الوزن (BMI)", ["Normal Weight", "Overweight", "Obese"])
occupation = st.sidebar.selectbox("المهنة", ['Nurse', 'Doctor', 'Engineer', 'Lawyer', 'Teacher', 'Software Engineer', 'Scientist', 'Manager'])

# 3. بناء الجدول الرياضي (الـ 23 ميزة)
input_row = {col: 0 for col in model.feature_names_in_}

input_row.update({
    'Gender': 1 if gender == "Male" else 0,
    'Age': age,
    'Sleep Duration': sleep_dur,
    'Stress Level': stress,
    'Physical Activity Level': steps,
    'Daily Steps': steps,
    'Heart Rate': heart_rate,
    'Systolic_BP': systolic, # القيمة التي تدخلينها يدوياً
    'Diastolic_BP': diastolic # القيمة التي تدخلينها يدوياً
})

# تفعيل الـ BMI والمهنة (One-Hot Encoding)
if f'BMI Category_{bmi_cat}' in input_row:
    input_row[f'BMI Category_{bmi_cat}'] = 1
if f'Occupation_{occupation}' in input_row:
    input_row[f'Occupation_{occupation}'] = 1

input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# 4. عرض الجدول (Input Vector) للتأكد من البيانات
st.subheader("📋 مصفوفة الخصائص الطبية (23 Features)")
st.write(input_df) # سيظهر هنا ضغط الدم الذي أدخلتِه

# 5. النتيجة والتوصية
if st.button("تحليل جودة النوم 🚀"):
    probs = model.predict_proba(input_df)[0]
    score = round(probs[1] * 10, 1)
    
    # منطق لضمان حلاوة النتيجة ومنطقيتها
    if systolic > 140 or sleep_dur < 4:
        score = min(score, 4.5)
        
    st.markdown(f"## مؤشر جودة النوم: {score} / 10")
    
    if score >= 7.5:
        st.success("النتيجة: نوم صحي ومثالي ✨")
    else:
        st.warning("النتيجة: جودة النوم منخفضة، يرجى مراجعة العادات اليومية ⚠️")
