import pandas as pd
from sqlalchemy import create_engine,inspect
from pathlib import Path
import os
from dotenv import load_dotenv

# === Load DB Credentials ===
project_root = Path(__file__).resolve().parent.parent.parent  # Adjust if needed
env_path = project_root / "credentials" / "credentials.env"
ehr_dir = project_root /"ehr_data"/"cleaned"
load_dotenv(dotenv_path=env_path)

pg_user = os.getenv("PG_USER")
pg_password = os.getenv("PG_PASSWORD")
pg_host = os.getenv("PG_HOST")
pg_port = os.getenv("PG_PORT")
pg_database = os.getenv("PG_DATABASE")

db_url = f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
engine = create_engine(db_url)
inspector = inspect(engine)

# === File Paths & Table Names ===

files_to_load = {
    "subjects.csv": "subjects",
    "demographics.csv": "demographics",
    "diagnosis.csv": "diagnosis",
    "lab_results.csv": "labs",
    "medications.csv": "medications",
    "metabolomic.csv": "metabolomics",
    "metagenomic.csv": "metagenomics"
}
print(f"Loading data from {ehr_dir} into PostgreSQL database '{pg_database}'")
# === Load Each File into PostgreSQL ===
for file_stem, table_name in files_to_load.items():
    file_path = ehr_dir / file_stem
    if file_path.exists():
        df = pd.read_csv(file_path, sep=",", engine="python")
        print(df.columns.tolist())

        if table_name in inspector.get_table_names():
            # Append if exists
            df.to_sql(table_name, engine, if_exists="append", index=False)
            print(f"Appended {len(df)} rows to existing table '{table_name}'")
        else:
            # Create if doesn't exist
            df.to_sql(table_name, engine, if_exists="fail", index=False)
            print(f"Created table '{table_name}' and inserted {len(df)} rows")

    else:
        print(f"File not found: {file_path}")

print("Data loading complete.")