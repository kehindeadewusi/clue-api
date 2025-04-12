def test_query_uses_index(test_db_conn):
    """Tests if a query uses the expected index."""

    # ... setup data and define query ...

    with test_db_conn.cursor() as cur:
        cur.execute("EXPLAIN ANALYZE " + query)
        explain_output = cur.fetchall()

    # Parse explain_output to find if "Index Scan" is in the plan
    index_scan_used = any("Index Scan" in line for line in explain_output)
    assert index_scan_used, "Query did not use an index"
