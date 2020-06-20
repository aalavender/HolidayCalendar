"""
A component which allows you to get holiday  and calendar infomation
使用https://pypi.org/project/sxtwl/, 这里的信息有，阴历，阳历，二十四节气，天干地支，星期几等
For more details about this component, please refer to the documentation at
https://github.com/aalavender/HolidayCalendar

"""
import logging
import asyncio
import voluptuous as vol
import datetime
import time
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME)
import sxtwl
import requests

__version__ = '0.1.1'
_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ["sxtwl", "requests"]

COMPONENT_REPO = 'https://github.com/aalavender/HolidayCalendar'
SCAN_INTERVAL = datetime.timedelta(hours=12)
ICON = 'mdi:calendar-today'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
})

Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ShX = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
numCn = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑","白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"]
ymc = ["十一", "十二", "正", "二", "三", "四", "五", "六", "七", "八", "九", "十" ]
rmc = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
xingqi = ["星期日","星期一", "星期二","星期三","星期四", "星期五","星期六"]

#复活节:每年春分后月圆第一个星期天  母亲节:每年5月份的第2个星期日  父亲节:每年6月份的第3个星期天感恩节 每年11月最后一个星期四
# otherEastHolidaysList={5:(2,7,'母亲节'),6:(3,7,'父亲节')}

SolarHolidaysList=[
    {1:'元旦', 8: '周恩来逝世纪念日', 10: '中国公安110宣传日', 21: '列宁逝世纪念日', 26: '国际海关日'}, #1月
    {2: '世界湿地日', 4: '世界抗癌日', 7: '京汉铁路罢工纪念', 10: '国际气象节', 14: '情人节', 19: '邓小平逝世纪念日', 21: '国际母语日', 24: '第三世界青年日'},
    {1: '国际海豹日', 3: '全国爱耳日', 5: '周恩来诞辰纪念日,中国青年志愿者服务日', 6: '世界青光眼日', 8: '国际劳动妇女节', 12: '孙中山逝世纪念日,中国植树节', 14: '马克思逝世纪念日', 15: '国际消费者权益日', 17: '国际航海日', 18: '全国科技人才活动日', 21: '世界森林日,世界睡眠日', 22: '世界水日', 23: '世界气象日', 24: '世界防治结核病日'},
    {1: '国际愚人节', 2: '国际儿童图书日', 7: '世界卫生日', 22: '列宁诞辰纪念日', 23: '世界图书和版权日', 26: '世界知识产权日'},
    {1: '国际劳动节', 3: '世界新闻自由日', 4: '中国青年节', 5: '马克思诞辰纪念日', 8: '世界红十字日', 11: '世界肥胖日', 23: '世界读书日', 27: '上海解放日', 31: '世界无烟日'},
    {1: '国际儿童节', 5: '世界环境日', 6: '全国爱眼日', 8: '世界海洋日', 11: '中国人口日', 14: '世界献血日'},
    {1: '中国共产党诞生日,香港回归纪念日', 7: '中国人民抗日战争纪念日', 11: '世界人口日'},
    {1: '中国人民解放军建军节', 5: '恩格斯逝世纪念日', 6: '国际电影节', 12: '国际青年日', 22: '邓小平诞辰纪念日'},
    {3: '中国抗日战争胜利纪念日', 8: '世界扫盲日', 9: '毛泽东逝世纪念日', 10: '中国教师节', 14: '世界清洁地球日', 18: '“九·一八”事变纪念日', 20: '全国爱牙日', 21: '国际和平日', 27: '世界旅游日'},
    {1: '国庆节', 4: '世界动物日', 10: '辛亥革命纪念日', 13: '中国少年先锋队诞辰日', 25: '抗美援朝纪念日'},
    {12: '孙中山诞辰纪念日', 28: '恩格斯诞辰纪念日'},
    {1: '世界艾滋病日', 12: '西安事变纪念日', 13: '南TiaoXiuList京大屠杀纪念日', 24: '平安夜', 25: '圣诞节', 26: '毛泽东诞辰纪念日'} #12月
]

