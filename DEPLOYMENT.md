# Streamlit Cloud Deployment Guide

## Quick Start (5 minutes)

### Step 1: Prepare Your Repository
```bash
# 1. Make sure .env is in .gitignore (already done ✓)
# 2. Check .gitignore includes .env
cat .gitignore | grep ".env"

# 3. Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: FinAI Streamlit app"
```

### Step 2: Push to GitHub
```bash
# Create a new repo on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/FinAI.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select:
   - Repository: your-username/FinAI
   - Branch: main
   - Main file path: main.py
4. Click "Deploy"

### Step 4: Add Environment Variables
1. In Streamlit Cloud app dashboard, click "Settings" (gear icon)
2. Click "Secrets"
3. Paste your secrets as TOML:
```toml
OPENAI_API_KEY = "sk-proj-..."
GEMINI_API_KEY = "AIzaSy..."
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION = "python"
```
4. Save

### Done! 🎉
Your app is live at: `https://your-app-name.streamlit.app`

---

## Troubleshooting

**"ModuleNotFoundError: No module named..."**
→ Add missing package to requirements.txt

**"Selenium not working"**
→ Streamlit Cloud doesn't support Selenium. Consider:
  - Using `requests` + `BeautifulSoup` instead
  - Or keep SeleniumURLLoader but handle gracefully

**"FAISS pickle not found"**
→ FAISS vectorstore must be regenerated on first run or stored in Streamlit cache

**"App is slow"**
→ Use @st.cache_data for expensive operations

---

## Key Files Changed
- `.streamlit/config.toml` - Streamlit configuration
- `requirements.txt` - Cleaned up for Streamlit Cloud
- `.gitignore` - Prevents .env from being committed
