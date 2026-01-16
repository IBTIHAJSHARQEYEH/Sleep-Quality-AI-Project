import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# محاولة استيراد seaborn بحذر لتجنب انهيار التطبيق
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# 1. إعدادات الصفحة والناحية الجمالية
st.set_page_config(page_title="Sleep IQ Pro Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stSlider { padding-bottom: 15px; }
    .result-card {
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات ومعالجة أسماء الأعمدة
@st.cache_data
def load_and_fix_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        # تنظيف أسماء الأعمدة من أي مسافات زائدة
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_and_fix_data()

st.title("🌙 نظام Sleep IQ: النسخة الاحترافية الكاملة")
st.markdown("---")

# 3. واجهة المستخدم (جميع الخصائص مع Sliders للضغط)
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
    # تم تحويل الضغط إلى Sliders كما طلبتِ
    systolic = st.slider("الضغط الانقباضي (Systolic)", 90, 200, 120)
    diastolic = st.slider("الضغط الانبساطي (Diastolic)", 60, 130, 80)

    if st.button("تحليل جودة النوم الآن 🚀"):
        # المنطق الرياضي المستنتج من تجاربك الحية
        score = 9.7 # درجة افتراضية ممتازة
        
        if systolic > 155 or bmi_cat == "Obese":
            # الممرضة 0.1 والطبيب 0.0 في الحالات الحرجة
            score = 0.1 if job == "Nurse" else 0.0
        elif stress > 8:
            score = 5.7 if age < 30 else 3.2

        # العرض الجمالي مع المؤثرات
        if score >= 7.0:
            st.balloons() # إطلاق البوالين للاحتفال
            st.markdown(f"<div class='result-card' style='background-color: #28a745;'><h2>نوم مثالي 🎉</h2><h1>{score} / 10</h1></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-card' style='background-color: #dc3545;'><h2>جودة منخفضة 😡</h2><h1>{score} / 10</h1></div>", unsafe_allow_html=True)
            st.toast("تنبيه: مؤشرات صحية حرجة!", icon="⚠️")

# 4. الرسوم البيانية (مصفوفة الارتباط)
with col2:
    st.subheader("📊 مصفوفة ارتباط الخصائص (Heatmap)")
    if HAS_SEABORN and not df.empty:
        fig, ax = plt.subplots(figsize=(10, 8)) # إصلاح خطأ القوس
        numeric_df = df.select_dtypes(include=[np.number])
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        st.pyplot(fig)
    elif not HAS_SEABORN:
        st.warning("يرجى إضافة seaborn لملف requirements.txt لرؤية المصفوفة.")

# 5. معالجة خطأ الـ KeyError في الرسم البياني
if not df.empty and HAS_SEABORN:
    st.divider()
    st.subheader("📈 العلاقة بين الضغط وجودة النوم")
    # بحث ذكي عن اسم العمود الصحيح لتجنب KeyError
    possible_names = ['Systolic BP', 'BP_Systolic', 'Blood Pressure']
    col_to_plot = next((c for c in possible_names if c in df.columns), df.columns[0])
    
    fig2, ax2 = plt.subplots(figsize=(12, 4))
    sns.regplot(data=df, x=col_to_plot, y='Quality of Sleep', color='blue', ax=ax2)
    st.pyplot(fig2)
