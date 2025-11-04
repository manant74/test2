"""
Admin Panel - VibeTheForce
Gestione amministrativa: reset voti, statistiche database, QR code
"""
import streamlit as st
from services.vote_service import VoteService
from utils.theme import apply_star_wars_theme
import sqlite3
from datetime import datetime


def get_database_stats():
    """
    Recupera statistiche dettagliate dal database
    
    Returns:
        Dict con statistiche database
    """
    vote_service = VoteService()
    
    try:
        conn = sqlite3.connect(vote_service.db_path)
        cursor = conn.cursor()
        
        # Totale voti
        cursor.execute('SELECT COUNT(*) FROM votes')
        total_votes = cursor.fetchone()[0]
        
        # Totale commenti
        cursor.execute('SELECT COUNT(*) FROM comments')
        total_comments = cursor.fetchone()[0]
        
        # Timestamp ultimo voto
        cursor.execute('SELECT MAX(timestamp) FROM votes')
        last_vote_timestamp = cursor.fetchone()[0]
        
        # Timestamp primo voto
        cursor.execute('SELECT MIN(timestamp) FROM votes')
        first_vote_timestamp = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_votes': total_votes,
            'total_comments': total_comments,
            'last_vote_timestamp': last_vote_timestamp,
            'first_vote_timestamp': first_vote_timestamp
        }
        
    except sqlite3.Error as e:
        st.error(f"Errore nel recupero statistiche: {e}")
        return {
            'total_votes': 0,
            'total_comments': 0,
            'last_vote_timestamp': None,
            'first_vote_timestamp': None
        }


def render_admin_page():
    """Render della pagina Admin"""
    
    # Applica tema Star Wars
    apply_star_wars_theme()
    
    st.title("⚙️ Admin Panel - VibeTheForce")
    st.markdown("---")
    
    # Sezione Statistiche Database
    st.header("📊 Statistiche Database")
    
    stats = get_database_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Totale Voti",
            value=stats['total_votes']
        )
    
    with col2:
        st.metric(
            label="Totale Commenti",
            value=stats['total_comments']
        )
    
    with col3:
        if stats['last_vote_timestamp']:
            # Formatta timestamp
            last_vote_dt = datetime.fromisoformat(stats['last_vote_timestamp'])
            formatted_time = last_vote_dt.strftime("%H:%M:%S")
            st.metric(
                label="Ultimo Voto",
                value=formatted_time
            )
        else:
            st.metric(
                label="Ultimo Voto",
                value="N/A"
            )
    
    # Informazioni aggiuntive
    if stats['first_vote_timestamp'] and stats['last_vote_timestamp']:
        st.info(f"📅 Primo voto: {datetime.fromisoformat(stats['first_vote_timestamp']).strftime('%d/%m/%Y %H:%M:%S')}")
    
    st.markdown("---")
    
    # Sezione Reset Voti
    st.header("🔄 Reset Voti")
    st.warning("⚠️ Attenzione: questa operazione eliminerà tutti i voti e commenti in modo permanente!")
    
    # Conferma con checkbox
    confirm_reset = st.checkbox("Confermo di voler eliminare tutti i dati")
    
    if confirm_reset:
        if st.button("🗑️ Reset Database", type="primary"):
            vote_service = VoteService()
            success = vote_service.reset_votes()
            
            if success:
                st.success("✅ Database resettato con successo!")
                st.balloons()
                # Aggiorna la pagina dopo 2 secondi
                st.rerun()
            else:
                st.error("❌ Errore durante il reset del database")
    else:
        st.button("🗑️ Reset Database", disabled=True)
    
    st.markdown("---")
    
    # Sezione QR Code
    st.header("📱 QR Code per Condivisione")
    
    # Ottieni URL dell'app
    try:
        # URL dell'app Streamlit
        app_url = st.query_params.get("url", "https://vibetheforce.streamlit.app")
        
        # Se siamo in locale, usa localhost
        if "localhost" in str(st.get_option("browser.serverAddress")):
            app_url = f"http://localhost:{st.get_option('server.port')}"
        
        st.info(f"🔗 URL App: {app_url}")
        
        # Genera QR Code
        from utils.qr_generator import generate_qr_code
        
        qr_buffer = generate_qr_code(app_url)
        
        # Mostra QR Code
        st.image(qr_buffer, caption="Scansiona per votare!", width=300)
        
        # Download button
        st.download_button(
            label="⬇️ Scarica QR Code",
            data=qr_buffer,
            file_name="vibetheforce_qr.png",
            mime="image/png"
        )
        
    except Exception as e:
        st.error(f"Errore nella generazione del QR Code: {e}")
        st.info("Assicurati che la libreria qrcode sia installata: pip install qrcode[pil]")


if __name__ == "__main__":
    render_admin_page()
