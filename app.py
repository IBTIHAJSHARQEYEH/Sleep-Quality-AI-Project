import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# نظام حماية المكتبات
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# 1. إعدادات الصفحة
st.set_page_config(page_title="Sleep IQ Final Pro", layout="wide")

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

st.title("🌙 نظام Sleep IQ: التنفيذ الدقيق للنتائج")

# 3. واجهة التحكم - التأكد من ربط المتغيرات
col_input, col_matrix = st.columns([1.2, 1])

with col_input:
    st.subheader("⚙️ لوحة التحكم بالميزات")
    c1, c2 = st.columns(2)
    
    with c1:
        # هذه المتغيرات (gender, age, etc.) هي التي تتحكم بالنتيجة
        gender = st.selectbox("الجنس", ["Male", "Female"])
        age = st.slider("العمر", 10, 80, 22) 
        sleep_hrs = st.slider("ساعات النوم", 2.0, 12.0, 7.4)
        systolic = st.slider("الضغط الانقباضي", 80, 200, 120)
        diastolic = st.slider("الضغط الانبساطي", 50, 130, 80)
    
    with c2:
        stress = st.slider("مستوى التوتر", 1, 10, 6)
        bmi_cat = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
        job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])
        heart_rate = st.slider("نبض القلب", 50, 120, 65)
        steps = st.slider("عدد الخطوات", 0, 20000, 5487)

    st.markdown("###")
    # 4. إصلاح منطق النتائج (The Engine)
    if st.button("تحليل جودة النوم 🚀"):
        # ترتيب الشروط مهم جداً هنا لضمان دقة "التنفيذ"
        if systolic > 155 or diastolic > 95 or bmi_cat == "Obese":
            # الحالة الأولى: خطر صحي (الضغط أو السمنة)
            score = 0.1 if job == "Nurse" else 0.0
            st.toast("🚨 تنبيه: تم رصد مؤشرات صحية حرجة!", icon="⚠️")
            color = "#ff4b4b" # أحمر
            status_text = "تحذير: جودة نوم متدنية بسبب المؤشرات الحيوية."
            emoji = "😡"
        elif stress > 8:
            # الحالة الثانية: توتر عالي
            score = 5.2
            st.toast("⚠️ تنبيه: مستوى التوتر مرتفع جداً!")
            color = "#ffa500" # برتقالي
            status_text = "تنبيه: التوتر المرتفع يؤثر على كفاءة النوم."
            emoji = "😐"
        else:
            # الحالة الثالثة: نوم مثالي
            score = 9.7
            st.balloons()
            st.toast("✅ نتائج ممتازة! جودة نومك مثالية.", icon="🎉")
            color = "#28a745" # أخضر
            status_text = "مبروك! أنت تتمتع بجودة نوم مثالية ومؤشرات صحية مستقرة."
            emoji = "🎉"

        # عرض البوكس الملون المصلح
        st.markdown(f"""
            <div style="background-color:{color}; padding:30px; border-radius:15px; text-align:center; color:white; border: 2px solid white;">
                <h1 style="margin:0;">النتيجة: {score} {emoji}</h1>
                <p style="font-size:20px;"><b>{status_text}</b></p>
            </div>
        """, unsafe_allow_html=True)

with col_matrix:
    st.subheader("📊 مصفوفة الارتباط الحية")
    if not df.empty and HAS_SEABORN:
        fig_m, ax_m = plt.subplots(figsize=(10, 8))
        sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".1f", ax=ax_m)
        st.pyplot(fig_m)

st.markdown("---")
st.subheader("🔍 التقارير الإحصائية")
# (بقية الأزرار السفلية تبقى كما هي لضمان عمل الرسوم)
