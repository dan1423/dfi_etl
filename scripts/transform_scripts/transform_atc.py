import pandas as pd
from pathlib import Path

# === Setup paths ===
project_root = Path(__file__).resolve().parent.parent.parent
raw_atc_path = project_root /"standardized_vocabularies"/"raw"/"atc"/"WHO ATC-DDD 2024-07-31.csv"
output_csv_path = project_root /"standardized_vocabularies"/"cleaned" /"atc.csv"

# === Column mapping for standardization ===
column_map = {
    "atc_code": "atc_code",
    "atc_name": "atc_name"
}

# === Load raw LOINC file ===
print("Reading raw atc CSV...")
df = pd.read_csv(raw_atc_path, dtype=str, low_memory=False, encoding="utf-8")


df = df[list(column_map.keys())].rename(columns=column_map)

# === Drop duplicates on LOINC code ===
df = df.drop_duplicates(subset=["atc_code"])

# === Save transformed file ===
output_csv_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_csv_path, index=False)

print(f"Transformed atc data saved to: {output_csv_path}")