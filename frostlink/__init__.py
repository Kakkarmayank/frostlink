# frostlink/__init__.py

from .config import load_config, auto_launch_if_missing

# Auto-launch Streamlit setup if config is missing
auto_launch_if_missing()

from .pandas_io import read_sql, read_table
from .sql_io import connect

# ---- Spark Integration ----
try:
    from .spark_io import read_spark, spark_table
except ImportError:
    # If PySpark isn't installed yet, skip gracefully
    def read_spark(*args, **kwargs):
        raise ImportError("PySpark not installed. Please run: pip install pyspark")
    def spark_table(*args, **kwargs):
        raise ImportError("PySpark not installed. Please run: pip install pyspark")

__all__ = [
    "read_sql",
    "read_table",
    "read_spark",
    "spark_table",
    "connect",
    "load_config",
]
