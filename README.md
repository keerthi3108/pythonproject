# AI Study Question Generator (StudyAI)

A modern SaaS-style web app built with **Python** and **Streamlit**. Generate MCQs, short-answer questions, and True/False items on any topic—with explanations and export tools.

**No API key required** — works fully offline by default. Optional OpenAI integration if you add a key.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)

## Features

- **Authentication** — Login, signup, logout; users stored in `users.json`; duplicate usernames blocked
- **Dashboard** — Topic, difficulty (Easy / Medium / Hard), question count, question type
- **Offline generator** — Built-in question banks (Python, math, science, history) + smart templates
- **Optional OpenAI** — Enable in sidebar if you add an API key
- **UI** — Dark theme, cards, sidebar profile, loading animation, success/error messages
- **Extras** — Copy all, download TXT, clear results, session topic history, saved generations

## Project structure

```
study-ai/
├── app.py              # Entry point
├── auth.py             # Login / signup / users.json
├── components.py       # UI components (navbar, cards, forms)
├── local_generator.py  # Offline question engine (default)
├── utils.py            # Optional OpenAI API + export helpers
├── ui_styles.py        # Global CSS theme
├── users.json          # User database
├── .env                # Local API key (not committed)
├── .env.example        # Sample env file
├── requirements.txt
├── .streamlit/config.toml
└── README.md
```

## Quick start (local)

### 1. Prerequisites

- Python 3.9 or newer
- No API key needed (optional [OpenAI key](https://platform.openai.com/api-keys) for AI mode)

### 2. Install dependencies

```bash
cd study-ai
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

### Demo account

| Username | Password |
|----------|----------|
| `demo`   | `demo123` |

You can also register a new account from the **Sign Up** tab.

## Deploy on Streamlit Cloud

1. Push this folder to a GitHub repository (root = `study-ai` or set **Main file path** to `study-ai/app.py`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app.
3. Set **Main file path** to `app.py` (if the repo root is `study-ai`).
4. Under **Secrets**, add:

```toml
OPENAI_API_KEY = "sk-your-actual-key-here"
OPENAI_MODEL = "gpt-4o-mini"
```

5. Deploy. Streamlit Cloud loads secrets as environment variables automatically.

**Note:** Commit `users.json` with at least `{"users": {}}` so signups work on Cloud. User data persists only if the app has writable storage; for production, use a real database.

## Environment variables

| Variable       | Required | Description                          |
|----------------|----------|--------------------------------------|
| `OPENAI_API_KEY` | Yes      | Your OpenAI API key                     |
| `OPENAI_MODEL`   | No       | Model id (default: `gpt-4o-mini`)       |

## How it works

1. User signs up or logs in (`auth.py` + `users.json`).
2. On the dashboard, they choose topic, difficulty, count, and type.
3. `utils.py` calls `https://api.openai.com/v1/chat/completions` with a structured JSON prompt.
4. Results render as cards; users can copy, download, or revisit **Saved (session)**.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Invalid API key | Check `.env` or Streamlit Secrets |
| Rate limit | Wait and retry with fewer questions |
| JSON parse error | Click **Generate** again |
| `st.copy_button` error | Upgrade Streamlit: `pip install -U streamlit` |

## License

MIT — use freely for learning and projects.
