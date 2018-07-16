# -*- coding: utf-8 -*-
import scrapy
from qgggzy.items import QuanguoItem
from scrapy.selector import Selector


class QuanguoSpider(scrapy.Spider):
    name = 'quanguo'
    allowed_domains = ['ggzy.gov.cn']
    url = 'http://deal.ggzy.gov.cn/ds/deal/dealList.jsp'
    page = 1
    heard = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }

    def start_requests(self):
        yield scrapy.FormRequest(url=self.url, method='POST', headers=self.heard,
                                 formdata={'TIMEBEGIN_SHOW': '2018-04-16', 'TIMEEND_SHOW': '2018-07-16',
                                           'TIMEBEGIN': '2018-04-16',
                                           'TIMEEND': '2018-07-16', 'DEAL_TIME': '04',
                                           'DEAL_CLASSIFY': '00', 'DEAL_STAGE': '0001', 'DEAL_PROVINCE': '0',
                                           'DEAL_CITY': '0',
                                           'DEAL_PLATFORM': '0', 'DEAL_TRADE': '0', 'isShowAll': '0',
                                           'PAGENUMBER': str(self.page), 'FINDTXT': ''},
                                 callback=self.parse,
                                 dont_filter=True)

    def parse(self, response):
        items = []
        pageCount = response.xpath('//div[@class="paging"]/span/text()').extract()[0][1:-1]
        print(pageCount)
        for each in response.xpath('//*[@id="publicl"]/div[@class="publicont"]'):
            item = QuanguoItem()
            area = each.xpath('.//p[@class="p_tw"]/span[2]/text()').extract()
            if area:
                item['area'] = area[0]
            else:
                item['area'] = ''
            lypt = each.xpath('.//p[@class="p_tw"]/span[4]/text()').extract()
            if lypt:
                item['lypt'] = lypt[0]
            else:
                item['lypt'] = ''
            sysTime = each.xpath('.//h4/span[@class="span_o"]/text()').extract()
            if sysTime:
                item['sysTime'] = sysTime[0]
            else:
                item['sysTime'] = ''
            type = each.xpath('.//p[@class="p_tw"]/span[6]/text()').extract()
            if type:
                item['type'] = type[0]
            else:
                item['type'] = ''
            entryType = each.xpath('.//p[@class="p_tw"]/span[8]/text()').extract()
            if entryType:
                item['entryType'] = entryType[0]
            else:
                item['entryType'] = ''
            entryHy = each.xpath('.//p[@class="p_tw"]/span[10]/text()').extract()
            if entryHy:
                item['entryHy'] = entryHy[0]
            else:
                item['entryHy'] = ''
            url = each.xpath('.//h4/a/@href').extract()
            if url:
                item['url'] = url[0]
            else:
                item['url'] = ''
            items.append(item)

        for item in items:
            yield scrapy.Request(url=item['url'], meta={'meta': item}, callback=self.detail_parse)

        # 请求下一页
        # if self.page < pageCount:
        #     self.page += 1
        # yield scrapy.FormRequest(url=self.url, method='POST', headers=self.heard, formdata={'TIMEBEGIN_SHOW': '2018-04-15', 'TIMEEND_SHOW': '2018-07-15', 'TIMEBEGIN': '2018-04-15',
        #        'TIMEEND': '2018-07-15', 'DEAL_TIME': '04',
        #        'DEAL_CLASSIFY': '00', 'DEAL_STAGE': '0000', 'DEAL_PROVINCE': '0', 'DEAL_CITY': '0',
        #        'DEAL_PLATFORM': '0', 'DEAL_TRADE': '0', 'isShowAll': '0', 'PAGENUMBER': str(self.page), 'FINDTXT': ''},
        #                          callback=self.parse)

    def detail_parse(self, response):
        item = response.meta['meta']
        entryName = response.xpath('//div[@class="fully"]//div[@id="div_0201"]//li/a/@title').extract()
        if entryName:
            item['entryName'] = entryName[0]
        else:
            item['entryName'] = ''
        item = response.meta['meta']
        yield item
