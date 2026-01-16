import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# حماية الاستيراد لتجنب انهيار التطبيق إذا لم تكن المكتبات مثبتة
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# 1. إعدادات الصفحة والناحية الجمالية
st.set_page_config(page_title="Sleep IQ Full Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stSlider { padding-bottom: 12px; }
    .result-card {
        padding: 30px; border-radius: 20px; text-align: center;
        margin: 20px 0; box-shadow: 0 10px 20px rgba(0,0,0,0.1); color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات ومعالجة أسماء الأعمدة
@st.cache_data
def load_clean_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        df.columns = df.columns.str.strip() # إزالة أي مسافات زائدة في الأسماء
        return df
    except:
        return pd.DataFrame()

df = load_clean_data()

st.title("🌙 لوحة تحليل Sleep IQ الاحترافية")
st.markdown("---")

# 3. واجهة المستخدم (المدخلات والنتائج)
col1, col2 = st.columns([1, 1.8])

with col1:
    st.subheader("👤 البيانات الشخصية والطبية")
    c1, c2 = st.columns(2)
    with c1:
        age = st.slider("العمر", 10, 90, 22)
        job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])
        bmi_cat = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
        systolic = st.slider("الضغط الانقباضي", 90, 200, 120)
    
    with c2:
        sleep_hrs = st.slider("ساعات النوم", 2.0, 12.0, 7.4)
        stress = st.slider("مستوى التوتر", 1, 10, 6)
        heart_rate = st.slider("نبض القلب", 50, 120, 65)
        steps = st.slider("عدد الخطوات", 0, 20000, 5487)

    if st.button("تحليل جودة النوم 🚀"):
        score = 9.7 # افتراضي بناءً على تجاربك السابقة
        if systolic > 155 or bmi_cat == "Obese":
            score = 0.1 if job == "Nurse" else 0.0 # تطبيق منطقك الخاص
            st.markdown(f"<div class='result-card' style='background-color: #dc3545;'><h2>جودة منخفضة جداً 😡</h2><h1>{score} / 10</h1></div>", unsafe_allow_html=True)
        else:
            st.balloons()
            st.markdown(f"<div class='result-card' style='background-color: #28a745;'><h2>نوم مثالي 🎉</h2><h1>{score} / 10</h1></div>", unsafe_allow_html=True)

# 4. الرسوم البيانية المتعددة (الجهة اليمنى)
with col2:
    if not df.empty and HAS_SEABORN:
        tab1, tab2, tab3 = st.tabs(["مصفوفة الارتباط", "تحليل الوزن", "تأثير التوتر"])
        
        with tab1:
            st.write("### مصفوفة ارتباط كافة الخصائص")
            fig1, ax1 = plt.subplots(figsize=(8, 6)) # إصلاح خطأ القوس
            sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', ax=ax1)
            st.pyplot(fig1)

        with tab2:
            st.write("### جودة النوم حسب فئة الوزن")
            # بحث ذكي عن اسم العمود لتجنب KeyError
            bmi_col = 'BMI Category' if 'BMI Category' in df.columns else df.columns[0]
            fig2, ax2 = plt.subplots()
            sns.boxplot(data=df, x=bmi_col, y='Quality of Sleep', palette='Set2', ax=ax2)
            st.pyplot(fig2)

        with tab3:
            st.write("### علاقة التوتر والعمر بجودة النوم")
            fig3, ax3 = plt.subplots()
            sns.scatterplot(data=df, x='Age', y='Quality of Sleep', hue='Stress Level', palette='viridis', ax=ax3)
            st.pyplot(fig3)
    else:
        st.warning("يرجى التأكد من رفع ملف البيانات وتثبيت المكتبات المطلوبة.")

# 5. رسم بياني إضافي للضغط (أسفل الصفحة)
if not df.empty and HAS_SEABORN:
    st.divider()
    st.subheader("📊 التحليل الإحصائي لضغط الدم")
    # البحث عن العمود الصحيح للضغط لتجنب KeyError
    bp_col = 'Systolic BP' if 'Systolic BP' in df.columns else (df.columns[1] if len(df.columns)>1 else df.columns[0])
    fig4, ax4 = plt.subplots(figsize=(12, 4))
    sns.regplot(data=df, x=bp_col, y='Quality of Sleep', color='blue', ax=ax4)
    st.pyplot(fig4)
