import os
import pandas as pd
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent.parent
raw_dir = project_root /"standardized_vocabularies"/"raw" / "rxnorm"
output_csv_path = project_root /"standardized_vocabularies"/"cleaned" / "rxnorm.csv"

# File definitions
rxnconso_file = raw_dir / "RXNCONSO.RRF"
rxnconso_columns = [
    "rxcui", "lat", "ts", "lui", "stt", "sui", "ispref", "rxaui", "saui",
    "scui", "sdui", "sab", "tty", "code", "str", "srl", "suppress", "cvf"
]

print(f"Reading {rxnconso_file}")
df = pd.read_csv(rxnconso_file, sep='|', header=None, dtype=str, engine='python')
df.dropna(how='all', inplace=True)  # Drop empty lines

# Drop extra columns if any
if df.shape[1] > len(rxnconso_columns):
    print(f"Detected {df.shape[1]} columns, expected {len(rxnconso_columns)}. Dropping extra columns.")
    df = df.iloc[:, :len(rxnconso_columns)]

df.columns = rxnconso_columns
# Clean escape characters
df = df.astype(str).applymap(lambda x: x.strip("�"))

map_df = df[["rxcui", "str"]].dropna().drop_duplicates()
map_df.columns = ["rxcui", "medication_name"]
map_df =  map_df.drop_duplicates(subset=["rxcui"])

    

# Save to CSV
output_csv_path.parent.mkdir(parents=True, exist_ok=True)
map_df.to_csv(output_csv_path, index=False)

print(f"Transformed file saved to: {output_csv_path}")
print(f"{len(map_df)} rows written.")
