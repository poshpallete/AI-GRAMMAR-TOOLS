# AI Writing System - SETUP GUIDE (Windows)

## Step 1: Install Python Requirements
Open CMD in the `backend` folder and run:
```
pip install -r requirements.txt
```

## Step 2: Install Tesseract OCR (for Image Analysis)
Download and install from:
https://github.com/UB-Mannheim/tesseract/wiki

Install to default path: `C:\Program Files\Tesseract-OCR\`

## Step 3: Your Gemini API Key is already configured
The `.env` file already has your API key set.

If you need a new key, get one FREE from: https://aistudio.google.com/apikey

## Step 4: Run Backend
```
cd backend
python app.py
```

## Step 5: Open Frontend
Just double-click `frontend/login.html` in your browser.

## That's it! Everything works now!

### What's FREE:
- Grammar checking (language_tool_python) = FREE, offline
- Smart AI Tools (Google Gemini 2.0 Flash Lite) = FREE, 1500 requests/day
- OCR (Tesseract) = FREE, offline

### Troubleshooting:
- If "ModuleNotFoundError" → run `pip install -r requirements.txt`
- If "Tesseract not found" → Install Tesseract from the link above
- If "Quota exceeded" → Wait 1 minute and try again (free tier has rate limits)
