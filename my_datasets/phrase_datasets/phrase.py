# Define the classification dictionary
classification_dict ={
  "WBC count": [
    "Total leukocyte count",
    "WBC count",
    "White cell count",
    "Total white cell count",
    "Total white count"
  ],
  "Platelets": ["Platelet count", "Platelets", "Plt"],
  "Neutrophil %": [
    "Neutrophil %",
    "Polymorphs",
    "Polymorphonuclear leucocytes",
    "Neutrophils",
    "Segmented neutrophils"
  ],
  "Lymphocyte %": ["Lymphocyte %", "Lymphocytes"],
  "Haemoglobin": ["Hemoglobin", "Haemoglobin", "Hb"],
  "WBC count x Neutrophil %": [
    "Absolute neutrophil count (ANC)",
    "Abs Neutrophil count",
    "ANC"
  ],
  "WBC count x lymphocyte %": [
    "Absolute lymphocyte count (ALC)",
    "Abs Lymphocyte count",
    "ALC"
  ]
}

# Common terms that should be considered as "Unknown"
common_terms = {"count", "term", "percentage", "level", "amount", "value"}

# Valid short terms that should be classified correctly
valid_short_terms = {"hb", "wbc", "plts"}
