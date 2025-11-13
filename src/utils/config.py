import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# JSON Input paths
JSON_FILE_PATH = os.path.join(BASE_DIR, "data", "fake_property_data_new.json")

# Malformed JSON records output
MALFORMED_PATH = os.path.join(BASE_DIR, "audit_logs", "malformed_records.json")

# Audit CSV output
CSV_REPORT_PATH = os.path.join(BASE_DIR, "audit_logs", "table_count_comparison.csv")

# Batch size for ingestion
BATCH_SIZE = 500

# Database config for MySQL
DB_CONFIG = {
    "user": "db_user",
    "password": "6equj5_db_user",
    "host": "localhost",
    "database": "home_db"
}
