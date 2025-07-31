from flask import Flask, render_template, send_from_directory, request
import os
import files
import sys
import logs

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
    "Business": "fas fa-briefcase",
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
    list = files.read_json_recursively(f'../articles/{category}')
    articles = load_articles_from_json(list, category)
    path_title = request.path.strip('/').split('/')[-1].capitalize()
    return render_template('articles.html', articles=articles, title=path_title, category=category)

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

@app.route('/admin/restart')
def restart():
    logs.create_error_logs("Restating web site")
    os.execv(sys.executable, ['python'] + sys.argv)

@app.route('/logs')
def logs_page():
    log_type = request.args.get('log_type', 'info')  # Default to 'info'
    log_file_map = {
        'info': 'info.log',
        'warning': 'warning.log',
        'error': 'error.log'
    }

    log_file = log_file_map.get(log_type, 'info.log')   
    log_file_path = os.path.join('../logs', log_file)
    log_contents = []

    if os.path.exists(log_file_path):
        # Read the log file
        with open(log_file_path, 'r') as file:
            log_contents = file.readlines()  # Read the file into a list of lines

    return render_template('logs.html', logs=log_contents, log_type=log_type)

routes_list = create_routes_list()
create_dynamic_routes()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)