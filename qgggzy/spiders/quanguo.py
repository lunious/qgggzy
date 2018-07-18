# -*- coding: utf-8 -*-
import scrapy
from qgggzy.items import QuanguoItem
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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
    }

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='C:\demo\PY\qgggzy\chromedriver.exe')
        super(QuanguoSpider, self).__init__()
        dispatcher.connect(self.close, signals.spider_closed)

    def close(self, spider):
        # 当爬虫推出的时候关闭chrome
        print('spider closed')
        self.browser.quit()

    def start_requests(self):
        yield scrapy.Request(url=self.url, headers=self.header, meta={'usedSelenium': True}, callback=self.parse)

    def parse(self, response):

        yield scrapy.FormRequest(url=self.url, method='POST', meta={'usedSelenium': True},
                                 headers=self.header,
                                 formdata={'TIMEBEGIN_SHOW': '2018-04-18', 'TIMEEND_SHOW': '2018-07-18',
                                           'TIMEBEGIN': '2018-04-18',
                                           'TIMEEND': '2018-07-18', 'DEAL_TIME': '03',
                                           'DEAL_CLASSIFY': '00', 'DEAL_STAGE': '0001', 'DEAL_PROVINCE': '440000',
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
                item['showUrl'] = url[0].replace('/a/', '/b/')
            else:
                item['url'] = ''
                item['showUrl'] = ''
            items.append(item)
        for item in items:
            yield scrapy.Request(url=item['url'], headers=self.header, meta={'meta_1': item, 'usedSelenium': True},
                                 callback=self.detail_parse)

        # 下一页
        # if self.page < int(pageCount):
        #     self.page += 1
        #
        # yield scrapy.FormRequest(url=self.url, method='POST',meta={'cookiejar':response.meta['cookiejar'],'usedSelenium': True}, headers=self.header,
        #                          formdata={'TIMEBEGIN_SHOW': '2018-04-18', 'TIMEEND_SHOW': '2018-07-18',
        #                                    'TIMEBEGIN': '2018-04-18',
        #                                    'TIMEEND': '2018-07-18', 'DEAL_TIME': '03',
        #                                    'DEAL_CLASSIFY': '00', 'DEAL_STAGE': '0001', 'DEAL_PROVINCE': '440000',
        #                                    'DEAL_CITY': '0',
        #                                    'DEAL_PLATFORM': '0', 'DEAL_TRADE': '0', 'isShowAll': '0',
        #                                    'PAGENUMBER': str(self.page), 'FINDTXT': ''},
        #                          callback=self.begin_parse)

    def detail_parse(self, response):
        items = []
        item = response.meta['meta_1']
        entryName = response.xpath('//div[@class="fully"]/h4[@class="h4_o"]/text()').extract()
        entryNum = response.xpath('//div[@class="fully"]/p[@class="p_o"]/span[1]/text()').extract()
        if entryName:
            item['entryName'] = entryName[0]
        else:
            item['entryName'] = ''
        if entryNum:
            item['entryNum'] = entryNum[0][7:]
        else:
            item['entryNum'] = ''

        items.append(item)

        for item in items:
            yield scrapy.Request(url=item['showUrl'], headers=self.header, meta={'meta_2': item,'usedSelenium': True},
                                 callback=self.txt_parse)

    def txt_parse(self, response):
        item = response.meta['meta_2']

        mHtml = response.xpath('//*[@id="mycontent"]/*').extract()

        if mHtml:
            item['txt'] = mHtml[0]
        else:
            item['txt'] = response.body.decode("utf-8")
        yield item
