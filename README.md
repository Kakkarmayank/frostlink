# ❄️ Frostlink – Python ↔ Snowflake Connector  
Frostlink is a lightweight Python package that connects securely to **Snowflake** using **SSO** and an interactive **Streamlit UI**. Fetch Snowflake data directly into **Pandas** or **PySpark** — no manual setup, no credentials in code.  

**Install & Setup (one time):**  
`git clone https://github.com/Kakkarmayank/frostlink.git && cd frostlink && pip install -e . && python -m frostlink.config`  

**Example (Pandas):**  
`from frostlink import read_sql`  
`df = read_sql("SELECT * FROM RAW.SAP_ECC_APAC_AP1.A017 LIMIT 5")`  
`print(df)`  

**Example (PySpark):**  
`from frostlink import read_spark`  
`df = read_spark("SELECT * FROM RAW.SAP_ECC_APAC_AP1.A017 LIMIT 5")`  
`df.show()`  

**Highlights:**  
- 🧭 Streamlit setup — auto-creates `~/.sf/snowflake_config.json`  
- 🔐 Secure browser-based SSO login  
- ⚡ Works with Pandas, SQL, and Spark  
- 🧩 Ideal for teams & automation pipelines  

**Author:** Mayank Kakkar • Building smarter data bridges for Snowflake ❄️
