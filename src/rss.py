import feedparser
import requests
from bs4 import BeautifulSoup
import googlenewsdecoder as gnd
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

import ollama_sum

google_news_tech = 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'

def get_articles(rss_feed):
    articles = {}
    url = rss_feed
    feed = feedparser.parse(url)

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(convert_google_link, i.link): i.title for i in feed.entries}

        for future in as_completed(futures):
            title = futures[future]  
            try:
                decoded_url = future.result()  
                if decoded_url:
                    articles[title] = decoded_url
            except Exception as e:
                print(f"Error for article '{title}': {e}")

    return articles

def convert_google_link(url):
    try:
        decoded_url = gnd.new_decoderv1(url, interval=1)
        if decoded_url.get("status"):
            return [decoded_url["decoded_url"]]
        else:
            print("Error:", decoded_url["message"])
    except Exception as e:
        print(f'Error Occured: {e}')
    
    return

def download_articles(url):
    print(url)
    try:
        request = requests.get(url, timeout=30)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError as err:
        return None

    if request.status_code == 200:
        return request.text

def parse_article(content):
    soup  = BeautifulSoup(content, 'html.parser')
    return soup.get_text()

def parse_img(content):
    soup = BeautifulSoup(content, 'html.parser')
    image = soup.find('meta', property='og:image')
    if image == None:
        return  "https://i.kinja-img.com/image/upload/c_fill,h_675,pg_1,q_80,w_1200/0758f7e3d376d1a62f1578a1039361e5.jpg" # Placeholder image URL
    
    image = image['content']  # Return the content attribute as a string
    
    return image


if __name__ == "__main__":
    with open("articles.json", 'r') as file:
        articles = json.load(file)

    for i in range(len(articles)):

        link = list(articles.values())[i][0]
        titles = list(articles.keys())[i]

        content = download_articles(link)
        if content is None:
            continue

        image = parse_img(content)
        content = parse_article(content)

        articles.setdefault(titles, []).append(image)
        

        data = ollama_sum.summarize(content)
        
        articles.setdefault(titles, []).append(data)

    with open('json.json', 'w') as file:
        json.dump(articles, '../articles/' + file)