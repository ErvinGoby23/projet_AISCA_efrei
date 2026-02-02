from mistralai import Mistral
import os

API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=API_KEY)


def generate_bio(user_text_list, block_scores, top3_jobs):
    answers_txt = "\n".join([f"- {txt}" for txt in user_text_list])

    strengths = sorted(block_scores.items(), key=lambda x: x[1], reverse=True)[:2]

    strengths_txt = ", ".join(
        [f"bloc {b}" for b, _ in strengths]
    )

    jobs_txt = ", ".join([job["title"] for job in top3_jobs])

    prompt = f"""
Tu es un conseiller en orientation professionnelle.

À partir des éléments suivants :

Réponses utilisateur :
{answers_txt}

Forces principales : {strengths_txt}
Métiers recommandés : {jobs_txt}

Rédige un résumé de profil (BIO) clair et synthétique :
- 5 à 6 lignes maximum
- orienté utilisateur
- sans chiffres
- ton professionnel et bienveillant
"""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
