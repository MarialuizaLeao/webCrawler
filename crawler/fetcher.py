# can_fetch(url)
# respect_delay(url)
# fetch(url) -> (html, timestamp)

import requests
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

class Fetcher:
    def __init__(self):
        self.robots_cache = {}
        self.deley_cache = {}
        self.last_access = {}

    def can_fetch(self, url: str) -> bool:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain not in self.robots_cache:
            robots_url = f"{parsed_url.scheme}://{domain}/robots.txt"
            rp = RobotFileParser()
            rp.set_url(robots_url)
            try:
                rp.read()
                self.robots_cache[domain] = rp
                if rp.crawl_delay("*") is None:
                    self.deley_cache[domain] = 0.001
                else:
                    self.deley_cache[domain] = rp.crawl_delay("*")
            except:
                return False
        rp = self.robots_cache[domain]
        if rp is None:
            self.deley_cache[domain] = 0.001
            return True
        try:
            return rp.can_fetch("*", url)
        except:
            return True

    def respect_delay(self, url):
        now = time.time()
        last = self.last_access.get(url, 0)
        if now - last < self.deley_cache.get(url, 0.001):
            print(f"Sleeping for: {self.deley_cache.get(url, 0.001) - (now - last)}")
            time.sleep(self.deley_cache.get(url, 0.001) - (now - last))
        
        self.last_access[url] = time.time()

    def fetch(self, url: str) -> tuple:
        if not self.can_fetch(url):
            print(f"Cannot fetch {url}")
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

    
        