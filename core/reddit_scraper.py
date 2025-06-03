import praw
import prawcore
from config.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT


reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


seen_subs = set()
seen_posts = set()


def search_subreddits(keywords, limit=15):
    subs = []

    for kw in keywords:
        for result in reddit.subreddits.search(kw, limit=limit):
            name = result.display_name
            if name in seen_subs:
                continue
            seen_subs.add(name)

            subs.append({
                'name': name,
                'url': f"https://reddit.com/r/{name}",
                'description': result.public_description,
                'subscribers': result.subscribers,
            })

    return subs


def search_posts(keywords, limit=15):
    posts = []
    for kw in keywords:
        for submission in reddit.subreddit("all").search(kw, sort="hot", limit=limit):
            if submission.id in seen_posts:
                continue
            seen_posts.add(submission.id)

            post = {
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'subreddit': submission.subreddit.display_name,
                    'url': submission.url,
                    'permalink': f"https://reddit.com{submission.permalink}",
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'created_utc': submission.created_utc
            }
            
            posts.append(post)

    return posts


def get_subreddit_context(subreddit_name, limit=3):
    try:
        posts = reddit.subreddit(subreddit_name).hot(limit=limit)
        return [f"{p.title}\n{p.selftext[:200]}" for p in posts if not p.stickied and p.selftext]
    except prawcore.exceptions.Forbidden:
        # print(f"403 Forbidden: Skipping r/{subreddit_name} (private/quarantined)")
        return []
    except Exception as e:
        # print(f"Error fetching context for r/{subreddit_name}: {e}")
        return []