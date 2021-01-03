# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from typing import Optional


class HighlightItem(scrapy.Item):
    highlightId = scrapy.Field()
    title = scrapy.Field()
    caption = scrapy.Field()
    pass


# not available in Python v3.5 (running on server)
# @dataclass
# class HighlightDC(scrapy.Item):
#     highlightId: Optional[str] = field(default=None)
#     title: Optional[str] = field(default=None)
#     caption: Optional[str] = field(default=None)

# Not used, to demonstrate Python multi class extension below
class Zoom(HighlightItem):
    followUrl = scrapy.Field()
    meetingID = scrapy.Field()
    passcode = scrapy.Field()


# TODO: reverse hierarchy Image & Zoom should be top classes?
class Image(Zoom, HighlightItem):
    imageUrl = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
