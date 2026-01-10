import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# 1. تحميل الموديل والبيانات الأصلية للرسم البياني
model = joblib.load('sleep_model.pkl')
data = pd.read_csv('processed_sleep_data.csv')

st.set_page_config(page_title="Sleep IQ Pro", layout="wide")
st.title("🌙 نظام Sleep IQ: التحليل الشامل والرسوم البيانية")

# 2. القائمة الجانبية (مدخلات ابتهاج الكاملة)
st.sidebar.header("🩺 البيانات الشخصية والطبية")
gender = st.sidebar.selectbox("الجنس", ["Male", "Female"])
age = st.sidebar.slider("العمر", 18, 80, 25)
systolic = st.sidebar.slider("الضغط الانقباضي", 90, 180, 120)
diastolic = st.sidebar.slider("الضغط الانبساطي", 60, 110, 80)
sleep_dur = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
stress = st.sidebar.slider("مستوى التوتر", 1, 10, 5)
steps = st.sidebar.number_input("عدد الخطوات اليومية", value=5000)
heart_rate = st.sidebar.slider("نبض القلب", 60, 100, 72)
bmi_cat = st.sidebar.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
occupation = st.sidebar.selectbox("المهنة", ['Nurse', 'Doctor', 'Engineer', 'Lawyer', 'Teacher', 'Software Engineer'])

# 3. بناء الجدول الرياضي (الـ 23 ميزة)
input_row = {col: 0 for col in model.feature_names_in_}
input_row.update({
    'Gender': 1 if gender == "Male" else 0, 'Age': age, 'Sleep Duration': sleep_dur,
    'Stress Level': stress, 'Physical Activity Level': steps, 'Daily Steps': steps,
    'Heart Rate': heart_rate, 'Systolic_BP': systolic, 'Diastolic_BP': diastolic
})

if f'BMI Category_{bmi_cat}' in input_row: input_row[f'BMI Category_{bmi_cat}'] = 1
if f'Occupation_{occupation}' in input_row: input_row[f'Occupation_{occupation}'] = 1

input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# 4. العرض المرئي (الجدول والرسم البياني الملون)
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("🚀 نتيجة التحليل")
    if st.button("تحليل الحالة 💡"):
        probs = model.predict_proba(input_df)[0]
        score = round(probs[1] * 10, 1)
        if sleep_dur < 4 or systolic > 145: score = min(score, 4.0)
        
        st.metric("درجة جودة النوم", f"{score} / 10")
        if score >= 7.5: st.success("ممتاز جداً 🌟")
        elif score >= 5: st.info("متوسط ✅")
        else: st.error("منخفض ⚠️")

with col2:
    st.subheader("📊 العلاقة بين الخطوات وجودة النوم")
    # الرسم البياني الملون الذي طلبتِه
    fig = px.scatter(data, x='Daily Steps', y='Quality of Sleep', 
                     color='Stress Level', 
                     title="توزيع البيانات (الخطوات vs النوم)",
                     color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig, use_container_width=True)

# 5. إظهار جدول الـ 23 ميزة في الأسفل
st.subheader("📋 مصفوفة البيانات المرسلة للموديل (Input Vector)")
st.write(input_df)
