from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils import parse_manifest
from pprint import pprint
from balancing import get_steps
import json
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import glob

app = Flask(__name__)
CORS(app)

### Setup Manifest Upload Folder
UPLOAD_FOLDER = 'uploads'
manifest_path = os.path.join(UPLOAD_FOLDER, 'manifest.txt')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

### Setup Plan Folder
PLAN_FOLDER = 'plan'
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

def make_grid(prev_grid=None, start_pos=None, end_pos=None):
    if prev_grid is None: # If no previous grid, generate a new grid from the manifest
        print('Generating Grid')
        grid = np.zeros((8, 12), dtype=np.int32)
        with open('test_manifests/SilverQueen.txt') as file:
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
        print('start and end detected')
        start_x, start_y = start_pos[0]-1, start_pos[1]-1
        end_x, end_y = end_pos[0]-1, end_pos[1]-1
        grid[start_x, start_y] = 3 # (gray->red)
        grid[end_x, end_y] = 4 # (white->green)

    return grid

def display_grid(grid: np.ndarray):
    flipped_grid = np.flip(grid)
    plt.imshow(flipped_grid, cmap=cmap, vmin=0, vmax=4)
    plt.show()
    return grid

def save_grid(grid, step_num):
    image_path = os.path.join(PLAN_FOLDER, f'{step_num}.png')
    flipped_grid = np.flip(grid)
    plt.imshow(flipped_grid, cmap=cmap, vmin=0, vmax=4)
    plt.savefig(image_path)


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
    app.logger.info('Balance manifest called')
    with open(manifest_path) as file:
        manifest = file.read()
    steps = get_steps(manifest)
    grid = make_grid()
    
    for step_num, step in enumerate(steps):
        grid = make_grid(prev_grid=grid, start_pos=step.start_pos, end_pos=step.end_pos)
        save_grid(grid, step_num)
        display_grid(grid)

    return jsonify(), 200
    
if __name__ == '__main__':
    # balance_manifest()
    
    app.run(port=5000, debug=True)