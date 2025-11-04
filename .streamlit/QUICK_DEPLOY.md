# ⚡ Quick Deploy Reference - VibeTheForce

## 🚀 Deploy in 5 Minuti

### 1. GitHub Setup
```bash
git init
git add .
git commit -m "Deploy VibeTheForce"
git remote add origin https://github.com/YOUR_USERNAME/vibetheforce.git
git push -u origin main
```

### 2. Streamlit Cloud
1. Vai su https://share.streamlit.io
2. New app → Seleziona repository → `app.py`
3. Deploy!

### 3. Configure Secrets
Settings → Secrets:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

### 4. Get Gemini API Key
https://makersuite.google.com/app/apikey

## ✅ Verification Checklist
- [ ] App loads in < 3 seconds
- [ ] Voting works
- [ ] Results dashboard updates
- [ ] LLM analysis works (≥10 votes)
- [ ] QR code generates
- [ ] Admin panel accessible

## 🔗 Important URLs
- **Streamlit Cloud**: https://share.streamlit.io
- **Gemini API**: https://makersuite.google.com/app/apikey
- **Docs**: https://docs.streamlit.io

## 📝 Files Checklist
- [x] `requirements.txt` - Dependencies
- [x] `.streamlit/config.toml` - Theme config
- [x] `.streamlit/secrets.toml.example` - Secrets template
- [x] `.python-version` - Python 3.11
- [x] `app.py` - Main entry point
- [x] All services and pages implemented

## 🆘 Quick Fixes

**App won't start?**
→ Check logs for missing dependencies

**Gemini not working?**
→ Verify GEMINI_API_KEY in Secrets

**Database resets?**
→ Normal on redeploy, data persists otherwise

**Slow loading?**
→ Use @st.cache_data for heavy operations

---

**Full instructions**: See `DEPLOY_INSTRUCTIONS.md`
