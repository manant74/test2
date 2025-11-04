-- VibeTheForce Database Schema
-- SQLite database for storing votes and comments
-- Votes table
-- Stores individual votes with rating (1-5) and session tracking
CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rating INTEGER NOT NULL CHECK(
        rating >= 1
        AND rating <= 5
    ),
    session_id TEXT NOT NULL UNIQUE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- Comments table
-- Stores optional comments associated with votes
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vote_id INTEGER NOT NULL,
    comment TEXT NOT NULL CHECK(LENGTH(comment) <= 500),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vote_id) REFERENCES votes(id) ON DELETE CASCADE
);
-- Indexes for performance optimization
-- Index on rating for fast aggregation queries
CREATE INDEX IF NOT EXISTS idx_votes_rating ON votes(rating);
-- Index on timestamp for chronological queries
CREATE INDEX IF NOT EXISTS idx_votes_timestamp ON votes(timestamp);
-- Index on vote_id for fast comment lookups
CREATE INDEX IF NOT EXISTS idx_comments_vote_id ON comments(vote_id);
-- Index on session_id for duplicate vote prevention
CREATE INDEX IF NOT EXISTS idx_votes_session_id ON votes(session_id);