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


# 四川省
class SichuanPipeline(object):

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

        if item['entryOwner'] != '':
            try:
                self.cursor.execute(
                    "insert into sggjyzbjg (reportTitle,sysTime,url,entryName,entryOwner,ownerTel,tenderee,tendereeTel,biddingAgency,biddingAgencTel,placeAddress,placeTime,publicityPeriod,bigPrice,oneTree,twoTree,threeTree,treeCount) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE reportTitle = reportTitle",
                    (item['reportTitle'],
                     item['sysTime'],
                     item['url'],
                     item['entryName'],
                     item['entryOwner'],
                     item['ownerTel'],
                     item['tenderee'],
                     item['tendereeTel'],
                     item['biddingAgency'],
                     item['biddingAgencTel'],
                     item['placeAddress'],
                     item['placeTime'],
                     item['publicityPeriod'],
                     item['bigPrice'],
                     item['oneTree'],
                     item['twoTree'],
                     item['threeTree'],
                     item['treeCount'],
                     ))
                self.cursor.execute(
                    "Insert into entryjglist(entryName,sysTime,type,entity,entityId) select reportTitle,sysTime,'工程中标结果','sggjyzbjg',id from sggjyzbjg where id not in(select entityId from entryjglist where  entity ='sggjyzbjg' ) ")
                self.cursor.execute(
                    "update sggjy set sggjyzbjgId=(select id from sggjyzbjg  where sggjyzbjg.url = sggjy.url)")
                self.connect.commit()
            except Exception as error:
                logging.log(error)
            # try:
            # self.cursor.execute("update sggjy set sggjyzbjgId=(select id from sggjyzbjg  where sggjyzbjg.url = sggjy.url)")
            # self.cursor.execute("select sggjyzbjgId from sggjy where url = %s", item['url'])
            # result = self.cursor.fetchone()
            # if result == None:
            #     self.cursor.execute("update sggjy set sggjyzbjgId=(select id from sggjyzbjg  where sggjyzbjg.url = sggjy.url)")
            # else:
            #     print(result[0])
            # self.connect.commit()
            # except Exception as error:
            #     logging.log(error)
            return item

    def close_spider(self, spider):
        self.connect.close()


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
        parentFilename = './Data/'

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
                    "select id from qgggjy where url = %s",item['url']
                )
                result = self.cursor.fetchone()
                fp = open(parentFilename + str(result[0]) + '.txt', 'wb')
                fp.write(item['txt'].encode('utf-8'))
                fp.close()
            except Exception as error:
                logging.log(error)

            self.connect.commit()
            return item

    def close_spider(self, spider):
        self.connect.close()


