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
st.set_page_config(page_title="Sleep IQ Pro Analytics", layout="wide")

# 2. تحميل البيانات وتجهيز الأسماء
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('processed_sleep_data.csv')
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_data()

st.title("🌙 نظام Sleep IQ الاحترافي المتكامل")
st.markdown("---")

# 3. القسم العلوي: كافة الميزات بجانب المصفوفة
col_input, col_matrix = st.columns([1.2, 1])

with col_input:
    st.subheader("⚙️ لوحة التحكم بكافة الميزات")
    
    # توزيع الميزات على عمودين داخليين لترتيبها
    c1, c2 = st.columns(2)
    with c1:
        age = st.slider("العمر", 10, 90, 22)
        job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])
        sleep_hrs = st.slider("ساعات النوم (Sleep Duration)", 2.0, 12.0, 7.4)
        systolic = st.slider("الضغط الانقباضي (Systolic BP)", 90, 200, 120)
        heart_rate = st.slider("نبض القلب (Heart Rate)", 50, 120, 65)
    
    with c2:
        stress = st.slider("مستوى التوتر (Stress Level)", 1, 10, 6)
        bmi_cat = st.selectbox("فئة الوزن (BMI Category)", ["Normal Weight", "Overweight", "Obese"])
        steps = st.slider("عدد الخطوات اليومي", 0, 20000, 5487)
        physical_activity = st.slider("النشاط البدني (دقائق)", 0, 120, 45)
        sleep_quality_input = st.slider("الجودة المتوقعة (Input Quality)", 1, 10, 7)

    st.markdown("###")
    if st.button("تحليل النتيجة النهائية 🚀"):
        # تطبيق منطق البرمجة الخاص بكِ مع البالونات
        score = 9.7 
        if systolic > 155 or bmi_cat == "Obese":
            score = 0.1 if job == "Nurse" else 0.0
            st.error(f"تحذير: جودة النوم منخفضة جداً: {score} 😡")
        else:
            st.balloons() # إرجاع البالونات
            st.success(f"مبروك! جودة النوم مثالية: {score} 🎉")

with col_matrix:
    st.subheader("📊 مصفوفة الارتباط الحية")
    if not df.empty and HAS_SEABORN:
        fig_m, ax_m = plt.subplots(figsize=(10, 9))
        # عرض كافة العلاقات بين الميزات في المصفوفة
        sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='RdYlGn', fmt=".1f", ax=ax_m)
        st.pyplot(fig_m)

st.markdown("---")

# 4. القسم السفلي: أزرار إظهار الرسومات التفصيلية
st.subheader("🔍 استعراض التقارير البيانية")
col_b1, col_b2, col_b3 = st.columns(3)

if col_b1.button("📊 جودة النوم والوزن"):
    bmi_col = 'BMI Category' if 'BMI Category' in df.columns else df.columns[0]
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x=bmi_col, y='Quality of Sleep', palette='Set2', ax=ax1)
    st.pyplot(fig1)

if col_b2.button("📉 منحنى ضغط الدم"):
    bp_col = 'Systolic BP' if 'Systolic BP' in df.columns else (df.columns[1] if len(df.columns)>1 else df.columns[0])
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.regplot(data=df, x=bp_col, y='Quality of Sleep', color='blue', ax=ax2)
    st.pyplot(fig2)

if col_b3.button("🧪 تداخل التوتر والعمر"):
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=df, x='Age', y='Quality of Sleep', hue='Stress Level', palette='magma', ax=ax3)
    st.pyplot(fig3)
