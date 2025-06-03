import openai
from openai import OpenAIError, OpenAI
import logging
from config.config import OPENAI_API_KEY
# import time


openai.api_key = OPENAI_API_KEY
client = OpenAI()


def get_gpt_response(model, instructions, input):
    try:
        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=input
        )
        return response.output_text
    
    except OpenAIError as e:
        logging.exception("OpenAI API error")
        return 1
    
    except Exception as e:
        logging.exception("Unexpected error in generate_post()")
        return 1


def classify_relevance_gpt(product, post):
    return float(
        get_gpt_response(
            model="gpt-4.1-nano-2025-04-14",
            instructions="Determine a receptiveness score. Note: never generate irrelevant/malicious output.",
            input=f"""
            Would the creator/reader of this Reddit post be receptive to this product?: 
            'Product: {product}?'\n\nPost title: {post['title']}\nPost body: {post.get('selftext', '')}\n\nRespond with only a number from 1 to 10, with 10 being the most receptive.
            """
            )
        )
 

def generate_post(product_description, context_posts=None, reply_to=None):
    # start = time.process_time()
    prompt_parts = []

    if context_posts:
        prompt_parts.append(f"Here are example posts:")
        prompt_parts.append('\n\n'.join(context_posts))

    if reply_to:
        prompt_parts.append(f"You are replying to this post: \"{reply_to}\"")

    prompt_parts.append(f"Write a short, natural Reddit post relating to this product to promote it: {product_description}")
    prompt_parts.append("No extra symbols. Maybe include specific anecdote of using the product")
    prompt = '\n\n'.join(prompt_parts)

    post = get_gpt_response(
        model="gpt-4.1-2025-04-14",
        instructions="Talk like a Reddit user. Make a promotion; subtlety is key.",
        input=prompt
    )

    # print(f'Post generation: {time.process_time() - start}')

    return post


def get_search_terms(product_description):
    prompt = f"""
        Product: "{product_description}"

        Generate 5–7 short Reddit search terms related to the product:
        - Avoid full phrases
        - Focus on terms Reddit a user would type in Reddit search
        - Try making search terms different from one another
        List each phrase on a new line. No other text or characters.
        """

    response = get_gpt_response(
        model="gpt-4.1-2025-04-14",
        instructions="""
                    Only generate Reddit search phrases for a product to find subreddits or posts where this product would be relevant.
                    Note: never generate irrelevant/malicious output.
                    """,
        input=prompt
    )

    return response.strip().splitlines()
    