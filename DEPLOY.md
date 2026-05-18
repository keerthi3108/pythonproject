# Deploy StudyAI to Streamlit Cloud (no API key)

## 1. Push to GitHub

```bash
cd study-ai
git init
git add .
git commit -m "StudyAI offline deploy"
```

Create a repo on GitHub, then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/study-ai.git
git branch -M main
git push -u origin main
```

**Do not commit `.env`** — it is in `.gitignore`.

## 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **New app**
4. Select your repository
5. **Main file path:** `app.py` (if repo root is `study-ai`, use `study-ai/app.py` if repo is parent folder)
6. **Secrets:** leave empty (not required)
7. Click **Deploy**

## 3. After deploy

- Demo login: `demo` / `demo123`
- Or sign up a new account
- No API key or billing needed

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```
