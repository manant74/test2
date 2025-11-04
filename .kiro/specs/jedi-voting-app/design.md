# Documento di Design - VibeTheForce

## Panoramica

VibeTheForce è una Single Page Application (SPA) che implementa un sistema di votazione interattivo a tema Star Wars per conference. L'applicazione utilizza JavaScript vanilla, HTML5 e CSS3 per garantire semplicità, performance e deployment immediato su Netlify senza dipendenze esterne.

## Architettura

### Stack Tecnologico
- **Framework**: Streamlit (Python)
- **Database**: SQLite3
- **LLM Integration**: Google Gemini API per analisi commenti e statistiche
- **Styling**: Streamlit custom CSS + markdown
- **Deploy**: Streamlit Cloud (gratuito)
- **QR Code**: libreria Python `qrcode`

### Architettura Streamlit
```
┌─────────────────────────────────────────────────┐
│           Streamlit Cloud                       │
│  ┌──────────────────────────────────────────┐  │
│  │  Streamlit App (app.py)                  │  │
│  │  ├─ Voting Page                          │  │
│  │  ├─ Results Dashboard                    │  │
│  │  └─ Admin Panel                          │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │  SQLite Database (votes.db)              │  │
│  │  ├─ votes table                          │  │
│  │  └─ comments table                       │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │  Google Gemini API                       │  │
│  │  └─ Analisi commenti e insights          │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Struttura Progetto
```
vibetheforce/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
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

### Componenti Principali

1. **Voting Interface**: Interfaccia utente per la votazione con campo commento opzionale
2. **Results Dashboard**: Dashboard per visualizzare i risultati in tempo reale e statistiche LLM
3. **Vote Manager**: Gestione logica dei voti, commenti e persistenza
4. **LLM Analytics Engine**: Analisi automatica dei commenti e generazione insights
5. **Theme Engine**: Sistema per applicare il tema Star Wars
6. **QR Code Integration**: Gestione dell'accesso tramite QR Code

## Componenti e Interfacce

### 1. Voting Interface Component (Streamlit Page)

**Responsabilità:**
- Visualizzare le 5 opzioni di voto a tema Star Wars
- Campo textarea per commento opzionale (max 500 caratteri)
- Gestire l'interazione utente
- Fornire feedback visivo con st.success/st.error
- Prevenire voti multipli tramite session_state

**Implementazione Python (pages/1_🗳️_Vota.py):**
```python
import streamlit as st
from services.vote_service import VoteService

def render_voting_page():
    st.title("🌟 VibeTheForce - Vota!")
    st.subheader("Luke era un VibeCoder?")
    
    # Check if user already voted
    if st.session_state.get('has_voted', False):
        st.success("✅ Hai già votato! Grazie per il tuo feedback.")
        return
    
    # Voting buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    ratings = {
        1: ("⭐", "Youngling", col1),
        2: ("⭐⭐", "Padawan", col2),
        3: ("⭐⭐⭐", "Cavaliere Jedi", col3),
        4: ("⭐⭐⭐⭐", "Maestro Jedi", col4),
        5: ("⭐⭐⭐⭐⭐", "Gran Maestro", col5)
    }
    
    selected_rating = None
    for rating, (stars, label, col) in ratings.items():
        with col:
            if st.button(f"{stars}\n{label}", key=f"vote_{rating}", use_container_width=True):
                selected_rating = rating
    
    # Optional comment
    comment = st.text_area(
        "💬 Commento opzionale (max 500 caratteri)",
        max_chars=500,
        placeholder="Condividi il tuo feedback..."
    )
    
    # Submit vote
    if selected_rating:
        vote_service = VoteService()
        success = vote_service.submit_vote(selected_rating, comment)
        
        if success:
            st.session_state.has_voted = True
            st.balloons()
            st.success(f"🎉 Voto registrato: {ratings[selected_rating][0]} {ratings[selected_rating][1]}")
            st.rerun()
```

**Scala di Valutazione Star Wars:**
- 1 ⭐ - "Youngling" (Colore: Grigio)
- 2 ⭐⭐ - "Padawan" (Colore: Blu)
- 3 ⭐⭐⭐ - "Cavaliere Jedi" (Colore: Verde)
- 4 ⭐⭐⭐⭐ - "Maestro Jedi" (Colore: Viola)
- 5 ⭐⭐⭐⭐⭐ - "Gran Maestro" (Colore: Oro)

