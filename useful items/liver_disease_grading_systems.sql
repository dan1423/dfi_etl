INSERT INTO liver_meld_score_reference (meld_score_min, meld_score_max, description) VALUES
(6, 9, 'Mild severity'),
(10, 19, 'Moderate severity'),
(20, 29, 'Severe'),
(30, 39, 'Very severe'),
(40, 100, 'Critical');


INSERT INTO liver_child_pugh_score_reference (parameter, value_range, score, description) VALUES
-- Encephalopathy
('Encephalopathy', 'None', 1, 'No hepatic encephalopathy'),
('Encephalopathy', 'Grade 1–2', 2, 'Mild to moderate encephalopathy'),
('Encephalopathy', 'Grade 3–4', 3, 'Severe encephalopathy'),

-- Ascites
('Ascites', 'None', 1, 'No ascites'),
('Ascites', 'Mild', 2, 'Slight ascites, controlled with diuretics'),
('Ascites', 'Moderate to Severe', 3, 'Moderate to severe ascites, poorly controlled'),

-- Bilirubin (mg/dL)
('Bilirubin', '<2 mg/dL', 1, 'Bilirubin less than 2 mg/dL'),
('Bilirubin', '2–3 mg/dL', 2, 'Bilirubin between 2 and 3 mg/dL'),
('Bilirubin', '>3 mg/dL', 3, 'Bilirubin greater than 3 mg/dL'),

-- Albumin (g/dL)
('Albumin', '>3.5 g/dL', 1, 'Albumin greater than 3.5 g/dL'),
('Albumin', '2.8–3.5 g/dL', 2, 'Albumin between 2.8 and 3.5 g/dL'),
('Albumin', '<2.8 g/dL', 3, 'Albumin less than 2.8 g/dL'),

-- Prothrombin Time (sec prolonged)
('Prothrombin Time', '<4 sec', 1, 'Prothrombin time prolonged less than 4 seconds'),
('Prothrombin Time', '4–6 sec', 2, 'Prolonged by 4 to 6 seconds'),
('Prothrombin Time', '>6 sec', 3, 'Prolonged more than 6 seconds'),

-- INR
('INR', '<1.7', 1, 'INR less than 1.7'),
('INR', '1.7–2.3', 2, 'INR between 1.7 and 2.3'),
('INR', '>2.3', 3, 'INR greater than 2.3');

INSERT INTO liver_ascites_grading (grade, description) VALUES
(0, 'No ascites detected clinically or by imaging'),
(1, 'Mild ascites detectable only by ultrasound'),
(2, 'Moderate symmetrical distension of the abdomen'),
(3, 'Marked abdominal distension with tense ascites');

INSERT INTO liver_ecog_performance_status (ecog_score, description) VALUES
(0, 'Fully active, able to carry on all pre-disease performance without restriction'),
(1, 'Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature'),
(2, 'Ambulatory and capable of all selfcare but unable to carry out any work activities; up and about more than 50% of waking hours'),
(3, 'Capable of only limited selfcare; confined to bed or chair more than 50% of waking hours'),
(4, 'Completely disabled; cannot carry on any selfcare; totally confined to bed or chair'),
(5, 'Dead');


INSERT INTO liver_fibrosis_stage_reference (stage, description) VALUES
('F0', 'No fibrosis'),
('F1', 'Portal fibrosis without septa'),
('F2', 'Portal fibrosis with few septa'),
('F3', 'Numerous septa without cirrhosis'),
('F4', 'Cirrhosis');


INSERT INTO liver_hepatic_encephalopathy_grading (grade, description) VALUES
(0, 'Minimal hepatic encephalopathy; no detectable changes in personality or behavior, normal examination'),
(1, 'Trivial lack of awareness, euphoria or anxiety, shortened attention span'),
(2, 'Lethargy, disorientation to time, inappropriate behavior'),
(3, 'Somnolence, confusion, gross disorientation'),
(4, 'Coma, unresponsive to verbal or noxious stimuli');
