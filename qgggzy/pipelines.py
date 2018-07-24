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

id_name = {
    '2': '施工',
    '3': '监理',
    '4': '勘察',
    '5': '设计',
    '6': '政府采购',
    '8': '房建施工',
    '9': '市政施工',
    '10': '公路施工',
    '11': '水利施工',
    '12': '房建监理',
    '13': '市政监理',
    '14': '公路监理',
    '15': '水利监理',
    '16': '造价审计',
    '17': 'EPC',
    '18': 'PPP',
    '19': '装修',
    '20': '咨询服务',
    '21': '地质灾害',
    '22': '电梯',
    '23': 'IT',
    '24': '医院采购',
    '25': '学校采购',
    '26': '机关采购',
}

keyWord_id = {
    '施工总承包 专业承包 安全生产许可证 承装（修 试）电力设施许可证 养护': '2',
    '监理综合  建筑工程监理 市政公用工程监理 公路工程监理 水利水电工程监理 机电安装工程监理  电力工程监理 农林工程监理 铁路工程监理 冶炼工程监理 矿山工程监理 化工石油工程监理 港口与航道工程监理  航天航空工程监理  通信工程监理  专项监理   水运工程监理   水利工程施工监理  水土保持工程施工监理  设备制造监理  环境保护监理  人防工程监理  人防监理': '3',
    '岩土工程 工程勘察 地质勘察 工程测量': '4',
    '工程设计 行业设计 专业设计 专项设计': '5',
    '政府采购': '6',
    '房屋建筑施工总承包 房屋建筑总承包 建筑工程施工总承 钢结构工程专业承包 建筑装修装饰工程专业承包 建筑幕墙工程专业承包 建筑机电安装工程专业承包 消防设施工程专业承包 地基基础工程专业承包  古建筑工程专业承包 特种工程专业承包  模板脚手架专业承包   防水防腐保温工程专业承包  电子与智能化工程专业承包 起重设备安装工程专业承包': '8',
    '市政公用工程总承包 市政公用工程施工总承包 城市及道路照明工程专业承包 环保工程专业承包': '9',
    '公路工程施工总承包 公路交通工程专业承包  桥梁工程专业承包  隧道工程专业承包  公路路面工程专业承包  公路路基工程专业承包 ': '10',
    '水利水电工程施工总承包 水工金属结构制作与安装工程专业承包 水利水电机电安装工程专业承包 河湖整治工程专业承包 ': '11',
    '房屋建筑监理  建筑工程监理  人防工程监理  人防监理': '12',
    '市政公用工程监理 市政工程监理': '13',
    '公路工程监理 特殊独立大桥专项监理 公路机电工程专项监理 特殊独立隧道专项监理': '14',
    '水利水电工程监理 水利工程施工监理 水土保持工程施工监理   机电及金属结构设备制造监理  水利工程建设环境保护监理': '15',
    '工程造价 工程造价咨询': '16',
    'epc 工程总承包 设计施工总承包（设计） 设计施工总承包（施工总承包） 勘察设计施工总承包（勘察） 勘察设计施工总承包（设计） 勘察设计施工总承包（施工总承包） 勘察设计设备采购施工总承包（勘察） 勘察设计设备采购施工总承包（设计） 勘察设计设备采购施工总承包（设备采购） 勘察设计设备采购施工总承包（施工总承包）': '17',
    'PPP  政府和社会资本': '18',
    '装修 装饰 ': '19',
    '工程咨询': '20',
    '地质灾害 山洪治理 滑坡治理': '21',
    '特种设备安装维修许可证（电梯）': '22',
    '软件开发 软件服务': '23',
    '医院 卫生院 疗养院 门诊部 诊所 卫生所 卫生室 急救站 急救中心 康复中心 保健院 卫生管理所': '24',
    '学校 大学 学院 大专 党校 培训中心 高职 高中 中专 职高 普高 中学 小学 幼儿园': '25',
    '厅 局 队 办公室 站 中心 委员会 研究室 领导小组 指挥部 法院 人民政府 检察院 乡': '26',
}

nameWord_id = {
    '施工 施工总承包 专业承包 设计与施工 工程总承包 epc 展览工程 养护': '2',
    '监理': '3',
    '勘察 勘查 勘测': '4',
    '设计 设计与施工 epc': '5',
    '政府采购': '6',
    '绿化 景观 亮化': '9',
    '土地整理 农田 灌溉 农业': '11',
    '工程造价 工程造价咨询 概算 预算 结算 审计 决算 工程量清单编制 工程量清单审核': '16',
    'epc 工程总承包 设计施工总承包（设计） 设计施工总承包（施工总承包） 勘察设计施工总承包（勘察） 勘察设计施工总承包（设计） 勘察设计施工总承包（施工总承包） 勘察设计设备采购施工总承包（勘察） 勘察设计设备采购施工总承包（设计） 勘察设计设备采购施工总承包（设备采购） 勘察设计设备采购施工总承包（施工总承包）': '17',
    'PPP 政府和社会资本': '18',
    '装饰 装修': '19',
    '可研 工程咨询 图审 审图 水保 规划 检测 监测 评估': '20',
    '地质灾害 山洪治理 崩塌 滑坡 泥石流 地裂缝 水土流失 沙漠化 沼泽化 盐碱化': '21',
    '电梯 客梯 货梯 扶梯 升降机': '22',
    '计算机 服务器 网络 通讯 工作站 小型机 路由器 防火墙 交换机 集线器 数据 集成 主机 软件 智能化 安防 机房 主板 局域网 网卡 网桥 网关 中继器 CPU 主板 显卡 内存 硬盘': '23',
    '医院 卫生院 疗养院 门诊部 诊所 卫生所 卫生室 急救站 急救中心 康复中心 保健院 卫生管理所': '24',
    '学校 大学 学院 大专 党校 培训中心 高职 高中 中专 职高 普高 中学 小学 幼儿园': '25',
    '厅 局 队 办公室 站 中心 委员会 研究室 领导小组 指挥部 法院': '26',

}


