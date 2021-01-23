# 简介
农历采用 sxtwl 本地计算得出
是否工作日接口：http://tool.bitefu.net/jiari/
# 安装
后端：holidaycalendar目录放入 <config directory>/custom_components/ 目录
  
前端：data-card目录放入 <config directory>/www/plugin/目录

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
| jieqi | 当天的24节气，更具香港天文台的数据得出（网友代码） | 
| jnr | 当天的纪念日，没有None，需要事先在getAnniversary函数中定义 | 

# 特别说明
sensor.py文件中，每年的公休日需要手动更新一次，可以百度查询

#2021年休假日

XiuJiaList=[(1,1), (1,2), (1,3), (2,11), (2,12), (2,13), (2,14), (2,15), (2,16), (2,17), (4,3), (4,4), (4,5), (5,1), (5,2), (5,3), (5,4), (5,5), 
            (6,12), (6,13), (6,14), (9,19), (9,20), (9,21),(10,1), (10,2), (10,3), (10,4), (10,5), (10,6), (10,7)]
            
#2021年周末调休日

TiaoXiuList=[(2,7), (2,20), (4,25), (5,8), (9,18), (9,26), (10,9)]

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
