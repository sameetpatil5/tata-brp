# Setup Instructions for Blood Report Extraction App for development and testing purposes

## Prerequisites

- Python 3.x
- Virtual environment `.venv`
- Required Python packages listed in `requirements.txt`

---

## Local Configuration

### 1. Set Up the Virtual Environment

Create a virtual environment and activate it:

```bash
python -m venv .venv   # Creates the virtual environment
source .venv/bin/activate   # For Linux/macOS
.venv\Scripts\activate   # For Windows
```

### 2. Install Required Packages

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Download NLTK Data

Ensure that the necessary NLTK data is downloaded and stored in the virtual environment. Run the following Python script:

```python
import nltk

# Set the path to the virtual environment's nltk_data folder

nltk.download('wordnet', download_dir='.venv/nltk_data')
nltk.download('omw-1.4', download_dir='.venv/nltk_data')

# Set NLTK to only use the virtual environment's nltk_data folder

nltk.data.path = ['.venv\\nltk_data']

# Verify the directories NLTK will check

print(nltk.data.path)
```

### 4. Verify NLTK Data Path

Run the script above to ensure that NLTK is using the correct directory for its data files. You should see `.venv\\nltk_data` in the printed list.

### 5. Run the Application

After setting up the environment and downloading the necessary NLTK data, you can run the main script to start processing blood reports:

```bash
python blood_report_extraction.py
```

---

#### Testing

Unit tests are available in the `tests/` directory. To run the tests, use:

```bash
pytest tests/
```

#### Troubleshooting

If NLTK is unable to find the data, ensure that the environment variable NLTK_DATA is set to `.venv/nltk_data`.
Ensure all required dependencies are installed by checking `requirements.txt`.

For further assistance, please contact the project owner.

---
