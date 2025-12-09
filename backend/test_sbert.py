from backend.sbert.sbert_engine import compute_similarity, compute_global_score, compute_job_scores

user_texts = [
    "J'ai aidé un patient en difficulté émotionnelle.",
    "J'ai surveillé son état et prévenu une infirmière.",
    "Je suis très organisé dans la gestion des dossiers."
]

block_scores = compute_similarity(user_texts)
print("\n🔹 Scores par bloc :", block_scores)

global_score = compute_global_score(block_scores)
print("\n🔹 Score global :", global_score)

job_scores = compute_job_scores(block_scores)
print("\n🔹 Scores métiers :", job_scores)
