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
jieqi = ['小寒','大寒','立春','雨水','惊蛰','春分','清明','谷雨','立夏','小满','芒种','夏至','小暑','大暑','立秋','处暑','白露','秋分','寒露','霜降','立冬','小雪','大雪','冬至']
# 24节气模块\节气数据16进制加解密
# author: cuba3
# github: https://github.com/cuba3/pyGregorian2LunarCalendar

START_YEAR = 1901
# 1901-2100年二十节气最小公差数序列 向量压缩法
encryptionVectorList=[4, 19, 3, 18, 4, 19, 4, 19, 4, 20, 4, 20, 6, 22, 6, 22, 6, 22, 7, 22, 6, 21, 6, 21]
# 1901-2100年二十节气数据 每个元素的存储格式如下：
# 1-24
# 节气所在天（减去节气最小公约数）
# 1901-2100年香港天文台公布二十四节气按年存储16进制，1个16进制为4个2进制
solarTermsData=[
    0x6aaaa6aa9a5a, 0xaaaaaabaaa6a, 0xaaabbabbafaa, 0x5aa665a65aab, 0x6aaaa6aa9a5a, # 1901 ~ 1905
    0xaaaaaaaaaa6a, 0xaaabbabbafaa, 0x5aa665a65aab, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a,
    0xaaabbabbafaa, 0x5aa665a65aab, 0x6aaaa6aa9a56, 0xaaaaaaaa9a5a, 0xaaabaabaaeaa,
    0x569665a65aaa, 0x5aa6a6a69a56, 0x6aaaaaaa9a5a, 0xaaabaabaaeaa, 0x569665a65aaa,
    0x5aa6a6a65a56, 0x6aaaaaaa9a5a, 0xaaabaabaaa6a, 0x569665a65aaa, 0x5aa6a6a65a56,
    0x6aaaa6aa9a5a, 0xaaaaaabaaa6a, 0x555665665aaa, 0x5aa665a65a56, 0x6aaaa6aa9a5a,
    0xaaaaaabaaa6a, 0x555665665aaa, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a,
    0x555665665aaa, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a, 0x555665665aaa,
    0x5aa665a65a56, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a, 0x555665655aaa, 0x569665a65a56,
    0x6aa6a6aa9a56, 0xaaaaaaaa9a5a, 0x5556556559aa, 0x569665a65a55, 0x6aa6a6a65a56,
    0xaaaaaaaa9a5a, 0x5556556559aa, 0x569665a65a55, 0x5aa6a6a65a56, 0x6aaaa6aa9a5a,
    0x5556556555aa, 0x569665a65a55, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0x55555565556a,
    0x555665665a55, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0x55555565556a, 0x555665665a55,
    0x5aa665a65a56, 0x6aaaa6aa9a5a, 0x55555555556a, 0x555665665a55, 0x5aa665a65a56,
    0x6aaaa6aa9a5a, 0x55555555556a, 0x555665655a55, 0x5aa665a65a56, 0x6aa6a6aa9a5a,
    0x55555555456a, 0x555655655a55, 0x5a9665a65a56, 0x6aa6a6a69a5a, 0x55555555456a,
    0x555655655a55, 0x569665a65a56, 0x6aa6a6a65a56, 0x55555155455a, 0x555655655955,
    0x569665a65a55, 0x5aa6a5a65a56, 0x15555155455a, 0x555555655555, 0x569665665a55,
    0x5aa665a65a56, 0x15555155455a, 0x555555655515, 0x555665665a55, 0x5aa665a65a56,
    0x15555155455a, 0x555555555515, 0x555665665a55, 0x5aa665a65a56, 0x15555155455a,
    0x555555555515, 0x555665665a55, 0x5aa665a65a56, 0x15555155455a, 0x555555555515,
    0x555655655a55, 0x5aa665a65a56, 0x15515155455a, 0x555555554515, 0x555655655a55,
    0x5a9665a65a56, 0x15515151455a, 0x555551554515, 0x555655655a55, 0x569665a65a56,
    0x155151510556, 0x555551554505, 0x555655655955, 0x569665665a55, 0x155110510556,
    0x155551554505, 0x555555655555, 0x569665665a55, 0x55110510556, 0x155551554505,
    0x555555555515, 0x555665665a55, 0x55110510556, 0x155551554505, 0x555555555515,
    0x555665665a55, 0x55110510556, 0x155551554505, 0x555555555515, 0x555655655a55,
    0x55110510556, 0x155551554505, 0x555555555515, 0x555655655a55, 0x55110510556,
    0x155151514505, 0x555555554515, 0x555655655a55, 0x54110510556, 0x155151510505,
    0x555551554515, 0x555655655a55, 0x14110110556, 0x155110510501, 0x555551554505,
    0x555555655555, 0x14110110555, 0x155110510501, 0x555551554505, 0x555555555555,
    0x14110110555, 0x55110510501, 0x155551554505, 0x555555555555, 0x110110555,
    0x55110510501, 0x155551554505, 0x555555555515, 0x110110555, 0x55110510501,
    0x155551554505, 0x555555555515, 0x100100555, 0x55110510501, 0x155151514505,
    0x555555555515, 0x100100555, 0x54110510501, 0x155151514505, 0x555551554515,
    0x100100555, 0x54110510501, 0x155150510505, 0x555551554515, 0x100100555,
    0x14110110501, 0x155110510505, 0x555551554505, 0x100055, 0x14110110500,
    0x155110510501, 0x555551554505, 0x55, 0x14110110500, 0x55110510501,
    0x155551554505, 0x55, 0x110110500, 0x55110510501, 0x155551554505,
    0x15, 0x100110500, 0x55110510501, 0x155551554505,0x555555555515]

# 两个List合并对应元素相加或者相减，a[i]+b[i]:tpye=1 a[i]-b[i]:tpye=-1
def abListMerge(a, b=encryptionVectorList, type=1):
    c = []
    for i in range(len(a)):
        c.append(a[i]+b[i]*type)
    return c

# 解压缩16进制用
def unZipSolarTermsList(data,rangeEndNum=24,charCountLen=2):
    list2 = []
    for i in range(1,rangeEndNum+1):
        right=charCountLen*(rangeEndNum-i)
        if type(data).__name__=='str':
            data= int(data, 16)
        x=data >> right
        c=2**charCountLen
        list2=[(x % c)]+list2
    return abListMerge(list2)

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
        #网友的算法返回当年节气的日期表[6, 20, 4, 19, 5, 20, 4, 19, 5, 20, 5, 21, 6, 22, 7, 22, 7, 22, 8, 23, 7, 22, 7, 21]
        #因为24节气平均每月2个，所以可以推算出来
        jieqilist = unZipSolarTermsList(solarTermsData[day.y-START_YEAR])
        if (day.d == jieqilist[(day.m-1)*2]):
            self._entries["jieqi"] = jieqi[(day.m-1)*2]
        elif (day.d == jieqilist[(day.m-1)*2+1]):
            self._entries["jieqi"] = jieqi[(day.m-1)*2+1]
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
        api = 'http://tool.bitefu.net/jiari/'
        params = {'d': time.strftime("%Y%m%d", time.localtime()), 'apiserviceid': 1116}
        rep = requests.get(api, params)
        if rep.status_code != 200:
            return '无法获取节日数据'
        res = rep.text
        return "休息日" if res != "0" else "工作日"

    @property
    def icon(self):
        return ICON

    @property
    def device_state_attributes(self):
        return self._entries
