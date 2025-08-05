import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
env_path = project_root / "credentials" / "credentials.env"
sql_file_path = project_root/"create_tables.sql"

load_dotenv(dotenv_path=env_path)
pg_user = os.getenv("PG_USER")
pg_password = os.getenv("PG_PASSWORD")
pg_host = os.getenv("PG_HOST")
pg_port = os.getenv("PG_PORT")
pg_database = os.getenv("PG_DATABASE")

# === Execute SQL Script ===
def execute_sql_file(file_path):
    with open(file_path, 'r') as file:
        sql = file.read()

    try:
        conn = psycopg2.connect(
            dbname=pg_database,
            user=pg_user,
            password=pg_password,
            host=pg_host,
            port=pg_port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql)
        print("SQL file executed successfully.")
    except Exception as e:
        print("Error executing SQL file:", e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


execute_sql_file(sql_file_path)
