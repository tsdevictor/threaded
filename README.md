# Threaded

Threaded is a Reddit audience-research tool for discovering communities where potential users are already discussing problems related to a product idea.

Given a short product description, Threaded generates Reddit-style search terms, searches for relevant subreddits and posts, ranks communities by relevance and engagement signals, and surfaces community insights that help founders understand where their product may fit naturally.

The goal is not to automate posting or spam communities. Threaded is designed to help builders identify relevant conversations, understand user pain points, and engage thoughtfully.

## Demo

![Threaded ranking relevant Reddit communities for a sample pickup-sports app](screenshots/threaded-demo.png)

## Features

- Generates Reddit search terms from a product description
- Searches Reddit for relevant subreddits and posts using PRAW
- Ranks communities using relevance, engagement, recency, and receptiveness signals
- Uses GPT to classify post relevance and generate community insights
- Provides a lightweight Flask web interface for exploring results
- Includes CSRF protection, input sanitization, rate limiting, and environment-based secret management

## Example input

```text
A mobile app that helps college students find last-minute pickup soccer, basketball, and volleyball games near campus. Users can post games, see who is joining, and get notified when enough people are nearby to play.
```

## Tech stack

- Python
- Flask
- PRAW
- OpenAI API
- NumPy
- scikit-learn
- python-dotenv
- HTML/CSS/JavaScript

## How it works

1. The user enters a product description.
2. GPT generates short Reddit-style search terms related to the product.
3. The backend searches Reddit for matching subreddits and posts.
4. Posts and communities are scored using relevance, engagement, recency, and tone/receptiveness signals.
5. The app displays ranked subreddit recommendations and community insights.

## Setup

Clone the repository:

```bash
git clone https://github.com/tsdevictor/threaded.git
cd threaded
```

Create and activate a virtual environment:

```bash
python3.12 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

Add your API credentials to `.env`.

Run the app:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Environment variables

Create a `.env` file using `.env.example` as a template.

Required variables:

```env
OPENAI_API_KEY=your_openai_api_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=threaded/0.1 by your_username
```

Do not commit your real `.env` file. The committed `.env.example` file should contain only placeholder values.

## Project structure

```text
threaded/
  core/          GPT and relevance-scoring logic
  services/      subreddit and post-processing logic
  routes/        Flask routes
  static/        frontend JavaScript and CSS
  templates/     HTML templates
  screenshots/   demo screenshots
```

## Notes

Threaded is intended for audience research and market validation, not automated promotion. Any generated insight should be reviewed by a human before engaging with a Reddit community.

The app currently uses local Flask development settings and in-memory rate limiting. It is not configured for production deployment.