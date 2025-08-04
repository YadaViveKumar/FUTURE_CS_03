from flask import Flask, render_template, request, send_file
import os
from werkzeug.utils import secure_filename
from io import BytesIO
from utils import encrypt_file, decrypt_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    password = request.form.get('password')

    if not file or not password:
        return "File and password required."

    data = file.read()
    encrypted = encrypt_file(data, password)
    filename = secure_filename(file.filename) + '.enc'

    with open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as f:
        f.write(encrypted)

    return f"File uploaded and encrypted as <b>{filename}</b>"

@app.route('/download', methods=['POST'])
def download_file():
    filename = request.form.get('filename')
    password = request.form.get('password')

    if not filename or not password:
        return "Filename and password required."

    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return "File not found."

    with open(path, 'rb') as f:
        enc_data = f.read()

    try:
        decrypted = decrypt_file(enc_data, password)
    except Exception as e:
        return f"Decryption failed: {str(e)}"

    original_name = filename.replace('.enc', '')
    return send_file(BytesIO(decrypted), download_name=original_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
