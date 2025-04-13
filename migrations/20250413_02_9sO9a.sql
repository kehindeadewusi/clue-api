-- 
-- depends: 20250413_01_rjwHd

-- Partition for January 2025
CREATE TABLE sales_report_2025_01 PARTITION OF sales_report
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- Partition for February 2025
CREATE TABLE sales_report_2025_02 PARTITION OF sales_report
FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Partition for March 2025
CREATE TABLE sales_report_2025_03 PARTITION OF sales_report
FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');

-- Consider a default partition for data that doesn't fall into specific ranges
CREATE TABLE sales_report_other PARTITION OF sales_report
DEFAULT;


CREATE INDEX idx_product_name_2025_01 ON sales_report_2025_01 (product_name);
CREATE INDEX idx_region_2025_01 ON sales_report_2025_01 (region);

CREATE INDEX idx_product_name_2025_03 ON sales_report_2025_03 (product_name);
CREATE INDEX idx_region_2025_03 ON sales_report_2025_03 (region);
