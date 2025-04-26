import argparse
from crawler.crawler import Crawler
import threading
import time
import datetime
import csv

def log_thread_status(crawler, interval=5):
    start_time = time.time()
    with open("download_rate50.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Download Rate (pages/second)"])  # Write header

        while True:
            alive = [t for t in threading.enumerate() if t.name != "MainThread"]
            elapsed_time = time.time() - start_time
            download_rate = crawler.storage.page_count / elapsed_time if elapsed_time > 0 else 0
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Log to console
            print(f"[LOG] {len(alive)} threads active - {timestamp}")
            print(f"[LOG] Download rate: {download_rate:.2f} pages/second")

            # Write to CSV
            writer.writerow([timestamp, download_rate])
            csvfile.flush()  # Ensure data is written to disk

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

    # Record the start time
    start_time = time.time()
    

    crawler = Crawler(args.seed, args.limit, args.debug)
    monitor_thread = threading.Thread(target=log_thread_status, name="Monitor", daemon=True, args=[crawler])
    monitor_thread.start()

    threads = []
    for _ in range(50):
        t = threading.Thread(target=crawler.crawl, name=f"Crawler-{_}")
        t.start()
        threads.append(t)
        time.sleep(0.5)

    for t in threads:
        t.join()
        print(f"{t.name} finished...")

    # Record the end time
    end_time = time.time()

    crawler.storage.finalize()  # Close the last WARC file

    # Calculate and print the download rate
    total_pages = crawler.storage.page_count
    elapsed_time = end_time - start_time
    download_rate = total_pages / elapsed_time if elapsed_time > 0 else 0
    print(f"Total pages crawled: {total_pages}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Download rate: {download_rate:.2f} pages/second")
        
if __name__ == "__main__":
    main()


