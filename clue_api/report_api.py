from flask import Blueprint, jsonify, request

from clue_api.db import get_db
import psycopg2


bp = Blueprint('reports', __name__, url_prefix="/reports")

query_monthly_sales_summary = """
    SELECT
        TO_CHAR(sr.sales_date, 'YYYY-MM') AS month,
        SUM(sr.sales_amount) AS revenue,
        SUM(sr.quantity_sold) AS quantity
    FROM sales_report sr
    WHERE
        (%(start_date)s IS NULL OR sr.sales_date >= %(start_date)s::DATE)
        AND
        (%(end_date)s IS NULL OR sr.sales_date <= %(end_date)s::DATE)
    GROUP BY month
    ORDER BY month
"""
@bp.route('/monthly-sales-summary', methods=['GET'])
def monthly_sales_summary():
    conn = get_db()
    if conn is None:
        return jsonify({'error': 'Error connecting to the database'}), 500
    
    cursor = conn.cursor()

    results = []
    status_code = 200

    params = {
        'start_date': request.args.get('start_date'), # Expected format: YYYY-MM-DD
        'end_date': request.args.get('end_date')
    }

    try:
        cursor.execute(query_monthly_sales_summary, params)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': f'Internal error: {e}'}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(results), status_code

query_monthly_sales_breakdown = """
    SELECT
        TO_CHAR(sr.sales_date, 'YYYY-MM') AS month,
        sr.product_name,
        sr.region,
        SUM(sr.sales_amount) AS revenue,
        SUM(sr.quantity_sold) AS quantity
    FROM sales_report sr
    WHERE
        (%(product_name)s IS NULL OR sr.product_name = %(product_name)s)
        AND
        (%(region)s IS NULL OR sr.region = %(region)s)
        AND
        (%(start_date)s IS NULL OR sr.sales_date >= %(start_date)s::DATE)
        AND
        (%(end_date)s IS NULL OR sr.sales_date <= %(end_date)s::DATE)
    GROUP BY month, sr.product_name, sr.region
    ORDER BY month, sr.product_name, sr.region;
"""
@bp.route('/monthly-sales-breakdown', methods=['GET'])
def monthly_sales_breakdown():
    conn = get_db()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    cursor = conn.cursor()

    params = {
        'product_name': request.args.get('product'),
        'region': request.args.get('region'),
        'start_date': request.args.get('start_date'), # Expected format: YYYY-MM-DD
        'end_date': request.args.get('end_date')
    }

    try:
        cursor.execute(query_monthly_sales_breakdown, params)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(results), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': f'Internal error: {e}'}), 500
    finally:
        cursor.close()
        conn.close()


query_top_5_by_revenue = """
    SELECT 
        RANK() over (order by sum(sales_amount) desc) as rank, 
        MAX(product_name) as product_name, 
        product_id, 
        SUM(sales_amount) as revenue 
    FROM sales_report sr
    WHERE
        (%(start_date)s IS NULL OR sr.sales_date >= %(start_date)s::DATE)
        AND
        (%(end_date)s IS NULL OR sr.sales_date <= %(end_date)s::DATE)
    GROUP BY product_id 
    ORDER BY revenue desc 
    LIMIT 5
"""

@bp.route('/top-5-by-revenue', methods=['GET'])
def top_5_by_revenue():
    conn = get_db()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    cursor = conn.cursor()

    params = {
        'start_date': request.args.get('start_date'), # Expected format: YYYY-MM-DD
        'end_date': request.args.get('end_date')
    }

    try:
        cursor.execute(query_top_5_by_revenue, params)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(results), 200
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': f'Internal error: {e}'}), 500
    finally:
        cursor.close()
        conn.close()
