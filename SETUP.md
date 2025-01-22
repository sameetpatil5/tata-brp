# Setup Instructions for Blood Report Extraction App for Development and Testing Purposes

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

### 3. Set Up Environment Variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Ensure the `.env` file is not shared publicly or committed to version control.

### 4. Run the Application

After setting up the environment and installing the dependencies, you can run the FastAPI application locally:

```bash
python run.py
```

The application will be accessible at `http://127.0.0.1:8000`.

>Uncomment the development serve line in `run.py`.  `uvicorn.run("server.api:app", reload=True)`

---

#### Testing

>:warning: The `tests/` is currently dumped for multiple reasons.

Unit tests are available in the `tests/` directory. To run the tests, use:

```bash
pytest tests/
```

#### Troubleshooting

- Ensure all required dependencies are installed by checking `requirements.txt`.
- If the API key is not working, verify it is correctly set in the `.env` file.

For further assistance, please contact the project owner.

---
