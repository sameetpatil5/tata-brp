# Blood Report Extraction App

[![License](https://img.shields.io/badge/License-Proprietary-red)](LICENSE) [![Status: In Development](https://img.shields.io/badge/Status-In%20Development-orange)](https://github.com/sameetpatil5/) ![Legality](https://img.shields.io/badge/Legality-Confidential-red)

## Overview

This project automates the extraction and formatting of blood report data. It processes markdown inputs containing medical tables and extracts the data as required and sends the extracted data back. The application uses FastAPI and requires a Gemini API key for formatting operations.

---

## Features

- **Data Formatting**: Corrects formatting errors in markdown inputs using LLM.
- **Data Extraction**: Extract key parameters from blood reports.
- **Report Parsing**: Parse unstructured data and identifies the required phrases.
- **Unit Standardization**: Convert units into a unified format for analysis.
- **Configurable Output**: Output can be customized based on report format.

---

## Installation

To set up this project locally, follow the steps in the [setup.md](setup.md).

---

## Usage

Once the environment is set up, you can run the FastAPI application locally using:

```bash
python run.py
```

Access the application at `http://127.0.0.1:8000` and use the provided endpoints for formatting markdown inputs.

>Uncomment the development serve line in `run.py`.  `uvicorn.run("server.api:app", reload=True)`

---

## Project Structure

```bash
blood-report-extraction/
│
├── .venv
├── data/                         # Contains data for processing the report
├── server/                       # FastAPI application code
│   ├── modules/                  # Modules to process the report in various stages
│   │   ├── chunking.py
│   │   ├── data_extractor.py
│   │   ├── format_data.py
│   │   ├── phrase_detection.py
│   │   └── unit_conversion.py
│   ├── api.py                    # FastAPI app flie
│   ├── routes.py                 # Routes for FastAPI
│   ├── models.py                 # Models for FastAPI
│   └── ocrprocessor.py           # OCRProcessor for processing the report (build using the programs in `modules/`)
├── run.py                        # Entry point for the FastAPI app
├── tests/                        # Unit tests (> dumped)
├── .gitignore                    # GitIgnore files and directories
├── LICENSE                       # License
├── README.md                     # Project description and setup instructions
├── requirements.txt              # Required Python packages
├── setup.md                      # Setup instructions
└── vercel.json                   # Vercel deployment configuration
```

>The above directory structure and modules are subject to change.

---

## Testing

>:warning: The `tests/` is currently dumped for multiple reasons.

Unit tests are located in the `tests` folder. To run the tests, use:

```bash
pytest tests/
```

---

## Workflow Guidelines

### File and Folder Naming

- Use **snake_case** for all **files** and **folders**.
  - Example: `data_processing.py`, `utils`
- Name **data** and **datasets** in the **singular form**.
  - Example: `dataset.csv`, `config.json`

### Git Commit Guidelines

- Keep commits **simple and short**, describing the change.
  - Example: `Fix bug in data formatting`
- **Commit frequently** at small increments.
  - Example: `Add API endpoint for formatting`, `Update README`
- For **multiple changes**, separate messages with commas.
  - Example: `Fix API bug, update tests, improve error handling`

### Pull Request Guidelines

- Always create a **pull request** for merging changes to the `main` or *any* branch.
- Use clear and concise PR titles and descriptions.
  - Example: `Add table formatting functionality`

---

## License

This project is proprietary and for internal use only. All rights are reserved by [Your Company/Organization Name]. Unauthorized use, reproduction, or distribution of this project is prohibited.

---

### Contact

For inquiries or permissions, please contact the **development team**.

- Sameet Patil - [LinkedIn Profile](https://www.linkedin.com/in/sameetpatil5)
- Kartik Dani - [LinkedIn Profile](https://www.linkedin.com/in/kartik-dani-06744b257)
- Siddhant Ingole - [LinkedIn Profile](https://www.linkedin.com/in/siddhant-ingole-70b412260/)
