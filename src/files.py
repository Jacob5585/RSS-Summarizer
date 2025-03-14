import json
import os

def save_json(data, file_name):
    # with open('../articles/' + file_name + '.json', "w") as file:
    with open(file_name + '.json', 'w') as file:
        json.dump(data, file)

def read_json(file_name):
    # with open('../articles/' + file_name + '.json', 'r') as file:
    with open(file_name, 'r') as file:
        data = json.load(file)

    return data

def read_json_recursivly(root_folder):
    list = []
    # Walk through all the folders and subfolders
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:

            file_path = os.path.join(dirpath, filename)
            data = read_json(file_path)
            filename = filename.split('.', 1)[0] # Remove file extension
            data.update({'file_name': filename})
            list.append(data)
            
        return list

def read_names_recursivly(root_folder):
    list = []
    # Walk through all the folders and subfolders
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            filename = filename.split('.', 1)[0] # Remove file extension
            list.append(filename)
        
        return list

def check_audio(directory, file_name):
    # Walk through all the folders and subfolders
    for dirpath, dirnames, filenames in os.walk(directory):
        # Remove file extension
        filenames = [filename.split('.', 1)[0] for filename in filenames]

        if file_name in filenames:
            return True

    return False     

def delete_files(filepath):
    try:
        os.remove(f'{filepath}')
    except FileNotFoundError:
        print(f'File not found: {filepath}')
    except PermissionError:
        print(f'Permission Error: {filepath}')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # import scrape_articles
    
    # file_name = "tech.json"

    # articles_dict = scrape_articles.get_articles("https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen")
    
    # with open('../articles/' + file_name, "w") as file:
    #     json.dump(articles_dict, file)

    # root_folder = 'articles'  # Change this to the path of your folder
    # data = read_json_recursivly(root_folder)
    # print(data)
    pass