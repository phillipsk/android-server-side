import re
import scrapy
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.selector import Selector
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from missionChurch.items import Image
from twisted.internet import reactor


# Mark top level missionchurch dir as sources root in PyCharm
# HTTPCache is enabled in Scrapy setting.py
# highlights_main_spider, represents final version with xpath selectors
# css_highlights_spider, version with ItemLoader also with CSS selectors
# By default JSON standards and library handles unicode chars '\u2022'
# to run edit PyCharm run configurations -> crawl highlights -O highlights_main.json
# Do not use virtualenv, use macOS python 3.7 with Scrapy v2.4
# updated with pipeline and feed functionality
# added CrawlerProcess to run spider from script

class HighlightsSpider(scrapy.Spider):
    name = "highlights"
    allowed_domains = ['toolbox-media.com']
    start_urls = ['https://toolbox-media.com/missioncooljc/']

    def parse(self, response):
        items = []
        widgets = response.xpath("//section[contains(@id,'highlight')]")
        selector = Selector(response)  # debug in PyCharm evaluate expression
        regex = re.compile(r'[\n\r\t]')

        for section in widgets:
            subitem = Image()
            subitem['highlightId'] = section.xpath(".//@id").get()
            subitem['title'] = section.xpath(".//div[contains(@class, 'title')]//h1/text()").get()
            caption = section.xpath(".//div[contains(@class, 'description')]//text()").get()
            if caption is not None:
                subitem['caption'] = regex.sub(' ', caption).strip()  # .encode('ascii', 'ignore')
            subitem['imageUrl'] = section.xpath(".//div//img").attrib['src']
            subitem['width'] = section.xpath(".//div//img").attrib['width']
            subitem['height'] = section.xpath(".//div//img").attrib['height']
            subitem['followUrl'] = section.xpath(".//@href").get()
            items.append(subitem)
        return items


# process = CrawlerProcess(settings=get_project_settings())
#
# process.crawl(HighlightsSpider)
# process.start()  # the script will block here until the crawling is finished

# configure_logging()
runner = CrawlerRunner(settings=get_project_settings())
runner.crawl(HighlightsSpider)
# runner.crawl(MySpider2)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()  # the script will block here until all crawling jobs are finished