### 2. Results Dashboard Component (Streamlit Page)

**Responsabilità:**
- Visualizzare conteggi in tempo reale con auto-refresh
- Calcolare e mostrare statistiche
- Mostrare insights LLM quando disponibili (≥10 voti)
- Fornire visualizzazione ottimizzata per proiezione

**Implementazione Python (pages/2_📊_Risultati.py):**
```python
import streamlit as st
import pandas as pd
import plotly.express as px
from services.vote_service import VoteService
from services.analytics_service import AnalyticsService

def render_results_page():
    st.title("📊 Risultati in Tempo Reale")
    
    # Auto-refresh every 2 seconds
    st_autorefresh = st.empty()
    
    vote_service = VoteService()
    results = vote_service.get_results()
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Totale Voti", results['total_votes'])
    with col2:
        st.metric("Media", f"{results['average_rating']:.2f} ⭐")
    with col3:
        st.metric("Commenti", results['total_comments'])
    
    # Vote distribution chart
    df = pd.DataFrame({
        'Rating': ['⭐ Youngling', '⭐⭐ Padawan', '⭐⭐⭐ Cavaliere', 
                   '⭐⭐⭐⭐ Maestro', '⭐⭐⭐⭐⭐ Gran Maestro'],
        'Voti': [results['votes'][i] for i in range(1, 6)]
    })
    
    fig = px.bar(df, x='Rating', y='Voti', 
                 title='Distribuzione Voti',
                 color='Voti',
                 color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    # LLM Automatic Comment (if >= 10 votes)
    if results['total_votes'] >= 10:
        st.subheader("🤖 Commento Automatico (Gemini AI)")
        analytics_service = AnalyticsService()
        auto_comment = analytics_service.generate_automatic_comment()
        
        if auto_comment:
            st.info(auto_comment)
    
    # Auto-refresh
    time.sleep(2)
    st.rerun()
```

### 3. Vote Service Component

**Responsabilità:**
- Gestire la persistenza dei voti in SQLite
- Salvare commenti opzionali
- Prevenire voti duplicati tramite session_state
- Fornire API per statistiche

**Implementazione Python (services/vote_service.py):**
```python
import sqlite3
from datetime import datetime
from typing import Optional, Dict
import streamlit as st

class VoteService:
    def __init__(self, db_path='votes.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                session_id TEXT NOT NULL UNIQUE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vote_id INTEGER NOT NULL,
                comment TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vote_id) REFERENCES votes(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def submit_vote(self, rating: int, comment: Optional[str] = None) -> bool:
        """Submit a vote with optional comment"""
        try:
            # Generate session ID
            if 'session_id' not in st.session_state:
                st.session_state.session_id = f"{datetime.now().timestamp()}"
            
            session_id = st.session_state.session_id
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert vote
            cursor.execute(
                'INSERT INTO votes (rating, session_id) VALUES (?, ?)',
                (rating, session_id)
            )
            vote_id = cursor.lastrowid
            
            # Insert comment if provided
            if comment and comment.strip():
                cursor.execute(
                    'INSERT INTO comments (vote_id, comment) VALUES (?, ?)',
                    (vote_id, comment.strip())
                )
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            # Session already voted
            return False
        except Exception as e:
            st.error(f"Errore: {e}")
            return False
    
    def get_results(self) -> Dict:
        """Get voting results and statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get vote counts
        cursor.execute('''
            SELECT rating, COUNT(*) as count
            FROM votes
            GROUP BY rating
        ''')
        vote_counts = {i: 0 for i in range(1, 6)}
        for rating, count in cursor.fetchall():
            vote_counts[rating] = count
        
        # Get total votes
        total_votes = sum(vote_counts.values())
        
        # Calculate average
        if total_votes > 0:
            weighted_sum = sum(rating * count for rating, count in vote_counts.items())
            average_rating = weighted_sum / total_votes
        else:
            average_rating = 0.0
        
        # Get comment count
        cursor.execute('SELECT COUNT(*) FROM comments')
        total_comments = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'votes': vote_counts,
            'total_votes': total_votes,
            'average_rating': average_rating,
            'total_comments': total_comments
        }
    
    def get_all_comments(self) -> list:
        """Get all comments for LLM analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.comment, v.rating, c.timestamp
            FROM comments c
            JOIN votes v ON c.vote_id = v.id
            ORDER BY c.timestamp DESC
        ''')
        
        comments = cursor.fetchall()
        conn.close()
        
        return comments
    
    def reset_votes(self):
        """Reset all votes and comments (admin function)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM comments')
        cursor.execute('DELETE FROM votes')
        
        conn.commit()
        conn.close()
```

