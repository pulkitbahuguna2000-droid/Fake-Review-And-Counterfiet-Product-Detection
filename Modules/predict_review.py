import re
import joblib
import numpy as np
from scipy.sparse import hstack

# =========================
# LOAD MODEL FILES
# =========================

model = joblib.load(
    "Models/fake_review_model.pkl"
)

vectorizer = joblib.load(
    "Models/tfidf_vectorizer.pkl"
)

scaler = joblib.load(
    "Models/scaler.pkl"
)


# =========================
# TEXT CLEANING
# =========================

def clean_text(text):
    text = str(text).lower()
    text = re.sub(
        r'[^\w\s]',
        '',
        text
    )
    text = re.sub(
        r'\s+',
        ' ',
        text
    )
    return text.strip()


# =========================
# REVIEW EXPLANATION
# =========================

def explain_review(review, is_genuine):
    reasons = []

    fake_words = [
        "amazing",
        "excellent",
        "best",
        "perfect",
        "must buy",
        "buy now",
        "cheap",
        "guaranteed",
        "life changing"
    ]

    short_review_words = len(
        review.split()
    )

    review_lower = review.lower()

    for word in fake_words:
        if word in review_lower:
            reasons.append(
                f"Contains promotional word: '{word}'"
            )

    if short_review_words < 5:
        reasons.append(
            "Review is very short and lacks product details"
        )

    if review.count("!") >= 2:
        reasons.append(
            "Contains excessive excitement symbols"
        )

    # Exclamation check
    excl_ratio = review.count('!') / (len(review) + 1)
    if excl_ratio > 0.05:
        reasons.append(
            f"High density of exclamation marks ({excl_ratio:.1%})"
        )

    # Caps check
    caps_ratio = sum(1 for w in review.split() if w.isupper() and len(w) > 1) / (len(review.split()) + 1)
    if caps_ratio > 0.1:
        reasons.append(
            f"High percentage of ALL-CAPS words ({caps_ratio:.1%})"
        )

    if len(reasons) == 0:
        if is_genuine:
            reasons.append(
                "Text pattern matches previously learned genuine review patterns"
            )
        else:
            reasons.append(
                "Text pattern matches previously learned fake review patterns"
            )

    return reasons


# =========================
# PREDICTION FUNCTION
# =========================

def predict_review(review):
    cleaned_review = clean_text(
        review
    )

    # 1. Transform text using TF-IDF
    vector_text = vectorizer.transform(
        [cleaned_review]
    )

    # 2. Extract single numerical metadata features
    word_count = len(review.split())
    excl_ratio = review.count('!') / (len(review) + 1)
    caps_ratio = sum(1 for w in review.split() if w.isupper() and len(w) > 1) / (len(review.split()) + 1)
    punct_ratio = sum(1 for c in review if c in '.,!?;:"') / (len(review) + 1)

    # 3. Scale numerical features
    num_features = np.array([[word_count, excl_ratio, caps_ratio, punct_ratio]])
    num_features_scaled = scaler.transform(num_features)

    # 4. Combine text and metadata vectors
    vector_combined = hstack([vector_text, num_features_scaled])

    # 5. Predict
    prediction = model.predict(
        vector_combined
    )

    confidence = model.predict_proba(
        vector_combined
    )

    confidence_score = max(
        confidence[0]
    ) * 100

    is_genuine = (prediction[0] == 1)
    explanation = explain_review(
        review,
        is_genuine
    )

    # 6. Hybrid Rule Override
    # Count how many spam indicator flags are triggered in the explanation
    spam_rules = [
        "Contains promotional",
        "Contains excessive excitement",
        "High density of exclamation",
        "High percentage of ALL-CAPS",
        "Review is very short"
    ]
    triggered_rules_count = sum(
        1 for reason in explanation if any(rule in reason for rule in spam_rules)
    )

    # If the model predicts Genuine, but triggers 2 or more spam rules, override to Fake Review
    if is_genuine and triggered_rules_count >= 2:
        is_genuine = False
        confidence_score = confidence_score * 0.8  # Adjust confidence to reflect rule override penalty
        explanation.append(
            "ML classified as human-written, but overridden due to high density of spam indicators."
        )

    if is_genuine:
        return (
            "Genuine Review",
            confidence_score,
            explanation
        )
    else:
        return (
            "Fake Review",
            confidence_score,
            explanation
        )