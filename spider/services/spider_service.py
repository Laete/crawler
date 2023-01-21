from typing import Optional, List
from multiprocessing.pool import ThreadPool


class SpiderService:
    _current_link: Optional[str]
    # TODO: temp; will be removed in favor of Queue
    _processed_links: List[str]
    _spiders: ThreadPool

    def __init__(self):
        self.current_link = None
        self._processed_links = ['ab', 'vc', 'cd']

    def get_processed_links(self):
        return self._processed_links

    def process_link(self):
        # adds link to queue
        # starts link processing
        pass

    def _process_link(self):
        # while queue has not-processed or depth isn't reached
        # spawns new spider in thread
        # puts new links into queue
        # async
        pass
    