import os
from dotenv import load_dotenv

load_dotenv('config.env', override=True)

DB_NAME = os.environ.get('DB_NAME', '')
DB_NAME = 'postgres' if len(DB_NAME) == 0 else DB_NAME

DB_HOST = os.environ.get('DB_HOST', '')
DB_HOST = 'localhost' if len(DB_HOST) == 0 else DB_HOST

DB_PORT = os.environ.get('DB_PORT', '5432')
DB_PORT = 5432 if len(DB_PORT) == 0 else DB_PORT

DB_USER = os.environ.get('DB_USER', '')
if not DB_USER:
    print("Database error: \"DB_USER\" environment variable is missing")
    exit(1)

DB_PASS = os.environ.get('DB_PASS', '')
if not DB_PASS:
    print("Database error: \"DB_PASS\" environment variable is missing")
    exit(1)
