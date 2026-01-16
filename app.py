import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. إعدادات الصفحة
st.set_page_config(page_title="Sleep IQ: Comprehensive Analysis", layout="wide")

st.title("🌙 نظام Sleep IQ: التحليل الشامل (ساعات النوم والنشاط الفيزيائي)")

# 2. القائمة الجانبية مع كل الحقول الأساسية
st.sidebar.header("🩺 المدخلات الحيوية والفيزيائية")

with st.sidebar:
    gender = st.selectbox("الجنس", ["Male", "Female"])
    age = st.slider("العمر", 18, 80, 30)
    
    # ساعات النوم (تم إعادتها كعنصر أساسي)
    sleep_dur = st.slider("ساعات النوم (Sleep Duration)", 2.0, 12.0, 7.5) 
    
    occupation = st.selectbox("المهنة", [
        "Accountant", "Doctor", "Engineer", "Lawyer", "Manager", 
        "Nurse", "Salesperson", "Sales Representative", "Scientist", 
        "Software Engineer", "Teacher"
    ])
    
    systolic = st.slider("الضغط الانقباضي", 90, 180, 120)
    stress = st.slider("مستوى التوتر", 1, 10, 5)
    
    st.markdown("---")
    # التحليل الفيزيائي
    phys_level = st.slider("المستوى الحركي (Physical Activity)", 30, 100, 60)
    bmi_cat = st.selectbox("فئة الوزن", ["Normal", "Overweight", "Obese"])

# 3. محرك النتائج: ربط ساعات النوم بالتشخيص
col_res, col_viz = st.columns([1, 1.2])

with col_res:
    st.subheader("🚀 تقرير تحليل النوم")
    if st.button("تحليل الحالة 💡"):
        # حساب النتيجة بناءً على ساعات النوم وضغط الدم والتوتر
        # القاعدة: نقص ساعات النوم عن 6 يؤدي لتشخيص الأرق تلقائياً في بياناتك
        score = (sleep_dur * 0.8) - (stress * 0.3) - ((systolic - 120) * 0.1) + (phys_level * 0.02)
        final_score = round(max(1.0, min(10.0, score)), 1)
        
        st.metric("درجة جودة النوم", f"{final_score} / 10")
        
        # التشخيص الطبي المتوقع (Sleep Disorder)
        st.markdown("---")
        st.subheader("🩺 التشخيص النهائي")
        
        if sleep_dur < 6.0 or final_score <= 5.0 or systolic >= 140:
            if bmi_cat == "Obese":
                st.error("التشخيص: Sleep Apnea (انقطاع التنفس) ⚠️")
            else:
                st.error("التشخيص: Insomnia (أرق) ⚠️")
            st.info(f"ملاحظة: ساعات النوم ({sleep_dur}) غير كافية إحصائياً.")
        else:
            st.success("التشخيص: None (حالة طبيعية) ✅")

with col_viz:
    st.subheader("📊 مصفوفة الارتباط (Heatmap)")
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".1f", ax=ax)
        st.pyplot(fig)
    except:
        st.info("ارفع ملف البيانات لرؤية المصفوفة.")
