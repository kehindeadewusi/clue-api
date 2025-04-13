import psycopg2
import csv
import yaml

from . import pandas_importer as pi
from .db import get_db

def get_schema(schema_path: str):
    """Reads a YAML file and convert to a dictionary.

    Args:
        schema_path: The path to the YAML file.

    Returns:
        dict: A Python dictionary or None.
    
    """
    try:
        with open(schema_path, 'r') as f:
            data = yaml.safe_load(f)
            return data
    except FileNotFoundError:
        print(f"Error: YAML file not found at {schema_path}")
        raise
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {schema_path}")
        raise


def load_csv(csv_path:str, schema_path:str, table: str, error_log_table:str):
    """Loads data from a CSV file into a PostgreSQL table, with validation.

    Loads data from a CSV file into a PostgreSQL table using COPY. It validates
    records meaning that it won't fail because of a single bad record.

    Args:
        csv_path: Path to the CSV file.
        schema_path: a YAML schema that is passed to a dict e.g. {'id': 'integer', 'amount': 'numeric'}.
            It is used for simple data type checking for validation.
        table: Name of the PostgreSQL table.
        error_log_table: The table to store the records that fail validation.
    """
    conn = None
    column_types = get_schema(schema_path)

    try:
        conn = get_db()
        cur = conn.cursor()

        with open(csv_path, 'r') as f:
            reader = csv.reader(f)

            csv_header = next(reader)
            if column_types and set(csv_header) != set(column_types.keys()):
                raise ValueError("CSV headers and schema keys must match. One key for each header.")
            
            # Create a temp table with text columns for staging
            staging_table = f"temp_{table}"
            temp_table_columns = ", ".join([f"{col} TEXT" for col in csv_header])
            
            # staging table, we insert validated records here.
            cur.execute(f"DROP TABLE IF EXISTS {staging_table}")
            conn.commit()
            cur.execute(f"CREATE TABLE {staging_table} ({temp_table_columns})")
            conn.commit()
            
            # and validation log table
            cur.execute(f"DROP TABLE IF EXISTS {error_log_table}")
            conn.commit()
            cur.execute(f"CREATE TABLE {error_log_table} ({temp_table_columns})")
            conn.commit()

            # Load data into the temporary staging table (efficiently)
            # Using Pandas for this, to manipulate types.
            print("saving with Pandas...")
            pi.save_with_pandas(csv_path, column_types, staging_table, error_log_table)
            print("done saving with Pandas")

            target_columns = list(column_types.keys())
            select_columns = ", ".join([col for col in column_types])
            insert_query = f"INSERT INTO {table} ({', '.join(target_columns)}) SELECT {select_columns} FROM {staging_table}"
            
            try:
                cur.execute(insert_query)
                conn.commit()
                print(f"Successfully loaded and validated data from '{csv_path}' into '{table}'.")
            except psycopg2.Error as e:
                conn.rollback()
                print("Error during data insertion")
                raise
    except (psycopg2.Error, ValueError) as e:
        if conn:
            conn.rollback()
        print("Error loading data")
        raise
    finally:
        if conn:
            cur.close()
            conn.close()
