# -*- coding: utf-8 -*-
import scrapy
from qgggzy.items import QuanguoItem
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class QuanguoSpider(scrapy.Spider):
    name = 'quanguo'
    allowed_domains = ['ggzy.gov.cn']
    url = 'http://deal.ggzy.gov.cn/ds/deal/dealList.jsp'
    page = 1
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='C:\demo\PY\qgggzy\chromedriver.exe')
        super(QuanguoSpider,self).__init__()
        dispatcher.connect(self.close,signals.spider_closed)

    def close(self,spider):
        #当爬虫推出的时候关闭chrome
        print('spider closed')
        self.browser.quit()

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.header, meta={'cookiejar': 1}, callback=self.parse)

    def parse(self, response):

        yield scrapy.FormRequest(url=self.url, method='POST', meta={'cookiejar': response.meta['cookiejar']},
                                 headers=self.header,
                                 formdata={'TIMEBEGIN_SHOW': '2018-04-17', 'TIMEEND_SHOW': '2018-07-17',
                                           'TIMEBEGIN': '2018-04-17',
                                           'TIMEEND': '2018-07-17', 'DEAL_TIME': '04',
                                           'DEAL_CLASSIFY': '00', 'DEAL_STAGE': '0001', 'DEAL_PROVINCE': '0',
                                           'DEAL_CITY': '0',
                                           'DEAL_PLATFORM': '0', 'DEAL_TRADE': '0', 'isShowAll': '0',
                                           'PAGENUMBER': str(self.page), 'FINDTXT': ''},
                                 callback=self.begin_parse)

    def begin_parse(self, response):
        items = []
        pageCount = response.xpath('//div[@class="paging"]/span/text()').extract()[0][1:-1]
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
            yield scrapy.Request(url=item['url'], headers=self.header, meta={'meta': item}, callback=self.detail_parse)
            # yield SplashRequest(url=item['url'], args={'timeout', 10}, headers=self.header, meta={'meta': item},
            #                     callback=self.detail_parse)
        # 请求下一页
        # if self.page < int(pageCount):
        #     self.page += 1
        #
        # yield scrapy.FormRequest(url=self.url, method='POST',meta={'cookiejar':response.meta['cookiejar']}, headers=self.header, formdata={'TIMEBEGIN_SHOW': '2018-04-17', 'TIMEEND_SHOW': '2018-07-17', 'TIMEBEGIN': '2018-04-17',
        #        'TIMEEND': '2018-07-17', 'DEAL_TIME': '04',
        #        'DEAL_CLASSIFY': '00', 'DEAL_STAGE': '0001', 'DEAL_PROVINCE': '0', 'DEAL_CITY': '0',
        #        'DEAL_PLATFORM': '0', 'DEAL_TRADE': '0', 'isShowAll': '0', 'PAGENUMBER': str(self.page), 'FINDTXT': ''},
        #                          callback=self.begin_parse)

    def detail_parse(self, response):
        item = response.meta['meta']
        entryName = response.xpath('//div[@class="detail"]/h4[@class="h4_o"]/text()').extract()
        if entryName:
            item['entryName'] = entryName[0]
        else:
            item['entryName'] = ''
        yield item
