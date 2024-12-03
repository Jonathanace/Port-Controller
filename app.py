from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils import parse_manifest
from pprint import pprint

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
manifest_path = os.path.join(UPLOAD_FOLDER, 'manifest.txt')

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

        file.save(manifest_path)
        
        return '', 200 # FIXME: return ship's name here

@app.route('/process-manifest', methods=['POST'])
def process_manifest():
    data = request.get_json()
    if not data['parse_option']: 
        return jsonify({'error': 'No parsing option passed'}), 400
    
    with open(manifest_path) as file:
        pprint(parse_manifest(file))
    
    if data['parse_option'] == 'balance':
        pass
    elif data['parse_option'] == 'load/unload':
        pass # FIXME
    else:
        return jsonify({'error': 'Invalid parsing option passed'}), 400




if __name__ == '__main__':
    app.run(port=5000)
