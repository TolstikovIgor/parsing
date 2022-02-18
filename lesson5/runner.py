from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson_5 import settings
from lesson_5.spiders.labirint import LabirintSpider
from lesson_5.spiders.book24 import Book24Spider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    name_books = 'python'

    process.crawl(LabirintSpider, name_books = name_books)
    process.crawl(Book24Spider, name_books = name_books)
    process.start()