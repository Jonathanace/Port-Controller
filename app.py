from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils import parse_manifest
from pprint import pprint
from balancing import get_steps as get_balancing_steps
from unloading_loading import get_steps as get_unloading_steps
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

global employee_name
employee_name = None

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

def get_manifest():
    return [open(entry.path, 'r').read() for entry in os.scandir('uploads/') if entry.is_file()][0]

def get_manifest_path():
    return next(os.scandir('uploads/')).path

def get_ship_name():
    manifest_path = get_manifest_path()
    ship_name = os.path.basename(manifest_path).replace(".txt", "")
    return ship_name

def make_grid(prev_grid=None, start_pos=None, end_pos=None, cargo_name=None, cargo_weight=None):
    if prev_grid is None: # If no previous grid, generate a new grid from the manifest
        # print('Generating Grid')
        grid = np.zeros((8, 12), dtype=np.int32)
        manifest = get_manifest()
        for item in parse_manifest(manifest):
            # print(f'{item['company']} at {item['location']}')
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
        display_text = 'Move {cargo_name} from the {start_type} to the {end_type}.\nCargo should weigh: {cargo_weight} lbs'
        # print('start and end detected')
        if start_pos == 'Dock':
            cargo_name = cargo_name
            start_type = 'Dock'
            pass
        else:
            cargo_name = "the cargo"
            start_type = 'Red Square'
            start_x, start_y = start_pos[0]-1, start_pos[1]-1
            grid[start_x, start_y] = 3 # (gray->red)

        if end_pos == 'Dock':
            end_type = 'Dock'
        else:
            end_type = 'Green Square'
            end_x, end_y = end_pos[0]-1, end_pos[1]-1
            grid[end_x, end_y] = 4 # (white->green)
        display_text = display_text.format(cargo_name=cargo_name, start_type=start_type, end_type=end_type, cargo_weight=cargo_weight)
    else: 
        display_text = "Initial grid"
        
    return grid, display_text

def display_grid(grid: np.ndarray):
    flipped_grid = np.flip(grid, axis=0)
    plt.imshow(flipped_grid, cmap=cmap, vmin=0, vmax=4)
    plt.show()
    return grid

def save_grid(grid, step_num, display_text):
    image_path = os.path.join(PLAN_FOLDER, f'{step_num}.png')
    flipped_grid = np.flip(grid, axis=0)
    plt.xticks(range(grid.shape[1]))
    plt.imshow(flipped_grid, cmap=cmap, vmin=0, vmax=4)
    plt.title(f'{get_ship_name()}\n{display_text}')
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
        ship_name = request.form.get('shipName')
        print(f'Ship name: {ship_name}')
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        remove_files = glob.glob(os.path.join(UPLOAD_FOLDER, '*'))
        for remove_file in remove_files:
            # app.logger.info(f'removing {remove_file}')
            os.remove(remove_file)

        remove_files = glob.glob(os.path.join(PLAN_FOLDER, '*'))
        for remove_file in remove_files:
            # app.logger.info(f'removing {remove_file}')
            os.remove(remove_file)
        app.logger.info('Uploading Manifest...')
        file.save(os.path.join(UPLOAD_FOLDER, ship_name))
        app.logger.info('Manifest Successfully Uploaded')
        return jsonify(), 200 

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
    
    manifest_path = get_manifest_path()
    
    if parse_option == 'Balance':
        app.logger.info('Balance function selected')
        steps = get_balancing_steps(manifest_path)
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
    manifest = get_manifest()
    parsed_manifest = parse_manifest(manifest)
    container_names = [{'id': i['company'], 'label': i['company']} for i in parsed_manifest if i['company'] not in ['UNUSED', 'NAN']]
    
    app.logger.info(f'container_names: {container_names}')
    return jsonify(container_names), 200

@app.route('/balance-manifest', methods=['POST'])
def balance_manifest():
    app.logger.info('balance_manifest called')
    manifest_path = get_manifest_path()
    steps = get_balancing_steps(manifest_path)
    grid, _ = make_grid()
    
    for step_num, step in enumerate(steps):
        grid, display_text = make_grid(prev_grid=grid, start_pos=step.start_pos, end_pos=step.end_pos, cargo_name=step.name, cargo_weight=step.weight)
        image_path = save_grid(grid, step_num, display_text)
        # display_grid(grid)

    return jsonify(), 200
    
@app.route('/log-comment', methods=['POST'])
def log_comment():
    global employee_name
    app.logger.info('log_comment called')
    try:
        data = request.get_json()
        app.logger.info('data received')
    except:
        pass
    comment = data['comment']
    if comment.endswith('signs in.'):
        if employee_name:
            print(f"Previous employee name found: {employee_name}")
            save_to_logfile(f"{employee_name} signs out.")
        else:
            employee_name = comment.rstrip(" signs in.")
            print('No previous employee name found.')
    save_to_logfile(comment)
    return jsonify(), 200

@app.route('/load-unload-manifest', methods=['POST'])
def load_unload_manifest():
    app.logger.info('Load Unload Request Called')
    data = request.get_json()
    unload_names = data.get("items")
    load_names_and_weights = [i.split("-") for i in data.get("namesAndWeights").split(",")]
    unload = [(i, 1) for i in unload_names]
    try:
        load = [(i[0], 1, int(i[1])) for i in load_names_and_weights if len(i)>1]
    except:
        # print(load_names_and_weights)
        pass
    print(f'load: {load}')
    print(f'unload: {unload}')
    steps = get_unloading_steps(file_path=get_manifest_path(),
                        file_name=get_ship_name(),
                        unload=unload,
                        load=load,
                        h=True)
    app.logger.info("Load/Unload steps processed")
    grid, _ = make_grid()
    
    for step_num, step in enumerate(steps):
        grid, display_text = make_grid(prev_grid=grid, start_pos=step.start_pos, end_pos=step.end_pos, cargo_name=step.name, cargo_weight=step.weight)
        image_path = save_grid(grid, step_num, display_text)



    return jsonify(), 200

if __name__ == '__main__':
    # balance_manifest()
    app.run(port=5000, debug=True)