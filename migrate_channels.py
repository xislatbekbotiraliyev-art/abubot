"""
Migration script to update channels table structure
Run this once to migrate from old username-only format to new id/username/title format
"""
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

# Determine which database to use
if DATABASE_URL and DATABASE_URL.startswith('postgresql'):
    import psycopg2
    
    def get_connection():
        return psycopg2.connect(DATABASE_URL)
    
    DB_TYPE = 'postgresql'
else:
    import sqlite3
    
    DB_NAME = 'bot_database.db'
    
    def get_connection():
        return sqlite3.connect(DB_NAME)
    
    DB_TYPE = 'sqlite'

logger.info(f"Using {DB_TYPE} database")


def migrate():
    """Migrate channels table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check if old table exists
        if DB_TYPE == 'postgresql':
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'channels'
            """)
        else:
            cursor.execute("PRAGMA table_info(channels)")
        
        columns = cursor.fetchall()
        logger.info(f"Current columns: {columns}")
        
        # Check if we need to migrate
        if DB_TYPE == 'postgresql':
            column_names = [col[0] for col in columns]
        else:
            column_names = [col[1] for col in columns]
        
        if 'id' in column_names:
            logger.info("Table already migrated!")
            return
        
        logger.info("Starting migration...")
        
        # Get existing channels
        cursor.execute("SELECT username FROM channels")
        old_channels = cursor.fetchall()
        logger.info(f"Found {len(old_channels)} channels to migrate")
        
        # Create new table
        cursor.execute("DROP TABLE IF EXISTS channels_old")
        cursor.execute("ALTER TABLE channels RENAME TO channels_old")
        
        cursor.execute('''
            CREATE TABLE channels (
                id TEXT PRIMARY KEY,
                username TEXT,
                title TEXT
            )
        ''')
        
        # Migrate data
        for (username,) in old_channels:
            # Use username as ID for old channels
            cursor.execute(
                'INSERT INTO channels (id, username, title) VALUES (%s, %s, %s)' if DB_TYPE == 'postgresql' 
                else 'INSERT INTO channels (id, username, title) VALUES (?, ?, ?)',
                (username, username, None)
            )
            logger.info(f"Migrated: {username}")
        
        # Drop old table
        cursor.execute("DROP TABLE channels_old")
        
        conn.commit()
        logger.info("Migration completed successfully!")
        
    except Exception as e:
        logger.error(f"Migration error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    try:
        migrate()
        print("\n✅ Migration completed successfully!")
        print("You can now use the new channel features.")
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)
