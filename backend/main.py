from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESPONSES_PATH = os.path.join(BASE_DIR, "models", "responses.json")

@app.post("/save-responses/")
def save_responses(data: dict):

    # Charger l'existant
    if os.path.exists(RESPONSES_PATH):
        with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
            all_responses = json.load(f)
    else:
        all_responses = []

    new_id = len(all_responses) + 1

    entry = {
        "id": new_id,
        "answers": data
    }

    all_responses.append(entry)

    # Sauvegarde
    with open(RESPONSES_PATH, "w", encoding="utf-8") as f:
        json.dump(all_responses, f, indent=4, ensure_ascii=False)

    return {"message": "saved", "id": new_id}
