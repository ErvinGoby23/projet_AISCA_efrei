from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, os

# Importer le moteur SBERT (étapes 3 + 4)
from sbert.analyzer import analyze_responses
from sbert.recommender import recommend_jobs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESPONSES_PATH = os.path.join(BASE_DIR, "models", "responses.json")


# -------------------------
# LECTURE SÉCURISÉE JSON
# -------------------------
def load_responses():
    if not os.path.exists(RESPONSES_PATH):
        return []

    try:
        with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []


# -------------------------
# ROUTE 1 : Sauvegarde
# -------------------------
@app.post("/save-responses/")
def save_responses(data: dict):

    all_responses = load_responses()

    new_id = len(all_responses) + 1

    entry = {
        "id": new_id,
        "answers": data
    }

    all_responses.append(entry)

    with open(RESPONSES_PATH, "w", encoding="utf-8") as f:
        json.dump(all_responses, f, indent=4, ensure_ascii=False)

    return {"message": "saved", "id": new_id}


# -------------------------
# ROUTE 2 : Analyse SBERT
# -------------------------
@app.post("/analyze/")
def analyze(data: dict):
    """
    data = réponses utilisateur envoyées par Streamlit
    """

    # convertir dict → liste de phrases
    text_list = list(data.values())

    # Appel du moteur SBERT (étapes 3 + 4)
    result = analyze_responses(text_list)

    return result

@app.post("/recommend/")
def recommend(data: dict):
    text_list = list(data.values())
    return recommend_jobs(text_list)
