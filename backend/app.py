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
    allow_origins=["*"],  # allow all for now; restrict later in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputText(BaseModel):
    text: str
    top_n: int = 3   # default: return top 3 emojis

@app.post("/predict")
def predict(data: InputText):
    X = vectorizer.transform([data.text])
    probs = model.predict_proba(X)[0]  # get probability distribution

    # Pick top_n indices
    top_n = min(data.top_n, len(encoder.classes_))
    top_indices = np.argsort(probs)[-top_n:][::-1]

    # Build result list
    results = [
        {"emoji": encoder.classes_[i], "confidence": round(float(probs[i]), 4)}
        for i in top_indices
    ]

    return {"input": data.text, "predictions": results}

