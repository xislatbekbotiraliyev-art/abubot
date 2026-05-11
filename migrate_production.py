"""
Production database migration script
Run this on Render or with DATABASE_URL environment variable
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Load .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL or not DATABASE_URL.startswith('postgresql'):
    print("❌ DATABASE_URL not found or not PostgreSQL!")
    print("This script is for production PostgreSQL database only.")
    print(f"Current DATABASE_URL: {DATABASE_URL}")
    sys.exit(1)

import psycopg2

def get_connection():
    return psycopg2.connect(DATABASE_URL)

logger.info("Using PostgreSQL database")


def migrate():
    """Migrate channels table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check current table structure
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'channels'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns]
        logger.info(f"Current columns: {column_names}")
        
        # Check if we need to migrate
        if 'id' in column_names:
            logger.info("✅ Table already migrated!")
            return
        
        logger.info("Starting migration...")
        
        # Get existing channels
        cursor.execute("SELECT username FROM channels")
        old_channels = cursor.fetchall()
        logger.info(f"Found {len(old_channels)} channels to migrate")
        
        # Rename old table
        cursor.execute("ALTER TABLE channels RENAME TO channels_old")
        
        # Create new table
        cursor.execute('''
            CREATE TABLE channels (
                id TEXT PRIMARY KEY,
                username TEXT,
                title TEXT
            )
        ''')
        
        # Migrate data
        for (username,) in old_channels:
            cursor.execute(
                'INSERT INTO channels (id, username, title) VALUES (%s, %s, %s)',
                (username, username, None)
            )
            logger.info(f"Migrated: {username}")
        
        # Drop old table
        cursor.execute("DROP TABLE channels_old")
        
        conn.commit()
        logger.info("✅ Migration completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Migration error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    try:
        migrate()
        print("\n✅ Production database migration completed!")
        print("You can now use the new channel features.")
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
