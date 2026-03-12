import sqlite3
from common import *
from flask import flash

    
def init_db():
    conn = sqlite3.connect('websites.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            name_data TEXT,
            price_data TEXT,
            updated_data TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            gmap TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_all_websites():
    conn = sqlite3.connect('websites.db')
    c = conn.cursor()
    c.execute('SELECT id, url, name_data, price_data, updated_data, last_updated, gmap FROM websites')
    websites = c.fetchall()
    conn.close()
    return websites

def add_website(url, name_data="", price_data="", updated_data="", gmap_link=''):
    conn = sqlite3.connect('websites.db')
    c = conn.cursor()
    c.execute('SELECT id FROM websites WHERE url = ?', (url,))
    existing = c.fetchone()
    if existing:
        flash('Url exist')
        return
    c.execute('''
        INSERT INTO websites (url, name_data, price_data, updated_data, last_updated, gmap) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (url, name_data, price_data, updated_data, get_time(), gmap_link))
    conn.commit()
    conn.close()

def delete_website(website_id):
    conn = sqlite3.connect('websites.db')
    c = conn.cursor()
    c.execute('DELETE FROM websites WHERE id = ?', (website_id,))
    conn.commit()
    conn.close()

def update_website_name(website_id):
    conn = sqlite3.connect('websites.db')
    c = conn.cursor()
    c.execute(f"UPDATE websites SET last_updated = ? WHERE id = ?", (get_time(), website_id))
    conn.commit()
    conn.close()

def update_website_data(website_id, name_data, price_data, updated_data, gmap_link):
    conn = sqlite3.connect('websites.db')
    c = conn.cursor()
    c.execute(f'''
        UPDATE websites 
        SET name_data = ?, price_data = ?, updated_data = ?, last_updated = ?, gmap = ?
        WHERE id = ?
    ''', (name_data, price_data, updated_data, get_time(), gmap_link, website_id))
    conn.commit()
    conn.close()
