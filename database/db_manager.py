"""
Database Manager for VibeTheForce
Handles SQLite database initialization, connection pooling, and common queries
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import Optional, List, Tuple
from pathlib import Path


class DatabaseManager:
    """Manages SQLite database operations with connection pooling and transaction support"""
    
    def __init__(self, db_path: str = "database/votes.db"):
        """
        Initialize DatabaseManager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_database_directory()
        self._initialized = False
    
    def _ensure_database_directory(self):
        """Ensure the database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
    
    def initialize_database(self):
        """
        Initialize database with schema from schema.sql
        Creates tables and indexes if they don't exist
        """
        if self._initialized:
            return
        
        schema_path = Path(__file__).parent / "schema.sql"
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(schema_sql)
            conn.commit()
        
        self._initialized = True
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections
        Provides automatic connection cleanup and transaction management
        
        Usage:
            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM votes")
        
        Yields:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(
            self.db_path,
            timeout=10.0,
            check_same_thread=False
        )
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @contextmanager
    def get_transaction(self):
        """
        Context manager for explicit transactions
        Automatically commits on success or rolls back on error
        
        Usage:
            with db_manager.get_transaction() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO votes ...")
                # Automatically commits if no exception
        
        Yields:
            sqlite3.Connection: Database connection with transaction
        """
        with self.get_connection() as conn:
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
    
    # Helper functions for common queries
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Tuple]:
        """
        Execute a SELECT query and return all results
        
        Args:
            query: SQL query string
            params: Query parameters (for parameterized queries)
        
        Returns:
            List of tuples containing query results
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT query and return the last row ID
        
        Args:
            query: SQL INSERT statement
            params: Query parameters
        
        Returns:
            Last inserted row ID
        """
        with self.get_transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.lastrowid
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Execute an UPDATE or DELETE query and return affected rows
        
        Args:
            query: SQL UPDATE/DELETE statement
            params: Query parameters
        
        Returns:
            Number of affected rows
        """
        with self.get_transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
    def get_vote_count(self) -> int:
        """
        Get total number of votes
        
        Returns:
            Total vote count
        """
        result = self.execute_query("SELECT COUNT(*) FROM votes")
        return result[0][0] if result else 0
    
    def get_votes_by_rating(self) -> dict:
        """
        Get vote counts grouped by rating
        
        Returns:
            Dictionary mapping rating (1-5) to count
        """
        results = self.execute_query(
            "SELECT rating, COUNT(*) as count FROM votes GROUP BY rating"
        )
        
        # Initialize all ratings with 0
        vote_counts = {i: 0 for i in range(1, 6)}
        
        # Update with actual counts
        for rating, count in results:
            vote_counts[rating] = count
        
        return vote_counts
    
    def get_average_rating(self) -> float:
        """
        Calculate average rating across all votes
        
        Returns:
            Average rating (0.0 if no votes)
        """
        result = self.execute_query(
            "SELECT AVG(CAST(rating AS FLOAT)) FROM votes"
        )
        avg = result[0][0] if result and result[0][0] is not None else 0.0
        return round(avg, 2)
    
    def get_comment_count(self) -> int:
        """
        Get total number of comments
        
        Returns:
            Total comment count
        """
        result = self.execute_query("SELECT COUNT(*) FROM comments")
        return result[0][0] if result else 0
    
    def get_all_comments_with_ratings(self) -> List[Tuple[str, int, str]]:
        """
        Get all comments with their associated ratings and timestamps
        
        Returns:
            List of tuples (comment, rating, timestamp)
        """
        return self.execute_query("""
            SELECT c.comment, v.rating, c.timestamp
            FROM comments c
            JOIN votes v ON c.vote_id = v.id
            ORDER BY c.timestamp DESC
        """)
    
    def reset_all_data(self):
        """
        Delete all votes and comments (admin function)
        Uses CASCADE to automatically delete related comments
        """
        with self.get_transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM comments")
            cursor.execute("DELETE FROM votes")
    
    def check_session_exists(self, session_id: str) -> bool:
        """
        Check if a session has already voted
        
        Args:
            session_id: Session identifier
        
        Returns:
            True if session has voted, False otherwise
        """
        result = self.execute_query(
            "SELECT COUNT(*) FROM votes WHERE session_id = ?",
            (session_id,)
        )
        return result[0][0] > 0 if result else False


# Singleton instance for application-wide use
_db_manager_instance: Optional[DatabaseManager] = None


def get_db_manager(db_path: str = "database/votes.db") -> DatabaseManager:
    """
    Get or create singleton DatabaseManager instance
    
    Args:
        db_path: Path to database file
    
    Returns:
        DatabaseManager instance
    """
    global _db_manager_instance
    
    if _db_manager_instance is None:
        _db_manager_instance = DatabaseManager(db_path)
        _db_manager_instance.initialize_database()
    
    return _db_manager_instance
