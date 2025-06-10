from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel
from textblob import TextBlob
import base64
import io
from reportlab.pdfgen import canvas

app = FastAPI(title="AI Immigration Navigator")

# Mount frontend static files relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend"), name="static")


class ImmigrationQuery(BaseModel):
    nationality: str
    current_visa: str
    target_visa: str
    occupation: str


class FormData(BaseModel):
    name: str
    dob: str
    country: str
    relationship: str


class WellnessQuery(BaseModel):
    message: str


class TranslationQuery(BaseModel):
    text: str
    language: str


@app.get("/", response_class=HTMLResponse)
def root_page():
    with open(BASE_DIR / "frontend" / "index.html") as f:
        return HTMLResponse(f.read())


@app.post("/api/immigration")
def immigration_steps(query: ImmigrationQuery):
    return {
        "forms": ["I-130", "I-765"],
        "steps": ["Complete forms", "Submit fees"],
        "timeline": "6-12 months",
        "cost": "$500-$1000",
        "feedback": f"Eligibility check for {query.target_visa}"
    }


@app.post("/api/fill_form")
def fill_form(data: FormData):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(100, 750, f"Form I-130 for {data.name}")
    pdf.drawString(100, 730, f"DOB: {data.dob}")
    pdf.drawString(100, 710, f"Country: {data.country}")
    pdf.drawString(100, 690, f"Relationship: {data.relationship}")
    pdf.save()
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode("utf-8")
    return {"pdf_base64": b64}


@app.post("/api/wellness")
def wellness(query: WellnessQuery):
    tb = TextBlob(query.message)
    polarity = tb.sentiment.polarity
    if polarity < 0:
        advice = "Consider speaking with a counselor or practicing relaxation."
    else:
        advice = "Keep up the positive mindset!"
    return {"score": polarity, "advice": advice}


@app.post("/api/translate")
def translate_text(q: TranslationQuery):
    # Placeholder translation logic
    translated = f"{q.text} (translated to {q.language})"
    return {"translation": translated}


@app.get("/api/timeline")
def sample_timeline():
    return {
        "events": [
            {"task": "Submit I-130", "start": "2025-01-01", "end": "2025-01-15"},
            {"task": "Biometrics", "start": "2025-02-01", "end": "2025-02-02"},
            {"task": "Interview", "start": "2025-03-01", "end": "2025-03-01"}
        ]
    }
