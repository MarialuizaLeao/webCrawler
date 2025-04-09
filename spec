Spec:
[X] Your implementation should include a main.py file, which will be
executed in the same virtual environment described above, as follows:
$ python3 main.py -s <SEEDS> -n <LIMIT> [-d]
with the following arguments:
    •-s <SEEDS>: the path to a file containing a list of seed URLs (one URL
    per line) for initializing the crawling process.
    •-n <LIMIT>: the target number of webpages to be crawled; the crawler
    should stop its execution once this target is reached.
    •-d: (optional argument) run in debug mode (see below)
[X] When executed in debugging mode (i.e. when -d is passed as
a command-line argument), your implementation must print a record of each
crawled webpage to standard output2 as it progresses. Such a record must be
formatted as a JSON document containing the following fields:
    •URL, containing the page URL;
    •Title, containing the page title;
    •Text, containing the first 20 words from the page visible text;
    •Timestamp, containing the Unix time3 when the page was crawled.

[] keep a frontier of URLs to be crawled
[] For each URL consumed from the frontier, your implementation must fetch the corresponding webpage, 
parse it, store the extracted HTML content in the local corpus
[] Enqueue the extracted outlinks in the frontier to be crawled later
[] Selection Policy
    [] must only follow discovered links to HTML pages (i.e. resources with MIME type text/html)
    [] o improve coverage, you may optionally choose to limit the crawling depth of any given website.
[X] Revisitation policy
    [] you must not revisit a previously crawled webpage
    [] normalize URLs and check for duplicates before adding new URLs to the frontier
[] Parallelization policy
    [] you must parallelize the crawling process across multiple threads
    [] You may experiment to find an optimal number of threads to maximize your download rate while minimizing the incurred parallelization overhead
[] Politeness policy
    [] your implementation must abide by the robots exclusion protocol
    [] Unless explicitly stated otherwise in a robots.txt file, you must obey a delay of at least 100ms between consecutive requests to the same website
[] Storage policy
    [] your implementation must crawl and store a total of 100,000 unique webpages
    [] The raw HTML content of the crawled webpages must be packaged using the WARC format with 1,000 webpages stored per WARC file (totalling 100 such files), compressed with gzip to reduce storage costs.