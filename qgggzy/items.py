# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 四川省(中标公示)
class SichuanGSItem(scrapy.Item):
    reportTitle = scrapy.Field()
    sysTime = scrapy.Field()
    url = scrapy.Field()
    entryName = scrapy.Field()
    entryOwner = scrapy.Field()
    ownerTel = scrapy.Field()
    tenderee = scrapy.Field()
    tendereeTel = scrapy.Field()
    biddingAgency = scrapy.Field()
    biddingAgencTel = scrapy.Field()
    placeAddress = scrapy.Field()
    placeTime = scrapy.Field()
    publicityPeriod = scrapy.Field()
    bigPrice = scrapy.Field()
    changeReason = scrapy.Field()
    oneTree = scrapy.Field()
    twoTree = scrapy.Field()
    threeTree = scrapy.Field()
    treeCount = scrapy.Field()
    oneCompany = scrapy.Field()
    onePrice = scrapy.Field()
    oneReviewPrice = scrapy.Field()
    oneScore = scrapy.Field()
    count = scrapy.Field()
    treeCount = scrapy.Field()

# 四川省（结果公告）
class SichuanGGItem(scrapy.Item):
    reportTitle = scrapy.Field()
    url = scrapy.Field()
    resource = scrapy.Field()
    sysTime = scrapy.Field()
    entryName = scrapy.Field()
    entryNum = scrapy.Field()
    purchasingType = scrapy.Field()
    Purchaser = scrapy.Field()
    purchasingAgent = scrapy.Field()

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