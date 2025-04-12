import os

DB_CONFIG = {
    'host': os.getenv("CLUE_DB_HOST", "127.0.0.1"),
    'database': os.getenv("CLUE_DB"),
    'port': os.getenv("CLUE_DB_PORT", 5432),
    'user': os.getenv("CLUE_DB_USER"),
    'password': os.getenv("CLUE_DB_PWD", "XXX"),
}

SECRET_KEY = os.getenv("CLUE_SECRET_KEY")
