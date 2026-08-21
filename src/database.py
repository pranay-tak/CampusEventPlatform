import sqlite3
import os
from datetime import datetime
import json

DB_PATH = "data/campus_events.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        role TEXT,
        interests TEXT
    )
    ''')
    
    # Events table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        category TEXT,
        date TEXT,
        start_time TEXT,
        end_time TEXT,
        venue TEXT,
        registration_link TEXT,
        contact TEXT,
        poster_path TEXT,
        generated_poster_path TEXT,
        tags TEXT,
        created_at TEXT
    )
    ''')
    
    # Interactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event_id INTEGER,
        interaction_type TEXT,
        timestamp TEXT
    )
    ''')
    
    # Notifications table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event_id INTEGER,
        message TEXT,
        notification_type TEXT,
        created_at TEXT,
        read BOOLEAN
    )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_sample_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        if os.path.exists("data/sample_users.json"):
            with open("data/sample_users.json", "r") as f:
                users = json.load(f)
                for u in users:
                    cursor.execute("INSERT INTO users (name, email, role, interests) VALUES (?, ?, ?, ?)",
                                   (u['name'], u['email'], u['role'], json.dumps(u['interests'])))
                    
    cursor.execute("SELECT COUNT(*) FROM events")
    if cursor.fetchone()[0] == 0:
        if os.path.exists("data/sample_events.json"):
            with open("data/sample_events.json", "r") as f:
                events = json.load(f)
                for e in events:
                    cursor.execute("""
                        INSERT INTO events (title, description, category, date, start_time, end_time, venue, registration_link, contact, tags, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (e.get('title'), e.get('description'), e.get('category'), e.get('date'), e.get('start_time'), 
                          e.get('end_time'), e.get('venue'), e.get('registration_link'), e.get('contact'), json.dumps(e.get('tags', [])), datetime.now().isoformat()))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    load_sample_data()
    print("Database initialized.")
