from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
from model.model import predict

app = FastAPI()

"""{age: float,
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
    thallium: int}       """

class Featureschema(BaseModel):
    age: int
    sex: int = Field(ge=0, le=1, description="0 or 1")
    chest_pain_type: int = Field(ge=1, le=4, description="-4")
    bp: float
    cholesterol: float
    fbs_over_120: int = Field(ge=0, le=1, description="0 or 1") 
    ekg_results: int = Field(ge=0, le=2, description="0 or 1 or 2")
    max_hr: float
    exercise_angina: int = Field(ge=0, le=1, description="0 or 1")
    st_depression: float
    slope_of_st: int = Field(ge=1, le=3, description="1-3")
    number_of_vessels_fluro: int = Field(ge=0, le=3, description="0-3")
    thallium: int

@app.post('/predict')
async def predict_endpoint(features: Featureschema):
    return predict(**features.dict())

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)