new_keyWord_id = {v: k for k, v in keyWord_id.items()}
new_nameWord_id = {v: k for k, v in nameWord_id.items()}


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

        id = ''
        name = ''

        # 指定目录的路径
        parentFilename = './Data/{0}'.format(item['pcode'])

        # 如果目录不存在，则创建目录
        if (not os.path.exists(parentFilename)):
            os.makedirs(parentFilename)

        for i in new_nameWord_id.keys():
            for j in new_nameWord_id.get(i).split():
                if j in item['entryName']:
                    if i not in id:
                        id += i + ','

        if id.endswith(','):
            for m in id[:-1].split(','):
                if id_name.get(m) not in name:
                    name += id_name.get(m) + ','

        for n in new_keyWord_id.keys():
            for o in new_keyWord_id.get(n).split():
                if o in item['txt']:
                    if n not in id:
                        id += n + ','

        if id.endswith(','):
            for q in id[:-1].split(','):
                if id_name.get(q) not in name:
                    name += id_name.get(q) + ','
        if id:
            item['label'] = id[:-1]
        else:
            item['label'] = ''
        if name:
            item['tempLabelName'] = name[:-1]
        else:
            item['tempLabelName'] = ''

        if item['entryName'] != '':
            try:
                self.cursor.execute(
                    "insert into qgggjy (area,city,lypt,sysTime,type,entryType,entryHy,url,showUrl,entryName,entryNum,label,tempLabelName) value(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE entryName = entryName",
                    (item['area'],
                     item['city'],
                     item['lypt'],
                     item['sysTime'],
                     item['type'],
                     item['entryType'],
                     item['entryHy'],
                     item['url'],
                     item['showUrl'],
                     item['entryName'],
                     item['entryNum'],
                     item['label'],
                     item['tempLabelName'],
                     ))
                self.cursor.execute(
                    "select id from qgggjy where url = %s", item['url']
                )
                result = self.cursor.fetchone()
                fp = open(parentFilename + '/' + str(result[0]) + '.txt', 'wb')
                fp.write(item['txt'].encode('utf-8'))
                fp.close()
                # 公告
                self.cursor.execute(
                    "insert into bjentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '北京' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from bjentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into tjentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '天津' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from tjentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into hbentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '河北' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from hbentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into sxentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '山西' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from sxentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into nmgentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '内蒙古' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from nmgentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into lnentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '辽宁' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from lnentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into jlentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '吉林' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from jlentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into hljentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '黑龙江' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from hljentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into shentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '上海' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from shentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into jsentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '江苏' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from jsentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into zjentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '浙江' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from zjentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into ahentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '安徽' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from ahentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into fjentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '福建' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from fjentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into jxentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '江西' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from jxentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into sdentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '山东' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from sdentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into hnentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '山东' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from sdentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into hubeientrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '湖北' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from hubeientrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into hunanentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '湖南' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from hunanentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into gdentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '广东' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from gdentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into gxentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '广西' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from gxentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into hainanentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '海南' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from hainanentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into gzentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '贵州' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from gzentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into ynentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '云南' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from ynentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into xzentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '西藏' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from xzentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into shanxientrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '陕西' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from shanxientrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into gsentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '甘肃' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from gsentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into qhentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '青海' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from qhentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into nxentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '宁夏' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from nxentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into xjentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '新疆' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from xjentrylist where entity='qgggjy')",
                )
                self.cursor.execute(
                    "insert into btentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '兵团' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from btentrylist where entity='qgggjy')",
                )
                # 公示
                self.cursor.execute(
                    "insert into bjentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '北京' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from bjentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into tjentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '天津' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from tjentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into hbentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '河北' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hbentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into ynentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '云南' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from ynentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into sxentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '山西' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from sxentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into nmgentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '内蒙古' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from nmgentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into lnentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '辽宁' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from lnentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into jlentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '吉林' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from jlentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into hljentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '黑龙江' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hljentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into shentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '上海' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from shentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into jsentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '江苏' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from jsentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into zjentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '浙江' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from zjentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into ahentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '安徽' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from ahentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into fjentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '福建' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from fjentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into jxentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '江西' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from jxentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into sdentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '山东' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from sdentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into hnentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '河南' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hnentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into hubeientryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '湖北' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hubeientryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into hunanentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '湖南' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hunanentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into gdentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '广东' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from gdentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into gxentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '广西' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from gxentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into hainanentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '海南' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hainanentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into gzentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '贵州' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from gzentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into xzentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '西藏' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from xzentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into shanxientryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '陕西' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from shanxientryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into gsentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '甘肃' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from gsentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into qhentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '青海' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from qhentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into nxentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '宁夏' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from nxentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into xjentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '新疆' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from xjentryjglist where entity='qgggjy')"
                )
                self.cursor.execute(
                    "insert into btentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '兵团' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from btentryjglist where entity='qgggjy')"
                )
                self.connect.commit()
            except Exception as error:
                logging.log(error)
            return item

    def close_spider(self, spider):
        self.connect.close()
