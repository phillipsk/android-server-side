from scrapy.loader import ItemLoader
from missionChurch.items import *


class HighlightsSpider(scrapy.Spider):
    name = "pro_highlights"
    allowed_domains = ['toolbox-media.com']
    start_urls = ['https://toolbox-media.com/missioncooljc/']

    def parse(self, response):
        l = ItemLoader(item=HighlightDC(), response=response)
        l.add_xpath('highlightId', "//section[contains(@id,'highlight')]//@id")
        l.add_xpath('title', "//section[contains(@id,'highlight')]"
                             "//div[contains(@class, 'title')]//h1//text()")
        l.add_xpath('caption', "//section[contains(@id,'highlight')]"
                               "//div[contains(@class, 'description')]//text()")

        # l.add_xpath('title', ".//div[contains(@class, 'title')]//h1/text()")
        # l.add_value('last_updated', 'today')  # you can also use literal values
        return l.load_item()
