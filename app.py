import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. إعدادات الصفحة والجماليات
st.set_page_config(page_title="Sleep IQ Professional Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stSlider { padding-bottom: 20px; }
    .result-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. تحميل البيانات الأصلية (تأكدي من وجود الملف في نفس المجلد)
@st.cache_data
def load_data():
    try:
        # استبدلي 'processed_sleep_data.csv' باسم ملفك الحقيقي
        df = pd.read_csv('processed_sleep_data.csv')
        return df
    except:
        # بيانات افتراضية في حال عدم وجود الملف للشرح فقط
        return pd.DataFrame(np.random.rand(100, 5), columns=['Age', 'Sleep_Duration', 'Stress_Level', 'BP_Systolic', 'Quality'])

df = load_data()

st.title("🌙 نظام Sleep IQ: التحليل الشامل والرسوم البيانية")
st.write("تحليل العلاقات بين الخصائص (Features) والتنبؤ بجودة النوم")

# 3. تقسيم الواجهة
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 إدخال بيانات الحالة")
    with st.container():
        age = st.slider("العمر", 10, 90, 26)
        sleep_hrs = st.slider("ساعات النوم", 2.0, 12.0, 7.8)
        stress = st.select_slider("مستوى التوتر", options=list(range(1, 11)), value=10)
        systolic = st.number_input("الضغط الانقباضي", value=120)
        bmi_cat = st.selectbox("فئة الوزن", ["Normal", "Overweight", "Obese"])
        job = st.selectbox("المهنة", ["Doctor", "Nurse", "Engineer", "Teacher"])

    if st.button("تحليل جودة النوم الآن"):
        # محاكاة منطق الموديل بناءً على تجاربك
        final_score = 8.5 # قيمة افتراضية
        
        # تطبيق القواعد التي اكتشفتِها في تجاربك
        if systolic > 155 or bmi_cat == "Obese":
            final_score = 0.1 if job == "Nurse" else 0.0
        elif age < 30 and stress < 5:
            final_score = 10.0 if job == "Doctor" else 9.7

        # عرض النتيجة مع الناحية الجمالية
        st.markdown(f"<div class='result-card'><h2>درجة الجودة المتوقعة</h2><h1>{final_score} / 10</h1></div>", unsafe_allow_html=True)
        
        if final_score >= 7.0:
            st.balloons() # بوالين للنتائج العالية
            st.success("ممتاز جداً! نوم هادئ 🎉")
        elif final_score >= 4.0:
            st.warning("جودة متوسطة 😐")
        else:
            st.error("جودة منخفضة جداً 😡") # إيموجي غاضب للنتائج المنخفضة
            st.toast("تحذير: مؤشرات صحية حرجة!", icon="⚠️")

with col2:
    st.subheader("📊 مصفوفة ارتباط الخصائص (Correlation Matrix)")
    # رسم Heatmap حقيقي من بياناتك
    fig, ax = plt.subplots(figsize=(10, 8))
    # نختار فقط الأعمدة الرقمية للارتباط
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
    st.pyplot(fig)
    st.caption("توضح هذه المصفوفة كيف ترتبط الميزات ببعضها (مثلاً العلاقة بين التوتر وضغط الدم).")

# 4. الرسوم البيانية التفصيلية للعلاقات
st.divider()
st.subheader("📈 تحليل العلاقات الثنائية (Feature Relationships)")

c1, c2 = st.columns(2)

with c1:
    st.write("العلاقة بين ساعات النوم وجودة النوم")
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=df, x='Sleep Duration', y='Quality of Sleep', ax=ax2, color='blue')
    st.pyplot(fig2)

with c2:
    st.write("توزيع الجودة بناءً على فئة الوزن (BMI)")
    fig3, ax3 = plt.subplots()
    sns.boxplot(data=df, x='BMI Category', y='Quality of Sleep', ax=ax3)
    st.pyplot(fig3)
