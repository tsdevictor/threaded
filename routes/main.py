from flask import Blueprint, render_template, request
from markupsafe import escape
from extensions.limiter import limiter
from services.subreddit_service import process_subreddits
from services.post_service import process_posts
from core.gpt import get_search_terms

main = Blueprint("main", __name__)
MAX_LENGTH = 500

@main.route("/", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def index():
    if request.method == "POST":
        product = request.form.get("product", "")[:MAX_LENGTH]
        product = escape(product)

        if not product:
            return render_template("results.html", results={"error": "Missing product description."})

        search_terms = get_search_terms(product)
        top_subs = process_subreddits(product, search_terms)
        top_posts = process_posts(product, search_terms)

        results = {
            "subreddits": top_subs,
            "hidden": top_posts,
            "error": None
        }

        return render_template("results.html", results=results)

    return render_template("index.html")
