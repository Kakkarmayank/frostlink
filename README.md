# ❄️ Frostlink – Python ↔ Snowflake Connector  
Frostlink is a lightweight Python package that connects seamlessly to **Snowflake** using secure **SSO** and an interactive **Streamlit setup UI**. It fetches data into **Pandas**, **SQL**, or **PySpark** in seconds — no credentials hardcoding, no DBT required.  
### 🚀 Quick Start  
```bash
git clone https://github.com/Kakkarmayank/frostlink.git
cd frostlink
pip install -e .
python -m frostlink.config
Enter Snowflake details (user, account, warehouse, db, schema) → auto-saved at ~/.sf/snowflake_config.json

🐼 Pandas Example
python
Copy code
from frostlink import read_sql
df = read_sql("SELECT * FROM RAW.SAP_ECC_APAC_AP1.A017 LIMIT 5")
print(df)
🔥 PySpark Example
python
Copy code
from frostlink import read_spark
df = read_spark("SELECT * FROM RAW.SAP_ECC_APAC_AP1.A017 LIMIT 5")
df.show()
💡 Highlights
✅ One-time Streamlit setup • ✅ Secure SSO login • ✅ Works with Pandas & Spark • ✅ Team-ready package • ✅ No DBT required

📁 Structure
frostlink/ → __init__.py · config.py · pandas_io.py · spark_io.py · sql_io.py · pyproject.toml

🧊 Author
Mayank Kakkar — Building smarter data bridges for Snowflake ❄️

yaml
Copy code

---

You can literally copy-paste that into your `README.md` — everything fits in **one screen / one cell**, ready for GitHub display.  

Would you like the same single-cell version rewritten for your **`snowfetch`** package name next?






