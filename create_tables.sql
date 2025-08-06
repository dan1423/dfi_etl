
CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    mrn TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS demographics (
   id SERIAL PRIMARY KEY,    
    subject_id INTEGER REFERENCES subjects(id),          
    mrn TEXT,                                     
    first_name TEXT,
    last_name TEXT,
    date_of_birth DATE,
    sex TEXT,
    race TEXT,
    ethnicity TEXT,
    death_date DATE
);

CREATE TABLE IF NOT EXISTS encounter (
    encounter_id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(id),
    encounter_type TEXT,
    encounter_date TEXT
);

CREATE TABLE IF NOT EXISTS disease (
    disease_id SERIAL PRIMARY KEY,
    disease_name TEXT,
    description TEXT,
    icd10_code TEXT
);

CREATE TABLE IF NOT EXISTS diagnosis (
    diagnosis_id SERIAL PRIMARY KEY,
     subject_id INTEGER REFERENCES subjects(id),
    encounter INTEGER REFERENCES encounter(encounter_id),
    dx_name TEXT,
    diagnosis_date DATE,
    disease_id INTEGER REFERENCES disease(disease_id),
    icd10_code TEXT,
    dxrank_id INTEGER
);

CREATE TABLE IF NOT EXISTS icd10_chapters
(
    chapter integer  PRIMARY KEY,
    description TEXT
);
CREATE TABLE IF NOT EXISTS icd10_code_ranges (
    code_range_id SERIAL PRIMARY KEY,
    chapter INTEGER REFERENCES icd10_chapters(chapter),
    code_range TEXT UNIQUE,
    description TEXT
);


CREATE TABLE IF NOT EXISTS icd10_codes (
    icd10_id SERIAL PRIMARY KEY,
    code TEXT,
    description TEXT,
    code_range TEXT
);

-- Labs
CREATE TABLE IF NOT EXISTS lab_component_loinc_map (
    id SERIAL PRIMARY KEY,
    loinc_code TEXT UNIQUE,
    component TEXT,
    system TEXT,
    class_type INTEGER,
    long_common_name TEXT,
    ucum_units TEXT

);

CREATE TABLE IF NOT EXISTS lab_component_snomed_map (
    id SERIAL PRIMARY KEY,
    snomed_code TEXT,
    snomed_term TEXT,
    hierarchy_type TEXT

);


CREATE TABLE IF NOT EXISTS labs (
    lab_id SERIAL PRIMARY KEY,
     subject_id INTEGER REFERENCES subjects(id),
    mrn TEXT,
    component_id TEXT,
    component_name TEXT,
    ord_value TEXT,
    result_in_range_yn TEXT,
    reference_unit TEXT,
    result_flag TEXT,
    spec_take_time TEXT,
    proc_id TEXT,
    proc_name TEXT,
    loinc_code TEXT ,
    snomect_code TEXT
);

-- Medications
CREATE TABLE IF NOT EXISTS medication_rxnorm_code_map (
    id SERIAL PRIMARY KEY,
    rxcui INTEGER,
    medication_name TEXT
);

CREATE TABLE IF NOT EXISTS medication_atc_code_map (
    atc_code TEXT PRIMARY KEY,
    atc_name TEXT
);
CREATE TABLE IF NOT EXISTS treatment (
    treatment_id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(id),
    disease_id INTEGER REFERENCES disease(disease_id),
    treatment_name TEXT,      
    treatment_type TEXT,       
    cpt_code TEXT,             
    icd_proc_code TEXT,        
    start_date DATE,
    end_date DATE,
    notes TEXT
);


CREATE TABLE IF NOT EXISTS medications (
    medication_id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(id),
    mrn TEXT,
    medication_name TEXT,
    thera_class_c TEXT,
    med_thera_class TEXT,
    pharm_class_c TEXT,
    med_pharm_class TEXT,
    pharm_subclass_c TEXT,
    med_pharm_sub_class TEXT,
    take_med_dose TEXT,
    take_med_dttm TEXT,
    rxnorm_code INTEGER,
    atc_code TEXT,
    treatment_id INTEGER REFERENCES treatment(treatment_id)
);

-- Vitals
CREATE TABLE IF NOT EXISTS vital (
    vital_id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(id),
    measurement_name TEXT,
    measurement_value TEXT,
    measurement_time TEXT,
    units TEXT,
    location TEXT,
    group_name TEXT,
    dept_id TEXT
);

-- Liver Disease Scores
CREATE TABLE IF NOT EXISTS liver_child_pugh_score_reference (
    parameter TEXT PRIMARY KEY,
    value_range TEXT,
    score INTEGER,
    description TEXT
);

CREATE TABLE IF NOT EXISTS liver_ecog_performance_status (
    ecog_score INTEGER PRIMARY KEY,
    description TEXT
);

CREATE TABLE IF NOT EXISTS liver_meld_score_reference (
    meld_range TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE IF NOT EXISTS liver_ascites_grading (
    grade TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE IF NOT EXISTS liver_hepatic_encephalopathy_grading (
    grade TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE IF NOT EXISTS liver_fibrosis_stage_reference (
    stage TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE IF NOT EXISTS liver_disease (
    liver_disease_id SERIAL PRIMARY KEY,
    diagnosis_date DATE,
    disease_id INTEGER REFERENCES disease(disease_id),
    etiology TEXT,
    fibrosis_stage TEXT,
    child_pugh_score TEXT,
    meld_score REAL,
    ascites_grade TEXT,
    he_grade TEXT ,
    ecog_score INTEGER,
    icd10_code TEXT
);


-- Metabolomics & Metagenomics
CREATE TABLE IF NOT EXISTS metabolomics (
    metabolomics_id TEXT,
    mrn TEXT,
    subject_id INTEGER REFERENCES subjects(id),
    hmmf_panel TEXT,
    ms_type TEXT,
    compound TEXT,
    pubchem_id TEXT,
    value TEXT,
    value_ug_ml TEXT,
    value_mm TEXT,
    value_um TEXT
);

CREATE TABLE IF NOT EXISTS metagenomics (
    result_id TEXT,
    mrn TEXT,
     subject_id INTEGER REFERENCES subjects(id),
    seq_id TEXT,
    clade_name TEXT,
    clade_taxid TEXT,
    relative_abundance TEXT,
    coverage TEXT,
    estimated_number_of_reads TEXT,
    filename TEXT,
    database_used TEXT,
    kingdom TEXT,
    phylum TEXT,
    class TEXT,
    "order" TEXT,
    family TEXT,
    genus TEXT,
    species TEXT,
    sgb TEXT,
    taxid TEXT,
    taxonomy TEXT,
    clean_relative_abundance TEXT
);

