# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StackItem(scrapy.Item):
    review = scrapy.Field()
    hotel_name = scrapy.Field()
    bubble = scrapy.Field()
    url = scrapy.Field()
    travel_type = scrapy.Field()
