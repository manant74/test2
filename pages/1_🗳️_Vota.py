"""
VibeTheForce - Pagina di Votazione
Interfaccia per votare il talk con tema Star Wars
"""

import streamlit as st
from services.vote_service import VoteService
from utils.theme import apply_star_wars_theme, RATING_LABELS

# Page configuration
st.set_page_config(
    page_title="Vota - VibeTheForce",
    page_icon="🗳️",
    layout="centered"
)

# Apply Star Wars theme
apply_star_wars_theme()

# Additional CSS for voting page specific styling
st.markdown("""
<style>
.stButton>button {
    height: 120px;
    white-space: pre-wrap;
}

.success-message {
    background-color: rgba(0, 255, 0, 0.2);
    border: 2px solid #00FF00;
    border-radius: 10px;
    padding: 15px;
    color: #00FF00;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    import time
    st.session_state.session_id = f"session_{int(time.time() * 1000)}"

if 'has_voted' not in st.session_state:
    st.session_state.has_voted = False

# Title
st.title("🗳️ VibeTheForce - Vota!")
st.subheader("Luke era un VibeCoder?")

# Check if user already voted
if st.session_state.has_voted:
    st.markdown("""
    <div class="success-message">
        ✅ Hai già votato! Grazie per il tuo feedback.<br>
        Che la Forza sia con te! ✨
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Vai alla pagina 📊 Risultati per vedere i risultati in tempo reale!")
    st.stop()

# Voting interface
st.markdown("### Seleziona il tuo livello di apprezzamento:")

# Create 5 columns for rating buttons
col1, col2, col3, col4, col5 = st.columns(5)

# Rating labels and emojis using theme constants
ratings = {
    1: {
        "stars": "⭐",
        "label": "Youngling",
        "full_label": RATING_LABELS[1],
        "col": col1
    },
    2: {
        "stars": "⭐⭐",
        "label": "Padawan",
        "full_label": RATING_LABELS[2],
        "col": col2
    },
    3: {
        "stars": "⭐⭐⭐",
        "label": "Cavaliere\nJedi",
        "full_label": RATING_LABELS[3],
        "col": col3
    },
    4: {
        "stars": "⭐⭐⭐⭐",
        "label": "Maestro\nJedi",
        "full_label": RATING_LABELS[4],
        "col": col4
    },
    5: {
        "stars": "⭐⭐⭐⭐⭐",
        "label": "Gran\nMaestro",
        "full_label": RATING_LABELS[5],
        "col": col5
    }
}

# Initialize selected_rating in session state if not exists
if 'selected_rating' not in st.session_state:
    st.session_state.selected_rating = None

# Display rating buttons
for rating, info in ratings.items():
    with info["col"]:
        button_label = f"{info['stars']}\n{info['label']}"
        if st.button(button_label, key=f"vote_{rating}", use_container_width=True):
            st.session_state.selected_rating = rating

# Show selected rating
if st.session_state.selected_rating:
    selected_info = ratings[st.session_state.selected_rating]
    st.success(f"✨ Hai selezionato: {selected_info['stars']} {selected_info['label'].replace(chr(10), ' ')}")

# Optional comment field
st.markdown("---")
comment = st.text_area(
    "💬 Commento opzionale (max 500 caratteri)",
    max_chars=500,
    placeholder="Condividi il tuo feedback sul talk...",
    help="Il commento è opzionale. Puoi votare anche senza lasciare un commento.",
    height=100
)

# Character counter
if comment:
    char_count = len(comment)
    st.caption(f"Caratteri: {char_count}/500")

# Submit button
st.markdown("---")
if st.button("🚀 Invia Voto", type="primary", use_container_width=True):
    if st.session_state.selected_rating is None:
        st.error("⚠️ Seleziona prima un livello di valutazione!")
    else:
        # Submit vote using VoteService
        vote_service = VoteService()
        success = vote_service.submit_vote(
            rating=st.session_state.selected_rating,
            comment=comment if comment.strip() else None
        )
        
        if success:
            # Mark as voted
            st.session_state.has_voted = True
            
            # Show success message
            selected_info = ratings[st.session_state.selected_rating]
            st.balloons()
            st.success(f"🎉 Voto registrato con successo: {selected_info['stars']} {selected_info['label'].replace(chr(10), ' ')}")
            st.info("Grazie per il tuo feedback! Che la Forza sia con te! ✨")
            
            # Rerun to update UI
            st.rerun()
        else:
            # Error already shown by VoteService
            pass

# Footer
st.markdown("---")
st.caption("Powered by VibeTheForce 🌟 | May the Force be with you!")
