import os
import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET

# === Define Paths ===
project_root = Path(__file__).resolve().parent.parent.parent
raw_dir = project_root /"standardized_vocabularies"/"raw" /"icd10"/ "icd10cm_tabular_2025.xml"
output_dir = project_root /"standardized_vocabularies"/"cleaned"
output_dir.mkdir(parents=True, exist_ok=True)

print(f"Reading ICD10 XML file")
# Parse XML
tree = ET.parse(raw_dir)
root = tree.getroot()

chapters = []
code_ranges = []
codes = []

# ICD-10 XML structure assumptions
for chapter_elem in root.findall(".//chapter"):
    chapter_num = int(chapter_elem.findtext("name").split()[0])
    chapter_desc = chapter_elem.findtext("desc")
    chapters.append({
        "chapter": chapter_num,
        "description": chapter_desc
    })

    for section in chapter_elem.findall(".//section"):
        code_range_text = section.findtext("name")
        section_desc = section.findtext("desc")
        code_ranges.append({
            "chapter": chapter_num,
            "code_range": code_range_text,
            "description": section_desc
        })

        for diag in section.findall(".//diag"):
            code_val = diag.findtext("name")
            code_desc = diag.findtext("desc")
            codes.append({
                "code": code_val,
                "description": code_desc,
                "subchapter_id": None 
            })

# Convert to DataFrames
chapters_df = pd.DataFrame(chapters).drop_duplicates()
code_ranges_df = pd.DataFrame(code_ranges).drop_duplicates()
codes_df = pd.DataFrame(codes).drop_duplicates()

# Save CSVs
chapters_df.to_csv(f"{output_dir}/icd10_chapters.csv", index=False)
code_ranges_df.to_csv(f"{output_dir}/icd10_code_ranges.csv", index=False)
codes_df.to_csv(f"{output_dir}/icd10_codes.csv", index=False)

print("ICD-10 XML parsed and CSVs saved:")
print(f"- {output_dir}/icd10_chapters.csv")
print(f"- {output_dir}/icd10_code_ranges.csv")
print(f"- {output_dir}/icd10_codes.csv")
