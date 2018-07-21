from scrapy import cmdline
import time
import os

min = [
    'scrapy crawl quanguo2',
]
# cmdline.execute(min[0].split())



# 定时任务
while True:
    print('开始执行')
    os.system(min[0])
    time.sleep(4)
