# Blood Report Extraction App

[![License](https://img.shields.io/badge/License-Proprietary-red)](LICENSE) [![Status: In Development](https://img.shields.io/badge/Status-In%20Development-orange)](https://github.com/sameetpatil5/) ![Legality](https://img.shields.io/badge/Legality-Confidential-red)

## Overview

This project is designed to automate the extraction and processing of blood report data. The goal is to extract structured information from various types of blood reports, standardize units, and provide actionable insights. The app uses Natural Language Processing (NLP) techniques to identify and map parameters from unstructured text data.

---

## Features

- **Data Extraction**: Extract key parameters from blood reports.
- **Unit Standardization**: Convert units into a unified format for analysis.
- **Report Parsing**: Parse unstructured data into a structured format.
- **Configurable Output**: Output can be customized based on report format.

---

## Installation

To set up this project locally, follow the steps in the [setup.md](setup.md).

---

## Usage

Once the environment is set up, you can run the main script to extract and process blood report data. Ensure that the `nltk_data` is properly configured as described in the setup instructions.

---

## Project Structure

```bash
blood-report-extraction/
│
├── blood_report_extraction.py      # Main script
├── data_preprocessing.py           # Data preprocessing module
├── report_scanner.py               # Scanning and extraction module
├── unit_converter.py               # Unit conversion module
├── parameter_mapping.py            # Parameter mapping module
├── config.py                       # Configuration file
├── tests/                          # Test files
│   └── test_blood_report_extraction.py  # Unit tests for blood report extraction
├── README.md                       # Project description and setup instructions
└── requirements.txt
```

>Currently, the project does not follow the above directory structure, and the modules are subject to change.

---

## Testing

Unit tests are located in the `tests` folder. To run the tests, use:

```bash
pytest tests/
```

---

## License

This project is proprietary and for internal use only. All rights are reserved by [Your Company/Organization Name]. Unauthorized use, reproduction, or distribution of this project is prohibited.

For inquiries or permissions, please contact [Your Contact Information].
