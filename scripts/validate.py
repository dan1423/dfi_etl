import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path

# === Paths & DB connection ===
project_root = Path(__file__).resolve().parent.parent
env_path = project_root / "credentials" / "credentials.env"

load_dotenv(dotenv_path=env_path)
pg_user = os.getenv("PG_USER")
pg_password = os.getenv("PG_PASSWORD")
pg_host = os.getenv("PG_HOST")
pg_port = os.getenv("PG_PORT")
pg_database = os.getenv("PG_DATABASE")
print(pg_user, pg_password, pg_host, pg_port, pg_database)

db_url = f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
engine = create_engine(db_url)

# === Tables & validation rules ===
validation_rules = {
    "medication_atc_code_map": {
        "required_columns": ["atc_code", "atc_name"],
        "unique_columns": ["atc_code"]
    },
    "medication_rxnorm_code_map": {
        "required_columns": ["rxcui", "medication_name"],
        "unique_columns": ["rxcui"]
    },
    "icd10_codes": {
        "required_columns": ["code", "description"],
        "unique_columns": ["code"]
    },
     "icd10_chapters": {
        "required_columns": ["chapter", "description"],
        "unique_columns": ["chapter"]
    },
     "icd10_code_ranges": {
        "required_columns": ["chapter", "code_range","description"],
        "unique_columns": ["code_range"]
    },
    "lab_component_loinc_map": {
        "required_columns": ["loinc_code", "component"],
        "unique_columns": ["loinc_code"]
    },
    "lab_component_snomed_map": {
        "required_columns": ["snomed_code", "snomed_term"],
        "unique_columns": ["snomed_code"]
    }
}

def is_column_numeric(conn, table, column):
    query = text("""
        SELECT data_type
        FROM information_schema.columns
        WHERE table_name = :table AND column_name = :column
    """)
    result = conn.execute(query, {"table": table, "column": column}).scalar()
    return result in ("integer", "bigint", "smallint", "numeric", "double precision", "real")

with engine.connect() as conn:
    for table, rules in validation_rules.items():
        print(f"\n Validating table: {table}")

        # Row count
        row_count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f" Row count: {row_count}")

        # Null checks
        for col in rules["required_columns"]:
            if is_column_numeric(conn, table, col):
                null_query = f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL"
            else:
                null_query = f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL OR {col} = ''"

            null_count = conn.execute(text(null_query)).scalar()
            if null_count > 0:
                print(f" {null_count} NULL/empty values in '{col}'")
            else:
                print(f" No NULLs in '{col}'")

        # Duplicate checks
        for col in rules["unique_columns"]:
            dup_count = conn.execute(text(f"""
                SELECT COUNT(*) FROM (
                    SELECT {col}, COUNT(*) 
                    FROM {table} 
                    GROUP BY {col} 
                    HAVING COUNT(*) > 1
                ) AS duplicates
            """)).scalar()
            if dup_count > 0:
                print(f" {dup_count} duplicate values in '{col}'")
            else:
                print(f" No duplicates in '{col}'")
