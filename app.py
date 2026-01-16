import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# حماية استيراد seaborn
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# 1. إعدادات الصفحة
st.set_page_config(page_title="Sleep IQ Full Features", layout="wide")

# 2. تحميل البيانات
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_data()

st.title("🌙 نظام Sleep IQ: النسخة الكاملة بالجودة الأصلية")
st.markdown("---")

# 3. القسم العلوي: كافة الميزات والمصفوفة
col_input, col_matrix = st.columns([1.2, 1])

with col_input:
    st.subheader("⚙️ التحكم بكافة الخصائص")
    
    c1, c2 = st.columns(2)
    with c1:
        age = st.slider("العمر", 10, 90, 22)
        job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])
        sleep_hrs = st.slider("ساعات النوم (Duration)", 2.0, 12.0, 7.4)
        # تعديل الضغط ليكون دقيقاً (الانقباضي يبدأ من 90 والانبساطي من 60)
        systolic = st.slider("الضغط الانقباضي (Systolic)", 80, 200, 120)
        diastolic = st.slider("الضغط الانبساطي (Diastolic)", 50, 130, 80)
    
    with c2:
        stress = st.slider("مستوى التوتر", 1, 10, 6)
        bmi_cat = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
        heart_rate = st.slider("نبض القلب", 50, 120, 65)
        steps = st.slider("عدد الخطوات", 0, 20000, 5487)
        physical_activity = st.slider("النشاط البدني (دقائق)", 0, 120, 45)

    if st.button("تحليل جودة النوم 🚀"):
        # إرجاع قيم الجودة المتوقعة الأصلية
        score = 9.7 # الجودة المثالية
        
        # المنطق الخاص بضغط الدم والمهنة والوزن
        if systolic > 155 or diastolic > 95 or bmi_cat == "Obese":
