from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils import parse_manifest
from pprint import pprint
from balancing import get_steps

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
        app.logger.info('Manifest Saved')
        return jsonify(), 200 # FIXME: return ship's name here

@app.route('/process-manifest', methods=['POST'])
def process_manifest():
    app.logger.info('Process Manifest called')
    data = request.get_json()
    if data:
        app.logger.info('Data received')
    else:
        app.logger.warning('Data not recieved')

    parse_option = data.get('parse_option')
    if not parse_option: 
        app.logger.warning('No parsing option passed!')
        return jsonify({'error': 'No parsing option passed'}), 400
    
    with open(manifest_path) as file:
        manifest = file.read()
        # app.logger.info('Parsing Manifest')
        # parsed_manifest = parse_manifest(file.read())
        # app.logger.info('Manifest Parsed')
    
    
    if parse_option == 'Balance':
        app.logger.info('Balance function selected')
        steps = get_steps(manifest)
        app.logger.info('Steps calculated for balancing operation')
        for step in steps:
            app.logger.info(step)
    elif parse_option == 'Load/Unload':
        pass # FIXME
    else:
        warning = f'Invalid parsing option passed: {parse_option}'
        app.logger.warning(warning)
        return jsonify({'error': warning}), 400
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)
