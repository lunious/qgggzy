# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
import pymysql
from qgggzy import settings
import os


# 全国
class QuanguoPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            port=settings.MYSQL_PORT,
            charset='utf8',
            use_unicode=False
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        # 指定目录的路径
        parentFilename = './Data/{0}'.format(item['area'])

        # 如果目录不存在，则拆创建目录
        if (not os.path.exists(parentFilename)):
            os.makedirs(parentFilename)

        if item['entryName'] != '':
            try:
                self.cursor.execute(
                    "insert into qgggjy (area,lypt,sysTime,type,entryType,entryHy,url,showUrl,entryName,entryNum) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE entryName = entryName",
                    (item['area'],
                     item['lypt'],
                     item['sysTime'],
                     item['type'],
                     item['entryType'],
                     item['entryHy'],
                     item['url'],
                     item['showUrl'],
                     item['entryName'],
                     item['entryNum'],
                     ))
                self.connect.commit()
            except Exception as error:
                logging.log(error)

            try:
                self.cursor.execute(
                    "select id from qgggjy where url = %s", item['url']
                )
                result = self.cursor.fetchone()
                fp = open(parentFilename + '/'+str(result[0]) + '.txt', 'wb')
                fp.write(item['txt'].encode('utf-8'))
                fp.close()
            except Exception as error:
                logging.log(error)

            self.connect.commit()
            return item

    def close_spider(self, spider):
        self.connect.close()
