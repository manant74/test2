# VibeTheForce - Luke era un VibeCoder?

Un'applicazione web interattiva per raccogliere feedback dal pubblico durante una conference sul VibeCoding utilizzando una scala di valutazione a tema Star Wars.

## 🚀 Caratteristiche

- **Votazione interattiva**: Scala da 1 a 5 stelle con tematiche Star Wars
- **Commenti opzionali**: I partecipanti possono lasciare feedback testuale (max 500 caratteri)
- **Dashboard tempo reale**: Visualizzazione live dei risultati con grafici Plotly
- **Analisi AI**: Commento automatico generato da Google Gemini quando ci sono ≥10 voti
- **Tema Star Wars**: Design immersivo con colori e animazioni a tema
- **QR Code**: Accesso facile tramite scansione QR Code
- **Admin Panel**: Gestione e reset dei voti

## 📁 Struttura Progetto

```
vibetheforce/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml.example # Example secrets file
├── database/
│   ├── db_manager.py        # Database operations
│   └── schema.sql           # Database schema
├── services/
│   ├── vote_service.py      # Voting logic
│   ├── analytics_service.py # LLM analytics
│   └── gemini_client.py     # Gemini API client
├── pages/
│   ├── 1_🗳️_Vota.py         # Voting page
│   ├── 2_📊_Risultati.py    # Results dashboard
│   └── 3_⚙️_Admin.py        # Admin panel
├── utils/
│   ├── theme.py             # Star Wars theme
│   └── qr_generator.py      # QR code generation
└── README.md
```

## 🛠️ Tecnologie

- **Framework**: Streamlit (Python)
- **Database**: SQLite3
- **LLM**: Google Gemini API
- **Visualizzazione**: Plotly
- **Deploy**: Streamlit Cloud

## 📦 Installazione Locale

1. **Clona il repository**
   ```bash
   git clone <repository-url>
   cd vibetheforce
   ```

2. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura i secrets**
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
   Modifica `.streamlit/secrets.toml` e aggiungi la tua Gemini API key:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key"
   ```
   
   Ottieni la tua API key da: https://makersuite.google.com/app/apikey

4. **Avvia l'applicazione**
   ```bash
   streamlit run app.py
   ```

5. **Apri il browser**
   L'app sarà disponibile su `http://localhost:8501`

## ☁️ Deploy su Streamlit Cloud

### Prerequisiti
- Account GitHub
- Account Streamlit Cloud (gratuito)
- Google Gemini API key

### Passaggi per il Deploy

1. **Prepara il repository GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Connetti a Streamlit Cloud**
   - Vai su [share.streamlit.io](https://share.streamlit.io)
   - Clicca "New app"
   - Seleziona il tuo repository GitHub
   - Branch: `main`
   - Main file path: `app.py`

3. **Configura i Secrets**
   - Nella dashboard dell'app, vai su "Settings" → "Secrets"
   - Aggiungi il seguente contenuto:
     ```toml
     GEMINI_API_KEY = "your-actual-gemini-api-key"
     ```

4. **Deploy**
   - Clicca "Deploy!"
   - L'app sarà disponibile su `https://<your-app-name>.streamlit.app`

5. **Verifica**
   - Testa che il caricamento sia < 3 secondi
   - Verifica che la votazione funzioni
   - Controlla che l'analisi LLM si attivi con ≥10 voti

### Aggiornamenti Automatici
Streamlit Cloud si aggiorna automaticamente ad ogni push su GitHub!

## 📱 QR Code

L'applicazione genera automaticamente un QR Code per facilitare l'accesso:

- Disponibile nella home page e nella pagina Admin
- Colori personalizzati Star Wars (tema Imperial: nero su bianco)
- Ideale per proiettare durante la conference
- I partecipanti possono scansionare per votare istantaneamente

### Configurazione URL per QR Code

Per il deployment su Streamlit Cloud, configura l'URL corretto:

1. Crea il file `.streamlit/secrets.toml`:
```toml
APP_URL = "https://your-app-name.streamlit.app"
```

2. Oppure imposta la variabile d'ambiente `APP_URL`

3. Il QR Code punterà automaticamente all'URL corretto

## 🎨 Scala di Valutazione Star Wars

- 1 ⭐ - "Youngling" (Grigio)
- 2 ⭐⭐ - "Padawan" (Blu)
- 3 ⭐⭐⭐ - "Cavaliere Jedi" (Verde)
- 4 ⭐⭐⭐⭐ - "Maestro Jedi" (Viola)
- 5 ⭐⭐⭐⭐⭐ - "Gran Maestro" (Oro)

## 🔒 Sicurezza

- **Prevenzione voti multipli**: Tramite session_state di Streamlit
- **Validazione input**: CHECK constraints in SQLite
- **API key protetta**: Gestita tramite Streamlit secrets
- **SQL injection**: Prevenuta con parametrized queries

## 📊 Funzionalità Admin

Accedi alla pagina Admin per:
- Visualizzare statistiche dettagliate
- Generare QR Code per l'app
- Reset completo dei voti e commenti
- Monitorare timestamp ultimo voto

## 🤖 Analisi LLM

Quando ci sono almeno 10 voti, Google Gemini genera automaticamente:
- Sentiment generale (positivo/negativo/misto)
- Pattern interessanti nella distribuzione
- Osservazioni statistiche significative
- Commento in italiano di 3-4 frasi a tema Star Wars

L'analisi si aggiorna ogni 30 secondi con nuovi voti.

## 📝 Licenza

Questo progetto è stato creato per la conference sul VibeCoding.

## 🌟 May the Force be with you!