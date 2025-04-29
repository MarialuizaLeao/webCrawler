import requests
from protego import Protego
import time
from urllib.parse import urlparse


class Fetcher:
    def __init__(self):
        self.robots_cache = {}
        self.delay_cache = {}
        self.last_access = {}

    def can_fetch(self, url: str) -> bool:
        """
        Check if the URL can be fetched according to the robots.txt rules.
        url: The URL to check.
        return: True if the URL can be fetched, False otherwise.
        """
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        # Check if the domain is already in the cache
        if domain not in self.robots_cache:
            robots_url = f"{parsed_url.scheme}://{domain}/robots.txt"
            try:
                robots_out = requests.get(robots_url)
                robot_parser = Protego.parse(robots_out.text)
                self.robots_cache[domain] = robot_parser
                # Check for crawl delay, if not set, default to 0.001
                if robot_parser.crawl_delay("*") is None:
                    self.delay_cache[domain] = 0.001
                else:
                    self.delay_cache[domain] = robot_parser.crawl_delay("*")
            except:
                # If robots.txt is not reachable, assume no time restrictions
                self.delay_cache[domain] = 0.001
                self.robots_cache[domain] = None

        robot_parser = self.robots_cache[domain] # Get the cached parser
        if robot_parser is None:
            return True
        try:
            return robot_parser.can_fetch("*", url)
        except:
            return True

    def respect_delay(self, url: str):
        """
        Respect the crawl delay for the given URL.
        url: The URL to check.
        """
        now = time.time()
        last = self.last_access.get(url,0)
        delay = self.delay_cache.get(url,0.001)
        if now - last < delay:
            time.sleep(delay - (now - last))
        self.last_access[url] = time.time()

    def fetch(self, url: str) -> tuple:
        """
        Fetch the content of the given URL.
        url: The URL to fetch.
        return: A tuple containing the response and the timestamp.
        """
        if not self.can_fetch(url):
            return None, None

        parsed = urlparse(url)
        self.respect_delay(parsed.netloc)

        try:
            response = requests.get(url, timeout=5)
            if 'text/html' in response.headers.get('Content-Type', ''):
                return response, time.time()
        except:
            return None, None

        return None, None

    
        