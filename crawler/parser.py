from bs4 import BeautifulSoup
import re

class Parser:
    def parse(self, html: str) -> tuple:
        """
        Parse the HTML content and extract the title, html content, outlinks and first 20 tokens.
        html: The HTML content of the page.
        return: A tuple containing the title, text, and a list of outlinks.
        """
        soup = BeautifulSoup(html, 'html.parser')
        if not soup:
            return '', '', []
        # Get page html content
        for tags_to_decompose in soup(['script', 'style', 'template']):
            tags_to_decompose.decompose()
        html_content = soup.prettify()
        # Get the title
        title = soup.title.string.strip() if soup.title and soup.title.string else ''
        # Get first 20 tokens, besides the title

        first_20_tokens = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'], limit=20):
            text = tag.get_text()
            tokens = re.findall(r'\b\w+\b', text)
            first_20_tokens.extend(tokens)
            if len(first_20_tokens) >= 20:
                break
        first_20_tokens = ' '.join(first_20_tokens[:20])

        # Get outlinks
        outlinks = set()
        for link in soup.find_all('a', href=True):
            if link.get('href'):
                outlinks.add(link.get('href'))

        return title, html_content, list(outlinks), first_20_tokens
