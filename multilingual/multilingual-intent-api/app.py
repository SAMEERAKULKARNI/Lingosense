import os
os.environ["USE_TF"] = "0"  # Force disable TensorFlow

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from langdetect import detect
from googletrans import Translator
from transformers import pipeline
from docx import Document
import fitz  # PyMuPDF for PDF reading

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# Load classifier model (only PyTorch)
classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion", framework="pt")
translator = Translator()

# --- Helpers ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(filepath):
    if filepath.endswith(".pdf"):
        text = ""
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif filepath.endswith(".docx"):
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def translate_to_english(text, src_lang):
    try:
        translated = translator.translate(text, src=src_lang, dest='en')
        return translated.text
    except:
        return text

# --- Text API ---
@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input.strip():
        return jsonify({"error": "Message is empty"}), 400

    lang = detect_language(user_input)
    translated_text = translate_to_english(user_input, lang) if lang != "en" else user_input
    intent_result = classifier(translated_text)[0]
    intent = intent_result['label']

    return jsonify({
        "language": lang,
        "translated": translated_text,
        "intent": intent
    })

# --- File Upload API ---
@app.route('/analyze-file', methods=['POST'])
def analyze_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        extracted_text = extract_text_from_file(file_path)
        if not extracted_text.strip():
            return jsonify({"error": "No text found in file"}), 400

        lang = detect_language(extracted_text)
        translated_text = translate_to_english(extracted_text, lang) if lang != "en" else extracted_text
        intent_result = classifier(translated_text[:512])[0]  # Limit long text
        intent = intent_result['label']

        return jsonify({
            "language": lang,
            "translated": translated_text[:500],  # Keep it short
            "intent": intent
        })

    return jsonify({"error": "Invalid file format"}), 400

# --- Start Server ---
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