### 4. LLM Analytics Engine Component

**Responsabilità:**
- Analizzare dati numerici di votazione con Google Gemini API
- Generare commento automatico descrittivo sui risultati
- Identificare pattern nella distribuzione dei voti
- Aggiornare commento ogni 30 secondi quando ci sono nuovi voti
- Presentare risultati in italiano con linguaggio naturale

**Implementazione Python (services/analytics_service.py):**
```python
import google.generativeai as genai
import streamlit as st
from services.vote_service import VoteService

class AnalyticsService:
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel('gemini-pro')
        self.vote_service = VoteService()
    
    def generate_automatic_comment(self) -> str:
        """Generate automatic comment on voting results using Gemini LLM"""
        results = self.vote_service.get_results()
        
        # Check minimum threshold
        if results['total_votes'] < 10:
            return ""
        
        # Prepare data for LLM
        vote_distribution = results['votes']
        
        # Calculate percentages
        percentages = {
            rating: (count / results['total_votes'] * 100) 
            for rating, count in vote_distribution.items()
        }
        
        # Create prompt for Gemini
        prompt = f"""
Analizza questi dati di votazione per una conference sul VibeCoding e genera un commento descrittivo in italiano.

Distribuzione voti (scala 1-5 stelle):
- 1 stella (Youngling): {vote_distribution[1]} voti ({percentages[1]:.1f}%)
- 2 stelle (Padawan): {vote_distribution[2]} voti ({percentages[2]:.1f}%)
- 3 stelle (Cavaliere Jedi): {vote_distribution[3]} voti ({percentages[3]:.1f}%)
- 4 stelle (Maestro Jedi): {vote_distribution[4]} voti ({percentages[4]:.1f}%)
- 5 stelle (Gran Maestro): {vote_distribution[5]} voti ({percentages[5]:.1f}%)

Totale voti: {results['total_votes']}
Media: {results['average_rating']:.2f} stelle

Genera un commento di esattamente 3-4 frasi in italiano che:
1. Descriva il sentiment generale (positivo/negativo/misto)
2. Identifichi il pattern più interessante nella distribuzione
3. Fornisca un'osservazione comparativa o statistica significativa

Usa un tono coinvolgente e a tema Star Wars quando appropriato. Rispondi SOLO con il testo del commento, senza titoli o formattazione.
"""
        
        try:
            response = self.model.generate_content(prompt)
            comment = response.text.strip()
            return comment
            
        except Exception as e:
            st.error(f"Errore nell'analisi LLM: {e}")
            return "Analisi temporaneamente non disponibile."
```

**Gemini Client (services/gemini_client.py):**
```python
import google.generativeai as genai
import streamlit as st

class GeminiClient:
    """Wrapper for Google Gemini API"""
    
    def __init__(self):
        self.api_key = st.secrets.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def is_configured(self) -> bool:
        """Check if Gemini API is properly configured"""
        return self.model is not None
    
    def generate_text(self, prompt: str) -> str:
        """Generate text using Gemini"""
        if not self.is_configured():
            raise ValueError("Gemini API not configured")
        
        response = self.model.generate_content(prompt)
        return response.text
```

### 5. Theme Engine Component

**Responsabilità:**
- Applicare stili Star Wars con Streamlit CSS
- Gestire colori e tipografia
- Fornire layout responsive
- Emoji e icone a tema

