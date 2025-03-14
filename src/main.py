import multiprocessing
import files

rss_feed = {
    "tech": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen",
    "finance": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen",
    "science": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen",
    "world_news": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen"
    }

def artciles():
    from scrape_articles import get_articles
    while True:
        for feed, rss in rss_feed.items():
            print(f'----------{feed}: {rss}----------')
            get_articles(rss, feed)
            print(f'\nGet articles for {feed} complete\n')
            # files.py.save_json('../articles/' + data + '.json', feed)

def audio():
    from text2speech import convert_to_audio
    while True:
        for feed, _ in rss_feed.items():
            try:
                data = files.py.read_json_recursivly('../articles/' + feed)
                audio_list = files.py.read_names_recursivly('../audio/' + feed)
            except ValueError as e:
                print(e)
                continue

            # Remove articles that have already been converted to audio
            for i in data.copy():
                if i['file_name'] in audio_list:
                    data.remove(i)

            if not len(data):
                continue
            
            print(f'Creating Audio for: {feed}:')
            # Limit the number of articles to convert to audio at a time to avoid crashing due to exceeding memory
            for i in range(0, len(data), 5):
                chunk = data[i:i + 5]
                convert_to_audio(chunk, feed)
            
            print(f'\nText2Spech for {feed} complete\n')

def delete():
    # Add in fuctionality to find to keep track of when the oldest article will be able to be deleted and sleep for that long

    from datetime import datetime, timedelta
    while True:
        for feed, _ in rss_feed.items():
            articles = files.py.read_names_recursivly('../articles/' + feed)
            articles += (files.py.read_names_recursivly('../audio/' + feed)) # Incase there are audio files that aren't in the articles
            articles = list(dict.fromkeys(articles)) # Removes any duplicates

            for article in articles:
                try:
                    time_stamp  = datetime.strptime(article, "%Y-%m-%d_%H-%M-%S-%f")
                    current_time = datetime.now()
                    time_difference = abs(current_time - time_stamp)

                    if time_difference > timedelta(days=1):
                        print(f'deleting: {article} from articles/{feed} and audio/{feed}')
                        files.py.delete_files(f'../articles/{feed}/{article}.json')
                        files.py.delete_files(f'../audio/{feed}/{article}.mp3')

                except ValueError as e:
                    print(f'ValueError: {e}')
                    continue
                

def main():
    process1 = multiprocessing.Process(target=artciles)
    process2 = multiprocessing.Process(target=audio)
    # process3 = multiprocessing.Process(target=delete)

    process1.start()
    process2.start()
    # process3.start()

if __name__ == "__main__":
    main()