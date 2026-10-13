"""
Smoke tests for the Retail Intelligence Platform.

These tests verify the project is reproducible from a fresh checkout:
  - Config loads without errors
  - Database connection succeeds
  - Model metrics file is valid JSON
  - All 10 SQL query files exist
  - No hardcoded DB password patterns in tracked files

Run with:
    python -m pytest tests/smoke_test.py -v
or:
    python tests/smoke_test.py
"""

import sys
import os
import json
import glob

# Ensure project root is importable regardless of where pytest is invoked from
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import DB_CONFIG, get_connection


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_config_imports():
    """DB_CONFIG should have been loaded from environment variables."""
    assert 'host' in DB_CONFIG, "DB_CONFIG missing 'host'"
    assert 'database' in DB_CONFIG, "DB_CONFIG missing 'database'"
    assert 'user' in DB_CONFIG, "DB_CONFIG missing 'user'"
    assert 'password' in DB_CONFIG, "DB_CONFIG missing 'password'"


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

    for key in ('r2', 'train_r2', 'mae', 'mae_pct', 'rmse', 'rmse_pct'):
        assert key in m, f"model_metrics.json missing key: {key}"


def test_sql_files():
    """All 10 SQL analytics files should be present."""
    files = sorted(glob.glob('sql/*.sql'))
    assert len(files) >= 10, \
        f"Expected at least 10 SQL files, found {len(files)}: {files}"


def test_no_obvious_secrets_in_tracked_files():
    """
    Fail if any tracked file contains a hardcoded DB password pattern.

    Detects lines like:  DB_PASSWORD=SomeActualPassword
    but ignores the placeholder in .env.example.
    """
    import subprocess
    import re

    # Match: DB_PASSWORD=<value> where value is NOT the literal placeholder
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

            continue  # template file is allowed to have the placeholder
        if f == 'tests/smoke_test.py':
            continue  # this test file contains the regex pattern itself
        try:
            content = open(f, encoding='utf-8', errors='ignore').read()
            if secret_pattern.search(content):
                offenders.append(f)
        except Exception:
            # Binary files or permission errors — skip
            pass

    assert not offenders, \
        f"Possible hardcoded DB password found in: {offenders}"


# ---------------------------------------------------------------------------
# Manual runner (python tests/smoke_test.py)
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("Running smoke tests manually...")
    print("-" * 60)

    test_config_imports()
    print("[PASS] test_config_imports")

    test_connection()
    print("[PASS] test_connection")

    test_metrics_file()
    print("[PASS] test_metrics_file")

    test_sql_files()
    print("[PASS] test_sql_files")

    test_no_obvious_secrets_in_tracked_files()
    print("[PASS] test_no_obvious_secrets_in_tracked_files")

    print("-" * 60)
    print("All 5 smoke tests passed successfully.")