from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils import parse_manifest

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:

        file_path = os.path.join(UPLOAD_FOLDER, 'manifest.txt')
        file.save(file_path)
        # Pass the file path to the process_file function
        
        return '', 200

# @app.route('/process-manifest', methods=['POST'])
# def process_manifest():




if __name__ == '__main__':
    app.run(port=5000)