**Implementazione Python (utils/theme.py):**
```python
import streamlit as st

def apply_star_wars_theme():
    """Apply Star Wars theme to Streamlit app"""
    st.markdown("""
    <style>
    /* Star Wars Theme */
    .stApp {
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
    }
    
    .stButton>button {
        background-color: #FFE81F;
        color: #000000;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #FFD700;
        font-size: 18px;
        padding: 15px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px #FFE81F;
    }
    
    h1, h2, h3 {
        color: #FFE81F;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px #FFE81F;
    }
    
    .stMetric {
        background-color: rgba(255, 232, 31, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #FFE81F;
    }
    
    .stTextArea>div>div>textarea {
        background-color: rgba(0, 0, 0, 0.5);
        color: #FFE81F;
        border: 1px solid #FFE81F;
    }
    </style>
    """, unsafe_allow_html=True)

# Rating colors
RATING_COLORS = {
    1: "#808080",  # Grigio - Youngling
    2: "#0066CC",  # Blu - Padawan
    3: "#00FF00",  # Verde - Cavaliere Jedi
    4: "#8A2BE2",  # Viola - Maestro Jedi
    5: "#FFD700"   # Oro - Gran Maestro
}

RATING_LABELS = {
    1: "⭐ Youngling",
    2: "⭐⭐ Padawan",
    3: "⭐⭐⭐ Cavaliere Jedi",
    4: "⭐⭐⭐⭐ Maestro Jedi",
    5: "⭐⭐⭐⭐⭐ Gran Maestro"
}
```

## Modelli Dati

### SQLite Database Schema

**database/schema.sql:**
```sql
-- Votes table
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
    session_id TEXT NOT NULL UNIQUE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Comments table
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vote_id INTEGER NOT NULL,
    comment TEXT NOT NULL CHECK(LENGTH(comment) <= 500),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vote_id) REFERENCES votes(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_votes_rating ON votes(rating);
CREATE INDEX IF NOT EXISTS idx_votes_timestamp ON votes(timestamp);
CREATE INDEX IF NOT EXISTS idx_comments_vote_id ON comments(vote_id);
```

### Python Data Models

**Vote Model:**
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Vote:
    id: Optional[int]
    rating: int  # 1-5
    session_id: str
    timestamp: datetime
    comment: Optional[str] = None
```

**Results Model:**
```python
@dataclass
class VoteResults:
    votes: dict[int, int]  # {rating: count}
    total_votes: int
    average_rating: float
    total_comments: int
    distribution: dict[int, float]  # {rating: percentage}
```

**Analytics Model:**
```python
@dataclass
class AutomaticComment:
    comment: str  # Generated narrative comment
    generated_at: datetime
    total_votes_analyzed: int
    average_rating: float
```

## Design dell'Interfaccia Utente

### Palette Colori Star Wars
- **Primario**: #FFE81F (Giallo Jedi)
- **Secondario**: #000000 (Nero spazio)
- **Accenti**: 
  - Blu Jedi: #0066CC
  - Verde Jedi: #00FF00
  - Rosso Sith: #FF0000
  - Viola Mace Windu: #8A2BE2
  - Oro: #FFD700

### Typography
- **Font Primario**: "Orbitron" o "Exo" (futuristico)
- **Font Secondario**: "Roboto" (leggibilità)
- **Dimensioni**: Responsive, ottimizzate per mobile e proiezione

### Layout Responsive

**Mobile (Voting Interface):**
```
┌─────────────────────────┐
│      VibeTheForce       │
│   "Luke era un Vibe-    │
│      Coder?"            │
├─────────────────────────┤
│  ⭐ Youngling           │
│  ⭐⭐ Padawan            │
│  ⭐⭐⭐ Cavaliere Jedi    │
│  ⭐⭐⭐⭐ Maestro Jedi     │
│  ⭐⭐⭐⭐⭐ Gran Maestro   │
└─────────────────────────┘
```

**Desktop (Results Dashboard):**
```
┌─────────────────────────────────────────────┐
│              VibeTheForce Results           │
├─────────────────────────────────────────────┤
│  Totale Voti: 42    │    Media: 4.2 ⭐     │
├─────────────────────────────────────────────┤
│  ⭐⭐⭐⭐⭐ Gran Maestro     ████████ 35%     │
│  ⭐⭐⭐⭐ Maestro Jedi       ██████ 28%       │
│  ⭐⭐⭐ Cavaliere Jedi      ████ 20%         │
│  ⭐⭐ Padawan               ██ 12%           │
│  ⭐ Youngling              █ 5%             │
└─────────────────────────────────────────────┘
```

## Gestione degli Errori

### Scenari di Errore
1. **Netlify Functions non disponibili**: Messaggio di errore chiaro
2. **Database temporaneamente inaccessibile**: Retry automatico
3. **Browser non supportato**: Messaggio di compatibilità
4. **Schermo troppo piccolo**: Layout adattivo

### Strategie di Recovery
- Retry automatico per chiamate API fallite (max 3 tentativi)
- Messaggi di errore user-friendly
- Timeout di 10 secondi per le chiamate
- Logging degli errori per debugging

## Strategia di Testing

### Unit Tests
- VoteManager: logica di voto e persistenza
- ThemeEngine: applicazione corretta degli stili
- Calcoli statistici: precisione delle metriche

### Integration Tests
- Flusso completo di votazione
- Aggiornamento real-time dei risultati
- Persistenza cross-sessione

### User Acceptance Tests
- Accessibilità tramite QR Code
- Usabilità su dispositivi mobile
- Performance su connessioni lente
- Compatibilità browser

### Performance Tests
- Tempo di caricamento < 3 secondi
- Responsività dell'interfaccia
- Gestione di alto volume di voti simultanei

## Deployment e Considerazioni Tecniche

### Deployment Strategy (Streamlit Cloud)

**Deploy su Streamlit Cloud:**
1. Push codice su GitHub repository
2. Connetti repository a Streamlit Cloud
3. Configura secrets (GEMINI_API_KEY)
4. Deploy automatico
5. URL: `https://vibetheforce.streamlit.app`

