import pandas as pd
from sqlalchemy import create_engine
import io
from clue_api.settings import DB_CONFIG


def get_connection():
    conn_str = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    conn_str = conn_str.format(**DB_CONFIG)

    return create_engine(conn_str)

def save_with_pandas(csv_path:str, schema:dict, table:str, error_log_table:str):
    df = pd.read_csv(csv_path)

    # supports a few data types only
    for k,v in schema.items():
        if v == 'int':
            df[k] = df[k].astype('int')
        elif v == 'date':
            df[k] = pd.to_datetime(df[k], format='%Y-%m-%d', errors='coerce')
        elif v == 'float':
            df[k] = pd.to_numeric(df[k], errors='coerce').astype('float')
        else: #v == 'str':
            df[k] = df[k].astype('str')
    
    #truncate existing table
    engine = get_connection()
    df.head(0).to_sql(table, engine, if_exists='replace',index=False)
    
    bad_records = df[df.isnull().any(axis=1)] #assuming all nulls are unacceptable.
    df = df.dropna()

    write_records(engine, df, table)
    write_records(engine, bad_records, error_log_table)


def write_records(engine, df, table:str):
    conn = None
    cur = None
    try:
        conn = engine.raw_connection()
        cur = conn.cursor()
        output = io.StringIO()

        df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        _ = output.getvalue()
        
        cur.copy_from(output, table)
        conn.commit()
    except:
        raise
    finally:
        cur.close()
        conn.close()
