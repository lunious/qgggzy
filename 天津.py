from scrapy import cmdline
import time
import os

min = [
    'scrapy crawl tianjin',
]

while True:
    print('开始执行')
    cmdline.execute(min[0].split())
    time.sleep(10)

