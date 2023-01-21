import datetime
from queue import Queue
from typing import Set
from threading import Thread
from spider.types import Link
from spider.services.spider import Spider


class SpiderService:
    _links_to_process: Queue
    _urls_to_display: Set[str]

    def __init__(self):
        self.current_link = None
        self._links_to_process = Queue()
        self._urls_to_display = set([])
        self._threads = []

    def get_processed_links(self):
        return self._urls_to_display

    def process_link(self, link: str):
        self._links_to_process.put(Link(url=link, depth=0))
        self._urls_to_display.add(link)
        workers_count = 10
        # TODO: display time delta
        before = datetime.datetime.now()
        print(f'Started crawling at {before}')
        self._threads = [
            Thread(target=self._process_link, args=[_], daemon=True).start() for _ in range(workers_count)
        ]
        self._links_to_process.join()
        after = datetime.datetime.now()
        print(f'Finished crawling at {after}, took {(after-before).total_seconds()} seconds')
        return self._urls_to_display

    def _process_link(self, threadNo: int):
        while True:
            link_to_process = self._links_to_process.get()
            spider = Spider(True)
            print(f'Crawling page {link_to_process.url} on thread {threadNo}, depth {link_to_process.depth}')
            new_links = spider.crawl_page(link_to_process.url)
            if link_to_process.depth < 3:  # TODO: const
                for new_link in new_links:
                    if new_link not in self._urls_to_display:
                        self._links_to_process.put(Link(url=new_link, depth=link_to_process.depth + 1))
            self._urls_to_display.update(new_links)
            self._links_to_process.task_done()


