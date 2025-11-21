from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# CORS — VERY IMPORTANT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key="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")

class InputNote(BaseModel):
    note: str

@app.post("/analyze")
def analyze(input: InputNote):
    prompt = f"""
You are a clinical triage assistant for paramedics.

Analyze this patient note:
\"{input.note}\"

Return your answer in this EXACT format (no extra text):

DIFFERENTIAL DIAGNOSES (Top 5):
1. ...
2. ...
3. ...
4. ...
5. ...

IMMEDIATE CRITICAL STEPS (Do these first):
1. ...
2. ...
3. ...

RED FLAGS:
- ...
- ...
- ...
"""


    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
