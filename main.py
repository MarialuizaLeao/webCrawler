import argparse
from crawler.crawler import Crawler
import threading
import time
import datetime

def log_thread_status(interval=5):
    while True:
        alive = [t for t in threading.enumerate() if t.name != "MainThread"]
        print(f"[LOG] {len(alive)} threads ativas - {datetime.datetime.now().strftime('%H:%M:%S')}")
        time.sleep(interval)

def main():
    # Configuracao do analisador de argumentos
    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument(
        "-s", dest='seed', required=True, help="The seed URL to start the crawling process."
    )
    parser.add_argument(
        "-n", dest='limit', type=int, required=True, help="The target number of webpages to be crawled; the crawler should stop its execution once this target is reached."
    )
    parser.add_argument(
        "-d", dest='debug', action='store_true', required=False, help="Run in debug mode"
    )
    args = parser.parse_args()

    monitor_thread = threading.Thread(target=log_thread_status, name="Monitor", daemon=True)
    monitor_thread.start()

    crawler = Crawler(args.seed, args.limit, args.debug)

    threads = []
    for _ in range(100):
        t = threading.Thread(target=crawler.crawl, name=f"Crawler-{_}")
        t.start()
        threads.append(t)
        time.sleep(0.5) # Small delay to give each thread a chance to start

    for t in threads:
        t.join()

    crawler.storage.finalize()  # Close the storage connection
    print(f"Total pages crawled: {crawler.storage.page_count}")
    
        
if __name__ == "__main__":
    main()


