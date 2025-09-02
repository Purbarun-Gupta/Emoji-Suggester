from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# --------------------------
# Load model, encoder, and vectorizer
# --------------------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# --------------------------
# FastAPI app
# --------------------------
app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputText(BaseModel):
    text: str

@app.post("/predict")
def predict(data: InputText):
    X = vectorizer.transform([data.text])
    prediction = model.predict(X)
    emoji = encoder.inverse_transform(prediction)[0]
    return {"emoji": emoji}
