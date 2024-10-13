from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import nltk
from nltk.corpus import words
import random

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Download required NLTK data
nltk.download('words', quiet=True)

def generate_caption():
    word_list = words.words()
    caption = ' '.join(random.choice(word_list) for _ in range(10))
    return caption.capitalize() + '.'

def generate_hashtags():
    word_list = words.words()
    hashtags = ['#' + random.choice(word_list) for _ in range(5)]
    return ' '.join(hashtags)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('home'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home'))
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        caption = generate_caption()
        hashtags = generate_hashtags()
        return render_template('result.html', filename=filename, caption=caption, hashtags=hashtags)

if __name__ == '__main__':
    app.run(debug=True)