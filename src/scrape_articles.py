import feedparser
import requests
from bs4 import BeautifulSoup
import googlenewsdecoder as gnd
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime
import ollama_sum
import files

@dataclass
class Article:
    title: str = ""
    url: str = ""
    image_url: str = ""
    published_date: str = ""
    summary: str = ""
    file_name: str = ""

def get_articles(rss_feed, catagory, max_articles = 10):
    counter = 0
    url = rss_feed
    feed = feedparser.parse(url)
    title_list = list(map(lambda article: article['title'], files.read_json_recursivly(f'../articles/{catagory}')))

    with ThreadPoolExecutor() as executor:

        futures = {}

        for entry in feed.entries:
            print(counter)
            if counter >= max_articles:
                break

            if entry.title in title_list:
                continue

            future = executor.submit(convert_google_link, entry.link)
            futures[future] = entry
            counter += 1

        for future in as_completed(futures):
            try:
                entry = futures[future]  # Get the original entry
                decoded_url = future.result()
                
                content = download_articles(decoded_url)
                ### print(download_articles)
                data = parse_article(content)
                ### print(parse_article)
                image = parse_img(content)
                # print(parse_img)
                data = ollama_sum.summarize(data)
                ### print(ollama_sum.summarize)
                title = entry.title
                published_date = entry.published
                
                if title and decoded_url and image and data:
                    article = Article()
                    article.title = title
                    article.url = decoded_url
                    article.image_url = image
                    article.published_date = published_date
                    article.summary = data
                    article.file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

                    articles_dict = asdict(article)
                    # print(articles_dict)
                    files.save_json(articles_dict, f'../articles/{catagory}/' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f"))

            except Exception as e:
                print(f"Error for article '{entry.title}': {e}")
                continue

def convert_google_link(url):
    try:
        decoded_url = gnd.new_decoderv1(url, interval=5)
        if decoded_url.get("status"):
            return decoded_url["decoded_url"]
        else:
            print("Error:", decoded_url["message"])
    except Exception as e:
        print(f'Error Occured: {e}')
    
    return

def download_articles(url):
    try:
        request = requests.get(url, timeout=30)
    except requests.exceptions.Timeout:
        print(f'url: {err}')
        return ""
    except requests.exceptions.ConnectionError as err:
        print(f'url: {url}: {err}')
        return ""

    if request.status_code == 200:
        return request.text

def parse_article(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"Error parsing article content: {e}")
        return ""

def parse_img(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        image = soup.find('meta', property='og:image')
        image = image['content']  # Return the content attribute as a string
        
        return image

    except Exception as e:
        print(f'parse img err: {e}')
        return  "https://static.vecteezy.com/system/resources/previews/016/916/479/original/placeholder-icon-design-free-vector.jpg" # Placeholder image URL


if __name__ == "__main__":
    articles = get_articles("https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen", 'tech')