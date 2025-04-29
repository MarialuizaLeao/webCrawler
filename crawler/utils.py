import json

def debug_output(url, title: str, text: str, timestamp: str) -> str:
    return json.dumps({
        "URL": url,
        "Title": title,
        "Text": text,
        "Timestamp": timestamp,
    }, ensure_ascii=False, indent=0)
