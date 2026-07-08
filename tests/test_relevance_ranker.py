import numpy as np
import pytest


class FakeModel:
    def encode(self, queries):
        # First query is product. Candidates are deliberately similar / dissimilar.
        vectors = []
        for q in queries:
            q = q.lower()
            if "study" in q or "exam" in q:
                vectors.append([1.0, 0.0])
            else:
                vectors.append([0.0, 1.0])
        return np.array(vectors)


def test_rank_posts_filters_irrelevant_posts(monkeypatch):
    import core.relevance_ranker as rr

    monkeypatch.setattr(rr, "model", FakeModel())

    candidates = [
        {
            "title": "Need a better study group for exams",
            "selftext": "Looking for classmates to study with.",
            "created_utc": rr.datetime.now(rr.timezone.utc).timestamp(),
            "score": 10,
            "num_comments": 5,
        },
        {
            "title": "Best hiking boots",
            "selftext": "Trail recommendations?",
            "created_utc": rr.datetime.now(rr.timezone.utc).timestamp(),
            "score": 100,
            "num_comments": 20,
        },
    ]

    ranked = rr.rank_posts("study group exam prep", candidates, min_sim=0.6)

    assert len(ranked) == 1
    assert "study group" in ranked[0]["title"].lower()


def test_rank_subreddits_returns_descending_relevance(monkeypatch):
    import core.relevance_ranker as rr

    monkeypatch.setattr(rr, "model", FakeModel())

    candidates = [
        {"name": "college", "description": "study exam prep", "score": 10},
        {"name": "outdoors", "description": "hiking camping gear", "score": 100},
    ]

    ranked = rr.rank_subreddits("study group exam prep", candidates, min_sim=0.3)

    assert ranked[0]["name"] == "college"
    assert all("relevance" in c for c in ranked)
