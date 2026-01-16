import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# حل مشكلة نقص المكتبات
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# 1. إعدادات الصفحة
st.set_page_config(page_title="Sleep IQ Final Layout", layout="wide")

# 2. تحميل البيانات ومعالجة الأسماء لتجنب KeyError
@st.cache_data
def load_clean_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        df.columns = df.columns.str.strip() 
        return df
    except:
        return pd.DataFrame()

df = load_clean_data()

st.title("🌙 نظام Sleep IQ: التنسيق النهائي للميزات")
st.markdown("---")

# 3. واجهة التحكم العلوية (الميزات والمصفوفة)
col_input, col_matrix = st.columns([1.2, 1])

with col_input:
    st.subheader("⚙️ لوحة التحكم بالميزات")
    c1, c2 = st.columns(2)
    
    with c1:
        # ترتيب العمود الأول: ساعات النوم فوق والضغط تحت
        sleep_hrs = st.slider("ساعات النوم (Sleep Duration)", 2.0, 12.0, 7.4)
        st.markdown("---")
        systolic = st.slider("الضغط الانقباضي (Systolic)", 80, 200, 120)
        diastolic = st.slider("الضغط الانبساطي (Diastolic)", 50, 130, 80)
        gender = st.selectbox("الجنس (Gender)", ["Male", "Female"])
        age = st.slider("العمر", 10, 90, 22)
    
    with c2:
        # ترتيب العمود الثاني: التوتر فوق، ثم الوزن، ثم المهنة تحت الوزن
        stress = st.slider("مستوى التوتر (Stress Level)", 1, 10, 6)
        st.markdown("---")
        bmi_cat = st.selectbox("فئة الوزن (BMI Category)", ["Normal Weight", "Overweight", "Obese"])
        job = st.selectbox("المهنة (Occupation)", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])
        heart_rate = st.slider("نبض القلب", 50, 120, 65)
        steps = st.slider("عدد الخطوات", 0, 20000, 5487)

    if st.button("تحليل جودة النوم 🚀"):
        # قيم الجودة الأصلية
        score = 9.7 
        
        # تصحيح الإزاحة (Indentation) لمنع الخطأ البرمجي
        if systolic > 155 or diastolic > 95 or bmi_cat == "Obese":
            score = 0.1 if job == "Nurse" else 0.0
            st.error(f"تحذير: مؤشرات صحية حرجة! الجودة: {score} 😡")
        elif stress > 8:
            score = 5.2
            st.warning(f"مستوى التوتر مرتفع! الجودة: {score} 😐")
        else:
            st.balloons() # إرجاع البالونات
            st.success(f"نتيجة ممتازة! الجودة المتوقعة هي: {score} 🎉")

with col_matrix:
    st.subheader("📊 مصفوفة الارتباط الحية")
    if not df.empty and HAS_SEABORN:
        # إصلاح الأقواس لمنع SyntaxError
        fig_m, ax_m = plt.subplots(figsize=(10, 8))
        sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".1f", ax=ax_m)
        st.pyplot(fig_m)

st.markdown("---")

# 4. الأزرار السفلية للرسومات
st.subheader("🔍 استعراض التقارير الإحصائية")
col_b1, col_b2, col_b3 = st.columns(3)

if col_b1.button("📊 جودة النوم vs الوزن"):
    if not df.empty and HAS_SEABORN:
        fig1, ax1 = plt.subplots()
        sns.boxplot(data=df, x='BMI Category', y='Quality of Sleep', palette='Set2', ax=ax1)
        st.pyplot(fig1)

if col_b2.button("📉 تحليل الضغط"):
    if not df.empty and HAS_SEABORN:
        bp_col = 'Systolic BP' if 'Systolic BP' in df.columns else (df.columns[1] if len(df.columns)>1 else df.columns[0])
        fig2, ax2 = plt.subplots()
        sns.regplot(data=df, x=bp_col, y='Quality of Sleep', color='blue', ax=ax2)
        st.pyplot(fig2)

if col_b3.button("🧪 التوتر والعمر"):
    if not df.empty and HAS_SEABORN:
        fig3, ax3 = plt.subplots()
        sns.scatterplot(data=df, x='Age', y='Quality of Sleep', hue='Stress Level', ax=ax3)
        st.pyplot(fig3)
