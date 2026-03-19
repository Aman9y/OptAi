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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS execution_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT,
            execution_time_ms REAL,
            memory_kb REAL,
            code_size_bytes INTEGER,
            success INTEGER,
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

def save_execution_metric(language, execution_time_ms, memory_kb, code_size_bytes, success):
    conn = sqlite3.connect('optiai.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO execution_metrics (language, execution_time_ms, memory_kb, code_size_bytes, success)
        VALUES (?, ?, ?, ?, ?)
    ''', (language, execution_time_ms, memory_kb, code_size_bytes, 1 if success else 0))
    conn.commit()
    conn.close()

def get_execution_metrics(limit=20):
    conn = sqlite3.connect('optiai.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT language, execution_time_ms, memory_kb, code_size_bytes, success, timestamp
        FROM execution_metrics
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"language": r[0], "execution_time_ms": r[1], "memory_kb": r[2],
         "code_size_bytes": r[3], "success": bool(r[4]), "timestamp": r[5]}
        for r in rows
    ]

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