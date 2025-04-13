# Optimized Data Aggregation API

The project handles the following:

1. Schema design, optimization and loading
1. Report aggregation and API.

## Installing the project.

To install locally, you may run the following command:

```sh
pip install .
```

This makes the `clue` command group available in the path. This is implemented via the entrypoint script in the `pyproject.toml` module.

## Database Configuration

The project requires a PostgreSQL db to work. Set the following environmental variables befor running the app:

```sh
export CLUE_DB_HOST=dbserver #The PostgreSQL DB Host, defaults to 127.0.0.1
export CLUE_DB=analyticsdb #The name of the database e.g. sales
export CLUE_DB_PORT=5432 #The database host port, defaults to 5432
export CLUE_DB_USER=meuser # The database user
export CLUE_DB_PWD=optionalPassword # Optional database password
export CLUE_SECRET_KEY=somerandomsecretkey # Flask secret key. Can be set to "dev" in development. 
```

## Integration Testing

The tests require d PostgreSQL db for the integration tests. Check the [GitHub actions workflow](.github/workflows/test.yml) for the continuous integration test flow. The test and default databases are separated, to run the tests locally, you would need to set the environmental variables for the test database.

```sh
export CLUE_TEST_DB_HOST=dbserver #The PostgreSQL DB Host, defaults to 127.0.0.1
export CLUE_TEST_DB=analyticsdb #The name of the database e.g. sales
export CLUE_TEST_DB_PORT=5432 #The database host port, defaults to 5432
export CLUE_TEST_DB_USER=meuser # The database user
export CLUE_TEST_DB_PWD=optionalPassword # Optional database password
```

## Data Commands

After installation, type `clue` at the terminal to see the help for the available commands:

```sh
Usage: clue [OPTIONS] COMMAND [ARGS]...

  CLUE-API group of commands.

Options:
  --help  Show this message and exit.

Commands:
  import-data                Load data from a CSV file to a table
  create-schema              Create the sales report database schema.
  create-monthly-partitions  Create monthly partitions in the sales report table.
```

### Commands

`create-schema` and `sales_report` commands are created for convenience. For a more likely flow, you can run the [migrations](migrations/) which provides a more natural way to track changes to the database.

```sh
pip install yoyo-migrations
yoyo apply
```

#### Commands: Import Data

`import-data` loads a CSV file into the sales report table. For a simple run, use the migration to create the sales_report table. The `create-schema` command does the same.

For the simple loading...
```sh
clue import-data --csv_path tests/data/sales_data.csv -t sales_report
```
However this will fail if any invalid data is present in the CSV file. 
A second option involves specifying a simple schema for validation. It creates a validation_logs table to store invalid records:

```sh 
clue import-data --csv_path tests/data/sales_data_2.csv --schema_path tests/data/sales_data.yaml --table sales_report
```
This completes even when there are error rows. The errors are stored in a validation logs table.

## Rest API

This API is built with Flask. `waitress` WSGI server is included in the dependencies for a production-like run. After installation, you can start the API with this command:

```sh
waitress-serve --host 127.0.0.1 --call clue_api:create_app
```
This will start the API on port 8080:

```
http://127.0.0.1:8080
```

3 anaytical sales reports are included, some assumptions were made:

1. A `sales_report` table is assumed. The scripts are provided in the [migrations folder](migrations/)
1. The columns are inferred, since no table nor column definitions were provided in the instructions.

The 3 reports are:

1. `reports/monthly-sales-summary` e.g. http://127.0.0.1:8080/reports/monthly-sales-summary?start_date=2024-01-01&end_date=2025-12-12
1. `reports/monthly-sales-breakdown` e.g. http://127.0.0.1:8080/reports/monthly-sales-breakdown?start_date=2024-01-01&end_date=2025-12-12
1. `reports/top-5-by-revenue` e.g. http://127.0.0.1:8080/reports/top-5-by-revenue?start_date=2024-01-01&end_date=2025-12-12

All the query parameters are optional but limiting the date range would be more performant as the correct partitions and table indexes would be used.

An OpenAPI documentation for the API is provided in the [docs folder](docs/openapi.yaml).

## Performance Optimizations

1. The schema design for the sales_report data is denormalized; it avoid joins which make it more performant and keeps the integrity of historical transactions.
1. The optimised sales_report table in [migrations/sales_schema.sql](migrations/20250413_01_rjwHd.sql) is partitioned by sales_date. The [second migration](migrations/20250413_02_9sO9a.sql) creates some monthly partitions and indexes on these monthly partitions. Inserted records are put into different partitions based on the sales date. This optimises queries that are based on the `sales_date` because these queries target specific partitions. 
1. Indexes are created for `product_name` and `region` per-partition. The per-partition indexes are smaller and more efficient because they target particular partitions of the table. 
1. Loading operations are more performant on the individual partitions as rebuilding indexes are limited to particular partitions.        
