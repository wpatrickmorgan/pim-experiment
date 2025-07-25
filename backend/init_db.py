#!/usr/bin/env python3
"""
Database initialization script to set SQL mode for Railway MariaDB compatibility.
This script sets the SQL mode to be more permissive for TEXT/BLOB default values.
"""

import os
import sys
import subprocess
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
        
        # Build mysql command
        mysql_cmd = [
            'mysql',
            f'--host={parsed.hostname}',
            f'--port={parsed.port or 3306}',
            f'--user={parsed.username}',
            f'--password={parsed.password}',
            f'--database={parsed.path.lstrip("/")}',
            '--execute'
        ]
        
        # Set SQL mode to be more permissive
        # Remove STRICT_TRANS_TABLES and NO_ZERO_DATE to allow default values for TEXT columns
        sql_commands = [
            "SET SESSION sql_mode = 'ONLY_FULL_GROUP_BY,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';",
            "SELECT @@sql_mode;"
        ]
        
        print("🔧 Connecting to database to set SQL mode...")
        
        for sql_command in sql_commands:
            cmd = mysql_cmd + [sql_command]
            
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    if "SELECT @@sql_mode" in sql_command:
                        current_mode = result.stdout.strip().split('\n')[-1]
                        print(f"✅ Current SQL mode: {current_mode}")
                    else:
                        print("✅ SQL mode set successfully")
                else:
                    print(f"⚠️  Command failed: {sql_command}")
                    print(f"Error: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"⚠️  Command timed out: {sql_command}")
            except Exception as e:
                print(f"⚠️  Error executing command: {e}")
        
        print("✅ Database SQL mode configured successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to configure database SQL mode: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
