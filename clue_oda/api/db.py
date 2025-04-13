import psycopg2
from clue_oda.settings import DB_CONFIGS
from flask import current_app, g

def get_db():
    if 'db' not in g:
        db_key = current_app.config['DATABASE']
        DB_CONFIG = DB_CONFIGS.get(db_key) # test or default.
        g.db = psycopg2.connect(**DB_CONFIG)
    
    return g.db
