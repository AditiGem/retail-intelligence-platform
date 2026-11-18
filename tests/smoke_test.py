"""
Smoke tests for the Retail Intelligence Platform.

These tests verify the project is reproducible from a fresh checkout:
  - Config loads and validates required environment variables
  - Database connection succeeds with valid credentials
  - Model metrics file exists and is valid JSON
  - All 10 SQL query files exist and execute cleanly
  - No secrets or credentials in tracked files or Git history

Run with:
    python -m pytest tests/smoke_test.py -v
or:
    python tests/smoke_test.py
"""

import sys
import os
import json
import glob
import re
import subprocess
import pytest

# Ensure project root is importable regardless of where pytest is invoked from
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import DB_CONFIG, validate_config, get_connection


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_config_imports():
    """DB_CONFIG should be loaded from environment variables."""
    assert 'host' in DB_CONFIG, "DB_CONFIG missing 'host'"
    assert 'database' in DB_CONFIG, "DB_CONFIG missing 'database'"
    assert 'user' in DB_CONFIG, "DB_CONFIG missing 'user'"
    assert 'password' in DB_CONFIG, "DB_CONFIG missing 'password'"


def test_config_validation_missing_env():
    """validate_config should raise EnvironmentError if required variables are missing."""
    orig_pwd = DB_CONFIG.get('password')
    try:
        DB_CONFIG['password'] = None
        with pytest.raises(EnvironmentError):
            validate_config()
    finally:
        DB_CONFIG['password'] = orig_pwd


def test_connection():
    """Live MySQL connection should succeed using config credentials."""
    c = get_connection()
    try:
        assert c.is_connected(), "MySQL connection reported not connected"
    finally:
        c.close()


def test_metrics_file():
    """model_metrics.json should exist and contain expected keys."""
    assert os.path.isfile('model_metrics.json'), \
        "model_metrics.json not found — run sales_forecast.py first"

    with open('model_metrics.json', encoding='utf-8') as f:
        m = json.load(f)

    for key in ('r2', 'train_r2', 'mae', 'mae_pct', 'rmse', 'rmse_pct', 'train_size', 'test_size'):
        assert key in m, f"model_metrics.json missing key: {key}"


def test_sql_files():
    """All 10 SQL analytics files should be present."""
    files = sorted(glob.glob('sql/*.sql'))
    assert len(files) == 10, \
        f"Expected exactly 10 SQL files, found {len(files)}: {files}"


def test_sql_queries_execution():
    """All 10 SQL query files should execute cleanly against the database."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        files = sorted(glob.glob('sql/*.sql'))
        for f in files:
            with open(f, encoding='utf-8') as sql_file:
                sql = sql_file.read()
            # Remove multi-statement or comments if any, then execute
            cursor.execute(sql)
            rows = cursor.fetchall()
            assert rows is not None, f"Query in {f} returned None"
        cursor.close()
    finally:
        conn.close()


def test_no_obvious_secrets_in_tracked_files():
    """
    Fail if any tracked file contains a hardcoded DB password pattern.
    Detects lines like: DB_PASSWORD=SomeActualPassword
    ignoring the placeholder in .env.example.
    """
    secret_pattern = re.compile(
        r'DB_PASSWORD\s*=\s*["\']?(?!your_password_here)[A-Za-z0-9@#!$%^&*_+\-]{6,}'
    )

    result = subprocess.run(
        ['git', 'ls-files'],
        capture_output=True,
        text=True,
        check=True,
    )

    offenders = []
    for f in result.stdout.splitlines():
        if not os.path.isfile(f):
            continue
        if f == '.env.example':
            continue
        if f == 'tests/smoke_test.py':
            continue
        try:
            content = open(f, encoding='utf-8', errors='ignore').read()
            if secret_pattern.search(content):
                offenders.append(f)
        except Exception:
            pass

    assert not offenders, f"Possible hardcoded DB password found in: {offenders}"


def test_no_compromised_password_in_history():
    """Verify that the previously compromised password string does not exist anywhere in git log -p."""
    res = subprocess.run(['git', 'log', '-p', '--all'], capture_output=True, text=True, errors='ignore').stdout
    # Check for the known compromised substring
    assert 'REDACTED_PASSWORD' not in res, "Compromised password string detected in git history!"


# ---------------------------------------------------------------------------
# Manual runner (python tests/smoke_test.py)
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("Running smoke tests manually...")
    print("-" * 60)

    test_config_imports()
    print("[PASS] test_config_imports")

    test_config_validation_missing_env()
    print("[PASS] test_config_validation_missing_env")

    test_connection()
    print("[PASS] test_connection")

    test_metrics_file()
    print("[PASS] test_metrics_file")

    test_sql_files()
    print("[PASS] test_sql_files")

    test_sql_queries_execution()
    print("[PASS] test_sql_queries_execution")

    test_no_obvious_secrets_in_tracked_files()
    print("[PASS] test_no_obvious_secrets_in_tracked_files")

    test_no_compromised_password_in_history()
    print("[PASS] test_no_compromised_password_in_history")

    print("-" * 60)
    print("All 8 smoke tests passed successfully.")
