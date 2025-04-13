import os

DB_CONFIGS = {
    "default": {
        'host': os.getenv("CLUE_DB_HOST", "127.0.0.1"),
        'database': os.getenv("CLUE_DB"),
        'port': os.getenv("CLUE_DB_PORT", 5432),
        'user': os.getenv("CLUE_DB_USER"),
        'password': os.getenv("CLUE_DB_PWD", "XXX"),
    },
    "test": {
        'host': os.getenv("CLUE_TEST_DB_HOST", "127.0.0.1"),
        'database': os.getenv("CLUE_TEST_DB"),
        'port': os.getenv("CLUE_TEST_DB_PORT", 5432),
        'user': os.getenv("CLUE_TEST_DB_USER"),
        'password': os.getenv("CLUE_TEST_DB_PWD", "XXX"),
    }
}

SECRET_KEY = os.getenv("CLUE_SECRET_KEY", "dev")
