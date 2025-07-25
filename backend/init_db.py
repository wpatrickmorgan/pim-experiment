#!/usr/bin/env python3
"""
Database initialization script to set SQL mode for Railway MariaDB compatibility.
This script sets the SQL mode to be more permissive for TEXT/BLOB default values.
"""

import os
import sys
import MySQLdb
from urllib.parse import urlparse

def init_database():
    """Initialize database with proper SQL mode settings."""
    
    # Parse DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found")
        return False
    
    try:
        parsed = urlparse(database_url)
        
        # Connect to database
        print("🔧 Connecting to database to set SQL mode...")
        conn = MySQLdb.connect(
            host=parsed.hostname,
            port=parsed.port or 3306,
            user=parsed.username,
            passwd=parsed.password,
            db=parsed.path.lstrip('/'),
            charset='utf8mb4'
        )
        
        cursor = conn.cursor()
        
        # Set SQL mode to be more permissive
        # Remove STRICT_TRANS_TABLES and NO_ZERO_DATE to allow default values for TEXT columns
        sql_mode_query = """
        SET SESSION sql_mode = 'ONLY_FULL_GROUP_BY,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
        """
        
        cursor.execute(sql_mode_query)
        
        # Also set it globally if we have permissions
        try:
            global_sql_mode_query = """
            SET GLOBAL sql_mode = 'ONLY_FULL_GROUP_BY,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
            """
            cursor.execute(global_sql_mode_query)
            print("✅ Set global SQL mode successfully")
        except MySQLdb.Error as e:
            print(f"⚠️  Could not set global SQL mode (this is normal for Railway): {e}")
        
        # Verify current SQL mode
        cursor.execute("SELECT @@sql_mode")
        current_mode = cursor.fetchone()[0]
        print(f"✅ Current SQL mode: {current_mode}")
        
        cursor.close()
        conn.close()
        
        print("✅ Database SQL mode configured successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to configure database SQL mode: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
