from flask import Blueprint, render_template, request
from markupsafe import escape
from extensions.limiter import limiter
from services.subreddit_service import process_subreddits
from services.post_service import process_posts

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

        top_subs = process_subreddits(product)
        top_posts = process_posts(product)

        results = {
            "subreddits": top_subs,
            "hidden": top_posts[:10],
            "error": None
        }

        return render_template("results.html", results=results)

    return render_template("index.html")
