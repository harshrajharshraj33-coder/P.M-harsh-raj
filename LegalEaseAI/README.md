# LegalEase

AI-Powered Legal Document Generator

LegalEase is a FastAPI + Streamlit application for creating
editable legal-document drafts using Google's Gemini API.

The application supports:

- Employment contracts
- NDAs
- Lease agreements
- Freelance contracts
- Agreements
- Other custom legal-document types

## Architecture

Frontend:

Streamlit

Backend:

FastAPI

AI:

Google Gemini

Document generation:

python-docx

PDF generation:

fpdf2

Text:

TXT

## Project Structure

LegalEase/

├── assets/

├── backend/

│   ├── ai_core/

│   └── document_generators/

├── frontend/

├── tests/

├── .env

├── requirements.txt

└── README.md


## Installation

Create a virtual environment.

Windows:

python -m venv .venv

Activate:

.venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


## Environment

Create .env.

Example:

GEMINI_API_KEY=your_api_key

GEMINI_MODEL=gemini-3.8-flash

DEMO_MODE=false

BACKEND_URL=http://127.0.0.1:8000


## Run Backend

uvicorn backend.main:app --reload --port 8000


Backend:

http://127.0.0.1:8000


Swagger:

http://127.0.0.1:8000/docs


## Run Frontend

Open another terminal.

streamlit run frontend/app.py


Frontend:

http://localhost:8501


## Demo Mode

If you don't have a Gemini API key:

DEMO_MODE=true

Then run the application normally.

Demo mode generates deterministic example documents.


## Test

Run:

pytest -q


## Workflow

1. Enter document type.
2. Enter parties.
3. Enter terms.
4. Select effective date.
5. Click Generate Document.
6. Review the document.
7. Click Edit if required.
8. Download TXT.
9. Download DOCX.
10. Download PDF.


## API

POST /generate


Example JSON:

{
    "document_type": "NDA",
    "parties": "Alice, Beta Ltd",
    "terms": "Confidentiality for 2 years; No disclosure",
    "effective_date": "2026-10-01"
}


## Legal Notice

LegalEase generates document drafts.

It does not replace a qualified lawyer.

Users should review important legal documents
and jurisdiction-specific requirements before signing.