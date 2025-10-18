import snowflake.connector
from .config import load_config

def connect(config_path: str | None = None):
    cfg = load_config(config_path)
    conn = snowflake.connector.connect(
        user=cfg["user"],
        account=cfg["account"],
        warehouse=cfg["warehouse"],
        database=cfg.get("database"),
        schema=cfg.get("schema"),
        role=cfg.get("role"),
        authenticator=cfg.get("authenticator", "externalbrowser"),
    )
    # Ensure warehouse is active
    conn.cursor().execute(f'USE WAREHOUSE "{cfg["warehouse"]}"')
    return conn
