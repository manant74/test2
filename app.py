"""
VibeTheForce - Main Streamlit Application
A Star Wars themed voting app for conference feedback
"""

import streamlit as st
from utils.theme import apply_star_wars_theme
from utils.qr_generator import generate_themed_qr_code
import base64

# Page configuration
st.set_page_config(
    page_title="VibeTheForce",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar on home page
)

# Apply Star Wars theme
apply_star_wars_theme()

# Hide sidebar on home page with custom CSS
st.markdown("""
<style>
    /* Hide sidebar on home page only */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Hide sidebar toggle button */
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    /* Adjust main content to use full width and reduce padding */
    .main .block-container {
        padding-top: 0.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 1rem;
        max-width: none;
    }
    
    /* Remove default Streamlit header spacing */
    .main .block-container > div:first-child {
        padding-top: 0;
        margin-top: 0;
    }
    
    /* Remove top margin from first element */
    .main .block-container > div:first-child > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Reduce title spacing */
    h1 {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Reduce spacing between elements */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    
    /* Compact QR container */
    .qr-container {
        margin-top: 0;
        padding: 1.5rem;
    }
    
    /* Reduce subtitle spacing */
    h2, h3 {
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Compact info box */
    .stAlert {
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Hide empty elements in columns */
    .element-container:empty {
        display: none !important;
    }
    
    /* Remove spacing from empty divs */
    div:empty {
        margin: 0 !important;
        padding: 0 !important;
        height: 0 !important;
    }
    
    /* Ensure columns start at the same height */
    [data-testid="column"] {
        padding-top: 0 !important;
    }
    
    /* Remove any default margin from column content */
    [data-testid="column"] > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    
    /* QR Code container styling */
    .qr-container {
        background: linear-gradient(145deg, rgba(51, 51, 51, 0.3) 0%, rgba(34, 34, 34, 0.3) 100%);
        border: 1px solid #666666;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin-top: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .qr-title {
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
        font-size: 1.2rem;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Create two columns layout
col1, col2 = st.columns([2, 1])

with col1:
    # Main content
    st.title("🌟 VibeTheForce")
    st.subheader("Luke era un VibeCoder?")
    
    st.markdown("""
    Benvenuto a **VibeTheForce**! 
    
    Un'applicazione a tema Star Wars per raccogliere feedback sui talk delle conferenze.
    
    **Come funziona:**
    - 🌟 Vota il talk usando i livelli Jedi (da Youngling a Gran Maestro)
    - 📈 Visualizza i risultati in tempo reale
    - 💬 Lascia commenti per feedback dettagliato
    - 🤖 Ricevi analisi AI automatiche sui commenti
    
    Che la Forza sia con te! ✨
    """)
    
    # Add some stats or info
    st.info("💡 **Suggerimento**: Usa il QR Code per accedere rapidamente dall'app mobile!")
    
    # Navigation buttons
    st.markdown("### 🚀 Naviga nell'applicazione")
    
    # Create navigation buttons
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("🗳️ **Vota**\n\nEsprimi il tuo voto", use_container_width=True):
            st.switch_page("pages/1_🗳️_Vota.py")
    
    with col_btn2:
        if st.button("📊 **Risultati**\n\nVisualizza i risultati", use_container_width=True):
            st.switch_page("pages/2_📊_Risultati.py")
    
    with col_btn3:
        if st.button("⚙️ **Admin**\n\nPannello amministrazione", use_container_width=True):
            st.switch_page("pages/3_⚙️_Admin.py")

with col2:
    # QR Code section - start immediately without empty space
    st.markdown("""
    <div class="qr-container" style="margin-top: 0; padding-top: 1rem;">
        <h3 class="qr-title">📱 Scansiona per accedere</h3>
    """, unsafe_allow_html=True)
    
    try:
        # Get current URL - detect deployment environment
        current_url = "http://localhost:8501"
        
        # Simplified URL detection - prioritize secrets
        try:
            # Check Streamlit secrets first
            if hasattr(st, 'secrets') and hasattr(st.secrets, 'get'):
                app_url = st.secrets.get('APP_URL', None)
                if app_url:
                    current_url = str(app_url).strip()
            
            # Fallback to environment variable
            elif 'APP_URL' in os.environ:
                current_url = str(os.environ['APP_URL']).strip()
                
        except Exception as e:
            # Keep localhost as fallback
            pass
        
        # Validate and clean the URL
        if current_url and current_url != "http://localhost:8501":
            # Clean up the URL
            current_url = current_url.strip()
            # Ensure it starts with http:// or https://
            if not current_url.startswith(('http://', 'https://')):
                current_url = f"https://{current_url}"
            # Remove any trailing slashes
            current_url = current_url.rstrip('/')
            
            # Validate it's a proper URL
            if not ('.' in current_url and len(current_url) > 10):
                current_url = "http://localhost:8501"  # Fallback to localhost if invalid
        
        # Debug: Show what URL we're using (visible only in non-production)
        if current_url != "http://localhost:8501":
            # Show debug info in a small, unobtrusive way
            st.markdown(f"""
            <div style="font-size: 0.7rem; color: #666; text-align: center; margin-bottom: 0.5rem;">
                🔗 {current_url}
            </div>
            """, unsafe_allow_html=True)
        
        # Generate QR code with Imperial theme
        qr_buffer = generate_themed_qr_code(current_url, theme='empire')
        
        # Convert to base64 for display
        qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode()
        
        # Display QR code centered
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 10px; margin: 1rem auto; display: flex; justify-content: center; align-items: center;">
            <img src="data:image/png;base64,{qr_base64}" style="max-width: 200px; height: auto; display: block;">
        </div>
    </div>
        """, unsafe_allow_html=True)
        
        # Show URL info only in development
        if current_url == "http://localhost:8501":
            st.markdown("""
            <div style="font-size: 0.7rem; color: #888; text-align: center; margin-top: 0.5rem;">
                💡 Sviluppo locale - Configura APP_URL per produzione
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown("""
        <div style="text-align: center; color: #ff6b6b; padding: 2rem;">
            <p>QR Code non disponibile</p>
            <p style="font-size: 0.9rem;">Accedi direttamente dall'applicazione</p>
        </div>
    </div>
        """, unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    import time
    st.session_state.session_id = f"session_{int(time.time() * 1000)}"

if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False
