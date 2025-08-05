
# ETL Pipeline for DFI Clinical Data

This README outlines the steps to run the ETL (Extract, Transform, Load) process for integrating and standardizing liver disease-related clinical and omics data.

---

##  Directory Structure

```
├── project_root/
│   ├── create_tables.sql
│   ├── mapping structure.md
│   ├── README.md
│   ├── credentials/
│   │   ├── credentials.env
│   ├── standardized_vocabularies/
│   │   ├── raw/
│   │   │   ├── atc/
│   │   │   │   ├── WHO ATC-DDD 2024-07-31.csv
│   │   │   ├── icd10/
│   │   │   │   ├── icd10cm_tabular_2025.xml
│   │   │   ├── loinc/
│   │   │   │   ├── Loinc.csv
│   │   │   ├── rxnorm/
│   │   │   │   ├── RXNCONSO.RRF
│   │   │   ├── snomed/
│   │   │   │   ├── sct2_Concept_Full_US1000124_20250301.txt
│   │   │   │   ├── sct2_Description_Full-en_US1000124_20250301.txt
│   │   ├── cleaned/                     
│   ├── ehr_data/
│   │   ├── cleaned/                      
│   │   ├── raw/
│   │   │   ├── demographics.txt
│   │   │   ├── diagnosis.txt
│   │   │   ├── lab_results.txt
│   │   │   ├── medications.txt
│   │   │   ├── metabolomic.txt
│   │   │   ├── metagenomic.txt
│   ├── scripts/
│   │   ├── create_database_tables.py
│   │   ├── validate.py
│   │   ├── install_required_libraries.py
│   │   ├── validation_scripts/
│   │   ├── load_scripts/
│   │   │   ├── load_ehr_data.py
│   │   │   ├── load_standardized_vocabulary_data.py
│   │   ├── transform_scripts/
│   │   │   ├── transform_atc.py
│   │   │   ├── transform_loinc.py
│   │   │   ├── transform_rx_norm.py
│   │   │   ├── transform_snomed.py
│   │   │   ├── map_loinc_tolab_data.py
│   │   │   ├── transform_icd10.py
│   │   │   ├── transform_ehr.py
│   ├── useful items/
│   │   
│   │   ├── liver_disease_grading_systems.sql

```

---

##  Prerequisites

- Python 3.8+
- PostgreSQL server running and schema initialized
- Environment variables or `.env` file set for DB credentials
- create database
- Unzip standardized_vocabularies.zip
- Required Python packages:
  
-run required libraries (`install_required_libraries.py`) in '/scripts'
-or
```bash
  pip install pandas sqlalchemy psycopg2-python python-dotenv 
  ```



## ETL Process
## Step 1: Run Script to create tables
 ```bash
python scripts/create_database_tables.py
 ```

### Step 2: Extract
- Copy all raw ehr data files (e.g.,`labs.txt`, `medications.txt`) into the `ehr_data/raw` 

- Copy all standardized vocabulary files (e.g.,`loinc.csv`,`RXNCONSO.RRF`) into the `standard_vocabularies/raw/{folder_name} e.g. standardized_vocabularies/raw/loinc/loinc.csv` folder

# Step 3.1: Transform internal ehr data (skip this step for this project) 
-Transformation of ehr data needs to be improved in the future when accessing real data
-Current transformation renames file columns to match schema columns
-It also enerates subject ids by assessing demographics table for current patients and mapping mrns accross tables
-run the following script:
 ```bash
python scripts/transform_scripts/transform_ehr.py
```

- # Step 3.2 Extract approriate data from standardized vocabularies
-run the following scripts:
 ```bash
python scripts/transform_scripts/transform_loinc.py
python scripts/transform_scripts/transform_rx_norm.py
python scripts/transform_scripts/transform_atc.py
python scripts/transform_scripts/transform_snomed.py
python scripts/transform_scripts/transform_icd10.py
```
### Step 4.1: Load cleaned EHR data
- Load the transformed CSVs into PostgreSQL using SQLAlchemy
 ```bash
  python scripts/load_scripts/load_ehr_data.py
  ```
### Step 4.2: Load cleaned vocabulary data
- Load the transformed CSVs into PostgreSQL using SQLAlchemy
 ```bash
  python scripts/load_scripts/load_standardized_vocabulary_data.py
```
### Step 5: Validation
- Run post-ETL validation queries to confirm data quality:
  ```bash
  python scripts/validate.py
  ```

---

##  Notes

- Always rerun `transform` scripts if raw files are updated.
- Re-run `load` scripts only after verifying transformation outputs.
- Validation scripts must pass before using the database for analysis or visualization.



## Contact

For issues or questions, contact:oluwadare.daniel21@gmail.com
