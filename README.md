# Optimized Data Aggregation API

The project handles the following:

1. Schema design, optimization and loading
1. Report API and aggregation.

## Installing the project.

To install locally, you may run the following command:

```sh
pip install .
```

This makes the `clue` command group available in the path. This is implemented via the entrypoint script in the `pyproject.toml` module.

## Database Configuration

Before running the following commands that require a database connection, set the following environmental variables:

```sh
export CLUE_DB_HOST=dbserver #The PostgreSQL DB Host, defaults to 127.0.0.1
export CLUE_DB=analyticsdb #The name of the database e.g. sales
export CLUE_DB_PORT=5432 #The database host port, defaults to 5432
export CLUE_DB_USER=meuser # The database user
export CLUE_DB_PWD=optionalPassword # Optional database password
export CLUE_SECRET_KEY=somerandomsecretkey # Flask secret key. Can be set to "dev" in development. 
```

Note: Set or export the environmentation variables before the database operations and before using the API.

## Database Commands

After installation, type `clue` at the terminal to see the help for the available commands:

```sh
Usage: clue [OPTIONS] COMMAND [ARGS]...

  CLUE-API group of commands.

Options:
  --help  Show this message and exit.

Commands:
  create-schema              Create the sales report database schema.
  create-monthly-partitions  Create monthly partitions in the sales report table.
  import-data                Load data from a CSV file to a table
```

### Commands

`create-schema` Creates the database schema. A script that creates a single `sales_report` table is included in the `data` folder. The optimised table is partitioned by sales_date. 

```sh
clue create-schema --source ./data/optimised/sales_schema.sql
```

`create-monthly-partitions` command creates monthly partitions between a start and end year in an existing sales_report table. You `must` have run the `data/optimised/sales_schema.sql` query which supports partitioning. 

To create partitions every month for the year `2025`, you could run the command:

```sh
clue create-monthly-partitions -t sales_report -s 2025 -e 2025
```

`import-data` loads a CSV file into the sales report table. It has a switch between a simple, swift loading and a slightly less-efficient option which does validation of every record based on a `yaml schema`. 
In both cases, it uses the efficient `COPY` command.

For the simple loading...
```sh
clue import-data --csv_path ./data/sales_data.csv -t sales_report
```
This will fail completely if any invalid data is present in the CSV file. 
A second option involves specifying a simple schema for validation. It creates a validation_logs table where invalid records are stored. Use the following command:

```sh 
clue import-data --csv_path data/sales_data_2.csv --schema_path data/sales_data.yaml --table sales_report
```
This completes even when there are error rows. The errors are stored in a validation logs table.

## Rest API

`waitress` WSGI server is included in the dependencies. After installation, you can start the API with this command:

```sh
waitress-serve --host 127.0.0.1 --call clue_api:create_app
```
This will typically start the API on prt 8080:

```
http://127.0.0.1:8080
```

3 anaytical sales reports are included, built Flask. Some assumptions were made:

1. A `sales_report` table is assumed. The scripts provided in the `data` folder will create this table.
1. The columns are inferred, since no table nor column definitions were provided in the instructions.

The 3 reports are:

1. `reports/monthly-sales-summary` e.g. http://127.0.0.1:5000/reports/monthly-sales-summary?start_date=2024-01-01&end_date=2025-12-12
1. `reports/monthly-sales-breakdown` e.g. http://127.0.0.1:5000/reports/monthly-sales-breakdown?start_date=2024-01-01&end_date=2025-12-12
1. `reports/top-5-by-revenue` e.g. http://127.0.0.1:5000/reports/top-5-by-revenue?start_date=2024-01-01&end_date=2025-12-12

All the query parameters are optional but limiting the date range would be ideal.

An OpenAPI documentation for the API is provided in the [docs folder](docs/openapi.yaml).

## Performance Optimizations

1. The schema design for the sales_report data is denormalized; it avoid joins which make it more performant and keeps the integrity of historical transactions.
1. The optimised sales_report table in [data/optimised/sales_schema.sql](data/optimised/sales_schema.sql) is partitioned by sales_data. A script is also provided to create monthly partitions on the table. Inserted records are put into different partitions based on the sales date. This optimises queries that are based on the `sales_date` because these queries target specific partitions. 
1. Indexes are created for `product_name` and `region` per-partition. The per-partition indexes are smaller and more efficient because they target particular partitions of the table. 
1. Loading operations are more performant on the individual partitions as rebuilding indexes are limited to a partition.        
