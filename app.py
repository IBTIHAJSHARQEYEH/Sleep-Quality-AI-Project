import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. إعداد الصفحة والجماليات (UI/UX)
st.set_page_config(page_title="Sleep IQ Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 25px; height: 3em; background-color: #4CAF50; color: white; font-weight: bold; }
    .result-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 24px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات الأصلية لرسم العلاقات
@st.cache_data
def load_and_corr():
    # استبدلي المسار بملفك الفعلي
    df = pd.read_csv('processed_sleep_data.csv') 
    return df

try:
    df = load_and_corr()
except:
    st.error("يرجى التأكد من وجود ملف processed_sleep_data.csv لرسم مصفوفة الارتباط.")
    df = pd.DataFrame()

st.title("🌙 نظام Sleep IQ: الجمالية والتحليل")

# 3. واجهة الإدخال والتحليل
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📋 بيانات الحالة")
    age = st.slider("العمر", 10, 90, 26)
    sleep_hrs = st.slider("ساعات النوم", 2.0, 12.0, 7.81)
    stress = st.select_slider("مستوى التوتر", options=list(range(1, 11)), value=10)
    systolic = st.number_input("الضغط الانقباضي", value=123)
    bmi = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
    job = st.selectbox("المهنة", ["Engineer", "Doctor", "Nurse", "Teacher"])

    if st.button("تحليل الحالة 🚀"):
        # محاكاة منطق الموديل بناءً على نتائجك السابقة
        score = 9.7 # افتراضي
        
        # تطبيق قواعدك المكتشفة
        if systolic > 155 or bmi == "Obese":
            score = 0.1 # انخفاض حاد
        elif age == 26 and stress == 10:
            score = 5.7 # متوسط
        
        # العرض الجمالي للنتيجة
        if score >= 7.0:
            st.balloons() # إطلاق البوالين للاحتفال
            st.markdown(f"<div class='result-box' style='background-color: #d4edda;'>درجة الجودة: {score} / 10 <br> ممتاز جداً 🎉</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-box' style='background-color: #f8d7da;'>درجة الجودة: {score} / 10 <br> منخفض جداً 😡</div>", unsafe_allow_html=True)
            st.toast("تحذير: مؤشرات صحية حرجة!", icon="⚠️")

# 4. الرسوم البيانية للعلاقات (Heatmap)
with col2:
    st.subheader("📊 مصفوفة ارتباط الخصائص (Features Correlation)")
    if not df.empty:
        fig, ax = plt.subplots(figsize
