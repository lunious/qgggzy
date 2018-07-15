from scrapy import cmdline
import time
import os

min = [
    'scrapy crawl sichuan',
    'scrapy crawl quanguo',
]
# cmdline.execute(min[0].split())


# 定时任务
while True:
    print('开始执行>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    os.system(min[0])
    time.sleep(3600)  # 每隔1小时运行一次 1*60*60=3600s