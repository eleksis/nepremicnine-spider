# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Nepremicnina(scrapy.Item):
    iid = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
