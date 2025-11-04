# Deployment Checklist - VibeTheForce

## Pre-Deployment Checklist

### ✅ Configurazione Locale
- [ ] File `requirements.txt` completo con tutte le dipendenze
- [ ] File `.streamlit/config.toml` configurato con tema Star Wars
- [ ] File `.streamlit/secrets.toml.example` creato per documentazione
- [ ] File `.gitignore` esclude `votes.db` e `.streamlit/secrets.toml`
- [ ] File `.python-version` specifica Python 3.11
- [ ] Database schema (`database/schema.sql`) definito correttamente
- [ ] Tutti i servizi implementati (vote_service, analytics_service, gemini_client)
- [ ] Tutte le pagine Streamlit create (Vota, Risultati, Admin)
- [ ] Tema Star Wars applicato (`utils/theme.py`)
- [ ] QR Code generator implementato (`utils/qr_generator.py`)

### ✅ Test Locale
- [ ] App si avvia correttamente con `streamlit run app.py`
- [ ] Pagina di votazione funziona (5 opzioni + commento opzionale)
- [ ] Prevenzione voti multipli funziona (session_state)
- [ ] Dashboard risultati si aggiorna in tempo reale
- [ ] Analisi LLM si attiva con ≥10 voti (richiede Gemini API key)
- [ ] Admin panel permette reset voti
- [ ] QR Code viene generato correttamente
- [ ] Tema Star Wars applicato correttamente
- [ ] Database SQLite persiste i dati tra sessioni

## Deployment su Streamlit Cloud

### Step 1: Preparazione Repository GitHub

```bash
# Inizializza repository (se non già fatto)
git init

# Aggiungi tutti i file
git add .

# Commit iniziale
git commit -m "Deploy VibeTheForce to Streamlit Cloud"

# Aggiungi remote GitHub
git remote add origin https://github.com/YOUR_USERNAME/vibetheforce.git

# Push su GitHub
git push -u origin main
```

### Step 2: Connessione a Streamlit Cloud

1. Vai su [share.streamlit.io](https://share.streamlit.io)
2. Fai login con GitHub
3. Clicca "New app"
4. Seleziona:
   - **Repository**: `YOUR_USERNAME/vibetheforce`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Clicca "Advanced settings" (opzionale)
   - Python version: `3.11`

### Step 3: Configurazione Secrets

1. Nella dashboard dell'app, vai su **Settings** → **Secrets**
2. Aggiungi il seguente contenuto:

```toml
GEMINI_API_KEY = "your-actual-gemini-api-key-here"
```

3. Salva i secrets

**Come ottenere la Gemini API key:**
- Vai su https://makersuite.google.com/app/apikey
- Crea un nuovo progetto (se necessario)
- Genera una nuova API key
- Copia la key e incollala nei secrets di Streamlit Cloud

### Step 4: Deploy

1. Clicca **"Deploy!"**
2. Attendi il completamento del deploy (2-3 minuti)
3. L'app sarà disponibile su: `https://YOUR_APP_NAME.streamlit.app`

### Step 5: Verifica Post-Deploy

- [ ] App si carica in < 3 secondi
- [ ] Pagina di votazione è accessibile e funzionante
- [ ] Dashboard risultati mostra dati in tempo reale
- [ ] Analisi LLM funziona (testa con ≥10 voti)
- [ ] Admin panel è accessibile
- [ ] QR Code viene generato con URL corretto
- [ ] Tema Star Wars è applicato correttamente
- [ ] Database persiste i dati tra riavvii
- [ ] Nessun errore nei logs

## Monitoraggio e Manutenzione

### Logs
- Accedi ai logs dalla dashboard Streamlit Cloud
- Monitora errori e performance
- Controlla utilizzo risorse

### Aggiornamenti
```bash
# Fai modifiche al codice
git add .
git commit -m "Update: descrizione modifiche"
git push

# Streamlit Cloud si aggiorna automaticamente!
```

### Backup Database
Il database SQLite (`votes.db`) è persistente su Streamlit Cloud, ma considera:
- Export periodico dei dati per backup
- Implementa funzione di export CSV nella pagina Admin (opzionale)

### Limiti Streamlit Cloud (Piano Gratuito)
- **Risorse**: 1 GB RAM, 1 CPU core
- **Uptime**: App va in sleep dopo inattività
- **Riavvio**: ~30 secondi per riattivazione
- **Storage**: Persistente ma limitato

## Troubleshooting

### Problema: App non si avvia
**Soluzione:**
- Verifica che `requirements.txt` sia corretto
- Controlla i logs per errori di import
- Verifica che `.python-version` sia `3.11`

### Problema: Gemini API non funziona
**Soluzione:**
- Verifica che `GEMINI_API_KEY` sia configurata nei secrets
- Controlla che la key sia valida su https://makersuite.google.com
- Verifica i logs per errori API

### Problema: Database non persiste
**Soluzione:**
- Verifica che `votes.db` non sia in `.gitignore` per deploy
- Streamlit Cloud gestisce automaticamente la persistenza
- Controlla che `db_manager.py` crei il database correttamente

### Problema: Tempo di caricamento > 3 secondi
**Soluzione:**
- Ottimizza import (usa `@st.cache_data` e `@st.cache_resource`)
- Riduci dimensione dipendenze se possibile
- Verifica connessione Gemini API (timeout 30s)

## URL Utili

- **Streamlit Cloud Dashboard**: https://share.streamlit.io
- **Documentazione Streamlit**: https://docs.streamlit.io
- **Google Gemini API**: https://makersuite.google.com
- **Streamlit Community**: https://discuss.streamlit.io

## Contatti e Supporto

Per problemi o domande:
1. Controlla i logs su Streamlit Cloud
2. Consulta la documentazione Streamlit
3. Verifica la configurazione secrets
4. Testa localmente prima di fare push

---

**May the Force be with your deployment! 🌟**
