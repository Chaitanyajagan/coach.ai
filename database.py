import sqlite3
import hashlib
import json
from datetime import datetime

DB_NAME = "interview_app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database tables."""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Interviews Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            conversation TEXT NOT NULL,
            final_score REAL,
            verdict TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Create a new user. Returns True if successful, False if username exists."""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials. Returns user ID if valid, None otherwise."""
    conn = get_db_connection()
    c = conn.cursor()
    user = c.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and user['password'] == hash_password(password):
        return user['id']
    return None

def save_interview(user_id, role, messages, final_score, verdict):
    """Save a completed interview."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO interviews (user_id, role, conversation, final_score, verdict)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, role, json.dumps(messages), final_score, verdict))
    conn.commit()
    conn.close()

def get_user_interviews(user_id):
    """Get all past interviews for a user."""
    conn = get_db_connection()
    c = conn.cursor()
    interviews = c.execute('''
        SELECT * FROM interviews WHERE user_id = ? ORDER BY timestamp DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return interviews
