# # import json
# # from pathlib import Path
# # import os

# # CONFIG_PATH = Path.home() / ".sf" / "snowflake_config.json"

# # def _interactive_setup():
# #     """Prompt the user for Snowflake connection details and save to ~/.sf/snowflake_config.json"""
# #     print("\n🧭 FrostLink - First Time Snowflake Setup")
# #     print("Let's configure your Snowflake connection. This will only happen once.\n")

# #     user = input("👉 Snowflake user (email): ").strip()
# #     account = input("👉 Snowflake account (e.g. ***): ").strip()
# #     warehouse = input("👉 Default warehouse (e.g. TEST_WH): ").strip()
# #     database = input("👉 Default database (e.g. RAW): ").strip()
# #     schema = input("👉 Default schema (e.g. SAP_ECC_APAC_AP1): ").strip()
# #     role = input("👉 Role [optional]: ").strip()
# #     authenticator = input("👉 Authenticator [default externalbrowser]: ").strip() or "externalbrowser"

# #     config = {
# #         "user": user,
# #         "account": account,
# #         "warehouse": warehouse,
# #         "database": database,
# #         "schema": schema,
# #         "authenticator": authenticator
# #     }
# #     if role:
# #         config["role"] = role

# #     CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
# #     with open(CONFIG_PATH, "w", encoding="utf-8") as f:
# #         json.dump(config, f, indent=2)

# #     print(f"\n✅ FrostLink configuration saved to: {CONFIG_PATH}\n")


# # def _generate_from_env():
# #     """Optionally create config from environment variables if available"""
# #     env_user = os.getenv("SNOWFLAKE_USER")
# #     env_account = os.getenv("SNOWFLAKE_ACCOUNT")
# #     env_warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
# #     env_database = os.getenv("SNOWFLAKE_DATABASE")
# #     env_schema = os.getenv("SNOWFLAKE_SCHEMA")
# #     env_role = os.getenv("SNOWFLAKE_ROLE")
# #     env_auth = os.getenv("SNOWFLAKE_AUTH", "externalbrowser")

# #     if all([env_user, env_account, env_warehouse, env_database, env_schema]):
# #         CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
# #         config = {
# #             "user": env_user,
# #             "account": env_account,
# #             "warehouse": env_warehouse,
# #             "database": env_database,
# #             "schema": env_schema,
# #             "authenticator": env_auth
# #         }
# #         if env_role:
# #             config["role"] = env_role

# #         with open(CONFIG_PATH, "w", encoding="utf-8") as f:
# #             json.dump(config, f, indent=2)
# #         print(f"✅ FrostLink config auto-created from environment variables at {CONFIG_PATH}")
# #         return True

# #     return False


# # def ensure_config_exists():
# #     """Ensure the config file exists; create it if not."""
# #     if CONFIG_PATH.exists():
# #         return
# #     if not _generate_from_env():
# #         _interactive_setup()


# # def load_config(path: str | None = None) -> dict:
# #     """Load config from a given path, project dir, or ~/.sf/ (auto-create if missing)."""
# #     if not path:
# #         ensure_config_exists()

# #     candidates = []
# #     if path:
# #         candidates.append(Path(path))
# #     candidates += [
# #         Path("snowflake_config.json"),
# #         CONFIG_PATH
# #     ]

# #     for p in candidates:
# #         if p.exists():
# #             with open(p, "r", encoding="utf-8") as f:
# #                 return json.load(f)

# #     raise FileNotFoundError("❌ No Snowflake config found or created.")





import json
import os
import sys
from pathlib import Path
import streamlit as st
import snowflake.connector as sf
import subprocess

CONFIG_PATH = Path.home() / ".sf" / "snowflake_config.json"

