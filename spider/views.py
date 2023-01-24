import json
import logging

from django.views import generic
from django.http import HttpResponse

from .services import SpiderService


spider_service = SpiderService()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    _spider_service: SpiderService

    template_name = "spider/index.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_queryset(self):
        """Clear all links"""
        return spider_service.clear()


def query(request):
    request_body = json.loads(request.body.decode('utf-8'))
    url_to_crawl = request_body.get('source_url', '')
    max_depth = int(request_body.get('max_depth', '3'))
    workers_count = int(request_body.get('workers_count', '10'))
    limit_to_domain = request_body.get('limit_to_domain', True)
    result = []
    delta = -1
    if url_to_crawl != '':
        try:
            result, delta = spider_service.process_link(
                link=url_to_crawl,
                max_depth=max_depth,
                workers_count=workers_count,
                limit_to_domain=limit_to_domain
            )
        except Exception as ex:
            logger.error(ex)
            pass

    return HttpResponse(json.dumps({'result': list(result), 'delta': delta}), content_type='application/json')
