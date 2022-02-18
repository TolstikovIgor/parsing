from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagramparser.spiders.instagram import InstagramSpider
from instagramparser import settings


import copy
from colorlog import ColoredFormatter
import scrapy.utils.log
color_formatter = ColoredFormatter(
    (
        '%(log_color)s%(levelname)-5s%(reset)s '
        '%(c202)s[%(asctime)s]%(reset)s'
        '%(thin_c236)s %(name)s %(funcName)s %(bold_purple)s:%(lineno)d%(reset)s '
        '%(log_color)s%(message)s%(reset)s'
    ),
    datefmt='%y-%m-%d %H:%M:%S',

    log_colors={
        'DEBUG': 'blue',
        'INFO': 'bold_c25',
        'WARNING': 'red',
        'ERROR': 'bg_bold_red',
        'CRITICAL': 'red,bg_c244',
    }
)
_get_handler = copy.copy(scrapy.utils.log._get_handler)
def _get_handler_custom(*args, **kwargs):
    handler = _get_handler(*args, **kwargs)
    handler.setFormatter(color_formatter)
    return handler
scrapy.utils.log._get_handler = _get_handler_custom


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider)
    process.start()
