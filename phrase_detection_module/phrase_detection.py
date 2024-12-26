from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
from phrase_detection_module_constants import *
import joblib

# Load Dataset
data = pd.read_csv(AUGMENTED_PHRASE_DATASET)
X = data['Phrase']
y = data['Category']

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1, random_state=42)

# Vectorize Text
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Classifier
classifier = SVC(kernel='rbf', random_state=42)
classifier.fit(X_train_vec, y_train)

# Save Model
joblib.dump((classifier, vectorizer), PHRASE_DETECTION_MODEL)

# Evaluate Model
predictions = classifier.predict(X_test_vec)
print(classification_report(y_test, predictions))
