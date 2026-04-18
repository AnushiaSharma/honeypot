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
                   country TEXT,
                   city TEXT,
                   time TEXT
    )
    ''')

    conn.commit()
    conn.close()

import requests
from datetime import datetime
import sqlite3

def insert_attack(ip, username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Get location from IP
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = response.get("country", "Unknown")
        city = response.get("city", "Unknown")
    except:
        country = "Unknown"
        city = "Unknown"

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
    INSERT INTO attacks (ip, username, password, country, city, time)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (ip, username, password, country, city, time))

    conn.commit()
    conn.close()