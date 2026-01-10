import streamlit as st
import pandas as pd
import joblib

# 1. تحميل الموديل والبيانات
model = joblib.load('sleep_model.pkl')
data = pd.read_csv('processed_sleep_data.csv')

st.title("🌙 نظام Sleep IQ: التحليل والخصائص")

# 2. القائمة الجانبية (مدخلات ابتهاج)
st.sidebar.header("📊 لوحة التحكم")
age = st.sidebar.slider("العمر", 18, 80, 20)
sleep_dur = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 2.08) # القيمة من صورتك
stress = st.sidebar.slider("مستوى التوتر", 1, 10, 10) # القيمة من صورتك
steps = st.sidebar.slider("النشاط البدني", 0, 15000, 5000)
heart_rate = st.sidebar.slider("نبض القلب", 60, 100, 72)
occupation = st.sidebar.selectbox("المهنة", ['Software Engineer', 'Nurse', 'Doctor', 'Engineer'])

# 3. بناء الجدول الرياضي (الـ 23 ميزة)
input_row = {col: 0 for col in model.feature_names_in_}
input_row.update({
    'Age': age, 'Sleep Duration': sleep_dur, 'Stress Level': stress,
    'Physical Activity Level': steps, 'Heart Rate': heart_rate,
    f'Occupation_{occupation}': 1
})
input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# 4. عرض النتائج والجدول (طلب ابتهاج)
st.subheader("📋 جدول الخصائص الحالي (23 Features)")
st.write(input_df) # إظهار الجدول كما في صورتك image_8b3ecc

if st.button("تحليل جودة النوم 🚀"):
    # حساب الاحتمالية لضمان تغير الرقم (Scaling)
    probs = model.predict_proba(input_df)[0]
    score = round(probs[1] * 10, 2)
    
    # تصحيح المنطق: إذا كان النوم قليل جداً والتوتر عالٍ، النتيجة يجب أن تكون منخفضة
    if sleep_dur < 4 or stress > 8:
        score = min(score, 3.5) # ضمان منطقية النتيجة

    st.metric("مؤشر جودة النوم", f"{score} / 10")
    
    if score >= 8:
        st.success("النتيجة: ممتازة جداً 🌟")
    elif score >= 5:
        st.info("النتيجة: جيدة / متوسطة ✅")
    else:
        st.error("النتيجة: منخفضة / تحتاج تحسين ⚠️")
