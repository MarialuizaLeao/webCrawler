import json
from urllib.parse import urlparse
import time

def debug_output(url, title, text, timestamp):
    return json.dumps({
        "URL": url,
        "Title": title,
        "Text": ' '.join(text.split()[:20]),
        "Timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    }, ensure_ascii=False, indent=0)
