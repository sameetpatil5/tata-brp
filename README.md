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
├── .venv 
├── datasets/                       # Datasets
│   └── phrase_datasets/            # Phrase Datasets
│       └── phrase_datasets.csv
│       └── augmentated_phrase_dataset.csv
│       └── medical_synonym.json
├── models/
├── phrase_detection_module         # Phrase detection module
│   └── phrase_data_augmentation.py
│   └── phrase_detection_module_local_script.py
│   └── phrase_detection.py
├── .gitignore
├── LICENSE
├── README.md                       # Project description and setup instructions
└── requirements.txt
```

>The above directory structure, and the modules are subject to change.

---

## Testing

Unit tests are located in the `tests` folder. To run the tests, use:

```bash
pytest tests/
```

---

## Workflow Guidelines

### File and Folder Naming

- Use **snake_case** for all **files** and **folders**.
  - Example: `data_processing.py`, `phrase_detection_module`
- Name **data** and **datasets** in the **singular form**.
  - Example: `dataset.csv`, `synonym.json`

### Git Commit Guidelines

- Keep commits **simple and short**, describing the change.
  - Example: `Fix bug in data extraction`
- **Commit frequently** at small increments.
  - Example: `Add data preprocessing`, `Fix typo in README`
- For **multiple changes**, separate messages with commas.
  - Example: `Fix data loading, update training script, improve logging`

### Pull Request Guidelines

- Always create a **pull request** for merging changes to the `main` or *any* branch.
- Use clear and concise PR titles and descriptions.
  - Example: `Add data preprocessing step to pipeline`

---

## License

This project is proprietary and for internal use only. All rights are reserved by [Your Company/Organization Name]. Unauthorized use, reproduction, or distribution of this project is prohibited.

---

### Contact

For inquiries or permissions, please contact the **development team**.

- Sameet Patil - [LinkedIn Profile](https://www.linkedin.com/in/sameetpatil5)
- Kartik Dani - [LinkedIn Profile](https://www.linkedin.com/in/kartik-dani-06744b257)
- Siddhant Ingole - [LinkedIn Profile](https://www.linkedin.com/in/siddhant-ingole-70b412260/)
