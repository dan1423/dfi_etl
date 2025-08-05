

This document describes the source files used in the ETL pipeline and maps original columns to the transformed database schema.

Only **seven transformed clinical files** were made available by the dfi. These files were delivered in a clean, analysis-ready format (`.txt`, tab-delimited) and required no additional transformation beyond basic inspection:

- `diagnosis.txt`
- `lab_results.txt`
- `medications.txt`
- `demographics.txt`
- `metabolomics.txt`
- `metagenomics.txt`

These will be treated as *finalized* and used directly in the Load step of the ETL process.


The following files were obtained from authoritative public sources and transformed using custom scripts:

| Standard        | Source Format | Transformation Details |
|----------------|----------------|--------------------------|
| **ICD-10**      | XML (tabular)  | Parsed into chapters, subchapters, and codes |
| **LOINC**       | CSV            | Cleaned, filtered by `CLASS` and `PROPERTY`, and renamed to snake_case |
| **SNOMED CT**   | RF2 (TXT)      | Filtered for `observable entity` semantic tag and extracted descendants |
| **RxNorm**      | CSV/API        | Extracted `rxcui`, `medication_name`, mapped to drug classes |
| **ATC/DDD**     | WHO CSV        | Loaded into `medication_atc_code_map`, normalized headers |
| **Liver Scoring Tables** | Manual | Created MELD, Child-Pugh, ECOG, Fibrosis, Ascites, HE grading tables |


## Downloaded Medical Code Sets and Sources

This section lists the external standardized vocabularies and coding systems downloaded for integration or reference within the liver disease clinical data project. Code mapping is deferred as part of future work.

---

##  Standard Code Sets

