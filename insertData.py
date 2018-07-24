import time

from qgggzy import settings
import pymysql
import logging

connect = pymysql.connect(
    host=settings.MYSQL_HOST,
    db=settings.MYSQL_DBNAME,
    user=settings.MYSQL_USER,
    passwd=settings.MYSQL_PASSWD,
    port=settings.MYSQL_PORT,
    charset='utf8',
    use_unicode=False
)
cursor = connect.cursor()

while True:
    print('开始插入数据>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    try:
        # 公告
        cursor.execute(
            "insert into bjentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '北京' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from bjentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into tjentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '天津' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from tjentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into hbentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '河北' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from hbentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into sxentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '山西' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from sxentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into nmgentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '内蒙古' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from nmgentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into lnentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '辽宁' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from lnentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into jlentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '吉林' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from jlentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into hljentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '黑龙江' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from hljentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into shentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '上海' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from shentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into jsentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '江苏' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from jsentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into zjentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '浙江' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from zjentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into ahentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '安徽' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from ahentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into fjentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '福建' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from fjentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into jxentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '江西' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from jxentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into sdentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '山东' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from sdentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into hnentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '山东' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from sdentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into hubeientrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '湖北' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from hubeientrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into hunanentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '湖南' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from hunanentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into gdentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '广东' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from gdentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into gxentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '广西' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from gxentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into hainanentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '海南' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from hainanentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into gzentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '贵州' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from gzentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into ynentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '云南' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from ynentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into xzentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '西藏' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from xzentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into shanxientrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '陕西' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from shanxientrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into gsentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '甘肃' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from gsentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into qhentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '青海' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from qhentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into nxentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '宁夏' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from nxentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into xjentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '新疆' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from xjentrylist where entity='qgggjy')",
        )
        cursor.execute(
            "insert into btentrylist (entryName,sysTime,deadTime,type,entity,entityid,signstauts,labelExplain,lypt,entrynum,address) select entryName,sysTime,deadTime,type,'qgggjy',id,signStauts,tempLabelName,lypt,entryNum,city from qgggjy where area = '兵团' and entryType in ('采购/资审公告', '招标/资审公告', '交易公告') and id not in (select entityid from btentrylist where entity='qgggjy')",
        )
        # 公示
        cursor.execute(
            "insert into bjentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '北京' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from bjentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into tjentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '天津' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from tjentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into hbentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '河北' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hbentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into ynentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '云南' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from ynentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into sxentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '山西' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from sxentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into nmgentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '内蒙古' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from nmgentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into lnentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '辽宁' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from lnentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into jlentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '吉林' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from jlentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into hljentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '黑龙江' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hljentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into shentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '上海' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from shentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into jsentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '江苏' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from jsentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into zjentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '浙江' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from zjentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into ahentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '安徽' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from ahentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into fjentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '福建' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from fjentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into jxentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '江西' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from jxentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into sdentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '山东' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from sdentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into hnentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '河南' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hnentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into hubeientryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '湖北' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hubeientryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into hunanentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '湖南' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hunanentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into gdentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '广东' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from gdentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into gxentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '广西' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from gxentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into hainanentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '海南' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from hainanentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into gzentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '贵州' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from gzentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into xzentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '西藏' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from xzentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into shanxientryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '陕西' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from shanxientryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into gsentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '甘肃' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from gsentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into qhentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '青海' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from qhentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into nxentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '宁夏' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from nxentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into xjentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '新疆' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from xjentryjglist where entity='qgggjy')"
        )
        cursor.execute(
            "insert into btentryjglist (entryName,sysTime,type,entity,entityid,lypt,entrynum) select entryName,sysTime,type,'qgggjy',id,lypt,entryNum from qgggjy where area = '兵团' and entryType in ('交易结果公示', '中标公告', '成交公示', '交易结果') and id not in (select entityid from btentryjglist where entity='qgggjy')"
        )
        connect.commit()
        print('数据插入成功>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    except Exception as error:
        print('数据插入失败>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        logging.log(error)

    time.sleep(2)
