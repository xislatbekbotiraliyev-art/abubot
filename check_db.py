import os
from dotenv import load_dotenv
from database.db import get_all_channels, init_db
import psycopg2

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

print(f"Database URL: {DATABASE_URL[:50]}...")

# Initialize database
init_db()

# Check movies
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute('SELECT code, title FROM movies')
movies = cursor.fetchall()

print(f"\n📊 Kinolar soni: {len(movies)}")
for movie in movies:
    print(f"  - Kod: {movie[0]}, Nomi: {movie[1]}")

# Check channels
cursor.execute('SELECT id, username, title FROM channels')
channels = cursor.fetchall()

print(f"\n📢 Kanallar soni: {len(channels)}")
for channel in channels:
    channel_id, username, title = channel
    display_name = title if title else (username if username else channel_id)
    print(f"  - {display_name}")
    print(f"    🆔 ID: {channel_id}")
    print(f"    👤 Username: {username if username else 'Yo\'q'}")
    print()

conn.close()
