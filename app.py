import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# 1. تحميل الموديل والبيانات الأصلية
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('sleep_model.pkl')
        data = pd.read_csv('processed_sleep_data.csv')
        data.columns = data.columns.str.strip()
        return model, data
    except:
        return None, pd.DataFrame()

model, data = load_assets()

st.set_page_config(page_title="Sleep IQ Pro", layout="wide")
st.title("🌙 نظام Sleep IQ: التحليل الذكي والملاحظات الفيزيائية")

# 2. القائمة الجانبية (مدخلات المستخدم كاملة)
st.sidebar.header("🩺 البيانات الشخصية والطبية")
gender = st.sidebar.selectbox("الجنس", ["Male", "Female"])
age = st.sidebar.slider("العمر", 18, 80, 25)
systolic = st.sidebar.slider("الضغط الانقباضي", 90, 180, 120)
diastolic = st.sidebar.slider("الضغط الانبساطي", 60, 110, 80)
sleep_dur = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
stress = st.sidebar.slider("مستوى التوتر", 1, 10, 5)
steps = st.sidebar.number_input("عدد الخطوات اليومية", value=5000)
heart_rate = st.sidebar.slider("نبض القلب", 60, 100, 72)
bmi_cat = st.sidebar.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
occupation = st.sidebar.selectbox("المهنة", ['Nurse', 'Doctor', 'Engineer', 'Lawyer', 'Teacher', 'Accountant', 'Salesperson'])

# 3. بناء الجدول الرياضي وتطبيق السكيلنج (Scaling)
def scale_val(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val) if max_val != min_val else 0

if model:
    input_row = {col: 0 for col in model.feature_names_in_}
    input_row.update({
        'Gender': 1 if gender == "Male" else 0,
        'Age': scale_val(age, 18, 80),
        'Sleep Duration': scale_val(sleep_dur, 2, 12),
        'Stress Level': scale_val(stress, 1, 10),
        'Physical Activity Level': scale_val(steps, 0, 10000),
        'Daily Steps': scale_val(steps, 0, 10000),
        'Heart Rate': scale_val(heart_rate, 60, 100),
        'Systolic_BP': scale_val(systolic, 90, 180),
        'Diastolic_BP': scale_val(diastolic, 60, 110)
    })
    
    if f'BMI Category_{bmi_cat}' in input_row: input_row[f'BMI Category_{bmi_cat}'] = 1
    if f'Occupation_{occupation}' in input_row: input_row[f'Occupation_{occupation}'] = 1
    input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# 4. العرض والنتائج (الاعتماد الكلي على ذكاء الموديل والملاحظات المنطقية)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🚀 نتيجة التحليل الذكي")
    if st.button("تحليل الحالة 💡"):
        # النتيجة تعتمد 100% على الموديل الرياضي
        probs = model.predict_proba(input_df)[0]
        score = round(probs[1] * 10, 1)
        
        st.metric("درجة جودة النوم", f"{score} / 10")
        
        # --- الملاحظات الذكية التي تحلل "لماذا" النتيجة هكذا ---
        st.markdown("---")
        st.subheader("🩺 التفسير الفيزيائي والطبي")
        
        if score <= 5.0:
            if sleep_dur >= 7.0 and stress > 5:
                # تفسير ذكي: الساعات كافية لكن التوتر يفسدها
                st.error("التشخيص: انخفاض كفاءة النوم (رغم كفاية المدة) ⚠️")
                st.info(f"السبب الفيزيائي: يظهر الموديل أن مستوى التوتر العالي ({stress}) يمنع الاستفادة من ساعات النوم ({sleep_dur} ساعة)، مما يؤدي لتشخيص اضطراب النوم.")
            elif sleep_dur < 6.0:
                st.error("التشخيص: Insomnia (أرق) ⚠️")
                st.info("السبب الفيزيائي: المدة الزمنية للنوم غير كافية للتعافي الحيوي.")
            else:
                diag = "Sleep Apnea" if bmi_cat == "Obese" else "Sleep Disorder"
                st.error(f"التشخيص: {diag} ⚠️")
        else:
            st.success("التشخيص: None (حالة طبيعية) ✅")
            st.info("السبب الفيزيائي: هناك توازن إيجابي بين المؤشرات الحيوية وجودة النوم.")

with col2:
    st.subheader("📊 مصفوفة الارتباط الشاملة (Heatmap)")
    if not data.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(data.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".1f", ax=ax)
        st.pyplot(fig)

st.info("💡 هذا النظام يعتمد كلياً على نموذج التعلم الآلي (Machine Learning) لتحليل البيانات وتوقع النتائج.")
