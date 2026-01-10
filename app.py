import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import numpy as np

# إعداد الصفحة
st.set_page_config(page_title="Sleep IQ System", layout="wide")

# 1. تحميل الموديل والبيانات (وظيفة ابتهاج: ربط الملفات المرفوعة)
@st.cache_resource
def load_files():
    model = joblib.load('sleep_model.pkl')
    data = pd.read_csv('processed_sleep_data.csv')
    return model, data

try:
    model, data = load_files()
except Exception as e:
    st.error(f"خطأ في تحميل الملفات: {e}")

st.title("🌙 نظام Sleep IQ: التقييم الذكي لجودة النوم")
st.markdown("---")

# 2. لوحة التحكم (Input Panel) - الجزء الخاص بابتهاج
st.sidebar.header("📝 أدخل بياناتك الشخصية")
age = st.sidebar.slider("العمر", 18, 80, 25)
sleep_duration = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
daily_steps = st.sidebar.number_input("الخطوات اليومية", 0, 20000, 5000)
stress_level = st.sidebar.select_slider("مستوى التوتر", options=list(range(1, 11)), value=5)

# تجهيز البيانات للموديل (Mathematical Alignment)
input_dict = {col: 0 for col in model.feature_names_in_}
input_dict.update({
    'Age': age,
    'Sleep Duration': sleep_duration,
    'Daily Steps': daily_steps,
    'Stress Level': stress_level
})
input_df = pd.DataFrame([input_dict])

# 3. محرك التوقعات (The Prediction Engine)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚀 نتيجة التحليل الذكي")
    if st.button("احسب جودة نومي الآن"):
        # حساب الاحتمالية لتحويلها لدرجة من 10 (تعديل ابتهاج الرياضي)
        probs = model.predict_proba(input_df)[0]
        score = round(probs[1] * 10, 1) 
        
        st.metric(label="درجة جودة النوم المتوقعة", value=f"{score} / 10")
        
        if score >= 7:
            st.success(f"ممتاز! درجتك {score} تشير إلى كفاءة نوم عالية ✅")
            st.balloons()
        elif score >= 5:
            st.info(f"درجتك {score} متوسطة. حاول تحسين نشاطك البدني ℹ️")
        else:
            st.warning(f"تنبيه: درجتك {score} منخفضة. ننصح بمراجعة الطبيب ⚠️")

with col2:
    st.subheader("📊 موقعك بالنسبة للبيانات العامة")
    # تصحيح اسم العمود إلى 'Quality of Sleep' كما ظهر في الخطأ
    fig = px.scatter(data, x='Daily Steps', y='Quality of Sleep', 
                     color='Stress Level', template="plotly_dark",
                     labels={'Daily Steps': 'الخطوات', 'Quality of Sleep': 'جودة النوم'})
    
    # إضافة نقطة المستخدم اللحظية (النجمة الصفراء)
    try:
        user_y = 1 if 'score' in locals() and score >= 5 else 0.5
        fig.add_scatter(x=[daily_steps], y=[user_y], 
                        mode='markers', marker=dict(color='yellow', size=15, symbol='star'),
                        name='أنت هنا')
    except:
        pass
        
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("تم تطوير هذا النظام بواسطة ابتهاج وفريق العمل - مشروع التخرج 2026")
