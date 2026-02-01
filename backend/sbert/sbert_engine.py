import json, os
import numpy as np
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR,"..","data")

with open(os.path.join(DATA_DIR, "competencies.json"), "r", encoding="utf-8") as f:
    competencies = json.load(f)

with open(os.path.join(DATA_DIR, "jobs.json"), "r", encoding="utf-8") as f:
    jobs = json.load(f)


competency_embeddings = {
    c["id"]: model.encode(c["text"], convert_to_tensor=True)
    for c in competencies
}

blocks = {}
for c in competencies:
    blocks.setdefault(c["block_id"], []).append(c["id"])


def compute_similarity(text_list):
    user_emb = model.encode(text_list, convert_to_tensor=True)
    block_scores = {}

    for block_id, comp_ids in blocks.items():
        sims = []

        for cid in comp_ids:
            comp_emb = competency_embeddings[cid]
            score = util.cos_sim(user_emb, comp_emb)
            sims.append(float(score.max()))

        block_scores[block_id] = float(np.mean(sims))

    return block_scores


def compute_global_score(block_scores):
    return float(np.mean(list(block_scores.values())))


def compute_job_scores(block_scores):
    job_scores = {}

    for job in jobs:
        comp_ids = job["competencies"]

        scores = []
        for cid in comp_ids:
            block_id = next(c["block_id"] for c in competencies if c["id"] == cid)
            scores.append(block_scores[block_id])

        job_scores[job["id"]] = float(np.mean(scores))

    return job_scores
