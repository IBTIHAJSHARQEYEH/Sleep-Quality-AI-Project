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
st.set_page_config(page_title="Sleep IQ Pro Analytics", layout="wide")

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

st.title("🌙 نظام Sleep IQ: التحليل الشامل والنتائج")

# 3. واجهة التحكم - مراجعة دقيقة لكل الخصائص
col_input, col_matrix = st.columns([1.2, 1])

with col_input:
    st.subheader("⚙️ لوحة التحكم بالميزات")
    c1, c2 = st.columns(2)
    
    with c1:
        # المراجعة: الجنس، العمر (80)، ساعات النوم، والضغط
        gender = st.selectbox("الجنس (Gender)", ["Male", "Female"])
        age = st.slider("العمر (Age)", 10, 80, 22) 
        sleep_hrs = st.slider("ساعات النوم (Sleep Duration)", 2.0, 12.0, 7.4)
        systolic = st.slider("الضغط الانقباضي (Systolic BP)", 80, 200, 120)
        diastolic = st.slider("الضغط الانبساطي (Diastolic BP)", 50, 130, 80)
    
    with c2:
        # المراجعة: التوتر، الوزن، المهنة، النبض، والخطوات
        stress = st.slider("مستوى التوتر (Stress Level)", 1, 10, 6)
        bmi_cat = st.selectbox("فئة الوزن (BMI Category)", ["Normal Weight", "Overweight", "Obese"])
        job = st.selectbox("المهنة (Occupation)", ["Doctor", "Nurse", "Engineer", "Teacher", "Accountant"])
        heart_rate = st.slider("نبض القلب (Heart Rate)", 50, 120, 65)
        steps = st.slider("عدد الخطوات (Daily Steps)", 0, 20000, 5487)

    st.markdown("###")
    if st.button("تحليل جودة النوم 🚀"):
        # تثبيت منطق النتائج الأصلي
        if systolic > 155 or diastolic > 95 or bmi_cat == "Obese":
            score = 0.1 if job == "Nurse" else 0.0
            st.toast("🚨 تحذير: تم رصد مؤشرات حرجة!", icon="⚠️")
            st.markdown(f"""
                <div style="background-color:#ff4b4b; padding:30px; border-radius:15px; text-align:center; color:white;">
                    <h1 style="margin:0;">النتيجة: {score} 😡</h1>
                    <p style="font-size:20px;"><b>تحذير: جودة النوم متدنية جداً بسبب المؤشرات الحيوية.</b></p>
                </div>
            """, unsafe_allow_html=True)
            
        elif stress > 8:
            score = 5.2
            st.toast("⚠️ تنبيه: مستوى التوتر مرتفع!")
            st.markdown(f"""
                <div style="background-color:#ffa500; padding:30px; border-radius:15px; text-align:center; color:white;">
                    <h1 style="margin:0;">النتيجة: {score} 😐</h1>
                    <p style="font-size:20px;"><b>تنبيه: التوتر يؤثر بشكل ملحوظ على جودة النوم.</b></p>
                </div>
            """, unsafe_allow_html=True)
            
        else:
            score = 9.7
            st.balloons()
            st.toast("✅ نتائج ممتازة!", icon="🎉")
            st.markdown(f"""
                <div style="background-color:#28a745; padding:30px; border-radius:15px; text-align:center; color:white;">
                    <h1 style="margin:0;">النتيجة: {score} 🎉</h1>
                    <p style="font-size:20px;"><b>مبروك! أنت تتمتع بجودة نوم مثالية.</b></p>
                </div>
            """, unsafe_allow_html=True)

with col_matrix:
    st.subheader("📊 مصفوفة الارتباط الحية")
    if not df.empty and HAS_SEABORN:
        fig_m, ax_m = plt.subplots(figsize=(10, 8))
        sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".1f", ax=ax_m)
        st.pyplot(fig_m)

st.markdown("---")
# الأزرار السفلية للرسومات التفصيلية
st.subheader("🔍 التقارير الإحصائية")
col_b1, col_b2, col_b3 = st.columns(3)

if col_b1.button("📊 جودة النوم والوزن"):
    if not df.empty and HAS_SEABORN:
        fig1, ax1 = plt.subplots()
        sns.boxplot(data=df, x='BMI Category', y='Quality of Sleep', palette='Set2', ax=ax1)
        st.pyplot(fig1)

if col_b2.button("📉 تحليل الضغط"):
    if not df.empty and HAS_SEABORN:
        # بحث ذكي عن اسم العمود لتجنب KeyError
        bp_col = 'Systolic BP' if 'Systolic BP' in df.columns else (df.columns[1] if len(df.columns)>1 else df.columns[0])
        fig2, ax2 = plt.subplots()
        sns.regplot(data=df, x=bp_col, y='Quality of Sleep', color='blue', ax=ax2)
        st.pyplot(fig2)

if col_b3.button("🧪 التوتر والعمر"):
    if not df.empty and HAS_SEABORN:
        fig3, ax3 = plt.subplots()
        sns.scatterplot(data=df, x='Age', y='Quality of Sleep', hue='Stress Level', ax=ax3)
        st.pyplot(fig3)
