# Threaded

Threaded is a GPT-powered tool that helps you find the best subreddits to subtly promote your product. It analyzes Reddit in real time, ranks communities by relevance, engagement, and tone, and suggests authentic post ideas tailored to each subreddit.

## Features

- Keyword extraction and Reddit search using GPT
- Subreddit and post ranking by relevance, recency, and receptiveness
- AI-generated post suggestions that match subreddit tone
- Chat-style frontend with live result streaming and cancel button
- Secure backend with CSRF/XSS protection and secret management

## Tech Stack

- Flask (Python backend)
- OpenAI GPT-4 (language model)
- PRAW (Reddit API wrapper)
- Vanilla JavaScript, HTML, and CSS (frontend)
- NumPy and scikit-learn (ranking and vector math)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/tsdevictor/threaded.git
   cd threaded
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your OpenAI key:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

5. Run the Flask app:
   ```bash
   python app.py
   ```

## License

This project is open source and available under the MIT License.
