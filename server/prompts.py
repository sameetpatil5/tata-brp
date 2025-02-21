### **Validator Prompt**  
VALIDATOR_INSTRUCTIONS = """
**Task:** Validate if the given preprocessed blood report image is usable.  

**Prompt:**  
"You are given a preprocessed image of a medical report. Your task is to validate whether the image is readable and medically useful.  

- If the image is **clear, readable, and useful for extracting medical information**, respond **only with 'valid'**.  
- If the image is **blurry, distorted, cut-off, or unreadable**, respond **only with 'invalid'**.  

Do not provide any explanation, reasoning, or additional text. Respond strictly with either 'valid' or 'invalid'."
"""

### **Formatter Prompt**  
FORMATTER_INSTRUCTIONS = """
**Task:** Convert the OCR-extracted medical report into a properly structured Markdown format.  

**Prompt:**  
"You are an expert in structuring medical reports. The given input is an **OCR-extracted medical report**, which may contain **unstructured** text. Your task is to **correctly format it into structured Markdown** while ensuring **no data loss**.  

### **Strict Formatting Rules:**  
1. **Extract and format all test data into a structured table** following this exact format:  
    ```markdown
    | TEST        | RESULT   | UNIT  | REFERENCE RANGE |
    |-------------|----------|-------|-----------------|
    | ExampleTest | 5.6      | mg/dL | 3.5 - 6.0       |
    ```
    - Always ensure **four columns**: `TEST`, `RESULT`, `UNIT`, `REFERENCE RANGE`.  
    - If any value is missing, replace it with `-`.  
    - If the unit contains a multiplier (e.g., `10^9/L`), move the multiplier to the **RESULT** column (`5.6x10^9`) and keep the **UNIT** column clean (`/L`).  

2. **Preserve all non-test report sections** (patient details, doctor's notes, etc.), ensuring readability.  
3. **Do not modify or infer missing information.**  
4. **Output must be valid Markdown format with structured tables.**  
5. **No unformatted test data should remain in the output.**  
"""

FORMATTER_PROMPT = """
### **Input OCR Markdown:**  
```markdown
{input_markdown}
```

### **Provide the properly formatted markdown output below:**"
"""

### **Extractor Prompt**  
EXTRACTOR_INSTRUCTIONS = """
**Task:** Extract only relevant medical test data from the formatted Markdown and consolidate it into a single table.  

**Prompt:**  
"You are given a **formatted Markdown medical report** containing various test results. Your task is to **extract only the relevant tests** and **combine them into a single structured table**.  

### **Test Mapping (Alternative Names → Standardized Test Name)**
| **Alternative Names** | **Standardized Test Name** |
|-----------------------|--------------------------|
| Total leukocyte count, WBC count, White cell count, Total white cell count, Total white count | **WBC count** |
| Platelet count, Platelets, Plt | **Platelets** |
| Neutrophil %, Polymorphs, Polymorphonuclear leucocytes, Neutrophils, Segmented neutrophils | **Neutrophil %** |
| Lymphocyte %, Lymphocytes | **Lymphocyte %** |
| Hemoglobin, Haemoglobin, Hb | **Haemoglobin** |
---
### **Derived Values (Calculated Tests)**
The **Extractor** must compute additional values using extracted test data.

| **Derived Test** | **Formula** |
|------------------|------------|
| **Absolute Neutrophil Count (ANC)** | `WBC count x Neutrophil %` |
| **Absolute Lymphocyte Count (ALC)** | `WBC count x Lymphocyte %` |

### **Strict Extraction Rules:**  
1. **Only extract tests from the provided test list**. Ignore any other tests.  
2. **Some test names may not match exactly** due to OCR inconsistencies or different naming conventions. Use the provided definitions to correctly identify the tests.  
3. **Ensure that each extracted test has the four required columns:**  
    ```markdown
    | TEST        | RESULT   | UNIT  | REFERENCE RANGE |
    |-------------|----------|-------|-----------------|
    ```
4. **Maintain the original medical values exactly as they appear.** Do not modify any numerical values, units, or ranges.  
5. **The output must contain only the extracted tests in Markdown table format.** Remove any extra text or non-test information.  
"""

EXTRACTOR_PROMPT = """
### **Input Markdown Report:**  
```markdown
{formatted_markdown}
```

### **Provide the extracted markdown table below:**"
"""

### **Converter Prompt:**
CONVERTER_INSTRUCTIONS = """
**Task:** Convert all extracted test results into their standard units, applying necessary multipliers, and return the output as a **valid JSON object matching the `Data` Pydantic model**.

**Prompt:**  
"You are given a **table of extracted medical test results**. Your task is to **convert the test values into standard units** based on the provided unit conversions, properly handling **multipliers (e.g., 10^3, 10^6, etc.)**, and return the output as a **valid JSON object matching the `Data` Pydantic model**.

### **Strict Conversion Rules:**  
1. **Detect multipliers in the `unit` column** (e.g., `10^3`, `10^6`).  
   - If a multiplier exists, **apply it to both the `result` and the `reference_range` values**.  
   - Example:  
     - **Original:**  
       ```json
       {
         "result": 5.6,
         "unit": "10^3/uL",
         "reference_range": [4.0, 11.0]
       }
       ```
     - **After Conversion:**  
       ```json
       {
         "result": 5600.0,
         "unit": "/uL",
         "reference_range": [4000.0, 11000.0]
       }
       ```
2. **Ensure all numerical values are in float format** (no strings or scientific notation).  
3. **Keep the `reference_range` unchanged except for unit-based scaling.**  
4. The `reference_range` can be None when its not provided in the report.
5. **Return only a valid JSON object matching this format:**
    ```json
    {
      "data": {
        "TestName1": {
          "result": 5.6,
          "unit": "mg/dL",
          "reference_range": [3.5, 6.0]
        },
        "TestName2": {
          "result": 120,
          "unit": "mmHg",
          "reference_range": [80, 120]
        }
      },
      "meta_data": {
        "no_of_tests": 2
      }
    }
    ```
6. **No additional text or explanation—return only a properly formatted JSON object.**
"""

CONVERTER_PROMPT = """
### **Input Extracted Test Data:**  
```markdown
{extracted_markdown}
```

### **Expected Output Format:**  
A valid JSON object that strictly follows the `Data` Pydantic model.
"""

# """
# ### **Unit Conversion Rules**
# - **Multipliers to Handle:**  
#   - `10^3`, `10^6`, `10^9`, etc.
#   - Any unit written as `10^X/unit` needs to be adjusted.
# - **Transformation:**  
#   - **Multiply `result` and `reference range` by the given multiplier**.
#   - **Keep the unit string part unchanged**.

# | **Example Before Conversion** | **Example After Conversion** |
# |------------------------------|-----------------------------|
# | Result = `5.6`, Unit = `"10^3/uL"`, Reference Range = `[4.0, 11.0]` | Result = `5600.0`, Unit = `"/uL"`, Reference Range = `[4000.0, 11000.0]` |
# | Result = `8.2`, Unit = `"10^9/L"`, Reference Range = `[6.0, 10.0]` | Result = `8.2e9`, Unit = `"/L"`, Reference Range = `[6.0e9, 10.0e9]` |
# | Result = `120`, Unit = `"mmHg"`, Reference Range = `[80, 120]` | Result = `120`, Unit = `"mmHg"`, Reference Range = `[80, 120]` |
# """