import csv, random
from datetime import date

products = [
    {"product_id": 1001, "product_name": "Widget A", "unit_price": 5.25},
    {"product_id": 1002, "product_name": "Widget B", "unit_price": 3},
    {"product_id": 1003, "product_name": "Widget C", "unit_price": 2},
    {"product_id": 1004, "product_name": "Widget D", "unit_price": 1.5},
    {"product_id": 1005, "product_name": "Widget E", "unit_price": 10},
]
regions = ["North", "South", "East", "West"]
years = [2025, 2026]

with open('sales_data.csv', 'w', newline='') as csvfile:
    fieldnames = [
        "product_id", 
        "product_name", 
        "region",
        "sales_date",
        "quantity_sold",
        "sales_amount",
        "unit_price"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for year in years:
        for m in range(1, 13):
            print(year, m)
            for d in range(1, 29):
                d = date(year, m, d)
                
                for i in range(2000): #2k records a day.
                    product = random.choice(products)
                    qty = random.randint(2,10)
                    writer.writerow(
                        {
                            "product_id": product["product_id"],
                            "product_name": product["product_name"],
                            "region": random.choice(regions),
                            "sales_date": d.strftime("%Y-%m-%d"),
                            "quantity_sold": qty,
                            "sales_amount": product["unit_price"]*qty,
                            "unit_price": product["unit_price"]
                        }
                    )
        
