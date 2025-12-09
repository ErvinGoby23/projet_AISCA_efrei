import numpy as np
from .sbert_engine import compute_similarity, compute_global_score, compute_job_scores, jobs
from .progression import generate_progression


def normalize_score(score, min_val=0.0, max_val=1.0):
    """Normalise entre 0 et 1"""
    return (score - min_val) / (max_val - min_val)


def analyze_responses(user_text_list):
    """Pipeline complet étape 4 + 5 + 6"""

    # 1️⃣ Scores SBERT par bloc
    block_scores = compute_similarity(user_text_list)

    # 2️⃣ Score global brut
    global_score_raw = compute_global_score(block_scores)

    # 3️⃣ Normalisation 0-1
    global_score_normalized = normalize_score(global_score_raw, 0.2, 0.8)

    # 4️⃣ Scores métiers
    job_scores = compute_job_scores(block_scores)

    # 5️⃣ Calcul du TOP 3 métiers
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

    # 6️⃣ Génération du plan de progression par IA
    progression_plan = generate_progression(block_scores, top3_jobs)

    # 7️⃣ Réponse finale
    return {
        "block_scores": block_scores,
        "global_score": round(global_score_normalized, 4),
        "job_scores": job_scores,
        "top3_jobs": top3_jobs,
        "progression_plan": progression_plan
    }
