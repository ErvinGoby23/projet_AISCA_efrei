import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

with open(os.path.join(DATA_DIR, "jobs_descriptions.json"), "r", encoding="utf-8") as f:
    job_details = json.load(f)


def recommend_jobs(job_scores, top_n=3):
    """
    Transforme des scores métiers en Top N métiers lisibles
    """

    top = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    result = []
    for job_id, score in top:
        result.append({
            "job_id": job_id,
            "title": job_details[job_id]["title"],
            "score": float(score),
            "description": job_details[job_id]["description"]
        })

    return result
