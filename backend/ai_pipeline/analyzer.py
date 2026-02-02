from .sbert_engine import (
    compute_similarity,
    compute_global_score,
    compute_job_scores
)
from .recommender import recommend_jobs
from .progression import generate_progression
from .bio_generator import generate_bio


def analyze_responses(user_text_list):

    block_scores = compute_similarity(user_text_list)

    global_score = compute_global_score(block_scores)

    job_scores = compute_job_scores(block_scores)

    top3_jobs = recommend_jobs(job_scores)

    progression_plan = generate_progression(block_scores, top3_jobs)

    bio = generate_bio(user_text_list, block_scores, top3_jobs)

    return {
        "block_scores": block_scores,
        "global_score": round(global_score, 4),
        "top3_jobs": top3_jobs,
        "progression_plan": progression_plan,
        "bio": bio
    }
