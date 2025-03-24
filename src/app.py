from flask import Flask, render_template, send_from_directory, request
import files

# Create the Flask app
app = Flask(__name__, template_folder='../templates')

def create_routes_list():
    file_names  = files.list_directory('../articles')
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

routes_list = create_routes_list()
create_dynamic_routes()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)