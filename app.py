import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# 1. تحميل الموديل والبيانات الأصلية لضمان الدقة
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('sleep_model.pkl')
        data = pd.read_csv('processed_sleep_data.csv')
        data.columns = data.columns.str.strip()
        return model, data
    except:
        return None, pd.DataFrame()

model, data = load_assets()

st.set_page_config(page_title="Sleep IQ Full Analysis", layout="wide")
st.title("🌙 نظام Sleep IQ: التحليل الفيزيائي والمهني الشامل")

# 2. القائمة الجانبية: إضافة كافة المهن والنشاط الفيزيائي
st.sidebar.header("🩺 الملف الشخصي والمؤشرات الحيوية")

with st.sidebar:
    gender = st.selectbox("الجنس", ["Male", "Female"])
    age = st.slider("العمر", 18, 80, 30)
    
    # قائمة المهن الكاملة كما في ملف الإكسل
    all_occupations = [
        "Accountant", "Doctor", "Engineer", "Lawyer", "Manager", 
        "Nurse", "Salesperson", "Sales Representative", "Scientist", 
        "Software Engineer", "Teacher"
    ]
    occupation = st.selectbox("المهنة", all_occupations)
    
    # إضافة النشاط الفيزيائي (Physical Activity Level) كما طلبتِ
    phys_level = st.slider("مستوى النشاط الفيزيائي (30-100)", 30, 100, 60)
    steps = st.number_input("عدد الخطوات اليومية", value=5000)
    
    st.markdown("---")
    sleep_dur = st.slider("ساعات النوم", 2.0, 12.0, 7.0)
    systolic = st.slider("الضغط الانقباضي", 90, 180, 120)
    stress = st.slider("مستوى التوتر", 1, 10, 5)
    heart_rate = st.slider("نبض القلب", 60, 100, 72)
    bmi_cat = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])

# 3. معالجة البيانات للموديل (Scaling & Encoding)
def scale_val(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val) if max_val != min_val else 0

if model:
    input_row = {col: 0 for col in model.feature_names_in_}
    input_row.update({
        'Gender': 1 if gender == "Male" else 0,
        'Age': scale_val(age, 18, 80),
        'Sleep Duration': scale_val(sleep_dur, 2, 12),
        'Quality of Sleep': 0, # سيتم توقعه
        'Physical Activity Level': scale_val(phys_level, 30, 100),
        'Stress Level': scale_val(stress, 1, 10),
        'Heart Rate': scale_val(heart_rate, 60, 100),
        'Daily Steps': scale_val(steps, 0, 10000),
        'Systolic_BP': scale_val(systolic, 90, 180)
    })
    
    if f'BMI Category_{bmi_cat}' in input_row: input_row[f'BMI Category_{bmi_cat}'] = 1
    if f'Occupation_{occupation}' in input_row: input_row[f'Occupation_{occupation}'] = 1
    input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# 4. النتائج والملاحظات الذكية
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🚀 نتيجة التحليل الذكي")
    if st.button("تحليل الحالة 💡"):
        probs = model.predict_proba(input_df)[0]
        score = round(probs[1] * 10, 1)
        st.metric("درجة جودة النوم", f"{score} / 10")
        
        st.markdown("---")
        st.subheader("🩺 التفسير الفيزيائي والطبي")
        
        # ربط الملاحظة بالتوتر والساعات كما طلبتِ
        if score <= 5.5:
            if sleep_dur >= 7.0 and stress > 5:
                st.error("التشخيص: انخفاض كفاءة النوم (رغم كفاية المدة) ⚠️")
                st.info(f"الملاحظة: مستوى التوتر العالي ({stress}) يفسد جودة الـ {sleep_dur} ساعات التي نمتها.")
            else:
                diag = "Sleep Apnea" if bmi_cat == "Obese" else "Insomnia"
                st.error(f"التشخيص المتوقع: {diag} ⚠️")
        else:
            st.success("الحالة: None (طبيعية) ✅")
            st.info("السبب الفيزيائي: هناك توازن إيجابي بين نشاطك وجودة نومك.")

with col2:
    st.subheader("📊 مصفوفة الارتباط الشاملة (Heatmap)")
    if not data.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        # عرض الهيت ماب الشاملة لكل الأعمدة الفيزيائية والطبية
        sns.heatmap(data.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".1f", ax=ax)
        st.pyplot(fig)

st.info(f"💡 المهنة المختارة: {occupation} | مستوى النشاط الفيزيائي: {phys_level}%")
