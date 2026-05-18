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
                   latitude TEXT,
                   longitude TEXT,
                   time TEXT
                   )
    ''')
    

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS commands (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ip TEXT,
                   command TEXT,
                   time TEXT
                   )
    ''')

    conn.commit()
    conn.close()

import requests
from datetime import datetime
import sqlite3

def insert_attack(
    ip,
    username,
    password,
    country,
    city,
    latitude,
    longitude,
    time
):

    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO attacks
        (
            ip,
            username,
            password,
            country,
            city,
            latitude,
            longitude,
            time
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',

        (
            ip,
            username,
            password,
            country,
            city,
            latitude,
            longitude,
            time
        )
    )

    conn.commit()

    conn.close()

def insert_command(ip, command, time):

    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO commands (ip, command, time) VALUES (?, ?, ?)",
        (ip, command, time)
    )

    conn.commit()

    conn.close()

def get_location(ip):

    # LOCAL NETWORK DEMO LOCATIONS

    if (
        ip.startswith("127.")
        or
        ip.startswith("192.")
        or
        ip.startswith("10.")
    ):

        return (
            "India",
            "Dehradun",
            "30.3165",
            "78.0322"
        )

    try:

        response = requests.get(
            f"http://ip-api.com/json/{ip}"
        )

        data = response.json()

        country = data.get(
            'country',
            'Unknown'
        )

        city = data.get(
            'city',
            'Unknown'
        )

        latitude = data.get(
            'lat',
            '0'
        )

        longitude = data.get(
            'lon',
            '0'
        )

        return (
            country,
            city,
            latitude,
            longitude
        )

    except:

        return (
            "Unknown",
            "Unknown",
            "0",
            "0"
        )