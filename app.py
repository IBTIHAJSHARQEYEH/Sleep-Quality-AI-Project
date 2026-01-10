
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from datetime import datetime

# 1. إعدادات الواجهة والسمة الداكنة الاحترافية
st.set_page_config(page_title="Sleep IQ Analytics", page_icon="🌙", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 15px; border-left: 5px solid #4CAF50; }
    .advice-card { background-color: #262730; padding: 20px; border-radius: 10px; border-right: 5px solid #00aaff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 نظام Sleep IQ: التحليل والتوصيات الذكية")

# تحميل الموديل والبيانات من مجلد content
model = joblib.load('sleep_model.pkl')
df = pd.read_csv('processed_sleep_data.csv')

# 2. القائمة الجانبية لمدخلات المستخدم
with st.sidebar:
    st.header("⚙️ لوحة البيانات الشخصية")
    age = st.slider("العمر", 10, 80, 25)
    sleep_duration = st.slider("ساعات النوم", 1.0, 12.0, 7.0)
    steps = st.number_input("الخطوات اليومية", 0, 20000, 5000)
    stress_level = st.select_slider("مستوى التوتر", options=list(range(1, 11)), value=5)
    heart_rate = st.slider("معدل ضربات القلب", 40, 120, 75)
    
    with st.expander("🩺 القياسات الطبية"):
        systolic = st.slider("الضغط الانقباضي", 90, 180, 120)
        diastolic = st.slider("الضغط الانبساطي", 60, 110, 80)

# 3. عرض الرسوم البيانية والتوقعات
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 استكشاف نشاطك")
    fig = px.scatter(df, x='Daily Steps', y='Quality of Sleep', color='Stress Level',
                     title='العلاقة بين خطواتك وجودة النوم', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 تحليل جودة النوم")
    if st.button("🚀 الحصول على التوقع والتوصية"):
        # إصلاح خطأ السطر 50: بناء صف البيانات بشكل صحيح
        input_row = df.iloc[0:1, :].copy()
        
        # تحديث القيم بالمدخلات اليدوية
        mapping = {'Age': age, 'Sleep Duration': sleep_duration, 'Daily Steps': steps, 
                   'Stress Level': stress_level, 'Heart Rate': heart_rate,
                   'Systolic_BP': systolic, 'Diastolic_BP': diastolic}
        
        for key, val in mapping.items():
            if key in input_row.columns:
                input_row[key] = val

        try:
            # تنفيذ التوقع بناءً على 23 مدخلاً
            prediction = model.predict(input_row.values[:, :23])[0]
            st.balloons()
            st.metric(label="مؤشر جودة النوم المتوقع", value=f"{prediction:.2f}/10")

            # قسم التوصيات الصحية الذكية
            st.markdown('<div class="advice-card">', unsafe_allow_html=True)
            st.markdown("### 💡 توصية طبية مخصصة:")
            if prediction < 5:
                st.warning("⚠️ جودة نومك منخفضة. ننصحك بتقليل الكافيين وزيادة النشاط البدني الخفيف.")
            elif 5 <= prediction < 8:
                st.info("ℹ️ جودة نومك جيدة. حافظ على جدول نوم منتظم لتحسين النتائج.")
            else:
                st.success("✅ جودة نومك ممتازة! استمر على هذا النهج الصحي.")
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"خطأ تقني: {e}")

st.divider()
st.subheader("📋 سجل البيانات الحالي")
st.dataframe(df.head(10))
