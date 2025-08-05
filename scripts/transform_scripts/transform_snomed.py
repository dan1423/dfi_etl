# transform_snomed.py

import pandas as pd
import glob
import os
from pathlib import Path

# === Setup paths ===
project_root = Path(__file__).resolve().parent.parent.parent
rf2_dir = project_root /"standardized_vocabularies"/"raw" / "snomed"
output_file = project_root /"standardized_vocabularies"/"cleaned"/ "snomed.csv"
output_file.parent.mkdir(parents=True, exist_ok=True)
print("Reading raw SNOMED CT files...")
# === Locate RF2 concept and description files ===
concept_file = glob.glob(str(rf2_dir / "**/sct2_Concept_Full_*.txt"), recursive=True)[0]
description_file = glob.glob(str(rf2_dir / "**/sct2_Description_Full-en_*.txt"), recursive=True)[0]

# === Load files ===
concept_df = pd.read_csv(concept_file, sep="\t", dtype=str)
desc_df = pd.read_csv(description_file, sep="\t", dtype=str)

# === Filter active rows ===
concept_df = concept_df[concept_df["active"] == "1"]
desc_df = desc_df[(desc_df["active"] == "1") & (desc_df["typeId"] == "900000000000003001")]  # FSNs

# === Merge to link descriptions with concepts ===
merged_df = pd.merge(desc_df, concept_df, left_on="conceptId", right_on="id")

# === Filter for 'observable entity' FSNs ===
observable_df = merged_df[merged_df["term"].str.contains("observable entity", case=False, na=False)]

# === Prepare final DataFrame ===
final_df = pd.DataFrame()
final_df["snomed_code"] = observable_df["conceptId"]
final_df["fully_specified_name"] = observable_df["term"]
final_df["hierarchy_type"] = "Observable Entity"
final_df = final_df.drop_duplicates(subset=["snomed_code"])

# === Save to CSV ===
final_df.to_csv(output_file, index=False)

print(f"Transformed SNOMED observable entities saved to: {output_file}")
