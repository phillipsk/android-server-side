import scrapy
from itemloaders import ItemLoader
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from tutorial.items import *


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
        # 'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for selector in response.xpath("//*[@class='quote']"):
            # l = ItemLoader(item=FirstSpiderItem(), selector=selector)
            l = ItemLoader(item=InventoryItem(), selector=selector)
            l.add_xpath('text', './/span[@class="text"]/text()')
            l.add_xpath('author', '//small[@class="author"]/text()')
            # l.add_xpath('tags', './/meta[@class="keywords"]/@content')
            yield l.load_item()

        next_page = response.xpath(".//li[@class='next']/a/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


runner = CrawlerRunner(settings=get_project_settings())
runner.crawl(QuotesSpider)
# runner.crawl(MySpider2)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()  # the script will block here until all crawling jobs are finished
