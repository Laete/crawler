from django.views import generic

from .services import SpiderService, Spider


class IndexView(generic.ListView):
    spider_service: SpiderService

    template_name = 'spider/index.html'
    context_object_name = 'processed_urls'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spider_service = SpiderService()
        self.spider = Spider(True)

    def get_queryset(self):
        """Return all links"""
        #return self.spider_service.get_processed_links()
        return self.spider.crawl_page('https://en.wikipedia.org/wiki/Django_(web_framework)')
