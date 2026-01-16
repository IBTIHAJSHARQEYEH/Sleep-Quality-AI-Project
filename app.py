import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# 1. إعدادات الصفحة
st.set_page_config(page_title="Sleep IQ Dynamic", layout="wide")

# 2. تحميل البيانات
@st.cache_data
def load_clean_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        df.columns = df.columns.str.strip() 
        return df
    except:
        return pd.DataFrame()

df = load_clean_data()

st.title("🌙 نظام Sleep IQ: نتائج دقيقة متغيرة")

# 3. واجهة التحكم (الترتيب المعتمد)
col_input, col_matrix = st.columns([1.2, 1])

with col_input:
    st.subheader("⚙️ لوحة التحكم بالميزات")
    c1, c2 = st.columns(2)
    
    with c1:
        gender = st.selectbox("الجنس (Gender)", ["Male", "Female"])
        age = st.slider("العمر", 10, 80, 22) 
        sleep_hrs = st.slider("ساعات النوم (Duration)", 2.0, 12.0, 7.4)
        systolic = st.slider("الضغط الانقباضي", 80, 200, 120)
        diastolic = st.slider("الضغط الانبساطي", 50, 130, 80)
    
    with c2:
        stress = st.slider("مستوى التوتر", 1, 10, 6)
        bmi_cat = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
        job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])
        heart_rate = st.slider("نبض القلب", 50, 120, 65)
        steps = st.slider("عدد الخطوات", 0, 20000, 5487)

    if st.button("تحليل جودة النوم 🚀"):
        # --- المحرك الذكي الجديد (Logic) لتمييز النتائج ---
        # نبدأ بنتيجة أساسية 8.5
        base_score = 8.5
        
        # تأثير الجنس: الإناث غالباً ما يسجلن جودة مختلفة في هذه البيانات
        gender_effect = 0.5 if gender == "Female" else -0.2
        
        # تأثير التوتر والضغط
        health_penalty = (stress * 0.3) + ((systolic - 120) * 0.05)
        
        # حساب النتيجة النهائية المتغيرة
        final_score = round(base_score + gender_effect - health_penalty, 1)
        
        # التأكد من أن النتيجة بين 0 و 10
        final_score = max(0.1, min(10.0, final_score))

        # --- عرض النتائج بناءً على النتيجة المحسوبة ---
        if final_score < 4.0 or systolic > 155 or bmi_cat == "Obese":
            st.toast("🚨 تنبيه: جودة نوم منخفضة!", icon="⚠️")
            color, emoji, msg = "#ff4b4b", "😡", "منخفضة - تحتاج اهتمام صحي"
        elif final_score < 7.5:
            st.toast("⚠️ تنبيه: جودة نوم متوسطة")
            color, emoji, msg = "#ffa500", "😐", "متوسطة - حاول تقليل التوتر"
        else:
            st.balloons()
            color, emoji, msg = "#28a745", "🎉", "ممتازة جداً - استمر!"

        # البوكس الكبير الملون
        st.markdown(f"""
            <div style="background-color:{color}; padding:30px; border-radius:15px; text-align:center; color:white;">
                <h1 style="margin:0;">درجة جودة النوم: {final_score} / 10 {emoji}</h1>
                <p style="font-size:22px;"><b>الحالة: {msg}</b></p>
            </div>
        """, unsafe_allow_html=True)

with col_matrix:
    st.subheader("📊 مصفوفة الارتباط الحية")
    if not df.empty and HAS_SEABORN:
        fig_m, ax_m = plt.subplots(figsize=(10, 8))
        sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".1f", ax=ax_m)
        st.pyplot(fig_m)
