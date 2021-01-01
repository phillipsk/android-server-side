import json

import scrapy
from scrapy.selector import Selector
import re
from missionChurch.items import Image


# TODO: Mark top level missionchurch dir as sources root in PyCharm
# HTTPCache is enabled in Scrapy setting.py
# highlights_main_spider, represents final version with xpath selectors
# css_highlights_spider, version with ItemLoader also with CSS selectors
# By default JSON standards and library handles unicode chars '\u2022'
# to run edit PyCharm run configurations -> crawl highlights -O highlights_main.json
# Do not use virtualenv, use macOS python 3.7 with Scrapy v2.4


####
# //*[@id="resurrect-home-bottom-widgets"]
# /html/body/div[1]/div[2]/div/div/div/section[1]/div/a/img -- pastor image
# /html/body/div[1]/div[2]/div/div/div/section[3]/div/a/img
# /html/body/div[1]/div[2]/div/div/div/section[8]/div/a/img
# /html/body/div[1]/div[2]/div/div/div/section[12]/div/a/img
# /html/body/div[1]/div[2]/div/div/div/section[14]/div/a/img
# response.xpath("//section[contains(@id,'highlight')]/div/a/img")
# /html[@class='js no-touch rgba multiplebgs borderradius opacity resurrect-responsive-on']/body[@class='home page-template page-template-page-templates page-template-homepage page-template-page-templateshomepage-php page page-id-2493 custom-background resurrect-logo-font-oswald resurrect-heading-font-oswald resurrect-menu-font-oswald resurrect-body-font-open-sans resurrect-background-image-fullscreen resurrect-background-image-file-background-4']/div[@id='resurrect-container']/div[@id='resurrect-middle']/div[@id='resurrect-middle-content']/div[@id='resurrect-home-content']/div[@id='resurrect-home-bottom-widgets']/section[@id='ctfw-highlight-3']/div[@class='resurrect-caption-image resurrect-highlight resurrect-widget-first-element']/a/img[@class='resurrect-image']/@src

####


# class HighlightItemInline:
#     highlightId = None
#     title = None
#     caption = None
#
#     class Image:
#         imageUrl = None
#         width = None
#         height = None

class HighlightsSpider(scrapy.Spider):
    name = "highlights"
    allowed_domains = ['toolbox-media.com']
    start_urls = ['https://toolbox-media.com/missioncooljc/']

    def parse(self, response):
        items = []
        ditems = {}
        widgets = response.xpath("//section[contains(@id,'highlight')]")
        selector = Selector(response)
        regex = re.compile(r'[\n\r\t]')

        for section in widgets:
            # selector = Selector(section)
            # item = HighlightItem()
            # item['highlightId'] = section.xpath(".//@id").get()
            # item['title'] = section.xpath(".//div[contains(@class, 'title')]//h1/text()").get()
            # item['caption'] = section.xpath(".//div[contains(@class, 'description')]//text()").get()
            # # item['caption'] = regex.sub(' ', item.caption).strip()

            subitem = Image()
            subitem['highlightId'] = section.xpath(".//@id").get()
            subitem['title'] = section.xpath(".//div[contains(@class, 'title')]//h1/text()").get()
            caption = section.xpath(".//div[contains(@class, 'description')]//text()").get()

            # TODO: Caption is blank for several Highlight widgets
            # TODO: Handle this in android or python
            if caption is not None:
                subitem['caption'] = regex.sub(' ', caption).strip()  # .encode('ascii', 'ignore')
            subitem['imageUrl'] = section.xpath(".//div//img").attrib['src']
            subitem['width'] = section.xpath(".//div//img").attrib['width']
            subitem['height'] = section.xpath(".//div//img").attrib['height']

            subitem['followUrl'] = section.xpath(".//@href").get()

            # item.highlightId = section.xpath(".//@id").get()
            # item.title = section.xpath(".//div[contains(@class, 'title')]//h1/text()").get()
            # item.caption = section.xpath(".//div[contains(@class, 'description')]//text()").get()
            # item.caption = regex.sub(' ', item.caption).strip()
            #
            # # TODO: check URL domain prior to storing data --> section.xpath(".//@href").get() FOR PASTOR first element
            # if len(section.xpath(".//div/a/img").attrib) > 0:
            #     item.Image.imageUrl = section.xpath(".//div/a/img").attrib['src']
            #     item.Image.width = section.xpath(".//div/a/img").attrib['width']
            #     item.Image.height = section.xpath(".//div/a/img").attrib['height']

            # [a for a in dir(item) if not a.startswith('__') and not callable(getattr(item, a))]
            # for attr, value in item.__dict__.items():
            #     item.__getattribute__(value) = regex.sub(' ', value).strip()

            # yield subitem
            items.append(subitem)

        # s = json.dumps(items, default=lambda x: x.__dict__)

        # TODO: capture href links
        return items
