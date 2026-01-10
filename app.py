import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# تحميل الملفات
model = joblib.load('sleep_model.pkl')
data = pd.read_csv('processed_sleep_data.csv')

# --- وظيفة ابتهاج: معالجة الـ 23 ميزة رياضياً ---
def prepare_input(age, sleep_dur, steps, stress):
    # إنشاء قاموس يحتوي على كل الأعمدة الـ 23 التي تدرب عليها النموذج
    input_dict = {col: data[col].mean() if col in data.columns else 0 for col in model.feature_names_in_}
    
    # تحديث القيم التي تتحكمين بها في السلايدرز
    input_dict.update({
        'Age': age,
        'Sleep Duration': sleep_dur, 
        'Daily Steps': steps, 
        'Stress Level': stress
    })
    
    # تحويل القاموس لجدول بيانات (DataFrame)
    return pd.DataFrame([input_dict])[model.feature_names_in_]

# --- واجهة التطبيق ---
st.title("🌙 نظام تقييم النوم الذكي")

age = st.sidebar.slider("العمر", 18, 80, 25)
sleep_dur = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
steps = st.sidebar.slider("الخطوات", 0, 15000, 5000)
stress = st.sidebar.slider("مستوى التوتر", 1, 10, 5)

if st.button("تحديث التحليل الرياضي 🚀"):
    input_df = prepare_input(age, sleep_dur, steps, stress)
    
    # حساب الاحتمالية الدقيقة (Probability)
    probs = model.predict_proba(input_df)[0]
    # المعادلة الرياضية لابتهاج: تحويل الاحتمال لدرجة من 10
    score = round(probs[1] * 10, 1) 
    
    st.metric("درجة جودة نومك", f"{score} / 10")
    
    # رسم بياني يوضح مكانك الفعلي
    fig = px.scatter(data, x='Daily Steps', y='Quality of Sleep', color='Stress Level')
    fig.add_scatter(x=[steps], y=[score/10], mode='markers', marker=dict(color='red', size=15, symbol='star'))
    st.plotly_chart(fig)
