# =========================================
# AI WRITING SYSTEM - MAIN BACKEND
# =========================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import random
import base64
import tempfile
from pathlib import Path

from ai_engine.grammar_ai import grammar_engine
from ai_engine.ocr_engine import extract_text
from ai_engine.features_ai import (
    make_notes_ai,
    improve_assignment_ai,
    simplify_ai,
    expand_ai,
    paragraph_ai
)

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "db.sqlite3"
otp_store = {}

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS writing_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            corrected TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        ''')


def save_analysis(text, corrected, score):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO writing_analysis (text, corrected, score) VALUES (?, ?, ?)",
            (text, corrected, score),
        )


init_db()


@app.route('/api/health', methods=['GET'])
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


# =========================================
# OTP LOGIN
# =========================================
@app.route('/api/send-otp', methods=['POST'])
@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        if not email:
            return jsonify({"status": "fail"})
        otp = str(random.randint(1000, 9999))
        otp_store[email] = otp
        print(f"OTP for {email}: {otp}")
        return jsonify({"status": "sent"})
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status": "fail"})


@app.route('/api/verify-otp', methods=['POST'])
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json(silent=True) or {}
        email = data.get("email")
        otp = data.get("otp")
        if otp_store.get(email) == otp:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "fail"})
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status": "fail"})


# =========================================
# TEXT ANALYSIS (FULL AI)
# =========================================
@app.route('/api/analyze-text', methods=['POST'])
@app.route('/analyze-text', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json(silent=True) or {}
        text = data.get("text", "")

        if not text.strip():
            return jsonify({
                "highlighted": "", "corrected": "", "errors": [],
                "score": 0, "good_sentence": "", "better_sentence": "",
                "best_sentence": "", "suggestions": []
            })

        corrected, highlighted, errors, good, better, best, suggestions = grammar_engine(text)

        score = max(0, 100 - len(errors) * 5)
        save_analysis(text, corrected, score)

        return jsonify({
            "highlighted": highlighted,
            "corrected": corrected,
            "errors": errors,
            "score": score,
            "good_sentence": good,
            "better_sentence": better,
            "best_sentence": best,
            "suggestions": suggestions
        })

    except Exception as e:
        print("ERROR in analyze-text:", e)
        return jsonify({
            "highlighted": "", "corrected": "", "errors": [str(e)],
            "score": 0, "good_sentence": "", "better_sentence": "",
            "best_sentence": "", "suggestions": []
        })


# =========================================
# IMAGE ANALYSIS (OCR + FULL AI)
# =========================================
@app.route('/api/analyze-image', methods=['POST'])
@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file uploaded"})

        file = request.files['image']

        suffix = Path(file.filename or "upload.png").suffix[:10]
        with tempfile.NamedTemporaryFile(
            prefix="ai_writing_", suffix=suffix, delete=False
        ) as temp_file:
            filepath = temp_file.name
            file.save(temp_file)

        extracted = extract_text(filepath)

        # Clean up temp file
        try:
            os.remove(filepath)
        except:
            pass

        if not extracted or extracted.startswith("OCR Error") or extracted.startswith("No text"):
            return jsonify({
                "extracted": extracted or "No text found in image",
                "highlighted": "", "corrected": "", "errors": [],
                "good_sentence": "", "better_sentence": "",
                "best_sentence": "", "suggestions": ["Try uploading a clearer image with better lighting"]
            })

        corrected, highlighted, errors, good, better, best, suggestions = grammar_engine(extracted)
        score = max(0, 100 - len(errors) * 5)
        save_analysis(extracted, corrected, score)

        return jsonify({
            "extracted": extracted,
            "highlighted": highlighted,
            "corrected": corrected,
            "errors": errors,
            "good_sentence": good,
            "better_sentence": better,
            "best_sentence": best,
            "suggestions": suggestions,
            "score": score
        })

    except Exception as e:
        print("ERROR in analyze-image:", e)
        return jsonify({"error": f"Processing failed: {str(e)}"})


# =========================================
# LIVE CAMERA ANALYSIS (OCR + FULL AI)
# =========================================
@app.route('/api/analyze-live', methods=['POST'])
@app.route('/analyze-live', methods=['POST'])
def analyze_live():
    try:
        data = request.get_json(silent=True) or {}
        image_data = data.get("image")

        if not image_data:
            return jsonify({"error": "No image data"})

        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)

        with tempfile.NamedTemporaryFile(
            prefix="ai_writing_live_", suffix=".png", delete=False
        ) as temp_file:
            filepath = temp_file.name
            temp_file.write(image_bytes)

        extracted = extract_text(filepath)

        try:
            os.remove(filepath)
        except:
            pass

        if not extracted or extracted.startswith("OCR Error") or extracted.startswith("No text"):
            return jsonify({
                "extracted": extracted or "No text detected",
                "highlighted": "", "corrected": "", "errors": [],
                "good_sentence": "", "better_sentence": "",
                "best_sentence": "", "suggestions": ["Hold the text closer and ensure good lighting"]
            })

        corrected, highlighted, errors, good, better, best, suggestions = grammar_engine(extracted)
        score = max(0, 100 - len(errors) * 5)
        save_analysis(extracted, corrected, score)

        return jsonify({
            "extracted": extracted,
            "highlighted": highlighted,
            "corrected": corrected,
            "errors": errors,
            "good_sentence": good,
            "better_sentence": better,
            "best_sentence": best,
            "suggestions": suggestions,
            "score": score
        })

    except Exception as e:
        print("ERROR in analyze-live:", e)
        return jsonify({"error": f"Live processing failed: {str(e)}"})


# =========================================
# AI SMART TOOLS
# =========================================
@app.route('/api/make-notes', methods=['POST'])
@app.route('/make-notes', methods=['POST'])
def make_notes():
    try:
        text = (request.get_json(silent=True) or {}).get("text", "")
        return jsonify({"notes": make_notes_ai(text)})
    except Exception as e:
        return jsonify({"notes": f"Error: {str(e)}"})


@app.route('/api/improve-assignment', methods=['POST'])
@app.route('/improve-assignment', methods=['POST'])
def improve_assignment():
    try:
        text = (request.get_json(silent=True) or {}).get("text", "")
        return jsonify({"improved": improve_assignment_ai(text)})
    except Exception as e:
        return jsonify({"improved": f"Error: {str(e)}"})


@app.route('/api/simplify', methods=['POST'])
@app.route('/simplify', methods=['POST'])
def simplify():
    try:
        text = (request.get_json(silent=True) or {}).get("text", "")
        return jsonify({"result": simplify_ai(text)})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})


@app.route('/api/expand', methods=['POST'])
@app.route('/expand', methods=['POST'])
def expand():
    try:
        text = (request.get_json(silent=True) or {}).get("text", "")
        return jsonify({"result": expand_ai(text)})
    except Exception as e:
        return jsonify({"result": f"Error: {str(e)}"})


@app.route('/api/build-paragraph', methods=['POST'])
@app.route('/build-paragraph', methods=['POST'])
def build_paragraph():
    try:
        text = (request.get_json(silent=True) or {}).get("text", "")
        return jsonify({"paragraph": paragraph_ai(text)})
    except Exception as e:
        return jsonify({"paragraph": f"Error: {str(e)}"})


# =========================================
# DASHBOARD
# =========================================
@app.route('/api/get-dashboard-data', methods=['GET'])
@app.route('/get-dashboard-data', methods=['GET'])
def dashboard():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT text, score FROM writing_analysis ORDER BY id DESC LIMIT 10")
            rows = cursor.fetchall()
            cursor.execute("SELECT score FROM writing_analysis")
            scores = [row[0] for row in cursor.fetchall()]

        if not scores:
            return jsonify({"error": "No data"})

        avg = sum(scores) / len(scores)
        suggestions = []
        if avg < 50:
            suggestions.append("Focus on basic grammar and sentence formation.")
        elif avg < 70:
            suggestions.append("Improve sentence clarity and punctuation.")
        elif avg < 85:
            suggestions.append("Good writing. Work on vocabulary and style.")
        else:
            suggestions.append("Excellent writing! Enhance advanced tone and structure.")

        return jsonify({
            "avg_score": avg, "max_score": max(scores), "min_score": min(scores),
            "total": len(scores), "scores": scores,
            "recent": [{"text": r[0][:80], "score": r[1]} for r in rows],
            "suggestions": suggestions
        })
    except Exception as e:
        print("ERROR in dashboard:", e)
        return jsonify({"error": "Dashboard failed"})


# =========================================
# RUN SERVER
# =========================================
if __name__ == '__main__':
    init_db()
    print("====================================")
    print("  AI Writing System Started!")
    print("  Open: http://127.0.0.1:5000")
    print("====================================")
    app.run(debug=False, use_reloader=False)
