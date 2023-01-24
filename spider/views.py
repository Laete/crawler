from django.views import generic

from .services import SpiderService


class IndexView(generic.ListView):
    _spider_service: SpiderService

    template_name = "spider/index.html"
    context_object_name = "processed_urls"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._spider_service = SpiderService()

    def get_queryset(self):
        """Return all links"""
        return self._spider_service.process_link(
            "https://www.crummy.com/software/BeautifulSoup/"
        )
