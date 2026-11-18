# config.py
"""Central configuration loader. Reads credentials from environment."""
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host':     os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'retail_intelligence'),
    'user':     os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD')
}

def validate_config():
    """Raise a clear error if required env vars are missing or empty."""
    required = ['host', 'database', 'user', 'password']
    missing = [k for k in required if not DB_CONFIG.get(k)]
    if missing:
        env_names = [f"DB_{k.upper()}" for k in missing]
        raise EnvironmentError(
            f"Missing required database environment variable(s): {', '.join(env_names)}. "
            f"Please populate them in .env (see .env.example for template)."
        )

def get_connection():
    """Return a live MySQL connection using centralized DB_CONFIG."""
    import mysql.connector
    validate_config()
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        # Sanitize error message to prevent leaking sensitive information
        raise ConnectionError(
            f"Database connection failed: {err.msg} (Error Code: {err.errno})"
        ) from None
