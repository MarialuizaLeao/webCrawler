from crawler.frontier import Frontier
from crawler.fetcher import Fetcher
from crawler.parser import Parser
from crawler.storage import Storage
from crawler.utils import debug_output
import threading


class Crawler():
    def __init__(self, seed, limit, debug):
        self.frontier = Frontier()
        self.fetcher = Fetcher()
        self.parser = Parser()
        self.storage = Storage()
        self.debug = debug
        self.limit = limit

        # Read the seed URL from file
        with open(seed, 'r') as file:
            lines = file.readlines()
        for line in lines:
            self.frontier.add(line.strip())

    def crawl(self):
        # While there are URLs to discover
        while self.frontier.has_next():

            # If the storage limit is reached, stop crawling
            with self.storage.lock:
                if self.storage.page_count >= self.limit:
                    print(f"[{threading.current_thread().name}] Finished crawling. Storage limit reached.")
                    return

            # Get next URL from frontier
            url = self.frontier.get()
            if url is None:
                continue

            # Fetch page content
            fetched_content, timestamp = self.fetcher.fetch(url)
            if fetched_content is None:
                continue

            # Parse page content
            title, text, outlinks = self.parser.parse(fetched_content.text, url)

            if title == '' and text == '' and outlinks == []:
                continue

            # Print debug information
            if self.debug:
                print(debug_output(url, title, text, timestamp))

            # Store page content
            self.storage.store_page(url, text, fetched_content)

            for link in outlinks:
                if not self.frontier.was_visited(link):
                    self.frontier.add(link)