import os
import pandas as pd
from sqlalchemy import create_engine,text
from dotenv import load_dotenv
from pathlib import Path

# === Paths ===
project_root = Path(__file__).resolve().parent.parent.parent
env_path = project_root / "credentials" / "credentials.env"
vocab_dir = project_root /"standardized_vocabularies"/ "cleaned"

# === Load environment variables ===
load_dotenv(dotenv_path=env_path)
pg_user = os.getenv("PG_USER")
pg_password = os.getenv("PG_PASSWORD")
pg_host = os.getenv("PG_HOST")
pg_port = os.getenv("PG_PORT")
pg_database = os.getenv("PG_DATABASE")

# === Create DB connection ===
db_url = f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
engine = create_engine(db_url)

# === Vocabulary file → table mapping ===
vocab_tables = {
    "atc.csv": "medication_atc_code_map",
    "rxnorm.csv": "medication_rxnorm_code_map",
    "icd10_chapters.csv": "icd10_chapters",
    "icd10_ranges.csv": "icd10_ranges",
    "icd10_codes.csv": "icd10_codes",
    "loinc.csv": "lab_component_loinc_map",
    "snomed.csv": "lab_component_snomed_map"
}

# === Load each vocabulary ===
for rel_path, table_name in vocab_tables.items():
    csv_path = vocab_dir / rel_path

    if not csv_path.exists():
        print(f"Skipping {table_name}: file not found at {csv_path}")
        continue

    print(f"Loading {csv_path} into {table_name}...")
    df = pd.read_csv(csv_path, dtype=str)
    # clear table before importing
    with engine.begin() as conn:
        conn.execute(text(f'TRUNCATE TABLE {table_name} CASCADE'))
    
    # Insert into PostgreSQL
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Inserted {len(df)} rows into {table_name}.")

print("All vocabularies loaded successfully.")
