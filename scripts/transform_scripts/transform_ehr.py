import pandas as pd
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent.parent
raw_dir = project_root / "ehr_data" / "raw"
output_dir = project_root / "ehr_data" / "cleaned"
mapping_file = output_dir / "subjects.csv"
output_dir.mkdir(parents=True, exist_ok=True)

# === Config: PostgreSQL column order for each table ===
column_config = {
    "demographics": [
        "subject_id", "mrn", "first_name", "last_name",
        "date_of_birth", "sex", "race", "ethnicity", "death_date"
    ],
    "lab": [
        "subject_id", "mrn", "component_id", "component_name",
        "ord_value", "result_in_range_yn", "reference_unit", "result_flag",
        "spec_take_time", "proc_id", "proc_name", "loinc_code", "snomect_code"
    ],
    "diagnosis": [
        "subject_id", "dx_name", "diagnosis_date", "disease_id",
        "icd10_code", "dxrank_id"
    ],
    "medication": [
        "subject_id", "mrn", "medication_name", "thera_class_c", "med_thera_class",
        "pharm_class_c", "med_pharm_class", "pharm_subclass_c", "med_pharm_sub_class",
        "take_med_dose", "take_med_dttm", "rxnorm_code", "atc_code"
    ]
}

# Renaming rules from raw to standardized names
rename_map = {
    "birth_date": "date_of_birth",
    "lnc_code": "loinc_code"
}

def transform_columns(df, table_name):
    """Rename, add missing, and reorder columns for a table."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.rename(columns=rename_map)

    for col in column_config[table_name]:
        if col not in df.columns:
            df[col] = None

    return df[column_config[table_name]]



# Step 1: Process demographics & build subject_id mapping
print("Processing demographics...")
demographics = pd.read_csv(raw_dir / "demographics.txt", sep="\t", dtype=str)
demographics.columns = demographics.columns.str.strip().str.lower().str.replace(" ", "_")

# Load existing mapping
if mapping_file.exists():
    subject_map = pd.read_csv(mapping_file).rename(columns={"id": "subject_id"})
else:
    subject_map = pd.DataFrame(columns=["mrn", "subject_id"])

# Assign IDs for new MRNs
max_id = subject_map["subject_id"].max() if not subject_map.empty else 0
new_mrns = demographics.loc[~demographics["mrn"].isin(subject_map["mrn"]), "mrn"].unique()
new_ids = range(max_id + 1, max_id + len(new_mrns) + 1)
new_mapping = pd.DataFrame({"mrn": new_mrns, "subject_id": new_ids})

# Update mapping
subject_map = pd.concat([subject_map, new_mapping], ignore_index=True)
demographics = demographics.merge(subject_map, on="mrn", how="left")

# Transform columns for demographics
demographics = transform_columns(demographics, "demographics")

# Save subjects table (with `id` column) for PostgreSQL load
subjects_df = subject_map.rename(columns={"subject_id": "id"})
subjects_df.to_csv(output_dir / "subjects.csv", index=False)

# Save transformed demographics
demographics.to_csv(output_dir / "demographics.csv", index=False)
print(f"Subjects saved to {output_dir / 'subjects.csv'}")
print(f"Demographics saved to {output_dir / 'demographics.csv'}")

# Step 2: Process other tables
tables_map = {
    "lab_results": "lab",
    "diagnosis": "diagnosis",
    "medications": "medication",
    "metabolomic": "metabolomics",   # No transformation config yet
    "metagenomic": "metagenomics"    # No transformation config yet
}

for raw_file, table_name in tables_map.items():
    input_file = raw_dir / f"{raw_file}.txt"
    if not input_file.exists():
        print(f"Skipping {raw_file}: file not found.")
        continue

    print(f"Processing {raw_file}...")
    df = pd.read_csv(input_file, sep="\t", dtype=str)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    if "mrn" in df.columns:
        df = df.merge(subject_map, on="mrn", how="left")

    # Only transform if table config exists
    if table_name in column_config:
        df = transform_columns(df, table_name)

    output_file = output_dir / f"{raw_file}.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved {raw_file} to {output_file}")

print("All tables processed successfully.")
