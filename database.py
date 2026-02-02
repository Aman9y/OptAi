import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('optiai.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_code TEXT NOT NULL,
            optimized_code TEXT,
            language TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_optimization(original_code, optimized_code, language):
    conn = sqlite3.connect('optiai.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO code_history (original_code, optimized_code, language)
        VALUES (?, ?, ?)
    ''', (original_code, optimized_code, language))
    
    conn.commit()
    conn.close()

def get_history(limit=10):
    conn = sqlite3.connect('optiai.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT original_code, optimized_code, language, timestamp
        FROM code_history
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    return results