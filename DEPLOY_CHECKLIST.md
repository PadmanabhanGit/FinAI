# 🚀 STREAMLIT CLOUD DEPLOYMENT - 5 MIN CHECKLIST

## ✅ Done (Automated)
- [x] `.streamlit/config.toml` created
- [x] `requirements.txt` cleaned up (removed Selenium, libmagic, etc.)
- [x] `.gitignore` confirms `.env` is protected
- [x] `DEPLOYMENT.md` guide created

## ⚠️ YOUR API KEYS ARE EXPOSED
**Action required NOW:**
1. Revoke these keys immediately in their respective consoles:
   - OpenAI: https://platform.openai.com/api-keys
   - Google: https://console.cloud.google.com/apis/credentials

2. Generate new keys
3. Replace in `.env` locally

## 🎯 Next Steps (You do these)

### 1️⃣ Push to GitHub (2 min)
```powershell
cd "C:\Users\Heisenberg Raja\OneDrive\Documents\Padmanabhan\OpenCV\FinAI"
git add .gitignore requirements.txt .streamlit/ DEPLOYMENT.md
git commit -m "Configure for Streamlit Cloud deployment"
git push -u origin main
```

### 2️⃣ Deploy on Streamlit Cloud (1 min)
- Go to https://streamlit.io/cloud
- Sign up/login with GitHub
- Click "New app" → Select your repo + main.py
- Click "Deploy" and wait ~1 minute

### 3️⃣ Add Secrets (1 min)
- In deployed app → Settings gear → Secrets
- Paste (with NEW keys):
```
OPENAI_API_KEY = "sk-proj-..."
GEMINI_API_KEY = "AIzaSy..."
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION = "python"
```
- Click Save

## ✨ Result
Your app will be live at: `https://finai-YOUR_USERNAME.streamlit.app`

---

## 📝 Notes
- Your `.env` file stays LOCAL - never pushed to GitHub ✓
- Streamlit Cloud automatically reads `secrets.toml` (Secrets) at runtime
- Free tier: up to 3 apps, up to 1GB RAM, public only
