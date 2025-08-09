Video link https://www.youtube.com/watch?v=q0QLXp8o7Vc
README – Task 1: Court Data Fetcher & Mini-Dashboard

Court Chosen:
Faridabad District Court – eCourts portal (https://districts.ecourts.gov.in/faridabad)

Overview
--------
This Django web application allows a user to select a Case Type, Case Number, and Filing Year,
then fetches and displays case metadata and the most recent order/judgment details from the
Faridabad District Court public portal.

The app uses headless Selenium to automate navigation, bypass CAPTCHA using Tesseract OCR,
parse the results, and display them in a clean, user-friendly format.

Features Implemented
--------------------
1. UI Form:
   - Dropdown for Case Type.
   - Inputs for Case Number & Filing Year.

2. Backend Automation:
   - Selenium (headless Chrome) handles navigation.
   - Captcha is solved using Tesseract OCR (with image preprocessing for better accuracy).
   - Fetches:
     - Parties’ names
     - Filing date
     - Next hearing date
     - Latest order/judgment PDF link

3. Storage:
   - Each query and raw HTML response is logged in a SQLite database for debugging and auditing.

4. Display:
   - Parsed data shown on a results page.
   - PDF links are clickable and open in the browser.

5. Error Handling:
   - Invalid case number → user-friendly error message.
   - Court site downtime → clear notification to the user.

CAPTCHA Strategy
----------------
The Faridabad eCourts portal uses a simple image-based CAPTCHA.
- Screenshot of the CAPTCHA is taken via Selenium.
- Image is preprocessed (grayscale + threshold).
- Tesseract OCR is used to extract text.
- The extracted text is filled in automatically before form submission.

This approach is legal as it only automates publicly available data entry.

Setup Instructions
------------------

1. Prerequisites
   - Python 3.9+
   - Google Chrome
   - ChromeDriver (matching your Chrome version)
   - Tesseract OCR installed (`sudo apt install tesseract-ocr` on Linux or via brew on Mac)
   - Virtualenv (recommended)

2. Installation
   ```bash
   git clone <your_repo_url>
   cd <project_directory>
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Environment Variables
   Create a `.env` file in the project root:
   ```
   DEBUG=True
   SECRET_KEY=your_django_secret_key
   ```

4. Database Migration
   ```bash
   python manage.py migrate
   ```

5. Run the App
   ```bash
   python manage.py runserver
   ```
   Access at http://127.0.0.1:8000/

Sample Run
----------
1. Open the app in the browser.
2. Select Case Type, enter Case Number & Filing Year.
3. App solves CAPTCHA automatically, fetches data, and displays:
   - Parties’ names
   - Filing date
   - Next hearing date
   - Latest PDF link

Libraries Used
--------------
- Django
- Selenium
- Tesseract OCR (pytesseract)
- Pillow (image preprocessing)
- SQLite (default DB)

Notes
-----
- This app is tailored for the Faridabad District Court site structure.
- Minor adjustments may be needed if the HTML structure changes.
- Only public court data is fetched; no private data is accessed.
