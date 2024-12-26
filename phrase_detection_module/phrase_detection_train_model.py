from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
import pandas as pd
import joblib
from phrase_detection_module_constants import *

# Load Dataset
data = pd.read_csv(AUGMENTED_PHRASE_DATASET)
X = data['Phrase']
y = data['Category']

# Vectorize Text
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train Classifier using entire dataset
classifier = SVC(kernel='rbf', random_state=42)
classifier.fit(X_vec, y)

# Save Model
joblib.dump((classifier, vectorizer), PHRASE_DETECTION_MODEL)

# Load Test Data
test_data = pd.read_csv(PHRASE_TEST_DATASET)
X_test = test_data['Phrase']
y_test = test_data['Category']

# Vectorize Test Data
X_test_vec = vectorizer.transform(X_test)

# Evaluate Model on Test Data
predictions = classifier.predict(X_test_vec)
print(classification_report(y_test, predictions))
