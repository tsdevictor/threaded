import praw
import prawcore
from config.config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT


reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


def search_subreddits(keywords, limit=15):
    subs = []
    seen = set()

    for idx, kw in enumerate(keywords):
        counter = 0
        for result in reddit.subreddits.search(kw, limit=limit):
            name = result.display_name
            if name in seen:
                continue
            seen.add(name)
            counter += 1

            recent_scores, recent_comments, latest_timestamp = [], [], 0
            try:
                for post in reddit.subreddit(name).hot(limit=3):
                    recent_scores.append(post.score)
                    recent_comments.append(post.num_comments)
                    latest_timestamp = max(latest_timestamp, post.created_utc)
            except:
                pass

            activity = {
                "recent_score": sum(recent_scores)/len(recent_scores) if recent_scores else 0,
                "recent_comments": sum(recent_comments)/len(recent_comments) if recent_comments else 0,
                "latest_post_time": latest_timestamp
            }

            subs.append({
                'name': name,
                'url': f"https://reddit.com/r/{name}",
                'description': result.public_description,
                'subscribers': result.subscribers,
                **activity
            })
        # print(f'Keyword {idx} ("{kw}") led to {counter} new subreddits')

    return subs


def search_posts(keywords, limit=25):
    posts = []
    seen = set()

    for kw in keywords:
        for submission in reddit.subreddit("all").search(kw, sort="hot", limit=limit):
            if submission.id in seen:
                continue
            seen.add(submission.id)

            post = {
                    'id': submission.id,
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


def get_subreddit_context(subreddit_name, limit=5):
    try:
        posts = reddit.subreddit(subreddit_name).hot(limit=limit)
        return [f"{p.title}\n{p.selftext[:200]}" for p in posts if not p.stickied and p.selftext]
    except prawcore.exceptions.Forbidden:
        # print(f"403 Forbidden: Skipping r/{subreddit_name} (private/quarantined)")
        return []
    except Exception as e:
        # print(f"Error fetching context for r/{subreddit_name}: {e}")
        return []