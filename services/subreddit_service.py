from core.reddit_scraper import search_subreddits, get_subreddit_context
from core.relevance_ranker import rank_subreddits
from core.gpt import generate_post


def process_subreddits(product, search_terms):
    top_subs = []
    subreddits_raw = search_subreddits(search_terms)

    if not subreddits_raw:
        return top_subs

    subreddits_ranked = rank_subreddits(product, subreddits_raw, text_key="description")

    for sub in subreddits_ranked[:10]:
        context_posts = get_subreddit_context(sub['name'])
        suggestion = generate_post(product, context_posts=context_posts)
        top_subs.append({
            "name": sub['name'],
            "url": sub['url'],
            "description": sub['description'],
            "subscribers": sub['subscribers'],
            "relevance": sub['relevance'] * 10 / (sub['relevance'] + 0.3),
            "suggestion": suggestion
        })

    return top_subs
