import os
import logging
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

# Determine which database to use
if DATABASE_URL and DATABASE_URL.startswith('postgresql'):
    # Use PostgreSQL
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    def get_connection():
        """Get PostgreSQL connection"""
        return psycopg2.connect(DATABASE_URL)
    
    DB_TYPE = 'postgresql'
    logger.info("Using PostgreSQL database")
else:
    # Use SQLite (fallback for local development)
    import sqlite3
    
    DB_NAME = 'bot_database.db'
    
    def get_connection():
        """Get SQLite connection"""
        return sqlite3.connect(DB_NAME)
    
    DB_TYPE = 'sqlite'
    logger.info("Using SQLite database")


def init_db():
    """Initialize database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if DB_TYPE == 'postgresql':
        # PostgreSQL syntax
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                code TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                genre TEXT,
                duration TEXT,
                video_file_id TEXT,
                video_link TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id TEXT PRIMARY KEY,
                username TEXT,
                title TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                user_id BIGINT PRIMARY KEY
            )
        ''')
    else:
        # SQLite syntax
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                code TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                genre TEXT,
                duration TEXT,
                video_file_id TEXT,
                video_link TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id TEXT PRIMARY KEY,
                username TEXT,
                title TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY
            )
        ''')
    
    conn.commit()
    conn.close()
    logger.info(f"Database tables created successfully ({DB_TYPE})")


# Movie operations
def add_movie(code: str, title: str, description: str, genre: str, 
              duration: str, video_file_id: str = None, video_link: str = None) -> bool:
    """Add a new movie to database"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO movies (code, title, description, genre, duration, video_file_id, video_link)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''' if DB_TYPE == 'postgresql' else '''
            INSERT INTO movies (code, title, description, genre, duration, video_file_id, video_link)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (code, title, description, genre, duration, video_file_id, video_link))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.warning(f"Movie with code {code} already exists or error: {e}")
        return False


def get_movie(code: str) -> Optional[Tuple]:
    """Get movie by code"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM movies WHERE code = %s' if DB_TYPE == 'postgresql' else 'SELECT * FROM movies WHERE code = ?',
            (code,)
        )
        movie = cursor.fetchone()
        conn.close()
        return movie
    except Exception as e:
        logger.error(f"Error getting movie: {e}")
        return None


def delete_movie(code: str) -> bool:
    """Delete movie by code"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM movies WHERE code = %s' if DB_TYPE == 'postgresql' else 'DELETE FROM movies WHERE code = ?',
            (code,)
        )
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
    except Exception as e:
        logger.error(f"Error deleting movie: {e}")
        return False


# Channel operations
def add_channel(channel_id: str, username: str = None, title: str = None) -> bool:
    """Add a channel to database"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO channels (id, username, title) VALUES (%s, %s, %s)' if DB_TYPE == 'postgresql' else 'INSERT INTO channels (id, username, title) VALUES (?, ?, ?)',
            (channel_id, username, title)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.warning(f"Channel {channel_id} already exists or error: {e}")
        return False


def remove_channel(channel_id: str) -> bool:
    """Remove a channel from database"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM channels WHERE id = %s' if DB_TYPE == 'postgresql' else 'DELETE FROM channels WHERE id = ?',
            (channel_id,)
        )
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
    except Exception as e:
        logger.error(f"Error removing channel: {e}")
        return False


def get_all_channels() -> List[Tuple[str, str, str]]:
    """Get all channels - returns list of (id, username, title)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, title FROM channels')
        channels = cursor.fetchall()
        conn.close()
        return channels
    except Exception as e:
        logger.error(f"Error getting channels: {e}")
        return []


# Admin operations
def is_admin(user_id: int) -> bool:
    """Check if user is admin (from environment variable)"""
    admin_ids_str = os.environ.get('ADMIN_IDS', '')
    if not admin_ids_str:
        return False
    
    admin_ids = [int(id.strip()) for id in admin_ids_str.split(',') if id.strip()]
    return user_id in admin_ids


def add_admin(user_id: int) -> bool:
    """Add admin to database"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO admins (user_id) VALUES (%s)' if DB_TYPE == 'postgresql' else 'INSERT INTO admins (user_id) VALUES (?)',
            (user_id,)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False
