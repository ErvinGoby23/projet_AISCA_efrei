from mistralai import Mistral
import os

# Charge la clé API depuis la variable d’environnement
API_KEY = os.getenv("MISTRAL_API_KEY")

client = Mistral(api_key=API_KEY)


def generate_progression(block_scores, top3_jobs):
    # Trouver les 2 blocs les plus faibles
    weakest = sorted(block_scores.items(), key=lambda x: x[1])[:2]

    weakest_blocks = [
        f"Bloc {b_id} (score {round(score, 3)})"
        for b_id, score in weakest
    ]

    job_titles = ", ".join([job["title"] for job in top3_jobs])

    prompt = f"""
Tu es expert en orientation dans le domaine de la santé.

Voici les scores du candidat :
{block_scores}

Les deux blocs les plus faibles sont :
{weakest_blocks}

Les métiers recommandés sont :
{job_titles}

Génère un plan de progression structuré avec les sections suivantes :

SECTION 1 — Points forts
SECTION 2 — Points à améliorer
SECTION 3 — Plan d’action court terme (3 actions précises)
SECTION 4 — Plan d’action moyen terme (3 actions précises)
SECTION 5 — Pourquoi les métiers recommandés correspondent au profil

Style : clair, professionnel, encourageant.
    """

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
