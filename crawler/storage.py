from warcio.warcwriter import WARCWriter
from warcio.statusandheaders import StatusAndHeadersParser
from io import BytesIO
import gzip
import threading
from queue import Queue

class Storage:
    def __init__(self):
        self.page_count = 0
        self.batch_limit = 1000
        self.file_index = 0
        self.queue = Queue()
        self.writer_thread = threading.Thread(target=self._writer_loop, daemon=True)
        self.cache = []
        self.cache_limit = 100  # write every 50 pages
        self.running = True
        self.stream = open(f"data-{self.file_index}.warc.gz", 'wb')
        self.writer = WARCWriter(self.stream, gzip=True)

        self.writer_thread.start()

    def _open_new_writer(self):
        print(f"Opening new WARC file: data-{self.file_index}.warc.gz")
        self.stream = open(f"data-{self.file_index}.warc.gz", 'wb')
        self.writer = WARCWriter(self.stream, gzip=True)

    def store_page(self, url, response, timestamp):
       self.queue.put((url, response, timestamp))

    def _writer_loop(self):
        while self.running or not self.queue.empty():
            try:
                item = self.queue.get(timeout=1)
                if item:
                    self.cache.append(item)
                if len(self.cache) >= self.cache_limit:
                    self._flush_cache()
            except:
                continue
        self._flush_cache()
        self.stream.close()

    def _flush_cache(self):
        for url, response, timestamp in self.cache:
            http_payload = f"HTTP/1.1 {response.status_code} OK\r\n"
            for header, value in response.headers.items():
                http_payload += f"{header}: {value}\r\n"
            http_payload += "\r\n"
            http_payload = http_payload.encode('utf-8') + response.content

            payload_stream = BytesIO(http_payload)
            record = self.writer.create_warc_record(url, 'response', payload=payload_stream)
            self.writer.write_record(record)

            self.page_count += 1
            if self.page_count % self.batch_limit == 0:
                self.stream.close()
                self.file_index += 1
                self._open_new_writer()

        print(f"Total pages crawled: {self.page_count}")

        self.cache.clear()


    def finalize(self):
        self.running = False
        self.writer_thread.join()