import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from flask_cors import CORS

from tensorflow.keras.preprocessing.sequence import pad_sequences


from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import pickle

# Point to the model folder
import tensorflow as tf
import pickle

# Correct folder name: 'model'
model = tf.keras.models.load_model('model/lstm_model.keras')

with open('model/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)





import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
from newspaper import Article


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'


model = tf.keras.models.load_model('model/lstm_model.keras')

with open('model/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'


def preprocess_image(img):
    img = img.convert('L')
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageEnhance.Contrast(img).enhance(2.0)
    return img


def clean_extracted_text(text):
    lines = text.splitlines()
    cleaned_lines = []
    keywords_to_ignore = [
        "Most Popular", "Also Read", "Waqf", "Opposition", "appointment",
        "film industry", "teachers", "recruitment", "Bill", "Modi", "Colombo"
    ]
    for line in lines:
        if not line.strip():
            continue
        if any(keyword.lower() in line.lower() for keyword in keywords_to_ignore):
            continue
        cleaned_lines.append(line)
    return ' '.join(cleaned_lines)


@app.route('/')
def home():
    # Pass a default value for confidence
    return render_template('index.html', confidence=0)



@app.route('/predict', methods=['POST'])
def predict():
    article = request.form.get('article', '').strip()
    url = request.form.get('url', '').strip()
    file = request.files.get('image')

    if file and file.filename != '':
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1].lower()

        if ext in ['.png', '.jpg', '.jpeg']:
            img = Image.open(file)
            img = preprocess_image(img)
            extracted_text = pytesseract.image_to_string(img, lang='eng')
            article = clean_extracted_text(extracted_text).strip()
        elif ext == '.pdf':
            return render_template('index.html', prediction="PDF support not added yet", confidence=0)
    elif url:
        try:
            news_article = Article(url)
            news_article.download()
            news_article.parse()
            article = news_article.text.strip()
        except Exception as e:
            return render_template('index.html', prediction=f"URL Error: {e}", confidence=0)

    if not article:
        return render_template('index.html', prediction="No text provided", confidence=0)

    seq = tokenizer.texts_to_sequences([article])
    padded = pad_sequences(seq, maxlen=500)
    probability = model.predict(padded)[0][0]
    confidence_percent = round(probability * 100, 2)

    if probability > 0.6:
        label = "Real News ✅"
    elif probability > 0.55:
        label = "Possibly Real ⚠️"
    elif probability > 0.4:
        label = "Possibly Fake ⚠️"
    else:
        label = "Fake News ❌"

    return render_template('index.html', prediction=label, confidence=confidence_percent, article=article)


@app.route('/predict_json', methods=['POST'])
def predict_json():
    print("Request method:", request.method)
    print("Content-Type:", request.content_type)
    print("Raw data:", request.data)

    data = request.get_json()
    article = data.get('text', '').strip() if data else ''

    if not article:
        return jsonify({'error': 'No text provided'}), 400

    seq = tokenizer.texts_to_sequences([article])
    padded = pad_sequences(seq, maxlen=500)
    probability = model.predict(padded)[0][0]

    confidence_percent = float(round(probability * 100, 2))  # <-- FIXED HERE

    if probability > 0.6:
        label = "Real News ✅"
    elif probability > 0.55:
        label = "Possibly Real ⚠️"
    elif probability > 0.4:
        label = "Possibly Fake ⚠️"
    else:
        label = "Fake News ❌"

    return jsonify({
        'prediction': label,
        'confidence': confidence_percent
    })




if __name__ == '__main__':
    app.run(debug=True)