LunarHolidaysList={(1,1):'春节',(5,5):'端午节', (7,15):'中元节', (8,15):'中秋节', (12,8):'腊八节',(12,23):'小年'}
#2020年休假日
XiuJiaList=[(1,1), (1,24), (1,25), (1,26), (1,27), (1,28), (1,29), (1,30), (1,31), (2,1), (2,2), (4,4), (4,5), (4,6), 
            (5,1), (5,2), (5,3), (5,4), (5,5), (6,25), (6,26), (6,27), (10,1), (10,2), (10,3), (10,4), (10,5), (10,6)
            , (10,7), (10,8)]
#2020年周末调休日
TiaoXiuList=[(1,19), (4,26), (5,9), (6,28), (9,27), (10,10)]

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    name = config[CONF_NAME]
    _LOGGER.info("start async_setup_platform sensor HolidayCalendar")
    async_add_devices([HolidayCalSensor(name)], True)


class HolidayCalSensor(Entity):
    def __init__(self, name):
        self._name = name
        self._entries = {}

        self.lunar = sxtwl.Lunar()  #实例化日历库

    def getAnniversary(self, day):
        ''' 返回纪念日，没有返回None '''
        anni = {
            "0122": '子玉生日',
            "0216": '爸爸生日',
            "0809": '琪琪生日',
            "1125": '妈妈生日',
        }
        if day in anni.keys():
            return anni[day]
        else:
            return "None"

    def update(self):
        year = self.lunar.getYearCal(datetime.datetime.now().year)
        day = self.lunar.getDayBySolar(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
        self._entries["animal"] = ShX[year.ShX]
        self._entries["year"] = day.y
        self._entries["month"] = day.m
        self._entries["day"] = day.d
        self._entries["week"] = xingqi[day.week]
        self._entries["cyclicalYear"] = Gan[day.Lyear2.tg] + Zhi[day.Lyear2.dz]
        self._entries["cyclicalMonth"] = Gan[day.Lmonth2.tg] + Zhi[day.Lmonth2.dz]
        self._entries["cyclicalDay"] = Gan[day.Lday2.tg]+Zhi[day.Lday2.dz]
        if day.Lleap:
            self._entries["lunar"] = "润{0}月{1}".format(ymc[day.Lmc], rmc[day.Ldi])
        else:
            self._entries["lunar"] = "{0}月{1}".format(ymc[day.Lmc], rmc[day.Ldi])
        #节日
        self._entries["festival"] = 'None'
        if day.d in SolarHolidaysList[day.m-1]:
            self._entries["festival"] = SolarHolidaysList[day.m-1][day.d]
        if  (day.Lmc-1, day.Ldi+1) in LunarHolidaysList:
            if self._entries["festival"] == 'None':
                self._entries["festival"] = LunarHolidaysList[(day.Lmc-1, day.Ldi+1)]
            else:
                self._entries["festival"] += "," + LunarHolidaysList[(day.Lmc-1, day.Ldi+1)]
        #节气
        if (day.qk >= 0):
            self._entries["jieqi"] = jqmc[day.jqmc]
        else:
            self._entries["jieqi"] = 'None'

        # 获取周年纪念日，目前只有生日
        self._entries["jnr"] = self.getAnniversary(datetime.datetime.now().month + datetime.datetime.now().day)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        #:param day: 日期， 格式为 '20160404'
        #:return: bool
        # api = 'http://tool.bitefu.net/jiari/'
        # params = {'d': time.strftime("%Y%m%d", time.localtime()), 'apiserviceid': 1116}
        # rep = requests.get(api, params)
        # if rep.status_code != 200:
        #     return '无法获取节日数据'
        # res = rep.text
        lt = time.localtime()
        dt = (lt.tm_mon, lt.tm_mday)
        if dt in XiuJiaList:
            return "休息日"
        elif dt in TiaoXiuList:
            return "工作日"
        elif lt.tm_wday in (5,6):
            return "休息日"
        else:
            return "工作日"

    @property
    def icon(self):
        return ICON

    @property
    def device_state_attributes(self):
        return self._entries
