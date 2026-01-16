import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# نظام حماية للمكتبات المفقودة
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# 1. إعدادات الصفحة
st.set_page_config(page_title="Sleep IQ Final Edition", layout="wide")

# 2. تحميل البيانات ومعالجة الأعمدة
@st.cache_data
def load_and_fix_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_and_fix_data()

st.title("🌙 نظام Sleep IQ: النسخة الشاملة بكامل الخصائص")
st.markdown("---")

# 3. واجهة التحكم (الميزات والمصفوفة بجانب بعض)
col_input, col_matrix = st.columns([1.2, 1])

with col_input:
    st.subheader("⚙️ لوحة التحكم بالميزات")
    c1, c2 = st.columns(2)
    with c1:
        gender = st.selectbox("الجنس (Gender)", ["Male", "Female"])
        age = st.slider("العمر", 10, 90, 22)
        job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])
        sleep_hrs = st.slider("ساعات النوم", 2.0, 12.0, 7.4)
        systolic = st.slider("الضغط الانقباضي", 80, 200, 120)
        diastolic = st.slider("الضغط الانبساطي", 50, 130, 80)
    
    with c2:
        stress = st.slider("مستوى التوتر", 1, 10, 6)
        bmi_cat = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
        heart_rate = st.slider("نبض القلب", 50, 120, 65)
        steps = st.slider("عدد الخطوات", 0, 20000, 5487)
        activity = st.slider("النشاط البدني (دقائق)", 0, 120, 45)
        sleep_quality_input = st.slider("جودة النوم الحالية", 1, 10, 7)

    if st.button("تحليل جودة النوم 🚀"):
        # قيم الجودة الأصلية بناءً على القواعد الصحية
        score = 9.7 
        
        # منطق التنبؤ المصلح (إزاحة صحيحة)
        if systolic > 155 or diastolic > 95 or bmi_cat == "Obese":
            score = 0.1 if job == "Nurse" else 0.0
            st.error(f"تحذير: مؤشرات صحية حرجة! الجودة المتوقعة: {score} 😡")
        elif stress > 8:
            score = 5.2
            st.warning(f"مستوى التوتر مرتفع! الجودة المتوقعة: {score} 😐")
        else:
            st.balloons() # تأثير البالونات
            st.success(f"نتيجة ممتازة! الجودة المتوقعة هي: {score} 🎉")

with col_matrix:
    st.subheader("📊 مصفوفة الارتباط الحية")
    if not df.empty and HAS_SEABORN:
        fig_m, ax_m = plt.subplots(figsize=(10, 9)) [cite: image_f8abdd
