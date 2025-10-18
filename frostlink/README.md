# FrostLink

**FrostLink** is a tiny helper to fetch data from **Snowflake** into **Pandas** or **PySpark** with a single line. It supports **SSO** (`externalbrowser`) out of the box.

## Install from Git (no registry)

```bash
pip install "git+https://github.com/<org>/<repo>.git@v0.1.0#egg=frostlink"
# or from main branch
pip install "git+https://github.com/<org>/<repo>.git@main#egg=frostlink"
# with Spark extras
pip install "git+https://github.com/<org>/<repo>.git@v0.1.0#egg=frostlink[spark]"
```

## Config

Create `snowflake_config.json` in your project folder **or** `~/.sf/snowflake_config.json`:

```json
{
  "user": "FIRST.LAST@COMPANY.COM",
  "account": "ZSYFWFE-UDP",
  "warehouse": "TEST_WH",
  "database": "RAW",
  "schema": "SAP_ECC_APAC_AP1",
  "role": "DATA_ENGINEER",
  "authenticator": "externalbrowser"
}
```

## Pandas usage

```python
from frostlink import read_sql, read_table

df = read_sql("SELECT * FROM RAW.SAP_ECC_APAC_AP1.A017 LIMIT 20")
print(df.head())

df2 = read_table("RAW", "SAP_ECC_APAC_AP1", "A017", limit=100)
```

## PySpark usage (optional)

Make sure your Spark session includes Snowflake connector jars:

```python
from pyspark.sql import SparkSession

spark = (SparkSession.builder
    .appName("frostlink-demo")
    .config("spark.jars.packages",
            "net.snowflake:snowflake-jdbc:3.16.1,net.snowflake:spark-snowflake_2.12:2.12.1-spark_3.5")
    .getOrCreate())
```

Then:

```python
from frostlink import spark_read_table, spark_read_sql

df_s = spark_read_table(spark, "RAW", "SAP_ECC_APAC_AP1", "A017")
df_s.show(10, truncate=False)

df_q = spark_read_sql(spark, "SELECT COUNT(*) FROM RAW.SAP_ECC_APAC_AP1.A017")
df_q.show()
```

## Raw connection (cursor)

```python
from frostlink import connect
conn = connect()
print(conn.cursor().execute("select current_role(), current_warehouse()").fetchall())
conn.close()
```

## Build (optional)

```bash
pip install build
python -m build
# dist/frostlink-0.1.0-py3-none-any.whl
```

---

© 2025 FrostLink. MIT or your company license.
