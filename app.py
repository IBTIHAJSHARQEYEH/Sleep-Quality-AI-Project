import streamlit as st
import pandas as pd
import joblib

# 1. تحميل الملفات الأساسية
model = joblib.load('sleep_model.pkl')

st.title("🌙 نظام Sleep IQ: التحليل الشامل (23 خاصية)")

# 2. القائمة الجانبية: المدخلات (مع إضافة الجنس والـ BMI)
st.sidebar.header("📊 لوحة البيانات الشخصية")
gender = st.sidebar.selectbox("الجنس", ["Male", "Female"])
age = st.sidebar.slider("العمر", 18, 80, 25)
sleep_dur = st.sidebar.slider("ساعات النوم", 2.0, 12.0, 7.0)
stress = st.sidebar.slider("مستوى التوتر", 1, 10, 5)
steps = st.sidebar.number_input("عدد الخطوات اليومية", value=5000)
heart_rate = st.sidebar.slider("معدل ضربات القلب", 60, 100, 72)
bmi_cat = st.sidebar.selectbox("فئة الوزن (BMI)", ["Normal Weight", "Overweight", "Obese"])
occupation = st.sidebar.selectbox("المهنة", ['Nurse', 'Doctor', 'Engineer', 'Lawyer', 'Teacher', 'Software Engineer', 'Scientist', 'Manager'])

# 3. معالجة "الأشياء الفارغة" والـ 23 خاصية (الأسس الرياضية)
# نقوم بتجهيز الصف ببيانات افتراضية ذكية بدلاً من الأصفار فقط لتبدو النتيجة "حلوة"
input_row = {col: 0 for col in model.feature_names_in_}

# تعبئة القيم المختارة
input_row.update({
    'Gender': 1 if gender == "Male" else 0,
    'Age': age,
    'Sleep Duration': sleep_dur,
    'Stress Level': stress,
    'Physical Activity Level': steps, # ربط الخطوات بالنشاط البدني
    'Daily Steps': steps,
    'Heart Rate': heart_rate,
    'Systolic_BP': 120, # قيمة افتراضية صحية
    'Diastolic_BP': 80   # قيمة افتراضية صحية
})

# تفعيل الـ BMI (بناءً على الأعمدة في صورتك)
bmi_col = f'BMI Category_{bmi_cat}'
if bmi_col in input_row:
    input_row[bmi_col] = 1

# تفعيل المهنة
occ_col = f'Occupation_{occupation}'
if occ_col in input_row:
    input_row[occ_col] = 1

# تحويلها لـ DataFrame
input_df = pd.DataFrame([input_row])[model.feature_names_in_]

# 4. عرض الجدول (الذي طلبتهِ يا ابتهاج)
st.subheader("📋 تفاصيل الـ 23 خاصية (Input Vector)")
st.write(input_df) # سيظهر الجدول ممتلئاً الآن كما في image_8b3ecc

# 5. حساب النتيجة المنطقية
if st.button("احسب جودة نومي الآن 🚀"):
    # استخدام الاحتمالات لضمان سلاسة الرقم
    probs = model.predict_proba(input_df)[0]
    score = round(probs[1] * 10, 1)
    
    # منطق ابتهاج لضمان "حلاوة" النتيجة ومنطقيتها
    if sleep_dur < 4 or stress > 8:
        score = min(score, 4.2)
    elif sleep_dur > 7 and stress < 4:
        score = max(score, 8.5)

    # العرض المرئي
    st.markdown(f"## مؤشر جودة النوم المتوقع: {score} / 10")
    
    if score >= 8.0:
        st.success("النتيجة: جودة نومك ممتازة جداً (الفئة 1) ✅")
    elif score >= 5.0:
        st.info("النتيجة: جودة نومك متوسطة (تحتاج انتباه) ℹ️")
    else:
        st.error("النتيجة: جودة نومك منخفضة (تحتاج استشارة) ⚠️")
