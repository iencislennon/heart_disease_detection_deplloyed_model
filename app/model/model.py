import pickle 
import re 
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

with open(f"{BASE_DIR}/xgb_model.pkl", "rb") as f:
    model = pickle.load(f)

classes = ["Absense", "Presence"]

def predict(age: float,
    sex: int,                    # 0 or 1
    chest_pain_type: int,        # 1-4
    bp: float,                   # Blood Pressure
    cholesterol: float,
    fbs_over_120: int,           # 0 or 1
    ekg_results: int,            # 0, 1, 2
    max_hr: float,
    exercise_angina: int,        # 0 or 1
    st_depression: float,
    slope_of_st: int,            # 1-3
    number_of_vessels_fluro: int, # 0-3
    thallium: int                # 3, 6, 7
) -> dict:
    st_depression_log = np.log1p(st_depression)

    features = pd.DataFrame([{
        "Age": age,
        "Sex": sex,
        "Chest pain type": chest_pain_type,
        "BP": bp,
        "Cholesterol": cholesterol,
        "FBS over 120": fbs_over_120,
        "EKG results": ekg_results,
        "Max HR": max_hr,
        "Exercise angina": exercise_angina,
        "ST depression": st_depression,
        "Slope of ST": slope_of_st,
        "Number of vessels fluro": number_of_vessels_fluro,
        "Thallium": thallium,

        
        }
    ])

    proba = model.predict_proba(features)[0]
    predicted_class = classes[int(np.argmax(proba))]

    return { """ возвращаеть словарь с предсказанным классом и вероятностями обоих классов это удобно для fastapi он автоматически сериализует это в json"""
        "prediction": predicted_class,
        "probability_absence": round(float(proba[0]), 4),
        "probability_presence": round(float(proba[1]), 4)
    }