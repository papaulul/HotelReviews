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
class hotelItem(scrapy.Item):
    hotelname = scrapy.Field()
    hotel_rating = scrapy.Field()
    url = scrapy.Field()
    num_amenities = scrapy.Field()
    amenities = scrapy.Field()
    price_range =scrapy.Field()
    num_rooms = scrapy.Field()