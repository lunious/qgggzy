# -*- coding: utf-8 -*-
import scrapy
from qgggzy.items import QuanguoItem
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


class QuanguoSpider(scrapy.Spider):
    name = 'beijing'
    allowed_domains = ['ggzy.gov.cn']
    url = 'http://deal.ggzy.gov.cn/ds/deal/dealList.jsp'
    page = 1

    pcodeDic = {'北京': '110000', '天津': '120000', '河北': '130000', '山西': '140000', '内蒙古': '150000', '辽宁': '210000',
                '吉林': '220000', '黑龙江': '230000',
                '上海': '310000', '江苏': '320000', '浙江': '330000', '安徽': '340000', '福建': '350000', '江西': '360000',
                '山东': '370000', '广东': '440000',
                '广西': '450000', '海南': '460000', '河南': '410000', '湖北': '420000', '湖南': '430000', '重庆': '500000',
                '四川': '510000', '贵州': '520000',
                '云南': '530000', '西藏': '540000', '陕西': '610000', '甘肃': '620000', '青海': '630000', '宁夏': '640000',
                '新疆': '650000', '兵团': '650000', }

    pcityDic = {
        '成都市': '成都',
        '自贡市': '自贡',
        '攀枝花市': '攀枝花',
        '泸州市': '泸州',
        '德阳市': '德阳',
        '绵阳市': '绵阳',
        '广元市': '广元',
        '遂宁市': '遂宁',
        '内江市': '内江',
        '乐山市': '乐山',
        '南充市': '南充',
        '眉山市': '眉山',
        '宜宾市': '宜宾',
        '广安市': '广安',
        '达州市': '达州',
        '雅安市': '雅安',
        '巴中市': '巴中',
        '资阳市': '资阳',
        '阿坝州': '阿坝',
        '甘孜州': '甘孜',
        '凉山州': '凉山',
        '渝中区': '渝中',
        '大渡口区': '大渡口',
        '江北区': '江北',
        '沙坪坝区': '沙坪坝',
        '九龙坡区': '九龙坡 高新区',
        '南岸区': '南岸 经开',
        '北碚区': '北碚',
        '綦江区': '綦江',
        '双桥区': '双桥',
        '渝北区': '渝北',
        '巴南区': '巴南',
        '万州区': '万州',
        '涪陵区': '涪陵',
        '黔江区': '黔江',
        '长寿区': '长寿',
        '江津区': '江津',
        '合川区': '合川',
        '永川区': '永川',
        '南川区': '南川',
        '綦江县': '綦江',
        '潼南县': '潼南',
        '铜梁县': '铜梁',
        '大足县': '大足',
        '荣昌县': '荣昌',
        '璧山县': '璧山',
        '梁平县': '梁平',
        '城口县': '城口',
        '丰都县': '丰都',
        '垫江县': '垫江',
        '武隆县': '武隆',
        '忠县': '忠县',
        '开县': '开县 开州',
        '云阳县': '云阳',
        '奉节县': '奉节',
        '巫山县': '巫山',
        '巫溪县': '巫溪',
        '石柱县': '石柱土家族自治县 石柱县',
        '秀山县': '秀山土家族苗族自治县 秀山县',
        '酉阳县': '酉阳土家族苗族自治县 酉阳县',
        '彭水县': '彭水苗族土家族自治县 彭水县',
        '万盛区': '万盛',
        '两江新区': '两江新区',
        '东城区': '东城',
        '西城区': '西城',
        '朝阳区': '朝阳',
        '丰台区': '丰台',
        '石景山': '石景',
        '海淀区': '海淀',
        '门头沟': '门头',
        '房山区': '房山',
        '通州区': '通州',
        '顺义区': '顺义',
        '昌平区': '昌平',
        '大兴区': '大兴',
        '怀柔区': '怀柔',
        '平谷区': '平谷',
        '密云县': '密云',
        '延庆县': '延庆',
        '和平区': '和平',
        '河东区': '河东',
        '河西区': '河西',
        '南开区': '南开',
        '河北区': '河北',
        '红桥区': '红桥',
        '东丽区': '东丽',
        '西青区': '西青',
        '津南区': '津南',
        '北辰区': '北辰',
        '武清区': '武清',
        '宝坻区': '宝坻',
        '滨海新': '滨海',
        '宁河县': '宁河',
        '静海县': '静海',
        '蓟县': '蓟县',
        '石家庄市': '石家庄',
        '唐山市': '唐山',
        '秦皇岛市': '秦皇岛',
        '邯郸市': '邯郸',
        '邢台市': '邢台',
        '保定市': '保定',
        '张家口市': '张家口',
        '承德市': '承德',
        '沧州市': '沧州',
        '廊坊市': '廊坊',
        '衡水市': '衡水',
        '太原市': '太原',
        '大同市': '大同',
        '阳泉市': '阳泉',
        '长治市': '长治',
        '晋城市': '晋城',
        '朔州市': '朔州',
        '晋中市': '晋中',
        '运城市': '运城',
        '忻州市': '忻州',
        '临汾市': '临汾',
        '吕梁市': '吕梁',
        '呼和浩特市': '呼和浩特',
        '包头市': '包头',
        '乌海市': '乌海',
        '赤峰市': '赤峰',
        '通辽市': '通辽',
        '鄂尔多斯市': '鄂尔多斯',
        '呼伦贝尔市': '呼伦贝尔',
        '巴彦淖尔市': '巴彦淖尔',
        '乌兰察布市': '乌兰察布',
        '兴安盟': '兴安',
        '锡林郭勒盟': '锡林郭勒',
        '阿拉善盟': '阿拉善',
        '沈阳市': '沈阳',
        '大连市': '大连',
        '鞍山市': '鞍山',
        '抚顺市': '抚顺',
        '本溪市': '本溪',
        '丹东市': '丹东',
        '锦州市': '锦州',
        '营口市': '营口',
        '阜新市': '阜新',
        '辽阳市': '辽阳',
        '盘锦市': '盘锦',
        '铁岭市': '铁岭',
        '朝阳市': '朝阳',
        '葫芦岛市': '葫芦岛',
        '长春市': '长春',
        '吉林市': '吉林',
        '四平市': '四平',
        '辽源市': '辽源',
        '通化市': '通化',
        '白山市': '白山',
        '松原市': '松原',
        '白城市': '白城',
        '延边朝鲜族自治州': '延边',
        '哈尔滨市': '哈尔滨',
        '齐齐哈尔市': '齐齐哈尔',
        '鸡西市': '鸡西',
        '鹤岗市': '鹤岗',
        '双鸭山市': '双鸭山',
        '大庆市': '大庆',
        '伊春市': '伊春',
        '佳木斯市': '佳木斯',
        '七台河市': '七台河',
        '牡丹江': '牡丹江',
        '黑河市': '黑河',
        '绥化市': '绥化',
        '大兴安岭地区': '大兴安岭',
        '黄浦区': '黄浦',
        '徐汇区': '徐汇',
        '长宁区': '长宁',
        '静安区': '静安',
        '普陀区': '普陀',
        '闸北区': '闸北',
        '虹口区': '虹口',
        '杨浦区': '杨浦',
        '闵行区': '闵行',
        '宝山区': '宝山',
        '嘉定区': '嘉定',
        '浦东新区': '浦东',
        '金山区': '金山',
        '松江区': '松江',
        '青浦区': '青浦',
        '奉贤区': '奉贤',
        '崇明县': '崇明',
        '南京市': '南京',
        '无锡市': '无锡',
        '徐州市': '徐州',
        '常州市': '常州',
        '苏州市': '苏州',
        '南通市': '南通',
        '连云港市': '连云港',
        '淮安市': '淮安',
        '盐城市': '盐城',
        '扬州市': '扬州',
        '镇江市': '镇江',
        '泰州市': '泰州',
        '宿迁市': '宿迁',
        '杭州市': '杭州',
        '宁波市': '宁波',
        '温州市': '温州',
        '嘉兴市': '嘉兴',
        '湖州市': '湖州',
        '绍兴市': '绍兴',
        '金华市': '金华',
        '衢州市': '衢州',
        '舟山市': '舟山',
        '台州市': '台州',
        '丽水市': '丽水',
        '合肥市': '合肥',
        '芜湖市': '芜湖',
        '蚌埠市': '蚌埠',
        '淮南市': '淮南',
        '马鞍山市': '马鞍山',
        '淮北市': '淮北',
        '铜陵市': '铜陵',
        '安庆市': '安庆',
        '黄山市': '黄山',
        '滁州市': '滁州',
        '阜阳市': '阜阳',
        '宿州市': '宿州',
        '六安市': '六安',
        '亳州市': '亳州',
        '池州市': '池州',
        '宣城市': '宣城',
        '福州市': '福州',
        '厦门市': '厦门',
        '莆田市': '莆田',
        '三明市': '三明',
        '泉州市': '泉州',
        '漳州市': '漳州',
        '南平市': '南平',
        '龙岩市': '龙岩',
        '宁德市': '宁德',
        '南昌市': '南昌',
        '景德镇市': '景德',
        '萍乡市': '萍乡',
        '九江市': '九江',
        '新余市': '新余',
        '鹰潭市': '鹰潭',
        '赣州市': '赣州',
        '吉安市': '吉安',
        '宜春市': '宜春',
        '抚州市': '抚州',
        '上饶市': '上饶',
        '济南市': '济南',
        '青岛市': '青岛',
        '淄博市': '淄博',
        '枣庄市': '枣庄',
        '东营市': '东营',
        '烟台市': '烟台',
        '潍坊市': '潍坊',
        '济宁市': '济宁',
        '泰安市': '泰安',
        '威海市': '威海',
        '日照市': '日照',
        '莱芜市': '莱芜',
        '临沂市': '临沂',
        '德州市': '德州',
        '聊城市': '聊城',
        '滨州市': '滨州',
        '菏泽市': '菏泽',
        '郑州市': '郑州',
        '开封市': '开封',
        '洛阳市': '洛阳',
        '平顶山市': '平顶山',
        '安阳市': '安阳',
        '鹤壁市': '鹤壁',
        '新乡市': '新乡',
        '焦作市': '焦作',
        '濮阳市': '濮阳',
        '许昌市': '许昌',
        '漯河市': '漯河',
        '三门峡市': '三门峡',
        '南阳市': '南阳',
        '商丘市': '商丘',
        '信阳市': '信阳',
        '周口市': '周口',
        '驻马店市': '驻马',
        '济源市': '济源',
        '武汉市': '武汉',
        '黄石市': '黄石',
        '十堰市': '十堰',
        '宜昌市': '宜昌',
        '襄阳市': '襄阳',
        '鄂州市': '鄂州',
        '荆门市': '荆门',
        '孝感市': '孝感',
        '荆州市': '荆州',
        '黄冈市': '黄冈',
        '咸宁市': '咸宁',
        '随州市': '随州',
        '恩施土家族苗族自治州': '恩施',
        '仙桃市': '仙桃',
        '潜江市': '潜江',
        '天门市': '天门',
        '神农架林区': '神农架',
        '长沙市': '长沙',
        '株洲市': '株洲',
        '湘潭市': '湘潭',
        '衡阳市': '衡阳',
        '邵阳市': '邵阳',
        '岳阳市': '岳阳',
        '常德市': '常德',
        '张家界市': '张家界',
        '益阳市': '益阳',
        '郴州市': '郴州',
        '永州市': '永州',
        '怀化市': '怀化',
        '娄底市': '娄底',
        '湘西土家族苗族自治州': '湘西',
        '广州市': '广州',
        '韶关市': '韶关',
        '深圳市': '深圳',
        '珠海市': '珠海',
        '汕头市': '汕头',
        '佛山市': '佛山',
        '江门市': '江门',
        '湛江市': '湛江',
        '茂名市': '茂名',
        '肇庆市': '肇庆',
        '惠州市': '惠州',
        '梅州市': '梅州',
        '汕尾市': '汕尾',
        '河源市': '河源',
        '阳江市': '阳江',
        '清远市': '清远',
        '东莞市': '东莞',
        '中山市': '中山',
        '潮州市': '潮州',
        '揭阳市': '揭阳',
        '云浮市': '云浮',
        '南宁市': '南宁',
        '柳州市': '柳州',
        '桂林市': '桂林',
        '梧州市': '梧州',
        '北海市': '北海',
        '防城港市': '防城',
        '钦州市': '钦州',
        '贵港市': '贵港',
        '玉林市': '玉林',
        '百色市': '百色',
        '贺州市': '贺州',
        '河池市': '河池',
        '来宾市': '来宾',
        '崇左市': '崇左',
        '海口市': '海口',
        '三亚市': '三亚',
        '三沙市': '三沙',
        '五指山市': '五指山',
        '琼海市': '琼海',
        '儋州市': '儋州',
        '文昌市': '文昌',
        '万宁市': '万宁',
        '东方市': '东方',
        '定安县': '定安',
        '屯昌县': '屯昌',
        '澄迈县': '澄迈',
        '临高县': '临高',
        '白沙黎族自治县': '白沙',
        '昌江黎族自治县': '昌江',
        '乐东黎族自治县': '乐东',
        '陵水黎族自治县': '陵水',
        '保亭黎族苗族自治县': '保亭',
        '琼中黎族苗族自治县': '琼中',
        '贵阳市': '贵阳',
        '六盘水市': '六盘水',
        '遵义市': '遵义',
        '安顺市': '安顺',
        '毕节市': '毕节',
        '铜仁市': '铜仁',
        '黔西南布依族苗族自治州': '黔西',
        '黔东南苗族侗族自治州': '黔东',
        '黔南布依族苗族自治州': '黔南',
        '昆明市': '昆明',
        '曲靖市': '曲靖',
        '玉溪市': '玉溪',
        '保山市': '保山',
        '昭通市': '昭通',
        '丽江市': '丽江',
        '普洱市': '普洱',
        '临沧市': '临沧',
        '楚雄彝族自治州': '楚雄',
        '红河哈尼族彝族自治州': '红河',
        '文山壮族苗族自治州': '文山',
        '西双版纳傣族自治州': '西双版纳',
        '大理白族自治州': '大理',
        '德宏傣族景颇族自治州': '德宏',
        '怒江傈僳族自治州': '怒江',
        '迪庆藏族自治州': '迪庆',
        '拉萨市': '拉萨',
        '昌都地区': '昌都',
        '山南地区': '山南',
        '日喀则地区': '日喀则',
        '那曲地区': '那曲',
        '阿里地区': '阿里',
        '林芝地区': '林芝',
        '西安市': '西安',
        '铜川市': '铜川',
        '宝鸡市': '宝鸡',
        '咸阳市': '咸阳',
        '渭南市': '渭南',
        '延安市': '延安',
        '汉中市': '汉中',
        '榆林市': '榆林',
        '安康市': '安康',
        '商洛市': '商洛',
        '兰州市': '兰州',
        '嘉峪关市': '嘉峪关',
        '金昌市': '金昌',
        '白银市': '白银',
        '天水市': '天水',
        '武威市': '武威',
        '张掖市': '张掖',
        '平凉市': '平凉',
        '酒泉市': '酒泉',
        '庆阳市': '庆阳',
        '定西市': '定西',
        '陇南市': '陇南',
        '临夏回族自治州': '临夏',
        '甘南藏族自治州': '甘南',
        '西宁市': '西宁',
        '海东市': '海东',
        '海北藏族自治州': '海北',
        '黄南藏族自治州': '黄南',
        '海南藏族自治州': '海南',
        '果洛藏族自治州': '果洛',
        '玉树藏族自治州': '玉树',
        '海西蒙古族藏族自治州': '海西',
        '银川市': '银川',
        '石嘴山市': '石嘴山',
        '吴忠市': '吴忠',
        '固原市': '固原',
        '中卫市': '中卫',
        '乌鲁木齐市': '乌鲁木齐',
        '克拉玛依市': '克拉玛依',
        '吐鲁番地区': '吐鲁番',
        '哈密地区': '哈密',
        '昌吉回族自治州': '昌吉',
        '博尔塔拉蒙古自治州': '博尔塔拉',
        '巴音郭楞蒙古自治州': '巴音郭楞',
        '阿克苏地区': '阿克苏',
        '克孜勒苏柯尔克孜自治州': '克孜勒苏柯尔克孜',
        '喀什地区': '喀什',
        '和田地区': '和田',
        '伊犁哈萨克自治州': '伊犁哈萨克',
        '塔城地区': '塔城地',
        '阿勒泰地区': '阿勒泰地',
        '石河子市': '石河子',
        '阿拉尔市': '阿拉尔',
        '图木舒克市': '图木舒克',
        '五家渠市': '五家渠',
    }

    new_pcityDic = {v: k for k, v in pcityDic.items()}


    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
    }

    def __init__(self):
        # 从settings.py中获取设置参数
        options = Options()
        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                }
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument('-headless')  # 无头参数
        self.mySetting = get_project_settings()
        self.timeout = self.mySetting['SELENIUM_TIMEOUT']
        self.isLoadImage = self.mySetting['LOAD_IMAGE']
        self.windowHeight = self.mySetting['WINDOW_HEIGHT']
        self.windowWidth = self.mySetting['windowWidth']
        self.chromePath = self.mySetting['CHROMEDRIVER_PATH']
        # 初始化chrome对象
        self.browser = webdriver.Chrome(executable_path=self.chromePath, chrome_options=options)
        if self.windowHeight and self.windowWidth:
            self.browser.set_window_size(600, 600)
        self.browser.set_page_load_timeout(self.timeout)  # 页面加载超时时间
        self.wait = WebDriverWait(self.browser, 60)  # 指定元素加载超时时间
        super(QuanguoSpider, self).__init__()
        dispatcher.connect(self.close, signals.spider_closed)

    def close(self, spider):
        # 当爬虫退出的时候关闭chrome
        print('spider closed')
        self.browser.quit()

    def start_requests(self):
        yield scrapy.FormRequest(url=self.url, method='POST', meta={'usedSelenium': False},
                                 headers=self.header,
                                 formdata={'TIMEBEGIN_SHOW': '2018-04-23', 'TIMEEND_SHOW': '2018-07-23',
                                           'TIMEBEGIN': '2018-04-23',
                                           'TIMEEND': '2018-07-23', 'DEAL_TIME': '05',
                                           'DEAL_CLASSIFY': '00', 'DEAL_STAGE': '0000', 'DEAL_PROVINCE': '110000',
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
            for name in self.new_pcityDic.keys():
                if name in item['lypt']:
                    item['city'] = self.new_pcityDic.get(name)
                else:
                    item['city'] = '其它'
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
            entryName = each.xpath('.//h4/a/text()').extract()
            if entryName:
                item['entryName'] = entryName[0]
            else:
                item['entryName'] = ''

            items.append(item)

        for item in items:
            yield scrapy.Request(url=item['url'], headers=self.header, meta={'meta_1': item, 'usedSelenium': True},
                                 callback=self.detail_parse)

        # 下一页
        if self.page < int(pageCount):
            self.page += 1

        yield scrapy.FormRequest(url=self.url, method='POST',
                                 meta={'usedSelenium': True},
                                 headers=self.header,
                                 formdata={'TIMEBEGIN_SHOW': '2018-04-23', 'TIMEEND_SHOW': '2018-07-23',
                                           'TIMEBEGIN': '2018-04-23',
                                           'TIMEEND': '2018-07-23', 'DEAL_TIME': '05',
                                           'DEAL_CLASSIFY': '00', 'DEAL_STAGE': '0000', 'DEAL_PROVINCE': '110000',
                                           'DEAL_CITY': '0',
                                           'DEAL_PLATFORM': '0', 'DEAL_TRADE': '0', 'isShowAll': '0',
                                           'PAGENUMBER': str(self.page), 'FINDTXT': ''}, callback=self.parse,
                                 dont_filter=True)

    def detail_parse(self, response):
        items = []
        item = response.meta['meta_1']
        entryNum = response.xpath('//div[@class="fully"]/p[@class="p_o"]/span[1]/text()').extract()
        if entryNum:
            item['entryNum'] = entryNum[0][7:]
        else:
            item['entryNum'] = ''
        for name in self.pcodeDic.keys():
            if name == item['area']:
                item['pcode'] = self.pcodeDic.get(name)
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
