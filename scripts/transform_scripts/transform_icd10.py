import os
import pandas as pd
from pathlib import Path
import xml.etree.ElementTree as ET

# === Define Paths ===
project_root = Path(__file__).resolve().parent.parent.parent
raw_dir = project_root /"standardized_vocabularies"/"raw" /"icd10"/ "icd10cm_tabular_2025.xml"
output_dir = project_root /"standardized_vocabularies"/"cleaned"
output_dir.mkdir(parents=True, exist_ok=True)

print("Reading ICD10 XML file")
tree = ET.parse(raw_dir)
root = tree.getroot()

chapters = []
code_ranges = []
codes = []

for chap_el in root.findall("chapter"):
    chapter_num = int(chap_el.findtext("name").strip())
    chapter_desc = chap_el.findtext("desc").strip()

    chapters.append({
        "chapter": chapter_num,
        "description": chapter_desc
    })

    # Parse section ranges
    for section_ref in chap_el.findall(".//sectionRef"):
        first = section_ref.attrib.get("first")
        last = section_ref.attrib.get("last")
        section_desc = (section_ref.text or "").strip()
        code_range_str = f"{first}-{last}"

        # Add code range
        code_ranges.append({
            "chapter": chapter_num,
            "code_range": code_range_str,
            "description": section_desc
        })

        # Extract codes in this range
        for diag_el in root.findall(".//diag"):
            code_val = diag_el.findtext("name")
            desc_val = diag_el.findtext("desc")

            if not code_val or not desc_val:
                continue

            # Filter codes that fall in the first-last range
            if first <= code_val <= last:
                codes.append({
                    "code": code_val,
                    "description": desc_val,
                    "code_range": code_range_str
                })

# DataFrames
chapters_df = pd.DataFrame(chapters).drop_duplicates()
code_ranges_df = pd.DataFrame(code_ranges).drop_duplicates()
codes_df = pd.DataFrame(codes).drop_duplicates()

# Save
chapters_df.to_csv(output_dir / "icd10_chapters.csv", index=False)
code_ranges_df.to_csv(output_dir / "icd10_code_ranges.csv", index=False)
codes_df.to_csv(output_dir / "icd10_codes.csv", index=False)

print("ICD-10 XML parsed and CSVs saved:")
print(f"- {output_dir}/icd10_chapters.csv")
print(f"- {output_dir}/icd10_code_ranges.csv")
print(f"- {output_dir}/icd10_codes.csv")