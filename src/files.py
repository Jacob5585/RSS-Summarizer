import json
import os

def save_json(data, file_name):
    with open(file_name + '.json', 'w') as file:
        json.dump(data, file)

def read_json(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)

    return data

def read_json_recursivly(root_directory):
    list = []
    # Walk through all the directories and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:

            file_path = os.path.join(dirpath, filename)
            data = read_json(file_path)
            filename = filename.split('.', 1)[0] # Remove file extension
            data.update({'file_name': filename})
            list.append(data)
            
        return list

def read_names_recursivly(root_directory):
    list = []
    # Walk through all the directories and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            filename = filename.split('.', 1)[0] # Remove file extension
            list.append(filename)
        
        return list

def check_audio(directory, file_name):
    # Walk through all the directories and subdirectories
    for dirpath, dirnames, filenames in os.walk(directory):
        # Remove file extension
        filenames = [filename.split('.', 1)[0] for filename in filenames]

        if file_name in filenames:
            return True

    return False     

def list_directory(directory_path):
    directories = [directory for directory in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, directory))]

    if not directories:
        return False
    else:
        return directories

def delete_files(filepath):
    try:
        os.remove(f'{filepath}')
    except FileNotFoundError:
        print(f'File not found: {filepath}')
    except PermissionError:
        print(f'Permission Error: {filepath}')
    except Exception as e:
        print(f"An error occurred: {e}")