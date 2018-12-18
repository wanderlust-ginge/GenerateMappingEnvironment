import sys
import os
import yaml

def load_local_paths(file_name = ""):
    # If we have a loadstate.
    path_to_doctorm = ""
    path_to_app = ""
    path_to_mappers = ""
    if os.path.exists("./.automapper_local"):
        if os.path.isfile('./.automapper_local/local_saved_paths.yaml'):
            print("Previously_assigned_paths_exists!")
            persistent_data = load_yaml_from_file('./.automapper_local/local_saved_paths.yaml')
            path_to_doctorm = persistent_data['path_to_doctorm']
            path_to_app = persistent_data['path_to_app'].get(file_name, "")
            path_to_mappers = persistent_data['path_to_mappers'].get(file_name, "")
    return path_to_doctorm, path_to_app, path_to_mappers


def save_local_paths(path_to_doctorm, path_to_app, path_to_mappers, file_name = ""):
    if not os.path.exists("./.automapper_local"):
        os.makedirs("./.automapper_local")

    # If we have a savestate already
    if os.path.isfile('./.automapper_local/local_saved_paths.yaml'):
        persistent_data = load_yaml_from_file('./.automapper_local/local_saved_paths.yaml')
        if not path_to_doctorm == '':
            persistent_data['path_to_doctorm'] = sanitize_path(path_to_doctorm)
        if not path_to_app == '':
            persistent_data['path_to_app'][file_name] = sanitize_path(path_to_app)
        if not path_to_mappers == '':
            persistent_data['path_to_mappers'][file_name] = sanitize_path(path_to_mappers)
        with open('./.automapper_local/local_saved_paths.yaml', 'w') as outfile:
            yaml.dump(persistent_data, outfile, default_flow_style=False)
        return

    # Else we do not have a savestate. Create a new one.
    else:
        persistent_data = dict(
            path_to_doctorm=sanitize_path(path_to_doctorm),
            path_to_app=dict(),
            path_to_mappers=dict()
        )
        persistent_data['path_to_app'][file_name] = sanitize_path(path_to_app)
        persistent_data['path_to_mappers'][file_name] = sanitize_path(path_to_mappers)
        with open('./.automapper_local/local_saved_paths.yaml', 'w') as outfile:
            yaml.dump(persistent_data, outfile, default_flow_style=False)

def load_yaml_from_file(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

def ensure_path(original, new):
    if new == '':
        return original
    return new

def sanitize_path(path):
    path = path.replace('//', '/')
    path = path.replace('\\', '/')
    return path