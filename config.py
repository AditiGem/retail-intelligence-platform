# config.py
"""Central configuration loader. Reads credentials from environment."""
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host':     os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'retail_intelligence'),
    'user':     os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '')
}

def validate_config():
    """Raise a clear error if required env vars are missing."""
    missing = [k for k, v in DB_CONFIG.items() if k != 'host' and not v]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables for: {missing}. "
            f"Copy .env.example to .env and fill in values."
        )

def get_connection():
    """Return a live MySQL connection using DB_CONFIG."""
    import mysql.connector
    validate_config()
    return mysql.connector.connect(**DB_CONFIG)
