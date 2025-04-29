from warcio.warcwriter import WARCWriter
from warcio.statusandheaders import StatusAndHeaders
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
        """
        Open a new WARC file writer. The file name is based on the current file index.
        """
        self.stream = open(f"data-{self.file_index}.warc.gz", 'wb')
        self.writer = WARCWriter(self.stream, gzip=True)

    def store_page(self, url: str, html: str, fetched_content: object):
        """
        Store the page content in a WARC file.
        url: The URL of the page.
        html: The HTML content of the page.
        fetched_content: The fetched content object containing headers and other metadata.
        """
        with self.lock:
                if self.closed:
                    return

                encoded_html = html.encode("utf-8", errors='replace')
                headers_list = fetched_content.raw.headers.items()

                http_headers = StatusAndHeaders(statusline='200 OK', headers=headers_list, protocol='HTTP/1.0')

                payload_stream = BytesIO(encoded_html)
                record = self.writer.create_warc_record(url, record_type="application/http; msgtype=response", payload=payload_stream, http_headers=http_headers)
                self.writer.write_record(record)

                self.page_count += 1

                if self.page_count % self.batch_limit == 0:
                    self.stream.close()
                    self.file_index += 1
                    self._open_new_writer()

    def finalize(self):
        """
        Finalize the storage by closing the last WARC file writer.
        """
        with self.lock:
            self.stream.close()
            self.closed = True