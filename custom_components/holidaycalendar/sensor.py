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
xingqi = ["星期一", "星期二","星期三","星期四", "星期五","星期六","星期日"]


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
        day = self.lunar.getDayByLunar(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
        self._entries["animal"] = ShX[year.ShX]
        self._entries["year"] = datetime.datetime.now().year
        self._entries["month"] = datetime.datetime.now().month
        self._entries["day"] = datetime.datetime.now().day
        self._entries["week"] = xingqi[datetime.datetime.now().weekday()]
        self._entries["cyclicalYear"] = Gan[day.Lyear2.tg] + Zhi[day.Lyear2.dz]
        self._entries["cyclicalMonth"] = Gan[day.Lmonth2.tg] + Zhi[day.Lmonth2.dz]
        self._entries["cyclicalDay"] = Gan[day.Lday2.tg]+Zhi[day.Lday2.dz]
        if day.Lleap:
            self._entries["lunar"] = "润{0}月{1}".format(ymc[day.Lmc], rmc[day.Ldi])
        else:
            self._entries["lunar"] = "{0}月{1}".format(ymc[day.Lmc], rmc[day.Ldi])
        #节日
        self._entries["festival"] = 'None'
        #节气
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
