import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. إعدادات الصفحة والجماليات
st.set_page_config(page_title="Sleep IQ Full Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 12px; height: 3em; font-weight: bold; }
    .result-card { padding: 25px; border-radius: 15px; text-align: center; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات الحقيقية لمصفوفة الارتباط
@st.cache_data
def load_full_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        return df
    except:
        return pd.DataFrame()

df = load_full_data()

st.title("🌙 نظام Sleep IQ: النسخة الكاملة والمطورة")
st.markdown("---")

# 3. واجهة التحكم (كافة الخصائص الـ 23)
col1, col2 = st.columns([1.2, 1.5])

with col1:
    st.subheader("👤 البيانات الشخصية والطبية")
    
    # تقسيم المدخلات لتسهيل القراءة
    c1, c2 = st.columns(2)
    with c1:
        gender = st.selectbox("الجنس", ["Male", "Female"])
        age = st.slider("العمر", 10, 90, 22)
        job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant", "Lawyer", "Salesperson", "Scientist"])
    
    with c2:
        sleep_duration = st.slider("ساعات النوم", 2.0, 12.0, 7.4)
        stress_level = st.select_slider("مستوى التوتر", options=list(range(1, 11)), value=6)
        bmi_category = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])

    st.markdown("---")
    st.subheader("🩺 المؤشرات الحيوية")
    c3, c4 = st.columns(2)
    with c3:
        systolic = st.number_input("الضغط الانقباضي", value=120)
        diastolic = st.number_input("الضغط الانبساطي", value=80)
    
    with c4:
        heart_rate = st.slider("نبض القلب", 50, 120, 65)
        daily_steps = st.number_input("عدد الخطوات اليومية", value=5487)

    if st.button("تحليل جودة النوم بالذكاء الاصطناعي 🚀"):
        # منطق التنبؤ (Logic) بناءً على تجاربك
        score = 9.7 # الحالة المثالية
        
        # تطبيق قواعدك المكتشفة (قاعدة الـ 0.1 والـ 0.0)
        if systolic > 155 or bmi_category == "Obese":
            # الممرضة تأخذ 0.1 بينما الطبيب 0.0 في الحالات الحرجة
            score = 0.1 if job == "Nurse" else 0.0
        elif stress_level > 8:
            score = 5.2 # انخفاض بسبب التوتر

        # العرض الجمالي
        if score >= 7.0:
            st.balloons() # إطلاق البوالين
            st.markdown(f"<div class='result-card' style='background-color: #28a745;'><h2>نوم مثالي 🎉</h2><h1>{score} / 10</h1></div>", unsafe_allow_html=True)
        elif score >= 4.0:
            st.markdown(f"<div class='result-card' style='background-color: #ffc107; color: black;'><h2>جودة متوسطة 😐</h2><h1>{score} / 10</h1></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-card' style='background-color: #dc3545;'><h2>جودة منخفضة 😡</h2><h1>{score} / 10</h1></div>", unsafe_allow_html=True)
            st.toast("تحذير: مؤشرات صحية حرجة!", icon="⚠️")

# 4. الرسوم البيانية (مصفوفة الارتباط Heatmap)
with col2:
    st.subheader("📊 مصفوفة ارتباط الخصائص (Heatmap)")
    if not df.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        # اختيار البيانات الرقمية فقط للارتباط
        corr = df.select_dtypes(include=[np.number]).corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        st.pyplot(fig)
    else:
        st.info("ارفع ملف processed_sleep_data.csv لرؤية خريطة الارتباط الحقيقية.")

# 5. رسم بياني إضافي يوضح "تفاعل الميزات"
st.divider()
st.subheader("📉 العلاقة بين ضغط الدم وجودة النوم")
if not df.empty:
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.regplot(data=df, x='Systolic BP', y='Quality of Sleep', color='blue', ax=ax2)
    st.pyplot(fig2)
