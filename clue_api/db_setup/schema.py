import psycopg2
from clue_api.settings import DB_CONFIG

def read_query_from_file(filepath):
    """Reads text from the specified file.
    
    Reads text from a specified part. This is used as a helper to read SQL 
    files.
    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found at {filepath}")
        raise
    

def create_sales_table(script_path:str):
    """Creates sales table in PostgreSQL."""
    query = read_query_from_file(script_path)

    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute(query)
        conn.commit()
        print("Successfully created table.")
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"Error creating table: {e}")

    finally:
        if conn:
            cur.close()
            conn.close()


def create_monthly_partitions(table: str, start_year:int, end_year:int) -> None:
    """Creates monthly partitions between start and end year.
    
    The table must be partitioned already
    """

    if end_year < start_year:
        raise ValueError("Invalid year inputs.")
    
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                start_date = f"{year}-{month:02d}-01"
                next_month = month + 1
                next_year = year
                if next_month > 12:
                    next_month = 1
                    next_year += 1
                end_date = f"{next_year}-{next_month:02d}-01"
                partition_name = f"{table}_{year}_{month:02d}"

                create_partition_query = f"""
                    CREATE TABLE {partition_name} PARTITION OF {table}
                    FOR VALUES FROM ('{start_date}') TO ('{end_date}');
                """
                cur.execute(create_partition_query)
                print(f"Created partition: {partition_name} for dates from {start_date} to {end_date}")

                #create indexes for the partitions
                partition_name_4_index = f"{year}_{month:02d}" #shorter

                # add product name index per-partition
                product_name_idx_query = f"""
                    CREATE INDEX idx_pname_{partition_name_4_index} ON {partition_name} (product_name)
                """
                cur.execute(product_name_idx_query)
                print(f"Created product name partition index for {partition_name}")

                # add region index per-partition
                region_idx_query = f"""
                    CREATE INDEX idx_region_{partition_name_4_index} ON {partition_name} (region);
                """
                cur.execute(region_idx_query)
                print(f"Created region partition index for {partition_name}")

        # Create a default partition for all other data that don't have a partition
        default_partition = f"{table}_other"
        create_default_partition_query = f"""
            CREATE TABLE {default_partition} PARTITION OF {table}
            DEFAULT;
        """
        cur.execute(create_default_partition_query)
        print(f"Created default partition: {table}_other")
        
        create_default_product_name_index = f"""
            CREATE INDEX idx_pname_{table}_others ON {default_partition} (product_name)
        """
        cur.execute(create_default_product_name_index)
        print(f"Created product name index on default {default_partition}")

        create_default_region_index = f"""
            CREATE INDEX idx_region_{table}_others ON {default_partition} (region)
        """
        cur.execute(create_default_region_index)
        print(f"Created region index on default {default_partition}")

        conn.commit()
        print("Successfully created monthly partitions.")
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            cur.close()
            conn.close()
