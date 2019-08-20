"""
A component which allows you to get holiday  and calendar infomation
json接口的数据源：https://www.sojson.com/open/api/lunar/json.shtml
For more details about this component, please refer to the documentation at
https://github.com/aalavender/HolidayCalendar

"""
import logging
import asyncio
import voluptuous as vol
import datetime
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME)
import requests
import json

__version__ = '0.1.0'
_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ["requests"]

COMPONENT_REPO = 'https://github.com/aalavender/HolidayCalendar'
SCAN_INTERVAL = datetime.timedelta(hours=12)
ICON = 'mdi:calendar-today'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
})

'''以下的数据每年需要调整'''
HOLIDAY = {
    datetime.date(year=2019, month=1, day=1):  "元旦放假",

    datetime.date(year=2019, month=2, day=4): "春节放假",
    datetime.date(year=2019, month=2, day=5): "春节放假",
    datetime.date(year=2019, month=2, day=6): "春节放假",
    datetime.date(year=2019, month=2, day=7): "春节放假",
    datetime.date(year=2019, month=2, day=8): "春节放假",
    datetime.date(year=2019, month=2, day=9): "春节放假",
    datetime.date(year=2019, month=2, day=10): "春节放假",

    datetime.date(year=2019, month=4, day=5):  "清明节放假",
    datetime.date(year=2019, month=4, day=6):  "清明节放假",
    datetime.date(year=2019, month=4, day=7):  "清明节放假",

    datetime.date(year=2019, month=5, day=1):  "劳动节放假",
    datetime.date(year=2019, month=5, day=2):  "劳动节放假",
    datetime.date(year=2019, month=5, day=3):  "劳动节放假",
    datetime.date(year=2019, month=5, day=4):  "劳动节放假",

    datetime.date(year=2019, month=6, day=7): "端午节放假",
    datetime.date(year=2019, month=6, day=8): "端午节放假",
    datetime.date(year=2019, month=6, day=9): "端午节放假",

    datetime.date(year=2019, month=9, day=13): "中秋节放假",
    datetime.date(year=2019, month=9, day=14): "中秋节放假",
    datetime.date(year=2019, month=9, day=15): "中秋节放假",

    datetime.date(year=2019, month=10, day=1): "国庆节放假",
    datetime.date(year=2019, month=10, day=2): "国庆节放假",
    datetime.date(year=2019, month=10, day=3): "国庆节放假",
    datetime.date(year=2019, month=10, day=4): "国庆节放假",
    datetime.date(year=2019, month=10, day=5): "国庆节放假",
    datetime.date(year=2019, month=10, day=6): "国庆节放假",
    datetime.date(year=2019, month=10, day=7): "国庆节放假",
}

HOLIDAY_BUBAN = {
    datetime.date(year=2019, month=2, day=2):  "春节补班",
    datetime.date(year=2019, month=2, day=3):  "春节补班",

    datetime.date(year=2019, month=4, day=28): "劳动节补班",
    datetime.date(year=2019, month=5, day=5): "劳动节补班",

    datetime.date(year=2019, month=9, day=29): "国庆节补班",
    datetime.date(year=2019, month=10, day=12): "国庆节补班",
}

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    name = config[CONF_NAME]
    _LOGGER.info("start async_setup_platform sensor HolidayCalendar")
    async_add_devices([HolidayCalSensor(name)], True)


class HolidayCalSensor(Entity):
    def __init__(self, name):
        self._name = name
        self._entries = {}

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
        _LOGGER.info("sensor HolidayCalendar update from https://www.sojson.com/open/api/lunar/json.shtml")
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
        }
        json_text = requests.get("https://www.sojson.com/open/api/lunar/json.shtml", headers=header).content
        json_data = json.loads(json_text)
        if json_data["message"] == "success": #查询成功
            self._entries["animal"] = json_data["data"]["animal"]
            self._entries["year"] = json_data["data"]["year"]
            self._entries["month"] = json_data["data"]["month"]
            self._entries["day"] = json_data["data"]["day"]
            self._entries["week"] = json_data["data"]["week"]
            self._entries["cyclicalYear"] = json_data["data"]["cyclicalYear"]
            self._entries["cyclicalMonth"] = json_data["data"]["cyclicalMonth"]
            self._entries["cyclicalDay"] = json_data["data"]["cyclicalDay"]
            self._entries["lunar"] = "{0}月{1}".format(json_data["data"]["cnmonth"], json_data["data"]["cnday"])
            self._entries["festival"] = 'None'
            if json_data["data"]["festivalList"]:
                self._entries["festival"] = '/'.join(json_data["data"]["festivalList"])
            self._entries["jieqi"] = 'None'
            for key, value in json_data["data"]["jieqi"].items():
                if json_data["data"]["day"] == key:
                    self._entries["jieqi"] = value

            # 获取周年纪念日，目前只有生日
            self._entries["jnr"] = self.getAnniversary(json_data["data"]["month"]+json_data["data"]["day"])

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        '''状态一共有四种：1，工作日  2，周末 3，法定节假日 4，补班'''
        now_day = datetime.date.today()
        if now_day in HOLIDAY.keys():
            return HOLIDAY[now_day]
        elif now_day in HOLIDAY_BUBAN.keys():
            return HOLIDAY_BUBAN[now_day]
        # 判断是否为周六和周日
        elif now_day.weekday() > 4:  #周六5/周日6
            return "周末"
        else:
            return "工作日"

    @property
    def icon(self):
        return ICON

    @property
    def device_state_attributes(self):
        return self._entries
