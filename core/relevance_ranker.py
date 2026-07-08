from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from datetime import datetime, timezone
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_posts(product_desc, candidates, min_sim=0.6):
    now = datetime.now(timezone.utc).timestamp()
    queries = [product_desc] + [f"{c['title']} {c.get('selftext', '')}" for c in candidates]
    
    vectors = model.encode(queries)
    similarities = cosine_similarity([vectors[0]], vectors[1:])[0]

    ranked = []
    for i, sim in enumerate(similarities):
        if sim < min_sim:
            continue  # skip irrelevant posts

        c = candidates[i]
        hours_old = (now - c.get("created_utc", now)) / 3600
        recency_bonus = np.exp(-hours_old / 168)
        popularity_bonus = (c.get("score", 1) + c.get("num_comments", 1)) ** 0.3
        popularity_bonus = 5 * popularity_bonus / (10 + popularity_bonus)

        sim = max(sim, 0)
        sim = sim ** 2 + 9 * sim
        final_score = sim * recency_bonus * popularity_bonus
        c['relevance'] = final_score
        ranked.append(c)
    
    return sorted(ranked, key=lambda x: x['relevance'], reverse=True)



def rank_subreddits(product_desc, candidates, text_key='description', min_sim=0.3):
    queries = [product_desc] + [c.get(text_key, '') for c in candidates]
    vectors = model.encode(queries)
    similarities = cosine_similarity([vectors[0]], vectors[1:])[0]

    ranked = []
    for i, sim in enumerate(similarities):
        if sim < min_sim:
            continue

        c = candidates[i]
        popularity_bonus = (c.get("score", 1) + 1) ** 0.15
        
        sim = max(sim, 0)
        sim = sim ** 2 + sim
        final_score = sim * popularity_bonus
        c['relevance'] = final_score
        ranked.append(c)

    return sorted(ranked, key=lambda x: x['relevance'], reverse=True)
