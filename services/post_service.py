from core.reddit_scraper import search_posts, get_subreddit_context
from core.relevance_ranker import rank_posts
from core.gpt import generate_post
from core.utils import get_relative_time


def process_posts(product, search_terms):
    top_posts = []
    posts_raw = search_posts(search_terms)
    
    if not posts_raw:
        return top_posts
    
    ranked = rank_posts(product, posts_raw) 

    for post in ranked[:10]:
        context_posts = get_subreddit_context(post['subreddit'])
        suggestion = generate_post(product, context_posts=context_posts, reply_to=post)

        top_posts.append({
            "title": post['title'],
            "url": post['permalink'],
            "subreddit": post['subreddit'],
            "score": post['score'],
            "relative_date": get_relative_time(post['created_utc']),
            "comments": post['num_comments'],
            "relevance": post['relevance'] * 10 / (post['relevance'] + 3),
            "suggestion": suggestion
        })

    return top_posts
