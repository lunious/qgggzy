# -*- coding: utf-8 -*-
import scrapy
from qgggzy.items import QuanguoItem
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from selenium.webdriver.support.ui import WebDriverWait
import random


class QuanguoSpider(scrapy.Spider):
    name = 'quanguo'
    allowed_domains = ['ggzy.gov.cn']
    url = 'http://deal.ggzy.gov.cn/ds/deal/dealList.jsp'
    page = 1

    agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]

    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(agent),
    }

    def __init__(self):
        # 从settings.py中获取设置参数
        self.mySetting = get_project_settings()
        self.timeout = self.mySetting['SELENIUM_TIMEOUT']
        self.isLoadImage = self.mySetting['LOAD_IMAGE']
        self.windowHeight = self.mySetting['WINDOW_HEIGHT']
        self.windowWidth = self.mySetting['windowWidth']
        # 初始化chrome对象
        self.browser = webdriver.Chrome(executable_path='C:\demo\PY\qgggzy\chromedriver.exe')
        if self.windowHeight and self.windowWidth:
            self.browser.set_window_size(600, 600)
        self.browser.set_page_load_timeout(self.timeout)        # 页面加载超时时间
        self.wait = WebDriverWait(self.browser, 60)             # 指定元素加载超时时间
        super(QuanguoSpider, self).__init__()
        dispatcher.connect(self.close, signals.spider_closed)

    def close(self, spider):
        # 当爬虫推出的时候关闭chrome
        print('spider closed')
        self.browser.quit()

    def start_requests(self):
        yield scrapy.FormRequest(url=self.url, method='POST', meta={'usedSelenium': False},
                                 headers=self.header,
                                 formdata={'TIMEBEGIN_SHOW': '2018-04-19', 'TIMEEND_SHOW': '2018-07-19',
                                           'TIMEBEGIN': '2018-04-19',
                                           'TIMEEND': '2018-07-19', 'DEAL_TIME': '03',
                                           'DEAL_CLASSIFY': '00', 'DEAL_STAGE': '0000', 'DEAL_PROVINCE': '0',
                                           'DEAL_CITY': '0',
                                           'DEAL_PLATFORM': '0', 'DEAL_TRADE': '0', 'isShowAll': '0',
                                           'PAGENUMBER': str(self.page), 'FINDTXT': ''},
                                 callback=self.parse, dont_filter=True)

    def parse(self, response):
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
        if self.page < int(pageCount):
            self.page += 1


        yield scrapy.FormRequest(url=self.url, method='POST',
                                 meta={'usedSelenium': False},
                                 headers=self.header,
                                 formdata={'TIMEBEGIN_SHOW': '2018-04-19', 'TIMEEND_SHOW': '2018-07-19',
                                           'TIMEBEGIN': '2018-04-19',
                                           'TIMEEND': '2018-07-19', 'DEAL_TIME': '03',
                                           'DEAL_CLASSIFY': '00', 'DEAL_STAGE': '0000', 'DEAL_PROVINCE': '0',
                                           'DEAL_CITY': '0',
                                           'DEAL_PLATFORM': '0', 'DEAL_TRADE': '0', 'isShowAll': '0',
                                           'PAGENUMBER': str(self.page), 'FINDTXT': ''}, callback=self.parse, dont_filter=True)

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
            yield scrapy.Request(url=item['showUrl'], headers=self.header, meta={'meta_2': item, 'usedSelenium': True},
                                 callback=self.txt_parse)

    def txt_parse(self, response):
        item = response.meta['meta_2']

        mHtml = response.xpath('//*[@id="mycontent"]/*').extract()

        if mHtml:
            item['txt'] = mHtml[0]
        else:
            item['txt'] = response.body.decode("utf-8")
        yield item
