import numpy as np
from .sbert_engine import compute_similarity, compute_global_score, compute_job_scores, jobs
from .progression import generate_progression
from .progression import generate_progression
from .sbert_engine import competencies, jobs
from mistralai import Mistral
import os

# Charger la clé API
API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=API_KEY)


# ---------------------------------------------------------
# 1) CONTEXTE POUR L’IA
# ---------------------------------------------------------
def build_context(user_text_list, analysis_results):

    block_scores = analysis_results["block_scores"]
    global_score = analysis_results["global_score"]
    job_scores = analysis_results["job_scores"]
    top3 = analysis_results["top3_jobs"]

    percent_blocks = {b: round(s * 100, 1) for b, s in block_scores.items()}

    ordered = sorted(percent_blocks.items(), key=lambda x: x[1], reverse=True)

    strengths = [f"Bloc {b} ({v}%)" for b, v in ordered[:2]]
    weaknesses = [f"Bloc {b} ({v}%)" for b, v in ordered[-2:]]

    answers_txt = "\n".join([f"- {txt}" for txt in user_text_list])

    jobs_txt = "\n".join([
        f"- {job['title']} (score : {round(job['score']*100, 1)}%)"
        for job in top3
    ])

    context = f"""
======================
PROFIL UTILISATEUR
======================
Réponses données au questionnaire :
{answers_txt}

======================
SYNTHÈSE AISCA
======================
Score global : {round(global_score * 100, 1)} %

Scores par bloc :
{percent_blocks}

Forces détectées :
{strengths}

Faiblesses détectées :
{weaknesses}

======================
RECOMMANDATIONS MÉTIERS
======================
Top 3 métiers :
{jobs_txt}

Scores détaillés métiers :
{job_scores}

======================
INSTRUCTIONS POUR L'IA
======================
À partir de ces informations :

1) Rédige un résumé du profil.
2) Identifie les forces du candidat.
3) Identifie les points à améliorer.
4) Génère un plan d'action structuré :
   - Court terme (3 actions)
   - Moyen terme (3 actions)
5) Explique pourquoi les métiers recommandés correspondent au profil.

Réponds de manière structurée.
"""
    return context


# ---------------------------------------------------------
# 2) ANALYSE PRINCIPALE (manquante → CAUSAIT LE BUG)
# ---------------------------------------------------------
def analyze_responses(user_text_list):
    """
    Pipeline complet AISCA :
    - Scores SBERT
    - Score global
    - Top 3 métiers
    - Contexte IA
    - Plan & BIO via Mistral
    """

    # --- 1) Scores blocs ---
    block_scores = compute_similarity(user_text_list)

    # --- 2) Score global ---
    global_score = compute_global_score(block_scores)

    # --- 3) Scores métiers ---
    job_scores = compute_job_scores(block_scores)

    # Top 3 métiers enrichis
    sorted_jobs = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    top3_jobs = [
        {
            "job_id": jid,
            "title": next(job["title"] for job in jobs if job["id"] == jid),
            "description": next(job.get("description", "") for job in jobs if job["id"] == jid),
            "score": float(score)
        }
        for jid, score in sorted_jobs
    ]

    # --- 4) Bâtir le contexte pour IA ---
    analysis_results = {
        "block_scores": block_scores,
        "global_score": global_score,
        "job_scores": job_scores,
        "top3_jobs": top3_jobs
    }

    context = build_context(user_text_list, analysis_results)

    # --- 5) Génération IA ---
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": context}]
    )

    progression_plan = response.choices[0].message.content

    # --- 6) Retour final ---
    return {
        "block_scores": block_scores,
        "global_score": round(global_score, 4),
        "job_scores": job_scores,
        "top3_jobs": top3_jobs,
        "progression_plan": progression_plan
    }
