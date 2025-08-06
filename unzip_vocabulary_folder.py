import zipfile
import os
from pathlib import Path

# Paths
project_root = Path(__file__).resolve().parent
zip_file_path = project_root / "standardized_vocabularies.zip"
extract_to_path = project_root / "standardized_vocabularies" / "raw"

# Ensure the raw folder exists
os.makedirs(extract_to_path, exist_ok=True)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    for member in zip_ref.namelist():
        # Extract only files from the "raw" folder inside the zip
        if "/raw/" in member and not member.endswith('/'):
            # Remove the leading folder path inside the zip to avoid extra nesting
            raw_relative_path = member.split("/raw/", 1)[1]
            target_path = extract_to_path / raw_relative_path

            # Ensure subfolders exist
            os.makedirs(target_path.parent, exist_ok=True)

            # Extract file
            with zip_ref.open(member) as source, open(target_path, "wb") as target:
                target.write(source.read())

print(f"✅ Extracted 'raw' folder into {extract_to_path}")
