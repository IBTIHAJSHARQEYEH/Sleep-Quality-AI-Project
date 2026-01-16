import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# حل مشكلة نقص المكتبات الظاهرة في الصور
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# 1. إعدادات الصفحة
st.set_page_config(page_title="Sleep IQ Final Pro", layout="wide")

# 2. تحميل البيانات وتجهيزها لتجنب KeyError
@st.cache_data
def load_clean_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        df.columns = df.columns.str.strip() 
        return df
    except:
        return pd.DataFrame()

df = load_clean_data()

st.title("🌙 نظام Sleep IQ: النسخة المصلحة والنهائية")
st.markdown("---")

# 3. واجهة التحكم العلوية (الميزات والمصفوفة)
col_input, col_matrix = st.columns([1.2, 1])

with col_input:
    st.subheader("⚙️ لوحة التحكم بالميزات")
    c1, c2 = st.columns(2)
    
    with c1:
        gender = st.selectbox("الجنس (Gender)", ["Male", "Female"])
        age = st.slider("العمر", 10, 90, 22)
        # وضع الضغط تحت بعضه مباشرة
        systolic = st.slider("الضغط الانقباضي (Systolic)", 80, 200, 120)
        diastolic = st.slider("الضغط الانبساطي (Diastolic)", 50, 130, 80)
        sleep_hrs = st.slider("ساعات النوم (Duration)", 2.0, 12.0, 7.4)
    
    with c2:
        # نقل المهنة إلى العمود الثاني
        job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])
        stress = st.slider("مستوى التوتر", 1, 10, 6)
        bmi_cat = st.selectbox("فئة الوزن (BMI)", ["Normal Weight", "Overweight", "Obese"])
        heart_rate = st.slider("نبض القلب", 50, 120, 65)
        steps = st.slider("عدد الخطوات", 0, 20000, 5487)

    if st.button("تحليل جودة النوم 🚀"):
        # قيم الجودة الأصلية
        score = 9.7 
        
        # تصحيح الإزاحة (Indentation) كما في الصورة
        if systolic > 155 or diastolic > 95 or bmi_cat == "Obese":
            score = 0.1 if job == "Nurse" else 0.0
            st.error(f"تحذير: مؤشرات صحية حرجة! الجودة: {score} 😡")
        elif stress >
