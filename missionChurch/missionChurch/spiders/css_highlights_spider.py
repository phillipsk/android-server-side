import scrapy
from scrapy import Selector
import re


class QuotesSpider(scrapy.Spider):
    name = "css_highlights"
    start_urls = ['https://toolbox-media.com/missioncooljc/']

    # TODO: remove cache settings prior to production, alternative file option requires absolute path
    # start_urls = ['file:///highlights-missioncooljc.html']

    def parse(self, response):
        widgets = response.xpath("//section[contains(@id,'highlight')]")
        selector = Selector(response)
        for widget in widgets:
            # for quote in response.css('div.quote'):
            if len(widget.xpath(".//div/a/img").attrib) > 0:
                yield {
                    'highlight': widget.xpath(".//@id").get(),
                    'title': widget.xpath(".//div[contains(@class, 'title')]//h1/text()").get(),
                    'caption': re.sub('\s+', '', widget.xpath(".//div[contains(@class, 'description')]//text()").get()),
                    'tags': widget.css('div.tags a.tag::text').getall(),
                    'imageUrl': widget.xpath(".//div/a/img").attrib['src'],
                    'imageWidth': widget.xpath(".//div/a/img").attrib['width'],
                    'imageHeght': widget.xpath(".//div/a/img").attrib['height']
                }
