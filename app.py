import streamlit as st
import pandas as pd
import joblib

# 1. تحميل الموديل والبيانات (الأساس الذي عملتِ عليه)
model = joblib.load('sleep_model.pkl')
data = pd.read_csv('processed_sleep_data.csv')

st.title("🌙 نظام Sleep IQ: التحليل الشامل لـ 23 مؤشر")

# 2. القائمة الجانبية: توزيع الخصائص (Features)
st.sidebar.header("📊 مدخلاتك الشخصية")

# الخصائص الأساسية
age = st.sidebar.slider("العمر", 18, 80, 25)
sleep_dur = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
stress = st.sidebar.slider("مستوى التوتر", 1, 10, 5)
steps = st.sidebar.slider("الخطوات اليومية", 0, 15000, 5000)
heart_rate = st.sidebar.slider("معدل ضربات القلب", 60, 100, 72)

# الخصائص الإضافية (من الـ 23 ميزة)
occupation = st.sidebar.selectbox("المهنة", [
    'Nurse', 'Doctor', 'Engineer', 'Lawyer', 'Teacher', 'Software Engineer', 'Scientist', 'Manager'
])
bmi_cat = st.sidebar.selectbox("فئة الوزن (BMI)", ['Normal', 'Overweight', 'Obese'])
sleep_disorder = st.sidebar.selectbox("هل تعاني من اضطراب نوم؟", ['None', 'Insomnia', 'Sleep Apnea'])

# 3. بناء المتجه الرياضي (The 23 Feature Vector)
# وظيفة ابتهاج: تحويل الاختيارات إلى أرقام يفهمها الموديل (One-Hot Encoding)
input_row = {col: 0 for col in model.feature_names_in_} # تصفير الـ 23 ميزة

# تعبئة القيم الرقمية
input_row.update({
    'Age': age,
    'Sleep Duration': sleep_dur,
    'Stress Level': stress,
    'Daily Steps': steps,
    'Heart Rate': heart_rate
})

# تفعيل المهنة (Occupation)
occ_col = f'Occupation_{occupation}'
if occ_col in input_row:
    input_row[occ_col] = 1

# تفعيل فئة الوزن (BMI)
bmi_col = f'BMI Category_{bmi_cat}'
if bmi_col in input_row:
    input_row[bmi_col] = 1

# تفعيل اضطراب النوم (Sleep Disorder)
if sleep_disorder != 'None':
    dis_col = f'Sleep Disorder_{sleep_disorder}'
    if dis_col in input_row:
        input_row[dis_col] = 1

# تحويل البيانات لـ DataFrame متوافق مع الموديل
input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# 4. النتيجة النهائية والتفاعل
if st.button("تحليل جودة النوم 🚀"):
    probs = model.predict_proba(input_df)[0]
    score = round(probs[1] * 10, 2)
    
    # تحويل الرقم إلى فئات نصية (طلب ابتهاج)
    if score >= 8.0:
        status, color = "ممتازة جداً 🌟", "green"
    elif score >= 5.0:
        status, color = "متوسطة ✅", "blue"
    else:
        status, color = "منخفضة ⚠️", "red"

    st.markdown(f"### الحالة المتوقعة: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
    st.metric("مؤشر جودة النوم (من 10)", f"{score} / 10")
