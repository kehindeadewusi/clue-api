import pytest
import psycopg2
import timeit

# Assuming you have a fixture named 'test_db_conn' that provides a PostgreSQL connection
# (e.g., using pytest-postgresql)

def execute_query(conn, query):
    """Executes a query and returns the result."""
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def test_select_products_by_category(test_db_conn):
    """Tests the performance of selecting products by category."""

    # 1. Prepare Test Data (in a real test, you'd likely have a setup function)
    with test_db_conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS products (id SERIAL PRIMARY KEY, name TEXT, category TEXT, price DECIMAL);")
        cur.execute("INSERT INTO products (name, category, price) VALUES ('Laptop', 'Electronics', 1200.00), ('Mouse', 'Electronics', 25.00), ('T-shirt', 'Clothing', 30.00);")

    # 2. Define the Query
    query = "SELECT name, price FROM products WHERE category = 'Electronics';"

    # 3. Measure Execution Time
    def run_query():
        execute_query(test_db_conn, query)

    execution_time = timeit.timeit(run_query, number=100) / 100  # Average over 100 runs
    print(f"Average execution time: {execution_time} seconds")

    # 4. Assert Performance
    assert execution_time < 0.01, "Query execution time exceeded threshold"

    # 5. (Optional) Validate Results
    results = execute_query(test_db_conn, query)
    assert len(results) == 2, "Incorrect number of products returned"
    assert results[0][0] == 'Laptop', "Incorrect product name"
