import numpy as np
from .sbert_engine import compute_similarity, compute_global_score, compute_job_scores, jobs
from .progression import generate_progression


def normalize_score(score, min_val=0.0, max_val=1.0):
    """Normalise entre 0 et 1"""
    return (score - min_val) / (max_val - min_val)


def analyze_responses(user_text_list):
    """Pipeline complet étape 4 + 5 + 6 + Mode Debug pour vérifier la similarité SBERT"""

    print("\n====================")
    print("  🔍 DEBUG SBERT AISCA")
    print("====================\n")

    print("📌 Réponses utilisateur :")
    for i, txt in enumerate(user_text_list, 1):
        print(f"  Phrase {i} → {txt}")

    # ----------------------------
    # 1️⃣ Scores SBERT par bloc
    # ----------------------------
    block_scores = compute_similarity(user_text_list)

    print("\n=== Scores par bloc (NON normalisés) ===")
    for b, s in block_scores.items():
        print(f"  Bloc {b} → {s:.4f}")

    # ----------------------------
    # 2️⃣ Score global brut
    # ----------------------------
    global_score_raw = compute_global_score(block_scores)
    print("\n=== Score global brut ===")
    print(f"  {global_score_raw:.4f}")

    # ----------------------------
    # 3️⃣ Normalisation du score global
    # ----------------------------
    global_score_normalized = normalize_score(global_score_raw, 0.2, 0.8)
    print("\n=== Score global normalisé (0 à 1) ===")
    print(f"  {global_score_normalized:.4f}")

    # ----------------------------
    # 4️⃣ Scores métiers
    # ----------------------------
    job_scores = compute_job_scores(block_scores)

    print("\n=== Scores métiers ===")
    for jid, s in job_scores.items():
        print(f"  {jid} → {s:.4f}")

    # ----------------------------
    # 5️⃣ Top 3 métiers
    # ----------------------------
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

    print("\n=== TOP 3 métiers recommandés ===")
    for job in top3_jobs:
        print(f"  {job['title']} → {job['score']:.4f}")

    # ----------------------------
    # 6️⃣ IA Générative : Plan de progression
    # ----------------------------
    print("\n=== Génération du plan de progression (Mistral) ===")
    progression_plan = generate_progression(block_scores, top3_jobs)

    # ----------------------------
    # 7️⃣ Retour final
    # ----------------------------
    print("\n====================")
    print("  ✅ FIN DEBUG AISCA")
    print("====================\n")

    return {
        "block_scores": block_scores,
        "global_score": round(global_score_normalized, 4),
        "job_scores": job_scores,
        "top3_jobs": top3_jobs,
        "progression_plan": progression_plan
    }
