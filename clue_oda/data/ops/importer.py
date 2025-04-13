import psycopg2
from .db import get_db


def load_csv(csv_path:str, table:str) -> None:
    """Loads data from a CSV file into a PostgreSQL table.

    Args:
        csv_path: The path to the CSV file.
        table: PostgreSQL table to load into.
    Returns:
        None
    """
    conn = None
    
    try:
        conn = get_db()
        cur = conn.cursor()

        with open(csv_path, 'r') as f:
            print("inferring column headers from CSV")
            csv_header = next(f)
            csv_header = csv_header.strip()
            columns = csv_header.split(",")
            print(columns)

            cur.copy_from(
                file=f,
                table=table,
                sep=',',  # Assuming a strictly comma-delimited file.
                null='NULL', # Specify how NULL values are represented in the CSV
                columns=columns # We need to specify the columns, in case table has more columns.
            )

        conn.commit()
        print(F"successfully loaded CSV data into {table}")
    except psycopg2.Error as e:
        conn.rollback()
        raise
    finally:
        if conn:
            cur.close()
            conn.close()