### 1. **LOINC (Logical Observation Identifiers Names and Codes)**
- **File(s)**: `loinc.csv`
- **Source**: [https://loinc.org/downloads/](https://loinc.org/downloads/loinc/)
- **Description**: Standard codes for lab tests and clinical observations.
- **Use**: Will be used for mapping `Lab.ComponentName`, `ProcName`, and `ReferenceUnit`.

---

### 2. **SNOMED CT (Systematized Nomenclature of Medicine — Clinical Terms)**
- **File(s)**: `snomed_observable_entities.txt`, `snomed_full_download.zip`
- **Source**: [https://www.nlm.nih.gov/healthit/snomedct/index.html](https://www.nlm.nih.gov/healthit/snomedct/index.html)
- **Description**: Hierarchical terminology for clinical findings, procedures, and observable entities.
- **Use**: Will support concept mapping for labs, vitals, and diagnoses in future phases.

---

### 3. **RxNorm**

- **Source**: [https://www.nlm.nih.gov/research/umls/rxnorm/index.html](https://www.nlm.nih.gov/research/umls/rxnorm/index.html)
- **Description**: Normalized names for clinical drugs and their ingredients.
- **Use**: Will enable medication mapping to RxCUI for decision support and drug classification.

---

### 4. **ICD-10-CM (International Classification of Diseases, 10th Revision, Clinical Modification)**
- **File(s)**: `icd10cm_tabular_2025.xml`
- **Source**: [https://www.cms.gov/medicare/icd-10/2025-icd-10-cm](https://www.cms.gov/medicare/icd-10/2025-icd-10-cm)
- **Description**: Diagnosis codes used for clinical documentation and billing in the U.S.
- **Use**: To define and group liver-related diagnosis codes (e.g., K70–K77).

---

### 5. **ATC Classification System (Anatomical Therapeutic Chemical)**
- **File(s)**: `atc_codes.csv` *(optional/add-on if used with RxClass or DrugBank)*
- **Source**: [https://www.whocc.no/atc_ddd_index/](https://www.whocc.no/atc_ddd_index/)
- **Description**: Drug classification by therapeutic use and chemical properties.
- **Use**: May be used to classify drugs into broader therapeutic categories.

---

## 🕒 Last Updated
- **Date**: July 2025
- **Note**: These vocabularies will be used for future mapping and enrichment in the project.

---




Other files listed in this documentation are **for reference or potential future ingestion**, but were not available at the time of this project.



Source File Summary

| Original File                     | Transformed File       | Description                             |
|----------------------------------|------------------------|-----------------------------------------|
| **PAMER_DM_PATIENT_DEMO.txt**        | demographics.txt       | Patient demographics                    |
| **PAMER_DM_ENC.txt**                 | encounters.txt         | Encounter header records                |
| **PAMER_DM_ENC_ADT.txt**             | encounters.txt         | ADT event details                       |
| **PAMER_DM_ENC_DRG.txt**             | encounters.txt         | DRG classification for encounters       |
| **PAMER_DM_ENC_DX.txt**              | diagnosis.txt          | Diagnoses with ICD-10 codes             |
| **PAMER_DM_ENC_LAB.txt**             | labs.txt               | Lab test results                        |
| **PAMER_DM_ENC_FLO_PART_1.txt**      | vitals.txt             | Vitals and flow sheet part 1            |
| **PAMER_DM_ENC_FLO_PART_2.txt**      | vitals.txt             | Vitals and flow sheet part 2            |
| **PAMER_DM_ENC_RX.txt**              | medications.txt        | Inpatient medications                   |
| **PAMER_DM_ENC_RX_OUT.txt**          | medications.txt        | Outpatient medications                  |
| **PAMER_DM_ENC_RX_MAR.txt**          | medications.txt        | Medication administration records       |
| **PAMER_DM_RX_LOOKUPS_20210108.txt**| rx_lookup.txt          | Medication lookup metadata              |
| **PAMER_DM_ENC_PROC_CPT.txt**        | procedure_cpt.txt      | CPT-coded procedures                    |
| **PAMER_DM_ENC_PROC_ICD.txt**        | procedure_icd.txt      | ICD-coded procedures                    |
| **metabolomics.txt**                 | metabolomics.txt       | Metabolomics profiles                   |
| **metagenomics.txt**                 | metagenomics.txt       | Metagenomics profiles                   |

---
 Original-> Transformed-> Database Schema

| Original File | Transformed File | Column Names (from file) | Database Columns (mapped) |
|---------------|------------------|---------------------------|----------------------------|
|**PAMER_DM_PATIENT_DEMO.txt** | demographics.txt | mrn, birth_date, sex_code, race_code, ethnic_code, city, state_code, death_date | mrn, birth_date, sex, race, ethnicity, city, state, death_date,subject_id (generated) |
| **PAMER_DM_ENC.txt** | encounters.txt | har, adm_date, disc_date, encounter_type, MRN, min_service_date, max_service_date, encounter_EIO | har, adm_date, disc_date, encounter_type, MRN, min_service_date, max_service_date |
| **PAMER_DM_ENC_ADT.txt** | encounters.txt | mrn, har, pat_enc_csn_id, event_id, event_type_c, event_type, effective_time, event_time, adt_dept | effective_time, event_time, department |
| **PAMER_DM_ENC_DRG.txt** | encounters.txt | mrn, har, drg, drg_name, drg_rank, drg_type | har, drg, drg_name, drg_rank, drg_type |
| **PAMER_DM_ENC_DX.txt** | diagnosis.txt | mrn, har, dx_name, icd10_code, dx_rank, poa | mrn, icd10_code, dx_name, dx_rank |
| **PAMER_DM_ENC_LAB.txt** | labs.txt | mrn, component_id, component_name, ord_value, reference_unit, result_flag, spec_take_time, lnc_code | mrn, component_id, component_name, ord_value, reference_unit, result_flag, spec_take_time, loinc_code |
| **PAMER_DM_ENC_FLO_PART_1.txt** | vitals.txt | mrn, flo_meas_name, meas_value, recorded_time, units, meas_location, flo_group_name, dept_id | mrn, measurement_name, measurement_value, measurement_time, units, location, group_name, dept_id |
| **PAMER_DM_ENC_FLO_PART_2.txt** | vitals.txt | (same as above) | (same as above) |
| **PAMER_DM_ENC_RX.txt** | medications.txt | mrn, medication_id, medication_name, dose, quantity, dose_units, rxnorm_code, thera_class_c, pharm_class_c | mrn, medication_id, medication_name, take_med_dose, rxnorm_code, thera_class_c, pharm_class_c |
| **PAMER_DM_ENC_RX_OUT.txt** | medications.txt | MRN, ORDER_DATE, MED_ID, MEDICATION, MED_ROUTE, QUANTITY | mrn, medication_name, take_med_dose |
| **PAMER_DM_ENC_RX_MAR.txt** | medications.txt | mrn, MEDICATION_ID, MEDICATION_NAME, DOSE, DOSE_UNITS, TAKE_MED_DTTM, RXNORM_CODE | mrn, medication_id, medication_name, take_med_dose, take_med_dttm, rxnorm_code |
| **PAMER_DM_RX_LOOKUPS_20210108.txt** | rx_lookup.txt | medication_id, med_name, med_name_generic, pharm_class_c, pharm_sub_class_c, thera_class_c | medication_id, medication_name, med_pharm_class, med_pharm_sub_class, med_thera_class |
| **PAMER_DM_ENC_PROC_CPT.txt** | procedure_cpt.txt | mrn, cpt_code, proc_name, min_service_date, max_service_date | mrn, cpt_code, proc_name, min_service_date, max_service_date |
| **PAMER_DM_ENC_PROC_ICD.txt** | procedure_icd.txt | mrn, ICD_Code, icd_name, proc_date | mrn, icd_code, icd_name, proc_date |
| **metabolomics.txt** | metabolomics.txt | metabolomics_id, hmmf_panel, ms_type, compound, pubchem_id, value, value_ug_ml, value_mm, value_um | same |
| **metagenomics.txt** | metagenomics.txt | mrn, seq_id, clade_name, clade_taxid, relative_abundance, coverage, estimated_number_of_reads, ... | same |




