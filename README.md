# AI Grammar Assistant

AI Grammar Assistant is a full-stack writing-support application for grammar correction, writing improvement, OCR-based text extraction, and progress tracking. It runs locally and does not require a hosted AI API key.

## Features

- Grammar and spelling analysis with highlighted corrections
- Writing scores and sentence-improvement suggestions
- Image-to-text extraction with Tesseract OCR
- Live-camera capture for printed or handwritten text
- Offline FLAN-T5 tools for notes, simplification, expansion, assignment improvement, and paragraph generation
- SQLite-backed analysis history and performance dashboard
- Demo OTP login flow for local use

## Tech Stack

- **Backend:** Python, Flask, Flask-CORS
- **Language processing:** LanguageTool, FLAN-T5, Hugging Face Transformers
- **OCR:** Tesseract, PyTesseract, Pillow
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript, Chart.js

## Project Structure

```text
AI-GRAMMAR-TOOLS/
|-- backend/
|   |-- ai_engine/        Grammar, local text-generation, and OCR engines
|   |-- database/         Runtime SQLite database location
|   |-- app.py            Flask application and API routes
|   |-- requirements.txt  Python dependencies
|   `-- run_server.py     Local server entry point
|-- frontend/             Multi-page browser interface
|-- tests/                Lightweight application tests
`-- SETUP_WINDOWS.md      Windows-specific installation guide
```

## Local Setup

### 1. Prerequisites

- Python 3.10 or later
- Java, required by `language-tool-python`
- Tesseract OCR, required for image and camera analysis

### 2. Install and run the backend

```bash
cd backend
python -m venv .venv
```

Activate the environment on Windows:

```bat
.venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Then install the dependencies and start the server:

```bash
pip install -r requirements.txt
python run_server.py
```

The API runs at `http://127.0.0.1:5000`. The first launch can take longer because the local language models may need to be downloaded.

### 3. Start the frontend

From a second terminal:

```bash
cd frontend
python -m http.server 5500
```

Open `http://127.0.0.1:5500/` in a browser. For the demo login, enter an email address and read the generated OTP from the backend terminal.

To use a different backend URL, edit `frontend/config.js`.

## Core API Routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Confirm that the API is running |
| POST | `/analyze-text` | Analyze, score, correct, and save typed text |
| POST | `/analyze-image` | Extract and analyze text from an image |
| POST | `/analyze-live` | Analyze a captured camera frame |
| POST | `/make-notes` | Convert supplied text into study notes |
| POST | `/improve-assignment` | Improve grammar and vocabulary |
| POST | `/simplify` | Simplify supplied text |
| POST | `/expand` | Expand supplied text |
| POST | `/build-paragraph` | Generate a paragraph from a topic |
| GET | `/get-dashboard-data` | Return stored writing analytics |

## Security and Data Notes

- No hosted API key is required or included.
- `.env` files, credentials, runtime databases, caches, and generated reports are excluded from version control.
- The OTP flow is a local demonstration: codes are printed to the backend terminal and are not emailed. Replace it with a production authentication provider before deployment.
- Writing analyses are stored only in the local SQLite database created at runtime.

## Project Attribution

Initial development used AI-assisted scaffolding. The application was subsequently audited, customized, tested, and documented jointly by:

- [Sampreeti Mukherjee](https://github.com/poshpallete)
- [Tuhit Roy](https://github.com/tuhitroy02)

## Status

The application is suitable for local demonstration and continued development. Production deployment would require secure authentication, persistent hosted storage, rate limiting, and deployment-specific configuration.
