from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, os

from ai_pipeline.analyzer import analyze_responses
from ai_pipeline.recommender import recommend_jobs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESPONSES_PATH = os.path.join(BASE_DIR, "models", "responses.json")



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



@app.post("/analyze/")
def analyze(data: dict):
    """
    Analyse simple — SBERT seulement
    """
    text_list = list(data.values())
    return analyze_responses(text_list)



@app.post("/recommend/")
def recommend(data: dict):
    text_list = list(data.values())
    return recommend_jobs(text_list)



@app.post("/api/analyze/")
def analyze_full(data: dict):
    """
    Analyse complète AISCA :
    - Scores des blocs
    - Score global
    - Top 3 métiers
    - Plan de progression IA
    - Résumé automatique (bio)
    """

    user_text_list = list(data.values())

    result = analyze_responses(user_text_list)

    block_scores = result["block_scores"]
    global_score = result["global_score"]
    top3 = result["top3_jobs"]
    progression = result["progression_plan"]

    return {
        "block_scores": result["block_scores"],
        "global_score": result["global_score"],
        "top3": result["top3_jobs"],
        "progression": result["progression_plan"],
        "bio": result["bio"]
    }

