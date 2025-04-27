from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

class Parser:
    def parse(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        if not soup:
            return '', '', []
        # Extract title, text, and outlinks
        for tags_to_decompose in soup(['script', 'style', 'template']):
            tags_to_decompose.decompose()
        html_content = soup.prettify()
        title = soup.title.string.strip() if soup.title and soup.title.string else ''
        outlinks = set()
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            abs_url = urljoin(base_url, href)
            parsed = urlparse(abs_url)
            if parsed.scheme in ('http', 'https'):
                outlinks.add(abs_url)
        return title, html_content, list(outlinks)
