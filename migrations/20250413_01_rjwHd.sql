-- 
-- depends: 

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
