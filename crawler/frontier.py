from queue import Queue

class Frontier():
    def __init__(self):
        self.discovery = Queue() # URLs to discover
        self.visited = set() # URLs already visited

    def add(self, url: str):
        """
        Add a URL to the discovery queue if it has not been visited yet.
        url: The URL to add.
        """
        # Add URL to discovery queue
        if not self.was_visited(url) and self.discovery.qsize() < 100000:
            self.discovery.put(url)

    def get(self) -> str:
        """
        Get the next URL from the discovery queue.
        return: The next URL to crawl.
        """
        # Get URL from discovery queue
        url = self.discovery.get(timeout=3)
        self.visited.add(url)
        return url
        
    def has_next(self) -> bool:
        """
        Check if there are more URLs to discover.
        return: True if there are more URLs to discover, False otherwise.
        """
        # Check if there are more URLs to discover
        return not self.discovery.empty()
    
    def was_visited(self, url: str) -> bool:
        """
        Check if a URL has already been visited.
        url: The URL to check.
        return: True if the URL has been visited, False otherwise.
        """
        # Check if URL was already visited
        return url in self.visited