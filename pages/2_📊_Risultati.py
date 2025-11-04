"""
VibeTheForce - Dashboard Risultati in Tempo Reale
Visualizzazione dei risultati di votazione con metriche e grafici
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from services.vote_service import VoteService
from services.analytics_service import AnalyticsService
from utils.theme import apply_star_wars_theme, RATING_COLORS, RATING_LABELS

# Page configuration
st.set_page_config(
    page_title="Risultati - VibeTheForce",
    page_icon="📊",
    layout="wide"
)

# Apply Star Wars theme
apply_star_wars_theme()

# Additional CSS for results page - Ottimizzato per leggibilità da 5 metri
st.markdown("""
<style>
h1 {
    font-size: 3.5rem !important;
}

h2 {
    font-size: 2.5rem !important;
}

/* Metriche ottimizzate per leggibilità da 5 metri */
.stMetric {
    padding: 25px;
    border: 3px solid #CCCCCC;
}

.stMetric label {
    font-size: 2rem !important;
}

.stMetric [data-testid="stMetricValue"] {
    font-size: 4rem !important;
}

/* Info box styling */
.stAlert {
    font-size: 1.3rem;
}

/* Caption styling */
.caption-text {
    color: #CCCCCC;
    font-size: 1.2rem;
    text-align: center;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Risultati in Tempo Reale")
st.markdown("---")

# Get results from VoteService
vote_service = VoteService()
results = vote_service.get_results()

# Key metrics - 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="🗳️ Totale Voti",
        value=results['total_votes']
    )

with col2:
    st.metric(
        label="⭐ Media",
        value=f"{results['average_rating']:.2f}"
    )

with col3:
    st.metric(
        label="💬 Commenti",
        value=results['total_comments']
    )

st.markdown("---")

# Vote distribution chart with Plotly
st.subheader("Distribuzione Voti")

# Prepare data for chart using theme constants
rating_labels_list = [RATING_LABELS[i] for i in range(1, 6)]
vote_counts = [results['votes'][i] for i in range(1, 6)]

# Star Wars colors for each rating from theme constants
rating_colors_list = [RATING_COLORS[i] for i in range(1, 6)]

# Create Plotly bar chart
fig = go.Figure(data=[
    go.Bar(
        x=rating_labels_list,
        y=vote_counts,
        marker=dict(
            color=rating_colors_list,
            line=dict(color='#FFFFFF', width=2)
        ),
        text=vote_counts,
        textposition='outside',
        textfont=dict(
            size=24,
            color='#FFFFFF',
            family='Arial'
        )
    )
])

# Update layout for Star Wars theme and readability from 5 meters
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    height=600,
    margin=dict(t=50, b=100, l=80, r=50)
)

fig.update_xaxes(
    title="",
    title_font=dict(size=20, color='#FFFFFF'),
    tickfont=dict(size=20, color='#FFFFFF'),
    gridcolor='rgba(255, 255, 255, 0.2)'
)

fig.update_yaxes(
    title="Numero di Voti",
    title_font=dict(size=22, color='#FFFFFF'),
    tickfont=dict(size=20, color='#FFFFFF'),
    gridcolor='rgba(255, 255, 255, 0.2)'
)

fig.update_layout(
    font=dict(
        size=18,
        color='#FFFFFF',
        family='Arial'
    )
)

# Display chart
st.plotly_chart(fig, use_container_width=True)

# LLM Automatic Comment (if >= 10 votes)
st.markdown("---")

if results['total_votes'] >= 10:
    st.subheader("🤖 Commento Automatico (Gemini AI)")
    
    # Initialize analytics service
    analytics_service = AnalyticsService()
    
    # Generate automatic comment with caching (updates every 30 seconds)
    with st.spinner("Generazione analisi AI..."):
        auto_comment = analytics_service.generate_automatic_comment()
    
    if auto_comment:
        # Display comment in info box
        st.info(auto_comment)
    else:
        # Handle case when LLM is not available
        st.warning("⚠️ Analisi LLM temporaneamente non disponibile. Verifica la configurazione di GEMINI_API_KEY.")
else:
    # Show message when not enough votes
    votes_needed = 10 - results['total_votes']
    st.info(f"ℹ️ Servono almeno 10 voti per generare il commento automatico AI. Mancano ancora {votes_needed} voti!")

# Footer
st.markdown("---")
st.markdown(
    '<p class="caption-text">Aggiornamento automatico ogni 2 secondi | Powered by VibeTheForce 🌟</p>',
    unsafe_allow_html=True
)

# Auto-refresh every 2 seconds
time.sleep(2)
st.rerun()