# =============================
#  Streamlit UI for setup
# =============================
def _launch_streamlit_ui():
    """Launch the Streamlit UI setup page"""
    script_path = Path(__file__).resolve()
    print("🚀 Launching FrostLink setup UI...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(script_path)], check=False)
    sys.exit(0)

# =============================
#  Interactive setup (Streamlit)
# =============================
def _interactive_setup_ui():
    """Render the Streamlit UI to enter Snowflake connection details"""
    st.set_page_config(page_title="❄️ FrostLink Setup", page_icon="❄️", layout="centered")
    st.title("❄️ FrostLink / Snowfetch - Snowflake Configuration")

    st.markdown("""
    Welcome!  
    Use this setup page to configure your Snowflake connection details.  
    Once saved, they’ll be stored securely in:
    ```
    ~/.sf/snowflake_config.json
    ```
    This only needs to be done once.
    """)

    with st.form("snowflake_form"):
        st.subheader("🔧 Enter Snowflake Connection Details")

        col1, col2 = st.columns(2)
        with col1:
            user = st.text_input("Snowflake User (email)", placeholder="Enter your email")
            account = st.text_input("Account Identifier", placeholder="Enter Account Indetifier")
            warehouse = st.text_input("Default Warehouse", placeholder="e.g. TEST_WH")
        with col2:
            database = st.text_input("Default Database", placeholder="e.g. RAW")
            schema = st.text_input("Default Schema", placeholder="e.g. SAP_ECC_APAC_AP1")
            role = st.text_input("Role (optional)", placeholder="e.g. DATA_ENGINEER")

        authenticator = st.text_input(
            "Authenticator (default: externalbrowser)",
            value="externalbrowser",
            placeholder="externalbrowser"
        )

        test_connection = st.checkbox("✅ Test connection before saving", value=True)
        submit = st.form_submit_button("💾 Save Configuration")

    if submit:
        config = {
            "user": user.strip(),
            "account": account.strip(),
            "warehouse": warehouse.strip(),
            "database": database.strip(),
            "schema": schema.strip(),
            "authenticator": authenticator.strip() or "externalbrowser"
        }

        if role.strip():
            config["role"] = role.strip()

        # Validate required fields
        missing = [k for k, v in config.items() if not v and k != "role"]
        if missing:
            st.error(f"Please fill all required fields: {', '.join(missing)}")
            st.stop()

        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
        st.success(f"✅ Configuration saved successfully at: {CONFIG_PATH}")

        # Optional test connection
        if test_connection:
            st.info("🔄 Testing Snowflake connection... (SSO may open in browser)")
            try:
                conn = sf.connect(
                    user=config["user"],
                    account=config["account"],
                    warehouse=config["warehouse"],
                    database=config.get("database"),
                    schema=config.get("schema"),
                    role=config.get("role"),
                    authenticator=config.get("authenticator", "externalbrowser")
                )
                cur = conn.cursor()
                cur.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()")
                res = cur.fetchall()
                cur.close()
                conn.close()
                st.success(f"✅ Connection successful! User: {res[0][0]}, Role: {res[0][1]}, Warehouse: {res[0][2]}")
            except Exception as e:
                st.error(f"❌ Connection failed: {e}")

    st.caption("💡 Tip: Re-run this setup anytime to update your saved Snowflake credentials.")


# =============================
#  Config handling logic
# =============================
def ensure_config_exists():
    """Check for existing config; if not found, auto-launch Streamlit UI."""
    if CONFIG_PATH.exists():
        return
    print("⚙️  No Snowflake config found. Launching setup UI...")
    _launch_streamlit_ui()


def load_config(path: str | None = None) -> dict:
    """Load config file or trigger setup UI if missing."""
    if not path:
        ensure_config_exists()

    candidates = []
    if path:
        candidates.append(Path(path))
    candidates += [Path("snowflake_config.json"), CONFIG_PATH]

    for p in candidates:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)

    raise FileNotFoundError("❌ No Snowflake config found or created.")


# =============================
#  Streamlit entry point
# =============================
if __name__ == "__main__":
    # If run with streamlit: show the UI
    _interactive_setup_ui()



# # frostlink/config.py
# import json
# import os
# import sys
# import subprocess
# from pathlib import Path

# CONFIG_PATH = Path.home() / ".sf" / "snowflake_config.json"

# # Launch Streamlit app (runs same file via streamlit)
# def _launch_streamlit_ui():
#     script_path = Path(__file__).resolve()
#     # run streamlit in a subprocess using the same Python
#     subprocess.run([sys.executable, "-m", "streamlit", "run", str(script_path)], check=False)
#     # exit the caller so the importer doesn't hang
#     sys.exit(0)

# # Streamlit UI
# def _interactive_setup_ui():
#     import streamlit as st
#     import snowflake.connector as sf

