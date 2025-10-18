

from frostlink import read_sql

# Example 1: Quick environment check
df_info = read_sql("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()")
print(df_info)

# Example 2: Read table from Snowflake
query = "SELECT * FROM RAW.SAP_ECC_APAC_AP1.A017 LIMIT 5"
df = read_sql(query)
print(df)
