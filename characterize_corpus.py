import os
import re
from collections import Counter, defaultdict
from urllib.parse import urlparse
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
import pandas as pd
import threading

# Path to the directory containing WARC files
WARC_DIR = "/home/marialuiza/Documents/faculdade/ir/webCrawler/data_100/"

# Global data structures
domain_counts = Counter()  # Count of webpages per domain
domain_tokens = defaultdict(list)  # List of token counts per domain
total_unique_domains = set()  # Set of unique domains
webpage_token_counts = []  # List of token counts per webpage

# Lock for thread-safe updates
lock = threading.Lock()

# Function to tokenize text
def tokenize(text):
    tokens = re.findall(r'\w+', text.lower())
    return tokens

# Function to process a single WARC file
def process_warc_file(warc_file):
    local_domain_counts = Counter()
    local_domain_tokens = defaultdict(list)
    local_unique_domains = set()
    local_webpage_token_counts = []

    warc_path = os.path.join(WARC_DIR, warc_file)
    with open(warc_path, 'rb') as stream:
        for record in ArchiveIterator(stream):
            print(f"Processing record: {record.rec_headers.get_header('WARC-Record-ID')}")
            # Extract the URL
            url = record.rec_headers.get_header('WARC-Target-URI')
            domain = urlparse(url).netloc
            local_unique_domains.add(domain)
            
            # Extract the HTML content
            html = record.content_stream().read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract visible text and tokenize
            text = ' '.join(soup.stripped_strings)
            tokens = tokenize(text)
            token_count = len(tokens)
            
            # Update local data structures
            local_domain_counts[domain] += 1
            local_domain_tokens[domain].append(token_count)
            local_webpage_token_counts.append(token_count)

    # Merge local results into global data structures
    with lock:
        total_unique_domains.update(local_unique_domains)
        for domain, count in local_domain_counts.items():
            domain_counts[domain] += count
        for domain, tokens in local_domain_tokens.items():
            domain_tokens[domain].extend(tokens)
        webpage_token_counts.extend(local_webpage_token_counts)

# Process each WARC file using threads
threads = []
for warc_file in os.listdir(WARC_DIR):
    if warc_file.endswith('.warc.gz'):
        print(f"Processing {warc_file}...")
        thread = threading.Thread(target=process_warc_file, args=(warc_file,), name=f"Thread-{warc_file}")
        threads.append(thread)
        thread.start()

# Wait for all threads to finish
for thread in threads:
    print(f"Waiting for {thread.name} to finish...")
    thread.join()

# Calculate size distribution per domain
domain_size_distribution = {domain: len(tokens) for domain, tokens in domain_tokens.items()}

# Save results to CSV files
output_dir = "/home/marialuiza/Documents/faculdade/ir/webCrawler/data_100/analysis_results"
os.makedirs(output_dir, exist_ok=True)

# Total unique domains
with open(os.path.join(output_dir, "unique_domains.txt"), "w") as f:
    f.write(f"Total Unique Domains: {len(total_unique_domains)}\n")
    f.write("\n".join(sorted(total_unique_domains)))

# Size distribution (number of webpages per domain)
domain_counts_df = pd.DataFrame(list(domain_counts.items()), columns=["Domain", "Webpages"])
domain_counts_df.to_csv(os.path.join(output_dir, "domain_webpage_counts.csv"), index=False)

# Size distribution (number of tokens per domain)
domain_tokens_df = pd.DataFrame(
    [(domain, sum(tokens), len(tokens), sum(tokens) / len(tokens)) for domain, tokens in domain_tokens.items()],
    columns=["Domain", "Total Tokens", "Webpages", "Average Tokens per Webpage"]
)
domain_tokens_df.to_csv(os.path.join(output_dir, "domain_token_distribution.csv"), index=False)

# Size distribution (number of tokens per webpage)
webpage_tokens_df = pd.DataFrame(webpage_token_counts, columns=["Tokens"])
webpage_tokens_df.to_csv(os.path.join(output_dir, "webpage_token_counts.csv"), index=False)

print("Analysis complete. Results saved in:", output_dir)