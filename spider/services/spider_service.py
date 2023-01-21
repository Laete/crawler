from queue import Queue
from typing import Set
from multiprocessing.pool import ThreadPool
from spider.types import Link
from spider.services.spider import Spider


class SpiderService:
    _links_to_process: Queue
    _urls_to_display: Set[str]
    _spiders: ThreadPool

    def __init__(self):
        self.current_link = None
        self._links_to_process = Queue()
        self._urls_to_display = set([])
        self._spider = Spider(True)

    def get_processed_links(self):
        return self._urls_to_display

    def process_link(self, link: str):
        self._links_to_process.put(Link(url=link, depth=0))
        self._urls_to_display.add(link)
        self._process_link()
        self._links_to_process.join()
        return self._urls_to_display

    def _process_link(self):
        while self._links_to_process.qsize() > 0:
            link_to_process = self._links_to_process.get()
            new_links = self._spider.crawl_page(link_to_process.url)
            if link_to_process.depth < 2 and self._links_to_process.qsize() < 10:   # TODO: const
                for new_link in new_links:
                    if new_link not in self._urls_to_display:
                        self._links_to_process.put(Link(url=new_link, depth=link_to_process.depth + 1))
            self._urls_to_display.update(new_links)
            self._links_to_process.task_done()


