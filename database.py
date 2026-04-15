import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        username TEXT,
        password TEXT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

from datetime import datetime
import sqlite3

def insert_attack(ip, username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
    INSERT INTO attacks (ip, username, password, time)
    VALUES (?, ?, ?, ?)
    ''', (ip, username, password, time))

    conn.commit()
    conn.close()