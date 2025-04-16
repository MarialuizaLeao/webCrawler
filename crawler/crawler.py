from crawler.frontier import Frontier
from crawler.fetcher import Fetcher
from crawler.parser import Parser
from crawler.storage import Storage
from crawler.utils import debug_output


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
        # While there are URLs to discover and the limit is not reached
        while self.frontier.has_next():
            if self.storage.page_count >= self.limit:
                return

            # Get next URL from frontier
            url = self.frontier.get()
            if url is None:
                continue

            # Fetch page content
            html, timestamp = self.fetcher.fetch(url)
            if html is None:
                continue

            # Parse page content
            title, text, outlinks = self.parser.parse(html.text, url)

            if title == '' and text == '' and outlinks == []:
                continue

            # Print debug information
            if self.debug:
                print(debug_output(url, title, text, timestamp))

            # Store page content
            self.storage.store_page(url, html, timestamp)

            for link in outlinks:
                if not self.frontier.was_visited(link):
                    self.frontier.add(link)
