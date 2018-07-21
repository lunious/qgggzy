# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 全国
class QuanguoItem(scrapy.Item):
    area = scrapy.Field()
    city = scrapy.Field()
    lypt = scrapy.Field()
    sysTime = scrapy.Field()
    deadTime = scrapy.Field()
    signStauts = scrapy.Field()
    type = scrapy.Field()
    entryType = scrapy.Field()
    entryHy = scrapy.Field()
    url = scrapy.Field()
    showUrl = scrapy.Field()
    blankUrl = scrapy.Field()
    entryName = scrapy.Field()
    entryNum = scrapy.Field()
    oldEntityId = scrapy.Field()
    zbdlqy = scrapy.Field()
    zbdllxr = scrapy.Field()
    zbdldz = scrapy.Field()
    zbdldh = scrapy.Field()
    squCount = scrapy.Field()
    isShow = scrapy.Field()
    label = scrapy.Field()
    tempLabelName = scrapy.Field()
    entityUrl = scrapy.Field()
    txt = scrapy.Field()