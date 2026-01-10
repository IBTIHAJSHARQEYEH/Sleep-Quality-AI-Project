import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import numpy as np

# إعداد الصفحة لتكون عريضة واحترافية
st.set_page_config(page_title="Sleep IQ System", layout="wide")

# 1. تحميل الموديل والبيانات (وظيفة ابتهاج: ربط الملفات)
@st.cache_resource
def load_files():
    # تحميل الموديل الذي تم تدريبه
    model = joblib.load('sleep_model.pkl')
    # تحميل البيانات المعالجة (processed_sleep_data.csv)
    data = pd.read_csv('processed_sleep_data.csv')
    return model, data

try:
    model, data = load_files()
except Exception as e:
    st.error(f"خطأ في تحميل الملفات: تأكدي من وجود الملفات المطلوبة في GitHub")

st.title("🌙 نظام Sleep IQ: التقييم الذكي لجودة النوم")
st.markdown("---")

# 2. لوحة التحكم (Input Panel) - الجزء الخاص بابتهاج (Workflow)
st.sidebar.header("📝 لوحة البيانات الشخصية")
age = st.sidebar.slider("العمر", 18, 80, 25)
sleep_duration = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
steps = st.sidebar.slider("الخطوات اليومية (النشاط البدني)", 0, 15000, 5000)
stress_level = st.sidebar.slider("مستوى التوتر", 1, 10, 5)

# تجهيز البيانات للتنبؤ الرياضي (بناءً على الـ 23 ميزة)
input_dict = {col: 0 for col in model.feature_names_in_}
input_dict.update({
    'Age': age,
    'Sleep Duration': sleep_duration,
    'Physical Activity Level': steps,
    'Stress Level': stress_level
})
input_df = pd.DataFrame([input_dict])

# 3. عرض النتائج والرسوم البيانية
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚀 التحليل الذكي")
    if st.button("احسب جودة نومي الآن"):
        # حساب الاحتمالية لتحويلها لدرجة من 10 (إضافة ابتهاج الرياضية)
        probs = model.predict_proba(input_df)[0]
        score = round(probs[1] * 10, 1)  # احتمالية الفئة 1 مضروبة في 10
        
        st.metric(label="درجة جودة نومك المتوقعة", value=f"{score} / 10")
        
        if score >= 7:
            st.success(f"النتيجة: جودة نومك ممتازة ({score}/10) ✅")
            st.balloons()
        elif score >= 5:
            st.info(f"النتيجة: جودة نومك متوسطة ({score}/10) ℹ️")
        else:
            st.warning(f"النتيجة: جودة نومك منخفضة ({score}/10) ⚠️")

with col2:
    st.subheader("📊 استكشاف نشاطك")
    # حل مشكلة اسم العمود (Quality of Sleep) لمنع ظهور ValueError
    fig = px.scatter(data, x='Physical Activity Level', y='Quality of Sleep', 
                     color='Stress Level', template="plotly_dark",
                     labels={'Physical Activity Level': 'النشاط البدني', 'Quality of Sleep': 'جودة النوم'})
    
    # إضافة نقطة المستخدم اللحظية (النجمة الصفراء) عند التنبؤ
    if 'score' in locals():
        y_val = 1 if score >= 5 else 0
        fig.add_scatter(x=[steps], y=[y_val], mode='markers', 
                        marker=dict(color='yellow', size=15, symbol='star'),
                        name='أنت هنا')
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("تم تطوير النظام بواسطة ابتهاج وفريق العمل - مشروع التخرج 2026")
