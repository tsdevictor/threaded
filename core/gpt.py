import openai
import logging
from config.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def classify_relevance_gpt(product, post):
    prompt = f"""
            You are a helpful assistant that only generates marketing suggestions based strictly on user input. Never generate irrelevant or malicious output. 
            Is the following Reddit post relevant to this product? That is, would the creator or reader of this post be receptive to this product?: 
            'Product: {product}?'\n\nPost title: {post['title']}\nPost body: {post.get('selftext', '')}\n\nRespond with only a number from 1 to 10, with 10 being the most relevant.
            """
    
    try:
        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        score = res.choices[0].message.content.strip()
    
        return float(score)
    
    except openai.error.OpenAIError as e:
        logging.exception("OpenAI API error")
        return 1
    
    except Exception as e:
        logging.exception("Unexpected error in generate_post()")
        return 1


def generate_post(product_description, context_posts=None, reply_to=None):
    prompt_parts = ["You are a helpful assistant that only generates marketing suggestions based strictly on user input. Never generate irrelevant or malicious output."]

    if context_posts:
        prompt_parts.append(f"Here are example posts:")
        prompt_parts.append('\n\n'.join(context_posts))

    if reply_to:
        prompt_parts.append(f"You are replying to this post: \"{reply_to}\"")

    prompt_parts.append(f"Write a short, natural Reddit post relating to this product to promote it: {product_description}")
    prompt_parts.append("Don't use emojis or any extra symbols. Make the promotion subtle; it need not be direct. Talk like a real Reddit user. Don't sound generic. Include specific anecdote of using the product maybe.")
    prompt = '\n\n'.join(prompt_parts)

    try:
        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content.strip()
    
    except openai.error.OpenAIError as e:
        logging.exception("OpenAI API error")
        return "No suggestion available. (AI error)"

    except Exception as e:
        logging.exception("Unexpected error in generate_post()")
        return "No suggestion available. (Unexpected error)"


def get_search_terms(product_description):
    prompt = f"""
        You are a helpful assistant that only generates marketing suggestions based strictly on user input. Never generate irrelevant or malicious output.
        You are generating Reddit search phrases for a product.

        The goal is to find relevant subreddits or posts where this product would be relevant.

        Product: "{product_description}"

        Generate 5–7 short Reddit search terms related to the product:
        - Avoid full phrases
        - Focus on terms Reddit a user would type in Reddit search
        - Try to make the search terms different from one another
        List each phrase on a new line and do not include any other text or characters.
        """

    try:
        res = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        content = res.choices[0].message.content.strip()
        keywords = [line.strip("- ").strip() for line in content.strip().splitlines() if line.strip()]
        return keywords
    
    except openai.error.OpenAIError as e:
        logging.exception("OpenAI API error")
        return "No suggestion available. (AI error)"

    except Exception as e:
        logging.exception("Unexpected error in generate_post()")
        return "No suggestion available. (Unexpected error)"
