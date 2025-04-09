import argparse

from crawler.crawler import Crawler
import threading

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

    crawler = Crawler(args.seed, args.limit, args.debug)

    threads = []
    for _ in range(10):  # 10 threads for parallel crawling
        t = threading.Thread(target=crawler.crawl)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    crawler.storage.finalize()  # Close the storage connection
    print(f"Total pages crawled: {crawler.storage.page_count}")
    
        
if __name__ == "__main__":
    main()