#     st.set_page_config(page_title="❄️ FrostLink Setup", layout="centered")
#     st.title("❄️ FrostLink - Snowflake Configuration")
#     st.markdown(
#         "Enter your Snowflake details below. They will be saved to `~/.sf/snowflake_config.json`."
#     )

#     with st.form("snowflake_form"):
#         col1, col2 = st.columns(2)
#         with col1:
#             user = st.text_input("Snowflake User (email)", value="", placeholder="you@company.com")
#             account = st.text_input("Account Identifier", value="", placeholder="e.g. Z***")
#             warehouse = st.text_input("Default Warehouse", value="", placeholder="e.g. TEST_WH")
#         with col2:
#             database = st.text_input("Default Database", value="", placeholder="e.g. RAW")
#             schema = st.text_input("Default Schema", value="", placeholder="e.g. SAP_ECC_APAC_AP1")
#             role = st.text_input("Role (optional)", value="", placeholder="e.g. DATA_ENGINEER")

#         authenticator = st.text_input(
#             "Authenticator (default: externalbrowser)", value="", placeholder="externalbrowser"
#         )

#         test_connection = st.checkbox("Test connection before saving", value=True)
#         submitted = st.form_submit_button("Save configuration")

#     if submitted:
#         cfg = {
#             "user": user.strip(),
#             "account": account.strip(),
#             "warehouse": warehouse.strip(),
#             "database": database.strip(),
#             "schema": schema.strip(),
#             "authenticator": (authenticator.strip() or "externalbrowser")
#         }
#         if role.strip():
#             cfg["role"] = role.strip()

#         missing = [k for k, v in cfg.items() if not v and k != "role"]
#         if missing:
#             st.error(f"Please fill required fields: {', '.join(missing)}")
#             st.stop()

#         CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
#         CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
#         st.success(f"Saved config to: {CONFIG_PATH}")

#         if test_connection:
#             st.info("Testing connection (SSO browser may open)...")
#             try:
#                 conn = sf.connect(
#                     user=cfg["user"],
#                     account=cfg["account"],
#                     warehouse=cfg["warehouse"],
#                     database=cfg.get("database"),
#                     schema=cfg.get("schema"),
#                     role=cfg.get("role"),
#                     authenticator=cfg.get("authenticator", "externalbrowser"),
#                 )
#                 cur = conn.cursor()
#                 cur.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()")
#                 res = cur.fetchall()
#                 cur.close()
#                 conn.close()
#                 st.success(f"Connection OK: {res}")
#             except Exception as e:
#                 st.error(f"Connection failed: {e}")

#     st.caption("Re-run this page to update saved settings.")

# # Called by console script `frostlink-config`
# def main():
#     # Launch streamlit UI for interactive setup
#     _launch_streamlit_ui()

# # Called by import-time check to auto-launch UI if config missing
# def auto_launch_if_missing():
#     if CONFIG_PATH.exists():
#         return
#     # if no terminal (CI), don't try to launch
#     try:
#         _launch_streamlit_ui()
#     except Exception:
#         # fail silently in non-interactive environments
#         pass

# # Loader used by the package
# def load_config(path: str | None = None) -> dict:
#     # If no explicit path, ensure config exists (this may trigger UI on import)
#     if path is None:
#         auto_launch_if_missing()

#     candidates = []
#     if path:
#         candidates.append(Path(path))
#     candidates += [Path("snowflake_config.json"), CONFIG_PATH]

#     for p in candidates:
#         if p.exists():
#             return json.loads(p.read_text(encoding="utf-8"))

#     raise FileNotFoundError("No Snowflake config found.")
# # ======================================================
# #  Auto-launch if config missing
# # ======================================================
# def auto_launch_if_missing():
#     """Check if config exists; if not, launch Streamlit UI."""
#     from pathlib import Path
#     import sys, subprocess
#     from . import config  # same module

#     CONFIG_PATH = Path.home() / ".sf" / "snowflake_config.json"

#     if CONFIG_PATH.exists():
#         return

#     print("⚙️  No Snowflake config found — launching setup UI...")
#     script_path = Path(__file__).resolve()
#     subprocess.run([sys.executable, "-m", "streamlit", "run", str(script_path)], check=False)
#     sys.exit(0)