**requirements.txt:**
```
streamlit>=1.28.0
google-generativeai>=0.3.0
plotly>=5.17.0
pandas>=2.0.0
qrcode[pil]>=7.4.0
```

**.streamlit/config.toml:**
```toml
[theme]
primaryColor = "#FFE81F"
backgroundColor = "#000428"
secondaryBackgroundColor = "#004e92"
textColor = "#FFFFFF"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```

**Secrets Configuration (.streamlit/secrets.toml - locale):**
```toml
GEMINI_API_KEY = "your-api-key-here"
```

**QR Code Generation (utils/qr_generator.py):**
```python
import qrcode
from io import BytesIO

def generate_qr_code(url: str) -> BytesIO:
    """Generate QR code for the app URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#FFE81F", back_color="#000428")
    
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf
```

**Vantaggi Streamlit Cloud:**
- Deploy automatico da GitHub
- HTTPS incluso
- Gestione secrets integrata
- Riavvio automatico su crash
- Logs centralizzati
- Gratuito per progetti pubblici

### Performance

**Ottimizzazioni Streamlit:**
- `@st.cache_data` per query database frequenti
- `@st.cache_resource` per connessioni database
- Auto-refresh controllato (ogni 2 secondi)
- Lazy loading per analytics LLM

**Database Performance:**
- Indici su colonne frequentemente interrogate
- Query ottimizzate con JOIN
- Connection pooling
- Transazioni atomiche

### Sicurezza

**Input Validation:**
- Rating: CHECK constraint 1-5 in SQLite
- Comment: max 500 caratteri
- Session ID: validazione formato
- SQL injection: parametrized queries

**Rate Limiting:**
- Prevenzione voti multipli via session_state
- UNIQUE constraint su session_id
- Timeout Gemini API (30 secondi)

**API Security:**
- Gemini API key in secrets
- No esposizione credenziali nel codice
- HTTPS obbligatorio su Streamlit Cloud

### Accessibilità

**Streamlit Built-in:**
- Semantic HTML automatico
- Keyboard navigation nativa
- Screen reader compatible
- Responsive design automatico

**Custom Enhancements:**
- Contrasto colori WCAG AA
- Font size leggibile (18px+)
- Touch targets > 44px
- Emoji per comunicazione visiva

### Monitoraggio

**Streamlit Cloud Dashboard:**
- Logs in tempo reale
- Metriche di utilizzo
- Error tracking
- Resource monitoring

**Custom Analytics:**
- Conteggio voti in tempo reale
- Timestamp per analisi temporale
- Comment analytics via Gemini
- Export dati SQLite per analisi offline