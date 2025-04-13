"""Performance test.

The test checks if particular indexes are being used for the queries 
being executed by the API.
"""
import pytest
from clue_oda.api.report_api import (
    query_monthly_sales_summary, 
    query_monthly_sales_breakdown, 
    query_top_5_by_revenue
)

def parse_query(query:str, params:dict)->str:
    for k,v in params.items():
        query = query.replace(f"%({k})s", f"'{v}'")
    
    return query


def test_monthly_summary_uses_correct_partition(test_db_conn):
    """Tests if a query uses the expected index."""
    params = {
        "start_date": "2025-01-01",
        "end_date": "2025-01-31"
    }

    query = parse_query(query_monthly_sales_summary, params)
    import pdb; pdb.set_trace()
    # ... setup data and define query ...
    with test_db_conn.cursor() as cur:
        cur.execute("EXPLAIN ANALYZE " + query)
        explain_output = cur.fetchall()

    # Parse explain_output to find if correct partition sequence scan used in the plan
    found = any("Seq Scan on sales_report_2025_01" in line for line in explain_output)
    assert found, "Query did not scan correct partition."

    # Wrong partition not scanned. 
    found = any("Seq Scan on sales_report_2025_02" in line for line in explain_output)
    assert not found, "Query scanned wrong partition."
