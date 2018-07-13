# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
import pymysql
from scggzy import settings

# 全国公共交易网（四川）
class ScggzyPipeline(object):

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
                self.cursor.execute("Insert into entryjglist(entryName,sysTime,type,entity,entityId) select reportTitle,sysTime,'工程中标结果','sggjyzbjg',id from sggjyzbjg where id not in(select entityId from entryjglist where  entity ='sggjyzbjg' ) ")
                self.cursor.execute("update sggjy set sggjyzbjgId=(select id from sggjyzbjg  where sggjyzbjg.url = sggjy.url)")
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
