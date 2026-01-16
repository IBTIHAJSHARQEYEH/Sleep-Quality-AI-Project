import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. إعدادات الصفحة والجماليات
st.set_page_config(page_title="Sleep IQ Full Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stSlider { padding-bottom: 10px; }
    .result-card { padding: 25px; border-radius: 15px; text-align: center; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات مع التأكد من أسماء الأعمدة
@st.cache_data
def load_and_clean_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        return df
    except:
        return pd.DataFrame()

df = load_and_clean_data()

st.title("🌙 نظام Sleep IQ: النسخة الشاملة والمطورة")
st.markdown("---")

# 3. واجهة التحكم (كافة الخصائص مع Sliders للضغط)
col1, col2 = st.columns([1.2, 1.5])

with col1:
    st.subheader("👤 البيانات الشخصية والطبية")
    c1, c2 = st.columns(2)
    with c1:
        gender = st.selectbox("الجنس", ["Male", "Female"])
        age = st.slider("العمر", 10, 90, 22)
        job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant", "Lawyer", "Salesperson", "Scientist"])
        bmi_cat = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
    
    with c2:
        sleep_hrs = st.slider("ساعات النوم", 2.0, 12.0, 7.4)
        stress = st.slider("مستوى التوتر", 1, 10, 6)
        heart_rate = st.slider("نبض القلب", 50, 120, 65)
        steps = st.slider("عدد الخطوات اليومية", 0, 20000, 5487)

    st.markdown("---")
    st.subheader("🩺 ضغط الدم (بالمؤشر المنزلق)")
    # تم تحويلها لـ Sliders كما طلبتِ
    systolic = st.slider("الضغط الانقباضي (Systolic)", 90, 200, 120)
    diastolic = st.slider("الضغط الانبساطي (Diastolic)", 60, 130, 80)

    if st.button("تحليل جودة النوم 🚀"):
        score = 9.7 # افتراضي للحالات الجيدة
        
        # منطق الحالات الحرجة الذي اكتشفتِيه (قاعدة الطبيب والممرض)
        if systolic > 155 or bmi_cat == "Obese":
            score = 0.1 if job == "Nurse" else 0.0
        elif stress > 8:
            score = 5.2

        if score >= 7.0:
            st.balloons() # بوالين الاحتفال
            st.markdown(f"<div class='result-card' style='background-color: #28a745;'><h2>نوم مثالي 🎉</h2><h1>{score} / 10</h1></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-card' style='background-color: #dc3545;'><h2>جودة منخفضة 😡</h2><h1>{score} / 10</h1></div>", unsafe_allow_html=True)
            st.toast("تنبيه: مؤشرات صحية سيئة!", icon="⚠️")

# 4. الرسوم البيانية (مصفوفة الارتباط)
with col2:
    st.subheader("📊 مصفوفة ارتباط الخصائص (Heatmap)")
    if not df.empty:
        # إصلاح خطأ القوس
        fig, ax = plt.subplots(figsize=(10, 8)) 
        numeric_df = df.select_dtypes(include=[np.number])
        sns.heatmap(numeric_df.corr(), annot=True, cmap='RdYlGn', fmt=".2f", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("ارفع ملف البيانات لرؤية العلاقات البيانية.")

# 5. معالجة خطأ الـ KeyError في الرسم البياني
st.divider()
if not df.empty:
    st.subheader("📈 العلاقة بين الضغط وجودة النوم")
    # التأكد من كتابة اسم العمود بدقة كما هو في ملفك
    column_name = 'Systolic BP' if 'Systolic BP' in df.columns else 'BP_Systolic'
    fig2, ax2 = plt.subplots(figsize=(12, 4))
    sns.regplot(data=df, x=column_name, y='Quality of Sleep', color='blue', ax=ax2)
    st.pyplot(fig2)
