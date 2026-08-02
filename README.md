# Product Trust & Fake Review Verification System

A prototype web application built in Python using Streamlit to detect computer-generated reviews and verify the authenticity of physical product QR codes.

---

## Features

### 1. Customer Portal
* **Review Verification**: Paste customer review text. A machine learning model checks word usage patterns, combined with keyword rules (exclamations, capital ratios) to flag suspicious or promotional reviews.
* **Product Authentication**: Uses a webcam to scan a product's printed QR label. It checks a local database to verify if it's genuine and warns if it has been scanned before (potential photocopy).

### 2. Admin Portal
* **Register Products**: Generates unique 8-character IDs and prints matching QR codes.
* **View Inventory**: Tracks all registered products, scan counts, and alert statuses.
* **Scan Audit Logs**: Live dashboard showing verification history and warnings.
* **QR Download Panel**: Allows retrieval and download of any product's QR code image.

---

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone <your-repository-url>
   cd "Fake Review Detection"
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**:
   Runs schema setup to create SQLite tables:
   ```bash
   python database.py
   ```

5. **Start Web Application**:
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

---

## File Structure
* `app.py`: Streamlit frontend dashboard layout.
* `database.py`: Database table setup and initializations.
* `Modules/`: Authentication, database methods, and verification logic.
* `Models/`: Pre-trained classifier and vectorizer files.
* `qr_codes/`: Target folder for generated QR labels.
