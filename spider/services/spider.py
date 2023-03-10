from typing import List, Optional, Set
from urllib import request, parse
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Spider:
    _limit_to_domain: bool
    _current_hostname: Optional[str]
    _current_domain: Optional[str]
    _current_protocol: Optional[str]

    def __init__(self, limit_to_domain):
        self._limit_to_domain = limit_to_domain
        self._current_domain = None
        self._current_hostname = None
        self._current_protocol = None

    def crawl_page(self, link):
        """
        Initiates crawl
        :param link:
        :return:
        """
        parsed_link = parse.urlparse(link)
        self._current_hostname = parsed_link.netloc
        self._current_protocol = parsed_link.scheme

        page = self._get_page(link)
        links = self._find_links(page)
        normalized_links = self._filter_and_normalize_links(links)
        return normalized_links

    @staticmethod
    def _get_page(link) -> str:
        """
        Opens link, gets page content
        :param link:
        :return: str
        """
        try:
            fp = request.urlopen(link)
            mybytes = fp.read()

            mystr = mybytes.decode("utf8")
            fp.close()

            return mystr
        except Exception as e:
            logger.debug(f'Raised exception {e} on page {link}')
            return ''

    @staticmethod
    def _find_links(page) -> List[str]:
        """
        Gets all links from page
        :param page:
        :return:
        """
        soup = BeautifulSoup(page, "html.parser")
        return [link.get("href") for link in soup.find_all("a")]

    def _filter_and_normalize_links(self, links: List[str]) -> Set[str]:
        """
        Filters anchors and limits to domain, if needed
        Makes all links absolute
        :param links:
        :return:
        """
        result = set([])
        for link in links:
            if not link:
                continue
            if link.startswith("#"):  # removing local anchors
                continue

            # normalizing link
            parsed_url = parse.urlparse(link)
            scheme = parsed_url.scheme or self._current_protocol
            netloc = parsed_url.netloc or self._current_hostname
            normalized_link = parse.urlunparse((scheme, netloc, parsed_url.path, '', '', ''))

            # limiting to domain
            if self._limit_to_domain and f"{self._current_hostname}" not in normalized_link:
                continue
            result.add(normalized_link)
        return result
