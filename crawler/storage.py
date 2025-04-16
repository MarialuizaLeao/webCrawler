from warcio.warcwriter import WARCWriter
from io import BytesIO
import threading

class Storage:
    def __init__(self):
        self.page_count = 0
        self.batch_limit = 1000
        self.file_index = 0
        self.lock = threading.Lock()
        self.closed = False
        self._open_new_writer()

    def _open_new_writer(self):
        self.stream = open(f"data-{self.file_index}.warc.gz", 'wb')
        self.writer = WARCWriter(self.stream, gzip=True)

    def store_page(self, url, response, timestamp):
       with self.lock:
            if self.closed:
                return

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

    def finalize(self):
        with self.lock:
            if not self.closed:
                self.stream.close()
                self.closed = True