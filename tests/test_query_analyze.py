"""Performance test.

The test checks if particular indexes are being used for the queries 
being executed by the API.
"""
from clue_oda.api.report_api import (
    query_monthly_sales_summary, 
    query_monthly_sales_breakdown, 
    query_top_5_by_revenue
)
from . import parse_query


def test_monthly_summary_uses_correct_partition(test_db_conn):
    """Tests if a query uses the expected index."""
    params = {
        "start_date": "2025-01-01",
        "end_date": "2025-01-31"
    }

    query = parse_query(query_monthly_sales_summary, params)
    
    with test_db_conn.cursor() as cur:
        cur.execute("EXPLAIN ANALYZE " + query)
        explain_output = cur.fetchall()

    # Parse explain_output to find if correct partition sequence scan used in the plan
    explain_output = str(explain_output)
    found = "Scan on sales_report_2025_01" in explain_output
    assert found, "Query did not scan correct partition."

    # Wrong partition not scanned. 
    found = "Scan on sales_report_2025_02" in explain_output
    assert not found, "Query scanned wrong partition."


def test_monthly_breakdown_uses_correct_partition(test_db_conn):
    """Tests if a query uses the expected index."""
    params = {
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "product_name": "Widget A",
        "region": "North"
    }

    query = parse_query(query_monthly_sales_breakdown, params)
    
    with test_db_conn.cursor() as cur:
        cur.execute("EXPLAIN ANALYZE " + query)
        explain_output = cur.fetchall()
    
    # Parse explain_output to find if correct partition sequence scan used in the plan
    explain_output = str(explain_output)
    found = "Scan on sales_report_2025_01" in explain_output
    assert found, "Query did not scan correct partition."

    # Wrong partition not scanned. 
    found = "Scan on sales_report_2025_02" in explain_output
    assert not found, "Query scanned wrong partition."

    found = "Index Scan on idx_region_2025_01" in explain_output
    assert found, "Query did not use expected partition product name index."

    found = "Index Scan on idx_region_2025_01" in explain_output
    assert found, "Query did not use expected partition region index."


def test_top_5_uses_correct_partitions(test_db_conn):
    """Tests if a query uses the expected index."""
    params = {
        "start_date": "2025-01-01",
        "end_date": "2025-02-28",
    }

    query = parse_query(query_top_5_by_revenue, params)
    
    with test_db_conn.cursor() as cur:
        cur.execute("EXPLAIN ANALYZE " + query)
        explain_output = cur.fetchall()
    
    # Parse explain_output to find if correct partition sequence scan used in the plan
    explain_output = str(explain_output)
    found = "Scan on sales_report_2025_01" in explain_output
    assert found, "Query did not scan correct partition."

    # Wrong partition not scanned. 
    found = "Scan on sales_report_2025_02" in explain_output
    assert found, "Query scanned wrong partition."
