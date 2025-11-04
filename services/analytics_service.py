"""
Analytics Service - Analisi automatica dei risultati di votazione con Google Gemini
Genera commenti descrittivi sui pattern di votazione in linguaggio naturale italiano
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Dict
from services.gemini_client import GeminiClient
from services.vote_service import VoteService


class AnalyticsService:
    """
    Service per analisi automatica dei risultati di votazione tramite LLM
    
    Requisiti: 7.1, 7.2, 7.3, 7.4, 7.5
    """
    
    def __init__(self):
        """Inizializza Analytics Service con Gemini client e Vote service"""
        self.gemini_client = GeminiClient(timeout=30)
        self.vote_service = VoteService()
        
        # Cache per commento automatico (aggiornamento ogni 30 secondi)
        if 'analytics_cache' not in st.session_state:
            st.session_state.analytics_cache = {
                'comment': None,
                'last_update': None,
                'last_vote_count': 0
            }
    
    def generate_automatic_comment(self) -> Optional[str]:
        """
        Genera commento automatico sui risultati di votazione usando Gemini LLM
        
        Analizza la distribuzione numerica dei voti e genera un commento descrittivo
        di 3-4 frasi in italiano che identifica pattern e fornisce insights.
        
        Implementa caching per evitare chiamate ripetute:
        - Aggiornamento ogni 30 secondi
        - Solo se ci sono nuovi voti
        
        Returns:
            Commento automatico generato o None se non disponibile
            Stringa vuota se meno di 10 voti
        
        Requisiti: 7.1, 7.2, 7.3, 7.4, 7.5
        """
        # Verifica se Gemini è configurato
        if not self.gemini_client.is_configured():
            return "⚠️ Analisi LLM non disponibile: GEMINI_API_KEY non configurata."
        
        # Recupera risultati correnti
        results = self.vote_service.get_results()
        
        # Requisito 7.1: Minimo 10 voti per generare commento
        if results['total_votes'] < 10:
            return ""
        
        # Controlla cache per evitare chiamate ripetute
        cache = st.session_state.analytics_cache
        current_time = datetime.now()
        
        # Determina se serve aggiornamento
        needs_update = (
            cache['comment'] is None or
            cache['last_update'] is None or
            (current_time - cache['last_update']) > timedelta(seconds=30) or
            results['total_votes'] != cache['last_vote_count']
        )
        
        # Usa cache se non serve aggiornamento
        if not needs_update and cache['comment']:
            return cache['comment']
        
        # Genera nuovo commento
        try:
            comment = self._generate_comment_from_results(results)
            
            # Aggiorna cache
            st.session_state.analytics_cache = {
                'comment': comment,
                'last_update': current_time,
                'last_vote_count': results['total_votes']
            }
            
            return comment
            
        except Exception as e:
            st.error(f"Errore nella generazione commento automatico: {e}")
            return "⚠️ Analisi temporaneamente non disponibile."
    
    def _generate_comment_from_results(self, results: Dict) -> str:
        """
        Genera commento usando Gemini basato sui risultati di votazione
        
        Args:
            results: Dizionario con risultati da vote_service.get_results()
        
        Returns:
            Commento generato da Gemini
        """
        vote_distribution = results['votes']
        total_votes = results['total_votes']
        average_rating = results['average_rating']
        
        # Calcola percentuali per ogni rating
        percentages = {
            rating: round((count / total_votes * 100), 1) if total_votes > 0 else 0
            for rating, count in vote_distribution.items()
        }
        
        # Identifica rating più votato
        max_rating = max(vote_distribution.items(), key=lambda x: x[1])
        
        # Crea prompt per Gemini (Requisito 7.2, 7.3)
        prompt = f"""Analizza questi dati di votazione per una conference sul VibeCoding e genera un commento descrittivo in italiano.

Distribuzione voti (scala 1-5 stelle con tematiche Star Wars):
- 1 stella (Youngling): {vote_distribution[1]} voti ({percentages[1]:.1f}%)
- 2 stelle (Padawan): {vote_distribution[2]} voti ({percentages[2]:.1f}%)
- 3 stelle (Cavaliere Jedi): {vote_distribution[3]} voti ({percentages[3]:.1f}%)
- 4 stelle (Maestro Jedi): {vote_distribution[4]} voti ({percentages[4]:.1f}%)
- 5 stelle (Gran Maestro): {vote_distribution[5]} voti ({percentages[5]:.1f}%)

Totale voti: {total_votes}
Media: {average_rating:.2f} stelle
Rating più votato: {max_rating[0]} stelle con {max_rating[1]} voti

Genera un commento di esattamente 3-4 frasi in italiano che:
1. Descriva il sentiment generale (positivo/negativo/misto) basato sulla distribuzione
2. Identifichi il pattern più interessante nella distribuzione dei voti
3. Fornisca un'osservazione comparativa o statistica significativa

Usa un tono coinvolgente e a tema Star Wars quando appropriato (es. "La Forza è forte in questo talk", "Il lato luminoso prevale").
Rispondi SOLO con il testo del commento, senza titoli, formattazione markdown o introduzioni.
"""
        
        # Genera commento con Gemini
        comment = self.gemini_client.generate_text(prompt)
        
        if comment:
            return comment
        else:
            return "⚠️ Impossibile generare commento automatico al momento."
    
    def clear_cache(self):
        """
        Pulisce la cache del commento automatico
        Utile per forzare rigenerazione immediata
        """
        st.session_state.analytics_cache = {
            'comment': None,
            'last_update': None,
            'last_vote_count': 0
        }
