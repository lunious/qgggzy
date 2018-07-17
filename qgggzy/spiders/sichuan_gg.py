# -*- coding: utf-8 -*-
import scrapy
import datetime
import json
import time
from qgggzy.items import SichuanGGItem
from scrapy.selector import Selector

class SichuanGgSpider(scrapy.Spider):
    name = 'sichuan_gg'
    allowed_domains = ['scggzy.gov.cn']
    page = 1
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 转换成时间数组
    timeArray = time.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray))
    url = 'http://www.scggzy.gov.cn/Info/GetInfoListNew?keywords=&times=3&timesStart=&timesEnd=&province=&area=&businessType=purchase&informationType=PurchaseBid&industryType='
    start_urls = [url + '&page=' + str(page) + '&parm=' + str(timestamp)]

    def parse(self, response):
        js = json.loads(response.body_as_unicode())
        if '成功' == js['message']:
            data = json.loads(js['data'])
            pageCount = js['pageCount']
            items = []
            for each in data:
                item = SichuanGGItem()
                item['reportTitle'] = each['Title']
                item['sysTime'] = each['CreateDateStr']
                item['url'] = 'http://www.scggzy.gov.cn' + each['Link']
                items.append(item)
            for item in items:
                yield scrapy.Request(url=item['url'], meta={'meta': item}, callback=self.detail_parse)

            # if self.page < pageCount:
            #     self.page += 1
            #
            # yield scrapy.Request(url=self.url + '&page=' + str(self.page) + '&parm=' + str(self.timestamp))


    def detail_parse(self,response):
        item = response.meta['meta']
        res = response.xpath('//*[@id="hidThree0"]/@value').extract()
        # print(res)
        # entryName = Selector(text=res[0]).xpath('//tbody/tr/td[1]').extract()
        entryName = ''
        entryNum = ''
        purchasingType = ''
        Purchaser = ''
        purchasingAgent = ''
        for i in Selector(text=res[0]).xpath('//tbody/tr'):
            if i.xpath('.//td[1]').xpath('string(.)').extract()[0] == '采购项目名称':
                entryName = i.xpath('.//td[2]').xpath('string(.)').extract()
            if i.xpath('.//td[1]').xpath('string(.)').extract()[0] == '采购项目编号' or i.xpath('.//td[1]').xpath('string(.)').extract()[0] == '项目编号':
                entryNum = i.xpath('.//td[2]').xpath('string(.)').extract()
            if i.xpath('.//td[1]').xpath('string(.)').extract()[0] == '采购方式':
                purchasingType = i.xpath('.//td[2]').xpath('string(.)').extract()
            if i.xpath('.//td[1]').xpath('string(.)').extract()[0] == '采 购 人':
                Purchaser = i.xpath('.//td[2]').xpath('string(.)').extract()
            if i.xpath('.//td[1]').xpath('string(.)').extract()[0] == '代理机构':
                purchasingAgent = i.xpath('.//td[2]').xpath('string(.)').extract()

        if purchasingAgent:
            item['purchasingAgent'] = purchasingAgent[0]
        else:
            item['purchasingAgent'] = ''
        if entryName:
            item['entryName'] = entryName[0]
        else:
            item['entryName'] = ''
        if entryNum:
            item['entryNum'] = entryNum[0]
        else:
            item['entryNum'] = ''
        if purchasingType:
            item['purchasingType'] = purchasingType[0]
        else:
            item['purchasingType'] = ''
        if Purchaser:
            item['Purchaser'] = Purchaser[0]
        else:
            item['Purchaser'] = ''
        yield item
