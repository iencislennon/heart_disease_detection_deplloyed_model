import streamlit as st
import requests

st.title("Heart disease detection")


# 3 колонки для компактности
col1, col2, col3 = st.columns(3)

# Фича 1: Age (возраст, 29-77 типично)
with col1:
    age = st.number_input("Age", min_value=0, max_value=100, value=50, step=1)

# Фича 2: Sex (0-female, 1-male)
with col2:
    sex = st.selectbox("Sex", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")

# Фича 3: Chest pain type (1-4)
with col3:
    chest_pain = st.selectbox("Chest pain type", [1, 2, 3, 4],
                              format_func=lambda x: {1: "Typical angina", 2: "Atypical angina",
                                                     3: "Non-anginal pain", 4: "Asymptomatic"}[x])

# Следующий ряд
col1, col2, col3 = st.columns(3)

# Фича 4: BP (resting blood pressure, 94-200)
with col1:
    bp = st.number_input("BP (mm Hg)", min_value=80, max_value=250, value=120, step=1)

# Фича 5: Cholesterol (0-564, 0=missing)
with col2:
    cholesterol = st.number_input("Cholesterol (mg/dl)", min_value=0, max_value=1000, value=200, step=1)

# Фича 6: FBS over 120 (0/1)
with col3:
    fbs = st.selectbox("FBS over 120 (mg/dl)", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

# Ряд 3
col1, col2, col3 = st.columns(3)

# Фича 7: EKG results (0,1,2)
with col1:
    ekg = st.selectbox("EKG results", [0, 1, 2],
                       format_func=lambda x: {0: "Normal", 1: "ST-T abnormality", 2: "LVH"}[x])

# Фича 8: Max HR (71-202)
with col2:
    max_hr = st.number_input("Max HR", min_value=50, max_value=250, value=150, step=1)

# Фича 9: Exercise angina (0/1)
with col3:
    ex_angina = st.selectbox("Exercise angina", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

# Ряд 4
col1, col2, col3 = st.columns(3)

# Фича 10: ST depression (0-6.2)
with col1:
    st_depression = st.number_input("ST depression", min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f")

# Фича 11: Slope of ST (1-3)
with col2:
    slope_st = st.selectbox("Slope of ST", [1, 2, 3],
                            format_func=lambda x: {1: "Upsloping", 2: "Flat", 3: "Downsloping"}[x])

# Фича 12: Number of vessels fluro (0-4)
with col3:
    vessels = st.selectbox("Number of vessels fluro", [0, 1, 2, 3, 4])

# Ряд 5
col1, col2, col3 = st.columns(3)

with col1:
    # Фича 13: Thallium (3=normal, 6=fixed, 7=rev)
    thallium = st.selectbox("Thallium", [3, 6, 7],
                            format_func=lambda x: {3: "Normal", 6: "Fixed defect", 7: "Reversible defect"}[x])

# Сбор всех фич в словарь или список для модели
features = {
    'Age': age, 'Sex': sex, 'Chest pain type': chest_pain, 'BP': bp, 'Cholesterol': cholesterol,
    'FBS over 120': fbs, 'EKG results': ekg, 'Max HR': max_hr, 'Exercise angina': ex_angina,
    'ST depression': st_depression, 'Slope of ST': slope_st, 'Number of vessels fluro': vessels,
    'Thallium': thallium
}
if st.button("Predict", use_container_width=True):

    data = {
        "age": age,
        "sex": sex,
        "chest_pain_type": chest_pain,
        "bp": bp,
        "cholesterol": cholesterol,
        "fbs_over_120": fbs,
        "ekg_results": ekg,
        "max_hr": max_hr,
        "exercise_angina": ex_angina,
        "st_depression": st_depression,
        "slope_of_st": slope_st,
        "number_of_vessels_fluro": vessels,
        "thallium": thallium
    }
    API_URL = "https://heart-disease-detection-deplloyed-model.onrender.com/predict"

    try:
        with st.spinner("Predicting..."):
            response = requests.post(API_URL, json=data)
            response.raise_for_status() # error checking

        result = response.json()
        prediction = result.get("prediction")
        if prediction == "Presence":
            st.error(f"heart disease detected")
        else:
            st.success(f"no heart disease detected")
            
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Absence probability", f"{result['probability_absence']*100:.1f}%")
        with col2:
            st.metric("Presence probability", f"{result['probability_presence']*100:.1f}%")


    except requests.exceptions.RequestException as e:
            st.error(f"API error: {str(e)}")
    except Exception as e:
        st.error(f"error: {str(e)}")

