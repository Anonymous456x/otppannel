import sqlite3
import datetime

DB_NAME = "otp_bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        joined_at TEXT,
        total_otps INTEGER DEFAULT 0
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS otp_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        number TEXT,
        service TEXT,
        country TEXT,
        country_code TEXT,
        otp TEXT,
        requested_at TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS sent_otps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT,
        country TEXT,
        country_code TEXT,
        otp TEXT,
        sent_at TEXT
    )''')
    
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO users (user_id, username, first_name, joined_at)
                 VALUES (?, ?, ?, ?)''', 
              (user_id, username, first_name, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def log_otp(user_id, number, service, country, country_code, otp):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO otp_logs (user_id, number, service, country, country_code, otp, requested_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (user_id, number, service, country, country_code, otp, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def log_sent_otp(number, country, country_code, otp):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO sent_otps (number, country, country_code, otp, sent_at)
                 VALUES (?, ?, ?, ?, ?)''',
              (number, country, country_code, otp, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_user_otp_count(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM otp_logs WHERE user_id = ?", (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count
