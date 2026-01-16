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
st.set_page_config(page_title="Sleep IQ Interactive Dashboard", layout="wide")

# 2. تحميل البيانات
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_data()

st.title("🌙 نظام Sleep IQ التفاعلي")
st.markdown("---")

# 3. القسم العلوي: المدخلات بجانب المصفوفة
col_input, col_matrix = st.columns([1, 1.2])

with col_input:
    st.subheader("⚙️ التحكم بالمدخلات")
    age = st.slider("العمر", 10, 90, 22)
    sleep_hrs = st.slider("ساعات النوم", 2.0, 12.0, 7.4)
    stress = st.slider("مستوى التوتر", 1, 10, 6)
    systolic = st.slider("الضغط الانقباضي", 90, 200, 120)
    bmi_cat = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
    job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])

    if st.button("تحليل النتيجة 🚀"):
        score = 9.7 
        if systolic > 155 or bmi_cat == "Obese":
            score = 0.1 if job == "Nurse" else 0.0
            st.error(f"جودة النوم: {score} 😡")
        else:
            st.balloons()
            st.success(f"جودة النوم: {score} 🎉")

with col_matrix:
    st.subheader("📊 مصفوفة الارتباط الحية")
    if not df.empty and HAS_SEABORN:
        fig_m, ax_m = plt.subplots(figsize=(10, 7))
        sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".1f", ax=ax_m)
        st.pyplot(fig_m)

st.markdown("---")

# 4. القسم السفلي: أزرار لإظهار الرسومات البيانية (Buttons)
st.subheader("📈 استكشاف الرسومات التفصيلية")
col_b1, col_b2, col_b3 = st.columns(3)

# زر تحليل الوزن
if col_b1.button("📊 توزيع الجودة حسب الوزن"):
    st.write("### تحليل تأثير BMI على جودة النوم")
    bmi_col = 'BMI Category' if 'BMI Category' in df.columns else df.columns[0]
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=df, x=bmi_col, y='Quality of Sleep', palette='Set2', ax=ax1)
    st.pyplot(fig1)

# زر تحليل الضغط
if col_b2.button("📉 علاقة الضغط بالجودة"):
    st.write("### منحنى انحدار ضغط الدم")
    bp_col = 'Systolic BP' if 'Systolic BP' in df.columns else (df.columns[1] if len(df.columns)>1 else df.columns[0])
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.regplot(data=df, x=bp_col, y='Quality of Sleep', color='blue', ax=ax2)
    st.pyplot(fig2)

# زر تحليل التوتر والعمر
if col_b3.button("🧪 تفاعل العمر والتوتر"):
    st.write("### خريطة تشتت (العمر، التوتر، الجودة)")
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    sns.scatterplot(data=df, x='Age', y='Quality of Sleep', hue='Stress Level', palette='viridis', ax=ax3)
    st.pyplot(fig3)
