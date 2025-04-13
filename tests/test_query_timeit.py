import timeit
from clue_oda.api.report_api import query_monthly_sales_breakdown
from . import parse_query

def execute_query(conn, query):
    """Executes a query and returns the result."""
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def test_performance_monthly_breakdown(test_db_conn):
    params = {
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "product_name": "Widget A",
        "region": "North"
    }

    query = parse_query(query_monthly_sales_breakdown, params)

    def run_query():
        execute_query(test_db_conn, query)

    execution_time = timeit.timeit(run_query, number=100) / 100  # Execute and get average over 100 runs
    print(f"Average execution time: {execution_time} seconds")

    # Assert Performance, sorta stochastic. Maybe based on observations to get a reasonable execution time.
    assert execution_time < 1.5, "Execution time exceeded avg threshold"
