from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils import parse_manifest
from pprint import pprint
from balancing import get_steps
import json
import logging
import numpy as np
from saving_to_log_file import save_to_logfile
import glob

app = Flask(__name__)
CORS(app)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

### Setup Manifest Upload Folder
UPLOAD_FOLDER = 'uploads'
manifest_path = os.path.join(UPLOAD_FOLDER, 'manifest.txt')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

### Setup Plan Folder
PLAN_FOLDER = 'frontend/public/images'
if not os.path.exists(PLAN_FOLDER):
    os.makedirs(PLAN_FOLDER)
else:
    files = glob.glob(os.path.join(PLAN_FOLDER, '*'))
    for file in files:
        os.remove(file)

### Create colormap for plan display
# 0: white, 1: black, 2: gray, 3: red, 4: green
colors = ['white', 'black', 'gray', 'red', 'green']  
cmap = ListedColormap(colors)

def make_grid(prev_grid=None, start_pos=None, end_pos=None, name=None):
    if prev_grid is None: # If no previous grid, generate a new grid from the manifest
        print('Generating Grid')
        grid = np.zeros((8, 12), dtype=np.int32)
        with open(manifest_path) as file:
            manifest = file.read()
        for item in parse_manifest(manifest):
            # print(item)
            x, y = item['location'][0]-1, item['location'][1]-1
            if item['company'] == 'UNUSED':
                grid[x,y] = 0
            elif item['company'] == 'NAN':
                grid[x,y]=1
            else:
                grid[x,y]=2
    else: # If previous grid exists, update container location from previous move
        grid = prev_grid
        grid[grid == 3] = 0 # Remove container from old location (red->white)
        grid[grid == 4] = 2 # Add container to new location (green->gray)


    # Visualize start and end position if necessary
    
    if start_pos and end_pos:
        display_text = 'Move the cargo from the {start_type} to the {end_type}'
        print('start and end detected')
        if start_pos == 'Dock':
            start_type = 'Dock'
            pass
        else:
            start_type = 'Red Square'
            start_x, start_y = start_pos[0]-1, start_pos[1]-1
            grid[start_x, start_y] = 3 # (gray->red)

        if end_pos == 'Dock':
            end_type = 'Dock'
        else:
            end_type = 'Green Square'
            end_x, end_y = end_pos[0]-1, end_pos[1]-1
            grid[end_x, end_y] = 4 # (white->green)
        display_text = display_text.format(start_type=start_type, end_type=end_type)
    else: 
        display_text = "Initial grid"
        
    return grid, display_text

def display_grid(grid: np.ndarray):
    flipped_grid = np.flip(grid)
    plt.imshow(flipped_grid, cmap=cmap, vmin=0, vmax=4)
    plt.show()
    return grid

def save_grid(grid, step_num, display_text):
    image_path = os.path.join(PLAN_FOLDER, f'{step_num}.png')
    flipped_grid = np.flip(grid)
    plt.imshow(flipped_grid, cmap=cmap, vmin=0, vmax=4)
    plt.title(display_text)
    try:
        os.remove(image_path)
    except:
        pass
    plt.savefig(image_path)
    return image_path


@app.route('/upload', methods=['POST'])
def upload_file(file_path=None):
    if file_path is not None:
        file = file_path.read()
    else:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
    if file:
        try:
            os.remove(manifest_path)
            
        except:
            pass

        files = glob.glob(os.path.join(PLAN_FOLDER, '*'))
        for remove_file in files:
            app.logger.info(f'removing {remove_file}')
            os.remove(remove_file)
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
    
@app.route('/get-containers', methods=['GET'])
def get_containers():
    with open(manifest_path) as manifest:
        parsed_manifest = parse_manifest(manifest.read())
    container_names = [{'id': i['company'], 'label': i['company']} for i in parsed_manifest if i['company'] not in ['UNUSED', 'NAN']]
    
    app.logger.info(container_names)
    return jsonify(container_names), 200

@app.route('/balance-manifest', methods=['POST'])
def balance_manifest():
    app.logger.info('balance_manifest called')
    with open(manifest_path) as file:
        manifest = file.read()
    steps = get_steps(manifest)
    for step in steps:
        print(step)
    grid, _ = make_grid()
    
    for step_num, step in enumerate(steps):
        grid, display_text = make_grid(prev_grid=grid, start_pos=step.start_pos, end_pos=step.end_pos, name='placeholder_name')
        image_path = save_grid(grid, step_num, display_text)
        # display_grid(grid)

    return jsonify(), 200
    
@app.route('/log-comment', methods=['POST'])
def log_comment():
    app.logger.info('log_comment called')
    try:
        data = request.get_json()
        app.logger.info('data received')
    except:
        pass
    comment = data['comment']
    app.logger.info(f'saving to logfile: {comment}')
    save_to_logfile(comment)
    return jsonify(), 200


if __name__ == '__main__':
    # balance_manifest()
    app.run(port=5000, debug=True)