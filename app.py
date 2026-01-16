import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# حماية استيراد seaborn
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# 1. إعدادات الصفحة
st.set_page_config(page_title="Sleep IQ Full Analytics", layout="wide")

# 2. تحميل البيانات وتجهيزها
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        df.columns = df.columns.str.strip() # تنظيف الأسماء
        return df
    except:
        return pd.DataFrame()

df = load_data()

st.title("🌙 لوحة تحليل Sleep IQ المتقدمة")
st.markdown("---")

# 3. قسم مصفوفة الارتباط (العرض الكامل في الأعلى)
st.subheader("📊 مصفوفة ارتباط الخصائص الشاملة (Correlation Matrix)")
if not df.empty and HAS_SEABORN:
    fig_heat, ax_heat = plt.subplots(figsize=(15, 8)) # حجم كبير للمصفوفة
    corr = df.select_dtypes(include=[np.number]).corr()
    sns.heatmap(corr, annot=True, cmap='RdYlGn', fmt=".2f", ax=ax_heat)
    st.pyplot(fig_heat)
    st.info("توضح هذه المصفوفة كيف تؤثر كل ميزة (مثل الضغط أو التوتر) على جودة النوم بشكل إحصائي.")
else:
    st.warning("يرجى التأكد من رفع ملف البيانات وتثبيت seaborn لرؤية المصفوفة.")

st.divider()

# 4. واجهة المدخلات والرسوم التفصيلية (في الأسفل)
col_input, col_charts = st.columns([1, 2])

with col_input:
    st.subheader("👤 إدخال البيانات والتحليل")
    # جمع المدخلات
    age = st.slider("العمر", 10, 90, 22)
    sleep_hrs = st.slider("ساعات النوم", 2.0, 12.0, 7.4)
    stress = st.slider("مستوى التوتر", 1, 10, 6)
    systolic = st.slider("الضغط الانقباضي", 90, 200, 120)
    bmi_cat = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
    job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])

    if st.button("تشغيل التنبؤ بالذكاء الاصطناعي 🚀"):
        score = 9.7 # الحالة المثالية
        if systolic > 155 or bmi_cat == "Obese":
            score = 0.1 if job == "Nurse" else 0.0 # منطقك الخاص
            st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#dc3545; color:white; text-align:center;'><h2>النتيجة: {score} 😡</h2></div>", unsafe_allow_html=True)
            st.toast("تحذير من مؤشرات صحية حرجة!", icon="⚠️")
        else:
            st.balloons()
            st.markdown(f"<div style='padding:20px; border-radius:15px; background-color:#28a745; color:white; text-align:center;'><h2>النتيجة: {score} 🎉</h2></div>", unsafe_allow_html=True)

with col_charts:
    st.subheader("📈 التحليلات التفصيلية")
    if not df.empty and HAS_SEABORN:
        tab1, tab2 = st.tabs(["تأثير الوزن والضغط", "توزيع الجودة والعمر"])
        
        with tab1:
            # رسم بياني للوزن والضغط
            fig1, ax1 = plt.subplots(1, 2, figsize=(12, 5))
            bmi_col = 'BMI Category' if 'BMI Category' in df.columns else df.columns[0]
            sns.boxplot(data=df, x=bmi_col, y='Quality of Sleep', palette='Set2', ax=ax1[0])
            ax1[0].set_title("الجودة حسب الوزن")
            
            bp_col = 'Systolic BP' if 'Systolic BP' in df.columns else (df.columns[1] if len(df.columns)>1 else df.columns[0])
            sns.regplot(data=df, x=bp_col, y='Quality of Sleep', color='blue', ax=ax1[1])
            ax1[1].set_title("تأثير الضغط الانقباضي")
            st.pyplot(fig1)

        with tab2:
            # رسم بياني للعمر والتوتر
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            sns.scatterplot(data=df, x='Age', y='Quality of Sleep', hue='Stress Level', palette='viridis', ax=ax2)
            st.pyplot(fig2)
