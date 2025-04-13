import click

from clue_oda.data.ops import schema, importer, importer_2


@click.command(short_help="Load data from a CSV file to a table")
@click.option("--csv_path", "-c", required=True, help="The CSV file path")
@click.option("--schema_path", "-p", required=False, help="The YAML schema path")
@click.option("--table", "-t", required=True, help="Table to load")
@click.option("--error_table", "-e", default="validation_logs", help="Error log table.")
def import_data(csv_path: str, schema_path:str, table: str, error_table: str) -> None:
    """Generate the latest rate file."""
    if schema_path:
        print("schema detected...")
        importer_2.load_csv(csv_path, schema_path, table, error_log_table=error_table)
    else:
        print("no schema detected, optimising...")
        importer.load_csv(csv_path, table)

    click.echo(f"Created schema, source = {csv_path}")


@click.command(short_help="Create the sales report database schema.")
@click.option("--source", "-s", required=True, help="Source file (table)")
def create_schema(source: str) -> None:
    """Run the SQL script to create a sales table."""
    schema.create_sales_table(source)
    
    click.echo(f"Created schema, source = {source}")


@click.command(short_help="Create monthly partitions in the sales report table.")
@click.option("--table", "-t", required=True, help="Table to partition")
@click.option("--start_year", "-s", required=True, type=click.INT, help="Start year")
@click.option("--end_year", "-e", required=True, type=click.INT, help="End year")
def create_monthly_partitions(table: str, start_year:int, end_year: int) -> None:
    """Run the SQL script to create a sales table."""
    schema.create_monthly_partitions(table, start_year, end_year)
    
    click.echo(f"Created partitions from {start_year} to {end_year} on table {table}")


@click.group()
def cli_group() -> None:
    """CLUE-API group of commands."""
    click.echo("running commands...")

cli_group.add_command(create_schema)
cli_group.add_command(create_monthly_partitions)
cli_group.add_command(import_data)

def main() -> None:
    """Entry function."""
    try:
        cli_group()
    except SystemExit as err:
        # re-raise unless main() finished without an error
        if err.code:
            print(err)
            raise


if __name__ == "__main__":
    main()
