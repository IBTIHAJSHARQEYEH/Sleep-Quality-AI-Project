import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# 1. إعدادات الصفحة وتحميل الأصول
st.set_page_config(page_title="Sleep IQ", layout="wide")

@st.cache_resource
def load_data():
    model = joblib.load('sleep_model.pkl')
    data = pd.read_csv('processed_sleep_data.csv')
    return model, data

model, data = load_data()

st.title("🌙 نظام Sleep IQ للتحليل الرياضي")

# 2. القائمة الجانبية للمدخلات (وظيفة ابتهاج)
st.sidebar.header("📊 مدخلاتك الحية")
age = st.sidebar.slider("العمر", 18, 80, 25)
sleep_dur = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
steps = st.sidebar.number_input("الخطوات اليومية", 0, 20000, 5000)
stress = st.sidebar.slider("مستوى التوتر", 1, 10, 5)

# --- معالجة الـ 23 فيتشر (الأسس الرياضية لابتهاج) ---
# نقوم بإنشاء سجل جديد يحتوي على كل الأعمدة المطلوبة للموديل
input_row = {col: data[col].median() for col in model.feature_names_in_}
input_row.update({
    'Age': age,
    'Sleep Duration': sleep_dur,
    'Daily Steps': steps,
    'Stress Level': stress
})
input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# 3. العرض والنتائج
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 التحليل الرياضي الفعلي")
    if st.button("احسب الجودة الآن"):
        # استخدام الاحتمالات لجعل النتيجة متغيرة وليست ثابتة (10)
        probs = model.predict_proba(input_df)[0]
        # معادلة ابتهاج لتحويل الاحتمال لدرجة متغيرة
        score = round(probs[1] * 10, 1) 
        
        st.metric("درجة جودة النوم", f"{score} / 10")
        
        if score >= 7:
            st.success(f"ممتاز! درجتك {score} تعكس كفاءة عالية ✅")
        else:
            st.warning(f"درجتك {score} تنبهك لضرورة تحسين عاداتك ⚠️")

with col2:
    st.subheader("📈 موقعك في البيانات")
    # تصحيح اسم العمود إلى 'Quality of Sleep' لمنع الخطأ الأحمر
    fig = px.scatter(data, x='Daily Steps', y='Quality of Sleep', 
                     color='Stress Level', template="plotly_dark")
    
    # إضافة نجمة تمثل المستخدم الحالي وتتحرك مع الخطوات والنتيجة
    if 'score' in locals():
        fig.add_scatter(x=[steps], y=[score/10], mode='markers', 
                        marker=dict(color='yellow', size=15, symbol='star'), name='أنت')
    st.plotly_chart(fig, use_container_width=True)
