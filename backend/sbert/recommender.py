import json, os
from .sbert_engine import compute_similarity, compute_global_score, compute_job_scores

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

with open(os.path.join(DATA_DIR, "jobs_descriptions.json"), "r", encoding="utf-8") as f:
    job_details = json.load(f)


def recommend_jobs(user_text_list):
    """
    Retourne les 3 métiers les plus compatibles
    + description métier
    + score global
    + scores blocs
    """

    # 1. Scores blocs
    block_scores = compute_similarity(user_text_list)

    # 2. Score global AISCA
    global_score = compute_global_score(block_scores)

    # 3. Scores métiers
    job_scores = compute_job_scores(block_scores)

    # 4. Top 3
    top3 = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)[:3]

    # 5. Enrichir descriptions
    result = []
    for job_id, score in top3:
        result.append({
            "job_id": job_id,
            "title": job_details[job_id]["title"],
            "score": round(float(score), 4),
            "description": job_details[job_id]["description"]
        })

    return {
        "top3_jobs": result,
        "global_score": round(global_score, 4),
        "block_scores": block_scores
    }
