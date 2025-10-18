# frostlink/spark_io.py
from pyspark.sql import SparkSession
from .config import load_config

def get_spark_session(app_name: str = "FrostLinkSpark") -> SparkSession:
    """
    Create a Spark session with Snowflake connector pre-configured using your saved frostlink config.
    """
    cfg = load_config()
    sf_options = {
        "sfURL": f"{cfg['account']}.snowflakecomputing.com",
        "sfWarehouse": cfg["warehouse"],
        "sfDatabase": cfg["database"],
        "sfSchema": cfg["schema"],
        "sfRole": cfg.get("role", ""),
        "sfAuthenticator": cfg.get("authenticator", "externalbrowser"),
        "sfUser": cfg["user"],
    }

    spark = (
        SparkSession.builder
        .appName(app_name)
        .config("spark.jars.packages", "net.snowflake:snowflake-jdbc:3.13.30,net.snowflake:spark-snowflake_2.12:2.12.3-spark_3.5")
        .config("spark.sql.catalogImplementation", "in-memory")
        .getOrCreate()
    )

    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", "500000")

    # Attach Snowflake connection options to Spark session
    spark._jsc.hadoopConfiguration().set("sfURL", sf_options["sfURL"])
    return spark, sf_options


def read_spark(query: str):
    """
    Run a SQL query on Snowflake and return a Spark DataFrame.
    """
    spark, sf_options = get_spark_session()
    df = (
        spark.read
        .format("snowflake")
        .options(**sf_options)
        .option("query", query)
        .load()
    )
    return df


def spark_table(database: str, schema: str, table: str, limit: int = 100):
    """
    Load a table from Snowflake as a Spark DataFrame.
    """
    query = f'SELECT * FROM "{database}"."{schema}"."{table}" LIMIT {limit}'
    return read_spark(query)
