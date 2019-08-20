# 简介
获取万年历和节假日信息 
数据源地址： https://www.sojson.com/open/api/lunar/json.shtml
接口返回的数据很全面，如：农历、黄历、禁忌、星期、生肖、当月的节气、是否闰月、是不是大月等，具体自己体会。
本来用 sxtwl 自己写了一个更加全面的，但是 sxtwl 这个依赖包在ha上装不上
# 安装
放入 <config directory>/custom_components/ 目录

# 配置
**Example configuration.yaml:**
```yaml
sensor:
  - platform: holidaycalendar
    name: 万年历
```

# 属性说明
| 属性 | 说明 | 
| :-------------: |:-------------:| 
| animal | 年的属性，2019年是猪年 | 
| date | 当天日期 |
| cndate | 当天日期天干地支描述 | 
| lunar | 当天农历 | 
| festival | 当天的节日，没有None，多个用/隔离 | 
| jieqi | 当天的24节气，没有None | 
| jnr | 当天的纪念日，没有None，需要事先在getAnniversary函数中定义 | 


# 前台界面

![avatar](https://github.com/aalavender/HolidayCalendar/blob/master/1.PNG)

自定义了date-card，countdown参数不填就没有倒计时
![avatar](https://github.com/aalavender/HolidayCalendar/blob/master/2.PNG)

```yaml
entity: sensor.mo_nian_li
title: 万年历
type: 'custom:date-card'
countdown: 2019/09/01|开学
```
