from scrapy import cmdline
import time
import os

min = [
    'scrapy crawl quanguo',
    'scrapy crawl beijing',
]
# cmdline.execute(min[0].split())



# 定时任务
while True:
    print('开始执行')
    os.system(min[0])
    time.sleep(10)
