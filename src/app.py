import subprocess
# import sys
from flask import Flask, render_template, send_from_directory, request
import json # Remove after switch to SQLite
import os
import files

# Create the Flask app
app = Flask(__name__, template_folder='../templates')

def create_routes_list():
    file_names  = os.listdir('../articles')
    return [{'name': file_name.split('.')[0].capitalize(), 'url': f'/{file_name.split(".")[0].lower()}'} for file_name in file_names]

ROUTE_ICONS = {
    "Tech": "fas fa-laptop-code",
    "Politics": "fas fa-landmark",
    "Finance": "fas fa-dollar-sign",
    "Science": "fas fa-atom",
    "Bussiness": "fas fa-briefcase",
    "World_news": "fas fa-landmark",
    "US_news": "fas fa-landmark"   
}

def load_articles_from_json(data, category):
    articles = []

    for idx, article in enumerate(data):

        # Only get the article if the audio exists for it
        if not files.check_audio(f'../audio/{category}/', article['file_name']):
            continue

        title = sanitize_text(article["title"])
        summary = sanitize_text(article["summary"])

        article = {
            'id': idx,
            'title': title,
            'link': article["url"],
            'summary': summary,
            'image_url': article['image_url'],
            'audio_file': article['file_name'] + '.mp3',
            'published': article["published_date"]
        }
        articles.append(article)
    
    return articles

def sanitize_text(text):
    text = text.replace('\n', ' ')
    text = text.replace("'", "\\'")
    return text

def create_route(category):
    list = files.read_json_recursivly(f'../articles/{category}')
    articles = load_articles_from_json(list, category)
    path_title = request.path.strip('/').split('/')[-1].capitalize()
    return render_template('index.html', articles=articles, title=path_title, category=category)

def create_dynamic_routes():
    for route in routes_list:
        app.add_url_rule(route['url'], route['name'], lambda route=route['name'].lower(): create_route(route))

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('../audio', filename)

@app.route('/')
def main_menu():
    return render_template('main_menu.html', routes=routes_list, icons=ROUTE_ICONS)

@app.route('/admin')
def admin_page():
    return render_template('admin_page.html')

# @app.route('/admin/restart', methods=['POST'])
# def restart():
#     # Kill the existing process running 'flask_feed.py' using pkill (safer alternative)
#     subprocess.run("pkill -f 'flask_feed.py'", shell=True, stderr=subprocess.DEVNULL)

#     # Optionally, log to confirm the kill action
#     print("Existing process killed.")

#     # Change the working directory to where the script is located (if needed)
#     os.chdir('/home/jcormier/python/rss')

#     # Ensure that the Python interpreter is in the correct environment
#     # Restart the Flask app using the virtual environment's Python interpreter
#     try:
#         os.execv('/home/jcormier/python/rss/.env/bin/python', ['/home/jcormier/python/rss/.env/bin/python', 'flask_feed.py'])
#     except Exception as e:
#         # Log the error if execv fails
#         print(f"Error restarting the server: {e}")
#         return f"Error: {e}", 500

#     return '', 204  # No content response after restarting (you can also return a custom message)
    
routes_list = create_routes_list()
create_dynamic_routes()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)