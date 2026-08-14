# Windows Setup

## 1. Install prerequisites

Install the following software:

- Python 3.10 or later
- Java, required by LanguageTool
- Tesseract OCR from the maintained [UB Mannheim Windows distribution](https://github.com/UB-Mannheim/tesseract/wiki)

Install Tesseract in its default location:

```text
C:\Program Files\Tesseract-OCR\
```

## 2. Create a Python environment

Open Command Prompt in the `backend` directory:

```bat
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install dependencies

```bat
pip install -r requirements.txt
```

## 4. Start the backend

```bat
python run_server.py
```

The API will be available at `http://127.0.0.1:5000`. The first launch may download the local FLAN-T5 and LanguageTool resources.

## 5. Start the frontend

Open a second Command Prompt in the `frontend` directory:

```bat
python -m http.server 5500
```

Open `http://127.0.0.1:5500/` in a browser.

For the demo login, enter an email address and copy the generated OTP from the backend terminal. The application does not send email and does not require a Gemini or other hosted API key.

## Troubleshooting

- If Python reports a missing module, reactivate `.venv` and run `pip install -r requirements.txt` again.
- If OCR is unavailable, confirm that Tesseract is installed at the default path.
- If the frontend cannot reach the backend, confirm that port 5000 is available or update `frontend/config.js`.
