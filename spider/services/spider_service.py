import datetime
from queue import Queue
from typing import Set
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import logging

from spider.types import Link
from spider.services.spider import Spider


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SpiderService:
    _links_to_process: Queue
    _urls_to_display: Set[str]

    def __init__(self):
        self.current_link = None
        self._links_to_process = Queue()
        self._urls_to_display = set([])

    def get_processed_links(self):
        return self._urls_to_display

    def process_link(self, link: str):
        before = datetime.datetime.now()
        with ThreadPoolExecutor(max_workers=10) as executor:  # TODO: from form
            future_links_list = {executor.submit(self._process_link, Link(url=url, depth=0)) for url in [link]}
            while len(future_links_list) > 0:
                for future_links in as_completed(future_links_list):
                    result = future_links.result()
                    if len(result) > 0:
                        future_links_list.update([executor.submit(self._process_link, new_link) for new_link in result])
                    future_links_list.remove(future_links)
        after = datetime.datetime.now()
        logger.info(f'Finished crawling at {after}, took {(after - before).total_seconds()} seconds')
        return self._urls_to_display

    def _process_link(self, link_to_process: Link):
        self._urls_to_display.add(link_to_process.url)
        new_urls = Spider(True).crawl_page(link_to_process.url)  # TODO: from form
        new_links = []
        if link_to_process.depth < 2:  # TODO: from form
            new_links = [
                Link(url=new_link, depth=link_to_process.depth + 1) for new_link in new_urls
                if new_link not in self._urls_to_display
            ]
        self._urls_to_display.update(new_urls)

        return new_links

