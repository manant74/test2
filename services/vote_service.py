"""
Vote Service - Gestione logica di votazione e persistenza dati
"""
import sqlite3
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import streamlit as st
from database.db_manager import get_db_manager


class VoteService:
    """Service per gestire votazioni, commenti e statistiche"""
    
    def __init__(self, db_path: str = 'database/votes.db'):
        """
        Inizializza il VoteService
        
        Args:
            db_path: Percorso al database SQLite
        """
        self.db_path = db_path
        self.db_manager = get_db_manager(db_path)
    
    def submit_vote(self, rating: int, comment: Optional[str] = None) -> bool:
        """
        Invia un voto con commento opzionale
        
        Args:
            rating: Valutazione da 1 a 5
            comment: Commento opzionale (max 500 caratteri)
        
        Returns:
            True se il voto è stato registrato con successo, False altrimenti
        
        Requisiti: 1.2, 1.4, 6.3, 6.4
        """
        # Validazione rating
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            st.error("Rating deve essere un intero tra 1 e 5")
            return False
        
        # Validazione commento
        if comment and len(comment) > 500:
            st.error("Il commento non può superare i 500 caratteri")
            return False
        
        try:
            # Genera session_id se non esiste
            if 'session_id' not in st.session_state:
                st.session_state.session_id = f"session_{datetime.now().timestamp()}_{id(st.session_state)}"
            
            session_id = st.session_state.session_id
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert vote
            cursor.execute(
                'INSERT INTO votes (rating, session_id) VALUES (?, ?)',
                (rating, session_id)
            )
            vote_id = cursor.lastrowid
            
            # Insert comment se fornito
            if comment and comment.strip():
                cursor.execute(
                    'INSERT INTO comments (vote_id, comment) VALUES (?, ?)',
                    (vote_id, comment.strip())
                )
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            # Session ha già votato (UNIQUE constraint su session_id)
            st.error("Hai già votato! Non è possibile votare più volte.")
            return False
        except sqlite3.Error as e:
            st.error(f"Errore database: {e}")
            return False
        except Exception as e:
            st.error(f"Errore imprevisto: {e}")
            return False
    
    def get_results(self) -> Dict:
        """
        Recupera i risultati aggregati delle votazioni
        
        Returns:
            Dizionario con:
            - votes: dict con conteggio per ogni rating (1-5)
            - total_votes: numero totale di voti
            - average_rating: media con 2 decimali
            - total_comments: numero di commenti ricevuti
        
        Requisiti: 2.1, 2.3, 2.4, 6.5
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get vote counts per rating
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
            
            # Calculate average con 2 decimali
            if total_votes > 0:
                weighted_sum = sum(rating * count for rating, count in vote_counts.items())
                average_rating = round(weighted_sum / total_votes, 2)
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
            
        except sqlite3.Error as e:
            st.error(f"Errore nel recupero risultati: {e}")
            return {
                'votes': {i: 0 for i in range(1, 6)},
                'total_votes': 0,
                'average_rating': 0.0,
                'total_comments': 0
            }
    
    def get_all_comments(self) -> List[Tuple[str, int, str]]:
        """
        Recupera tutti i commenti con rating associato
        
        Returns:
            Lista di tuple (comment, rating, timestamp)
        
        Requisiti: 6.5
        """
        try:
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
            
        except sqlite3.Error as e:
            st.error(f"Errore nel recupero commenti: {e}")
            return []
    
    def reset_votes(self) -> bool:
        """
        Reset di tutti i voti e commenti (funzione admin)
        
        Returns:
            True se il reset è avvenuto con successo, False altrimenti
        
        Requisiti: 5.5
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete comments first (foreign key constraint)
            cursor.execute('DELETE FROM comments')
            # Delete votes
            cursor.execute('DELETE FROM votes')
            
            conn.commit()
            conn.close()
            
            return True
            
        except sqlite3.Error as e:
            st.error(f"Errore durante il reset: {e}")
            return False
