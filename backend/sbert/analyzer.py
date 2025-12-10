import numpy as np
from .sbert_engine import compute_similarity, compute_global_score, compute_job_scores, jobs
from .progression import generate_progression
from .enrichment import enrich_text_if_short


def normalize_score(score, min_val=0.0, max_val=1.0):
    return (score - min_val) / (max_val - min_val)


def analyze_responses(user_text_list):
    print("\n====================")
    print("  🔍 DEBUG SBERT AISCA")
    print("====================\n")

    print("📌 Réponses utilisateur (avant enrichissement) :")
    for i, txt in enumerate(user_text_list, 1):
        print(f"  Phrase {i} → {txt}")

    # ENRICHISSEMENT DES PHRASES
    enriched_list = []
    print("\n📌 Phrases enrichies (après IA) :")

    for idx, txt in enumerate(user_text_list, 1):
        if isinstance(txt, list):
            enriched = ", ".join(txt)
        else:
            enriched = enrich_text_if_short(txt, idx)

        enriched_list.append(enriched)
        print(" →", enriched)

    # 1️⃣ SIMILARITÉS SBERT
    block_scores = compute_similarity(enriched_list)

    print("\n=== Scores par bloc (NON normalisés) ===")
    for b, s in block_scores.items():
        print(f"  Bloc {b} → {s:.4f}")

    # 2️⃣ SCORE GLOBAL
    global_score_raw = compute_global_score(block_scores)
    print("\n=== Score global brut ===")
    print(f"  {global_score_raw:.4f}")

    global_score_normalized = normalize_score(global_score_raw, 0.2, 0.8)
    print("\n=== Score global normalisé (0 à 1) ===")
    print(f"  {global_score_normalized:.4f}")

    # 3️⃣ SCORES METIERS
    job_scores = compute_job_scores(block_scores)

    print("\n=== Scores métiers ===")
    for jid, s in job_scores.items():
        print(f"  {jid} → {s:.4f}")

    # 4️⃣ TOP 3
    sorted_jobs = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    top3_jobs = [
        {
            "job_id": jid,
            "title": next(job["title"] for job in jobs if job["id"] == jid),
            "score": float(score)
        }
        for jid, score in sorted_jobs
    ]

    print("\n=== TOP 3 métiers recommandés ===")
    for j in top3_jobs:
        print(f"  {j['title']} → {j['score']:.4f}")

    # 5️⃣ PLAN DE PROGRESSION (Mistral)
    print("\n=== Génération du plan de progression (Mistral) ===")
    progression_plan = generate_progression(block_scores, top3_jobs)

    print("\n====================")
    print("  ✅ FIN DEBUG AISCA")
    print("====================\n")

    # 🚀 IMPORTANT : RETOURNER LE DICTIONNAIRE
    return {
        "block_scores": block_scores,
        "global_score": round(global_score_normalized, 4),
        "job_scores": job_scores,
        "top3_jobs": top3_jobs,
        "progression_plan": progression_plan
    }
