import pandas as pd
from pathlib import Path

# === Setup paths ===
project_root = Path(__file__).resolve().parent.parent.parent
raw_loinc_path = project_root /"standardized_vocabularies"/"raw" / "loinc" / "Loinc.csv"
output_csv_path = project_root /"standardized_vocabularies"/"cleaned"/"loinc.csv"

# === Column mapping for standardization ===
column_map = {
    "LOINC_NUM": "loinc_code",
    "COMPONENT": "component",
    "SYSTEM": "system",
    "CLASSTYPE": "class_type",
    "LONG_COMMON_NAME": "long_common_name",
    "EXAMPLE_UCUM_UNITS": "ucum_units"

}

# === Load raw LOINC file ===
print("Reading raw LOINC CSV...")
df = pd.read_csv(raw_loinc_path, dtype=str, low_memory=False, encoding="utf-8")

# === Filter to chemistry lab entries (CLASSTYPE = 1) ===
df = df[df["CLASSTYPE"] == "1"]

# === Keep only required columns and rename ===
df = df[list(column_map.keys())].rename(columns=column_map)

# === Drop duplicates on LOINC code ===
df = df.drop_duplicates(subset=["loinc_code"])

# === Save transformed file ===
output_csv_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_csv_path, index=False)

print(f"Transformed LOINC data saved to: {output_csv_path}")