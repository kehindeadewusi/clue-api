import psycopg2
from clue_oda.settings import DB_CONFIGS

def get_db():
    DB_CONFIG = DB_CONFIGS.get("default")
    
    return psycopg2.connect(**DB_CONFIG)

def get_conn_str():
    conn_str = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    DB_CONFIG = DB_CONFIGS.get("default")

    return conn_str.format(**DB_CONFIG)
