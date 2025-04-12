-- The `create-partition` command creates a bunch of partitions and can be automated.

CREATE TABLE sales_report (
    sale_id SERIAL,
    product_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    region VARCHAR(100) NOT NULL,
    sales_date DATE NOT NULL,
    quantity_sold INT NOT NULL,
    sales_amount DECIMAL(10, 2) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,

    PRIMARY KEY (sales_date, sale_id)

) PARTITION BY RANGE (sales_date);

--NOTE: This is required when creating the partitions manually. 
-- Automating this would help - see create-partition command.
-- Partition for January 2024
-- CREATE TABLE sales_report_2024_01 PARTITION OF sales_report
-- FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- -- Partition for February 2024
-- CREATE TABLE sales_report_2024_02 PARTITION OF sales_report
-- FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- -- Partition for March 2024
-- CREATE TABLE sales_report_2024_03 PARTITION OF sales_report
-- FOR VALUES FROM ('2024-03-01') TO ('2024-04-01');

-- -- Consider a default partition for data that doesn't fall into specific ranges
-- CREATE TABLE sales_report_other PARTITION OF sales_report
-- DEFAULT;


-- CREATE INDEX idx_product_name_2024_01 ON sales_report_2024_01 (product_name);
-- CREATE INDEX idx_region_2024_01 ON sales_report_2024_01 (region);
-- -- ... and so on for other partitions
-- CREATE INDEX idx_product_name_2025_04 ON sales_report_2025_04 (product_name);
-- CREATE INDEX idx_region_2025_04 ON sales_report_2025_04 (region);


-- SELECT
--     TO_CHAR(sr.sales_date, 'YYYY-MM') AS sale_month,
--     sr.product_name,
--     sr.region,
--     SUM(sr.sales_amount) AS monthly_sales,
--     SUM(sr.quantity_sold) AS total_quantity_sold
-- FROM
--     sales_report sr
-- WHERE
--     (%(product_name)s IS NULL OR sr.product_name = %(product_name)s)
--     AND
--     (%(region)s IS NULL OR sr.region = %(region)s)
--     AND
--     (%(start_date)s IS NULL OR sr.sales_date >= %(start_date)s::DATE)
--     AND
--     (%(end_date)s IS NULL OR sr.sales_date <= %(end_date)s::DATE)
-- GROUP BY
--     sale_month,
--     sr.product_name,
--     sr.region
-- ORDER BY
--     sale_month,
--     sr.product_name,
--     sr.region;
