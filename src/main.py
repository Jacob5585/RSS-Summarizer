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
            # files.save_json('../articles/' + data + '.json', feed)

def audio():
    from text2speech import convert_to_audio
    while True:
        for feed, _ in rss_feed.items():
            try:
                data = files.read_json_recursivly('../articles/' + feed)
                audio_list = files.read_names_recursivly('../audio/' + feed)
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
    from datetime import datetime, timedelta
    from time import sleep

    oldest_time = 0
    while True:
        # Sleep until deleting is eligible (Doing this rp prevent unessary reading of files)
        sleep(oldest_time)

        for feed, _ in rss_feed.items():
            articles = files.read_names_recursivly('../articles/' + feed)
            articles += (files.read_names_recursivly('../audio/' + feed)) # Incase there are audio files that aren't in the articles
            articles = list(dict.fromkeys(articles)) # Removes any duplicates

            for article in articles:
                try:
                    time_stamp  = datetime.strptime(article, "%Y-%m-%d_%H-%M-%S-%f")
                    time_difference = abs(int((datetime.now() - time_stamp).total_seconds()))
                    time_difference = 86400 - time_difference #Subtract 86400 for 24 hours

                    if time_difference <= 0: # if time differences is less than or equal to 0 then its 24 hours or older
                        print(f'deleting: {article} from articles/{feed} and audio/{feed}')
                        files.delete_files(f'../articles/{feed}/{article}.json')
                        files.delete_files(f'../audio/{feed}/{article}.mp3')
                    else:
                        oldest_time = time_difference
                
                except ValueError as e:
                    print(f'ValueError: {e}')
                    continue
                

def main():
    process1 = multiprocessing.Process(target=artciles)
    process2 = multiprocessing.Process(target=audio)
    process3 = multiprocessing.Process(target=delete)

    process1.start()
    process2.start()
    process3.start()

if __name__ == "__main__":
    main()