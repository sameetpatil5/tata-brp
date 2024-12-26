# --- Download NLTK data --- #

# Import NLTK
import nltk

# Set the path to the virtual environment's nltk_data folder
nltk.download('wordnet', download_dir='.venv/nltk_data')
nltk.download('omw-1.4', download_dir='.venv/nltk_data')

# Set NLTK to only use the virtual environment's nltk_data folder
nltk.data.path = ['.venv\\nltk_data']

# Verify the directories NLTK will check
print(nltk.data.path)
