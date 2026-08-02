import pandas as pd
import re
import joblib
import numpy as np
from scipy.sparse import hstack
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import os

# Create Models directory if it doesn't exist
os.makedirs("Models", exist_ok=True)

data = pd.read_csv("reviews.csv")
print("\nDataset Loaded Successfully!")

# Select Required Columns
data = data[['text_', 'label']]
data.columns = ['original_text', 'label']

# Convert labels
data['label'] = data['label'].map({'CG': 0, 'OR': 1})

# Text Cleaning function
def clean_text(text):
    text = str(text).lower()                  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)       # Remove punctuation
    text = re.sub(r'\s+', ' ', text)          # Remove extra spaces
    return text.strip()

# Apply cleaning to a new column
data['review'] = data['original_text'].apply(clean_text)

# Extract Numerical Metadata Features
def extract_metadata(df):
    features = pd.DataFrame()
    
    # 1. Word count
    features['word_count'] = df['original_text'].apply(lambda x: len(str(x).split()))
    
    # 2. Exclamation ratio
    features['excl_ratio'] = df['original_text'].apply(lambda x: str(x).count('!') / (len(str(x)) + 1))
    
    # 3. ALL CAPS ratio
    features['caps_ratio'] = df['original_text'].apply(
        lambda x: sum(1 for w in str(x).split() if w.isupper() and len(w) > 1) / (len(str(x).split()) + 1)
    )
    
    # 4. Punctuation ratio
    features['punct_ratio'] = df['original_text'].apply(
        lambda x: sum(1 for c in str(x) if c in '.,!?;:"') / (len(str(x)) + 1)
    )
    
    return features

print("\nExtracting metadata features...")
metadata_features = extract_metadata(data)

# Scale metadata features
scaler = StandardScaler()
scaled_metadata = scaler.fit_transform(metadata_features)

# TF-IDF FEATURE EXTRACTION
print("\nFitting TF-IDF Vectorizer...")
vectorizer = TfidfVectorizer(max_features=5000)
X_text = vectorizer.fit_transform(data['review'])

# Combine TF-IDF and Scaled Metadata Features
X_combined = hstack([X_text, scaled_metadata])
y = data['label']

print("\nCombined Matrix Shape (Text + Metadata):", X_combined.shape)

# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X_combined,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining Samples :", X_train.shape[0])
print("Testing Samples  :", X_test.shape[0])

# LOGISTIC REGRESSION
model = LogisticRegression(max_iter=1000)

print("\nTraining Logistic Regression Model with Metadata...")
model.fit(X_train, y_train)

print("Model Training Completed!")

# MODEL EVALUATION
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")
print("{:.2f}%".format(accuracy * 100))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# SAVE MODEL AND SCALERS
joblib.dump(model, "Models/fake_review_model.pkl")
joblib.dump(vectorizer, "Models/tfidf_vectorizer.pkl")
joblib.dump(scaler, "Models/scaler.pkl")
print("Model, Vectorizer, and Scaler Saved Successfully inside Models/ directory!")
