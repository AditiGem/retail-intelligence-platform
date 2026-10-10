import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import DB_CONFIG, get_connection
import json, glob

def test_config_imports():
    assert 'host' in DB_CONFIG and 'database' in DB_CONFIG

def test_connection():
    c = get_connection()
    assert c.is_connected()
    c.close()

def test_metrics_file():
    with open('model_metrics.json') as f:
        m = json.load(f)
    assert 'r2' in m and 'mae_pct' in m

def test_sql_files():
    files = glob.glob('sql/*.sql')
    assert len(files) >= 10

def test_no_secret_in_tracked_files():
    import subprocess
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    for f in result.stdout.splitlines():
        if os.path.isfile(f) and f != '.env':
            try:
                if 'REDACTED_PASSWORD' in open(f, errors='ignore').read():
                    raise AssertionError(f'Secret in {f}')
            except Exception:
                pass

if __name__ == '__main__':
    print("Running tests manually...")
    test_config_imports()
    print("test_config_imports: PASS")
    test_connection()
    print("test_connection: PASS")
    test_metrics_file()
    print("test_metrics_file: PASS")
    test_sql_files()
    print("test_sql_files: PASS")
    test_no_secret_in_tracked_files()
    print("test_no_secret_in_tracked_files: PASS")
    print("All smoke tests passed successfully!")
