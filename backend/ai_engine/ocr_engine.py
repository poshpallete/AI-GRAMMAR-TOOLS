# =========================================
# OCR ENGINE - Tesseract + Fallback
# =========================================

import os
import sys

try:
    import pytesseract
    from PIL import Image

    if sys.platform == "win32":
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    elif sys.platform == "darwin":
        pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
    else:
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


def extract_text(image_path):
    try:
        if not os.path.exists(image_path):
            return "Image file not found."

        if not TESSERACT_AVAILABLE:
            return "OCR libraries not installed. Run: pip install pytesseract Pillow"

        image = Image.open(image_path)
        image = image.convert("L")
        text = pytesseract.image_to_string(image)
        cleaned = text.strip()

        if not cleaned:
            return "No text detected in the image. Try a clearer image with better contrast."

        return cleaned

    except Exception as e:
        print("OCR ERROR:", e)
        return f"OCR Error: {str(e)}"
