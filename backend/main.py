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


def load_responses():
    """Charge les réponses en évitant les erreurs JSON."""
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

    # Sauvegarde
    with open(RESPONSES_PATH, "w", encoding="utf-8") as f:
        json.dump(all_responses, f, indent=4, ensure_ascii=False)

    return {"message": "saved", "id": new_id}
