from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------
# Load model, encoder, and vectorizer
# -------------------------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# -------------------------------
# FastAPI app
# -------------------------------
app = FastAPI(
    title="Emoji Suggestion API",
    description="Predict emojis from text using a trained ML model",
    version="2.0"
)

# Allow frontend (React/Vercel) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your deployed frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Request & Response Schemas
# -------------------------------
class TextInput(BaseModel):
    text: str
    top_n: int = 3   # default: top 3 emojis

class EmojiPrediction(BaseModel):
    emoji: str
    confidence: float

class PredictionResponse(BaseModel):
    input: str
    predictions: list[EmojiPrediction]

# -------------------------------
# Routes
# -------------------------------
@app.get("/")
def home():
    return {"message": "Emoji Suggestion API is running 🎉"}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: TextInput):
    try:
        text = data.text.strip()
        if not text:
            return {"input": text, "predictions": []}

        # Transform input text
        X = vectorizer.transform([text])

        # Predict probabilities
        probs = model.predict_proba(X)[0]

        # Get top-N predictions
        top_n = min(data.top_n, len(encoder.classes_))
        top_indices = np.argsort(probs)[-top_n:][::-1]

        results = [
            {"emoji": encoder.classes_[i], "confidence": round(float(probs[i]), 4)}
            for i in top_indices
        ]

        return {"input": text, "predictions": results}

    except Exception as e:
        return {"input": data.text, "predictions": [], "error": str(e)}

