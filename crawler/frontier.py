from queue import Queue

class Frontier():
    def __init__(self):
        self.discovery = Queue() # URLs to discover
        self.visited = set() # URLs already visited

    def add(self, url):
        # Add URL to discovery queue
        if not self.was_visited(url) and self.discovery.qsize() < 100000:
            self.discovery.put(url)

    def get(self):
        # Get URL from discovery queue
        return self.discovery.get(timeout=3)
        
    def has_next(self):
        # Check if there are more URLs to discover
        return not self.discovery.empty()
    
    def was_visited(self, url):
        # Check if URL was already visited
        return url in self.visited