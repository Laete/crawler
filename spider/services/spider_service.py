import datetime
from queue import Queue
from typing import Optional, Set, List, Tuple
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
    _executor: Optional[ThreadPoolExecutor]

    def __init__(self):
        self.current_link = None
        self._links_to_process = Queue()
        self._urls_to_display = set([])
        self._executor = None

    def clear(self):
        self._urls_to_display = set([])
        if self._executor:
            self._executor.shutdown()

    def get_processed_links(self):
        return self._urls_to_display

    def process_link(self, link: str, max_depth: int, workers_count: int, limit_to_domain: bool) -> Tuple[Set[str], int]:
        before = datetime.datetime.now()
        self.clear()
        self._executor = ThreadPoolExecutor(max_workers=workers_count)
        with self._executor as executor:
            future_links_list = {
                executor.submit(self._process_link, Link(url=url, depth=0), limit_to_domain, max_depth) for url in [link]
            }
            while len(future_links_list) > 0:
                for future_links in as_completed(future_links_list):
                    result = future_links.result()
                    if len(result) > 0:
                        future_links_list.update([
                            executor.submit(self._process_link, new_link, limit_to_domain, max_depth) for new_link in result
                        ])
                    future_links_list.remove(future_links)
        after = datetime.datetime.now()
        delta = (after - before).total_seconds()
        logger.info(f'Finished crawling at {after}, took {delta} seconds')
        return self._urls_to_display, delta

    def _process_link(self, link_to_process: Link, limit_to_domain: bool, max_depth: int) -> List[str]:
        self._urls_to_display.add(link_to_process.url)
        new_urls = Spider(limit_to_domain).crawl_page(link_to_process.url)  # TODO: from form
        new_links = []
        if link_to_process.depth < max_depth:
            new_links = [
                Link(url=new_link, depth=link_to_process.depth + 1) for new_link in new_urls
                if new_link not in self._urls_to_display
            ]
        self._urls_to_display.update(new_urls)

        return new_links

