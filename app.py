import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# 1. تحميل الأصول الأساسية
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

st.set_page_config(page_title="Sleep IQ - Precision Mode", layout="wide")
st.title("🌙 نظام Sleep IQ: التحليل الطبي والفيزيائي المتوازن")

# 2. القائمة الجانبية
st.sidebar.header("🩺 مدخلات الحالة")
with st.sidebar:
    gender = st.selectbox("الجنس", ["Male", "Female"])
    age = st.slider("العمر", 18, 80, 41)
    systolic = st.slider("الضغط الانقباضي", 90, 180, 127)
    diastolic = st.slider("الضغط الانبساطي", 60, 110, 80)
    sleep_dur = st.slider("ساعات النوم", 2.0, 12.0, 7.0)
    stress = st.slider("مستوى التوتر", 1, 10, 6)
    
    st.markdown("---")
    phys_level = st.slider("مستوى النشاط الفيزيائي", 30, 100, 42)
    steps = st.number_input("عدد الخطوات اليومية", value=5022)
    heart_rate = st.slider("نبض القلب", 60, 100, 82)
    bmi_cat = st.selectbox("فئة الوزن", ["Normal Weight", "Overweight", "Obese"])
    
    occupation = st.selectbox("المهنة", ["Accountant", "Doctor", "Engineer", "Lawyer", "Manager", "Nurse", "Salesperson", "Sales Representative", "Scientist", "Software Engineer", "Teacher"])

# 3. معالجة البيانات
def scale_val(val, min_val, max_val):
    return (val - min_val) / (max_val - min_val) if max_val != min_val else 0

if model:
    input_row = {col: 0.0 for col in model.feature_names_in_}
    input_row.update({
        'Gender': 1.0 if gender == "Male" else 0.0,
        'Age': scale_val(age, 18, 80),
        'Sleep Duration': scale_val(sleep_dur, 2, 12),
        'Physical Activity Level': scale_val(phys_level, 30, 100),
        'Stress Level': scale_val(stress, 1, 10),
        'Heart Rate': scale_val(heart_rate, 60, 100),
        'Daily Steps': scale_val(steps, 0, 10000),
        'Systolic_BP': scale_val(systolic, 90, 180),
        'Diastolic_BP': scale_val(diastolic, 60, 110)
    })
    if f'BMI Category_{bmi_cat}' in input_row: input_row[f'BMI Category_{bmi_cat}'] = 1.0
    if f'Occupation_{occupation}' in input_row: input_row[f'Occupation_{occupation}'] = 1.0
    input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# 4. عرض النتائج والمنطق المطور للملاحظات
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🚀 نتيجة التحليل")
    if st.button("تحليل الحالة 💡"):
        probs = model.predict_proba(input_df)[0]
        score = round(probs[1] * 10, 1)
        st.metric("درجة جودة النوم", f"{score} / 10")

        st.markdown("---")
        st.subheader("🩺 التشخيص والملاحظة الدقيقة")
        
        # تشخيص الحالة بناءً على السكور وفئة الوزن
        if score <= 5.5:
            diagnosis = "Sleep Apnea" if bmi_cat == "Obese" else "Insomnia"
            st.error(f"⚠️ تحذير: تم تشخيص الحالة كـ {diagnosis}")
            
            # --- ملاحظة ذكية متوازنة لا تظلم المتغيرات ---
            if bmi_cat == "Obese" or systolic > 135:
                st.warning(f"الملاحظة: العوامل الصحية (الوزن والضغط) هي المؤثر الأكبر حالياً على جودة نومك.")
            elif stress > 7:
                st.info(f"الملاحظة: مستوى التوتر ({stress}) هو العامل الطاغي الذي يمنعك من النوم العميق.")
            else:
                st.info(f"الملاحظة: هناك تداخل بين عدة عوامل أدى لانخفاض جودة النوم إلى {score}.")
        else:
            st.success("✅ التشخيص: None (حالة طبيعية)")
            st.info("الملاحظة: مؤشراتك الحيوية ونمط حياتك في حالة توازن إيجابي.")

    st.markdown("---")
    st.subheader("🔢 بيانات المعالجة الرقمية (0-1)")
    st.dataframe(input_df.T.rename(columns={0: 'Value'}))

with col2:
    st.subheader("📊 مصفوفة الارتباط (Heatmap)")
    if not data.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(data.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".1f", ax=ax)
        st.pyplot(fig)
