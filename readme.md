# 简介
农历采用 sxtwl 本地计算得出
是否工作日接口：http://tool.bitefu.net/jiari/
# 安装
放入 <config directory>/custom_components/ 目录

# 配置
**Example configuration.yaml:**
```yaml
sensor:
  - platform: holidaycalendar
    name: 万年历
    scan_interval: 999999  # 这是阻止自动更新，用自动化在零点更新
```

# 属性说明
| 属性 | 说明 | 
| :-------------: |:-------------:| 
| animal | 年的属性，2019年是猪年 | 
| year | 年 |
| month | 月 |
| day | 天 |
| week | 星期x |
| cyclicalYear | 天干地支年 | 
| cyclicalMonth | 天干地支月 | 
| cyclicalDay | 天干地支天 | 
| lunar | 当天农历 | 
| festival | 当天的节日，未实现，None | 
| jieqi | 当天的24节气，未实现，None | 
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
