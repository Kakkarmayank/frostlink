import pandas as pd
from .sql_io import connect

def read_sql(sql: str, config_path: str | None = None) -> pd.DataFrame:
    """Run any SQL and return a Pandas DataFrame."""
    conn = connect(config_path)
    try:
        df = pd.read_sql(sql, conn)
    finally:
        conn.close()
    return df

def read_table(database: str, schema: str, table: str, limit: int = 1000, config_path: str | None = None):
    sql = f'SELECT * FROM "{database}"."{schema}"."{table}" LIMIT {limit}'
    return read_sql(sql, config_path)
