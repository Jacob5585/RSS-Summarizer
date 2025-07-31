import multiprocessing
from time import sleep
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from psutil import virtual_memory
from os import execv
from sys import executable, argv
import files
from scrape_articles import get_articles
from text2speech import run_text_2_speech
import logs

rss_feed = {
    "tech": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen",
    "finance": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen",
    "science": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen",
    "world_news": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen"
    }

def artciles():
    while True:
        for feed, rss in rss_feed.items():
            # print(f'----------{feed}: {rss}----------')
            get_articles(rss, feed)
            # print(f'\nGet articles for {feed} complete\n')
            logs.create_info_logs(f'\nGet articles for {feed} complete\n')

def audio(artciles_limit = 5):
    while True:
        for feed, _ in rss_feed.items():
            try:
                data = files.read_json_recursively('../articles/' + feed)
                audio_list = files.read_names_recursively('../audio/' + feed)
            except ValueError as e:
                # print(e)
                logs.create_error_logs(f'{e} from main.py audio function')
                continue

            # Remove articles that have already been converted to audio
            for i in data.copy():
                if i['file_name'] in audio_list:
                    data.remove(i)

            if not len(data):
                continue
            
            # print(f'Creating Audio for: {feed}:')
            logs.create_info_logs(f'Creating Audio for: {feed}:')
            # Limit the number of articles to convert to audio at a time to avoid crashing due to exceeding memory
            with ThreadPoolExecutor() as executor:
                executor.map(lambda item: run_text_2_speech(item['summary'], feed, item['file_name']), data[:artciles_limit])
            
            # print(f'\nText2Speech for {feed} complete\n')
            logs.create_info_logs(f'\nText2Speech for {feed} complete\n')

def delete():
    oldest_time = 0
    while True:
        # Sleep until deleting is eligible (Doing this rp prevent unnecessary reading of files)
        sleep(oldest_time)

        for feed, _ in rss_feed.items():
            articles = files.read_names_recursively('../articles/' + feed)
            articles += (files.read_names_recursively('../audio/' + feed)) # Incase there are audio files that aren't in the articles
            articles = list(dict.fromkeys(articles)) # Removes any duplicates

            for article in articles:
                try:
                    time_stamp  = datetime.strptime(article, "%Y-%m-%d_%H-%M-%S-%f")
                    time_difference = abs(int((datetime.now() - time_stamp).total_seconds()))
                    time_difference = 86400 - time_difference #Subtract 86400 for 24 hours

                    if time_difference <= 0: # if time differences is less than or equal to 0 then its 24 hours or older
                        # print(f'deleting: {article} from articles/{feed} and audio/{feed}')
                        logs.create_info_logs(f'deleting: {article} from articles/{feed} and audio/{feed}')
                        files.delete_files(f'../articles/{feed}/{article}.json')
                        files.delete_files(f'../audio/{feed}/{article}.mp3')
                    else:
                        oldest_time = time_difference
                
                except ValueError as e:
                    # print(f'ValueError: {e}')
                    logs.create_warning_logs(f'ValueError: {e} from main.py delete function')
                    continue
                

def main():
    max_memory = 90

    process1 = multiprocessing.Process(target=artciles)
    process2 = multiprocessing.Process(target=audio)
    process3 = multiprocessing.Process(target=delete)

    process1.start()
    process2.start()
    process3.start()

    while True:
        if virtual_memory().percent > max_memory:
            process1.terminate()
            process2.terminate()
            process3.terminate()
            logs.create_error_logs(f'Memory too high, restarting\nWaiting for process to terminate')

            process1.join()
            process2.join()
            process3.join()
            logs.create_error_logs(f'Process terminating\nRestarting program')

            execv(executable, ['python'] + argv)
        
        # Check memory every 10 seconds
        sleep(10)

if __name__ == "__main__":
    main()