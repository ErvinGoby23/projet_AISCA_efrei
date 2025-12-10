import json
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR,"../data", "mini_llm_data.json")


with open(DATA_PATH, "r", encoding="utf-8") as f:
    MINI_LLM = json.load(f)


def fill_template(template: str, data: dict):
    for key, values in data.items():
        if isinstance(values, list):
            template = template.replace("{" + key + "}", random.choice(values))
    return template


def generate_completion(question_id: int):
    """
    Génère une phrase complète basée sur la question.
    """
    q_key = f"q{question_id}_templates"

    if q_key not in MINI_LLM:
        # fallback générique
        return random.choice(MINI_LLM["generic_fallbacks"]) + "..."

    template = random.choice(MINI_LLM[q_key])

    # Charge dynamiquement les variables associées (ex: q1_actions, q1_impact)
    vars_for_template = {
        key.replace(f"{question_id}_", ""): values
        for key, values in MINI_LLM.items()
        if key.startswith(f"q{question_id}_") and key != q_key
    }

    return fill_template(template, vars_for_template)


def enrich_text_if_short(text: str, question_index: int):
    """
    Complète automatiquement une réponse trop courte (< 5 mots)
    en utilisant notre mini LLM maison basé sur JSON.
    """

    # Listes d'activités (questions avec choix multiple)
    if isinstance(text, list):
        return ", ".join(text)

    if not isinstance(text, str):
        return text

    # Normalisation
    cleaned = text.strip().lower()

    # Phrase assez longue → rien à faire
    if len(cleaned.split()) >= 5:
        return text

    # Sinon → génération d’une phrase complète
    return generate_completion(question_index)
