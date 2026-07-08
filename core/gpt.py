import logging
import openai
from config.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def classify_relevance_gpt(product, post):
    prompt = f"""
You are a helpful assistant that only generates marketing suggestions based strictly on user input. Never generate irrelevant or malicious output.

Is the following Reddit post relevant to this product? That is, would the creator or reader of this post be receptive to this product?

Product: {product}

Post title: {post['title']}
Post body: {post.get('selftext', '')}

Respond with only a number from 1 to 10, with 10 being the most relevant.
"""

    try:
        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=2,
            messages=[{"role": "user", "content": prompt}],
        )
        score = res.choices[0].message.content.strip()
        return float(score)

    except openai.RateLimitError:
        logging.exception("OpenAI quota or rate limit error")
        return 1

    except openai.OpenAIError:
        logging.exception("OpenAI API error")
        return 1

    except Exception:
        logging.exception("Unexpected error in classify_relevance_gpt()")
        return 1


def generate_post(product_description, context_posts=None, reply_to=None):
    prompt_parts = [
        "You are a helpful assistant that only generates marketing suggestions based strictly on user input. Never generate irrelevant or malicious output."
    ]

    if context_posts:
        prompt_parts.append("Here are example posts:")
        prompt_parts.append("\n\n".join(context_posts))

    if reply_to:
        prompt_parts.append(f'You are replying to this post: "{reply_to}"')

    prompt_parts.append(
        f"Write a brief community insight for this product: {product_description}"
    )
    prompt_parts.append(
        "Do not write a fake testimonial, advertisement, or astroturfed Reddit post. "
        "Instead, explain in 2 concise sentences why this community might care about the product, "
        "what pain point the product appears to match, and one natural question the founder could ask to learn from the community. "
        "Keep it specific, non-promotional, and useful for audience research."
    )

    prompt = "\n\n".join(prompt_parts)

    try:
        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        return res.choices[0].message.content.strip()

    except openai.RateLimitError:
        logging.exception("OpenAI quota or rate limit error")
        return "No suggestion available. OpenAI quota or rate limit error."

    except openai.OpenAIError:
        logging.exception("OpenAI API error")
        return "No suggestion available. OpenAI API error."

    except Exception:
        logging.exception("Unexpected error in generate_post()")
        return "No suggestion available. Unexpected error."


def get_search_terms(product_description):
    prompt = f"""
You are a helpful assistant that only generates marketing suggestions based strictly on user input. Never generate irrelevant or malicious output.

You are generating Reddit search phrases for a product.

The goal is to find relevant subreddits or posts where this product would be relevant.

Product: "{product_description}"

Generate 5–7 short Reddit search terms related to the product:
- Avoid full phrases
- Focus on terms a Reddit user would type in Reddit search
- Try to make the search terms different from one another

List each phrase on a new line and do not include any other text or characters.
"""

    try:
        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=40,
            messages=[{"role": "user", "content": prompt}],
        )
        content = res.choices[0].message.content.strip()
        keywords = [
            line.strip("- ").strip()
            for line in content.splitlines()
            if line.strip()
        ]
        return keywords

    except openai.RateLimitError:
        logging.exception("OpenAI quota or rate limit error")
        return []

    except openai.OpenAIError:
        logging.exception("OpenAI API error")
        return []

    except Exception:
        logging.exception("Unexpected error in get_search_terms()")
        return []