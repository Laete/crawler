from typing import List


class Spider:
    _limit_to_domain: bool

    def __init__(self, limit_to_domain):
        self._limit_to_domain = limit_to_domain

    def crawl_page(self, link):
        pass

    def _get_page(self, link) -> str:
        # Opens link, gets page content
        pass

    def _find_links(self, page) -> List[str]:
        # finds all links using regex
        pass

    def _filter_and_normalize_links(self, links: List[str]):
        # filters all non-links like # (anchors)
        # filters other domains if limit_to_domain
        # normalizes relative links to absolute
        pass
