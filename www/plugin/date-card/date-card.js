const week_dic = {
  "Monday":"星期一",
  "Tuesday":"星期二",
  "Wednesday":"星期三",
  "Thursday":"星期四",
  "Friday":"星期五",
  "Saturday":"星期六",
  "Sunday":"星期日",
};

class DateCard extends HTMLElement {
  set hass(hass) {
    if (!this.content) {
      const card = document.createElement('ha-card');
      this.config.title ? card.header = this.config.title : card.header = 'Date card';
      this.content = document.createElement('div');
      this.content.style.padding = '0 16px 16px';
      card.appendChild(this.content);
      this.appendChild(card);
    }

    this.dateObj = this.config.entity in hass.states ? hass.states[this.config.entity] : null;

    this.content.innerHTML = `
      <style type="text/css">
        .date-head {
            background-color: #42962e;
            width: 300px;
            margin-right: auto;
            margin-left: auto;
            text-align: center;
            font-size: 14px;
            color: #FFF;
            padding: 5px;
            border-radius: 4px 4px 0 0;
        }
        
        .date-content {
            background-color: #fb0;
            width: 300px;
            margin-right: auto;
            margin-left: auto;
            text-align: center;
            font-size: 64px;
            font-weight: bold;
            color: #FFF;
            padding: 5px;
            border-radius: 0 0 4px 4px;
        }
          
        .date-lunar {
            text-align: center;
            font-size: 14px;
            font-weight: bold;
            color: #000;
            padding: 5px;
        }
        
        .date-ganzhi {
            text-align: center;
            font-size: 14px;
            color: #000;
            padding: 5px;
        }
        
        .date-countdown {
            border-top-width: 1px;
            border-top-style: solid;
            border-top-color: #abd6b8;
            margin-left: 80px;
            margin-right: 80px;
            text-align: center;
            font-size: 14px;
            color: #000;
            padding: 10px;
        }
      </style>
      `

    if (this.dateObj.attributes.festival != "None"){
      this.content.innerHTML += `<div class="date-head">${this.dateObj.attributes.year} 年 ${this.dateObj.attributes.month} 月
          &nbsp;&nbsp;${week_dic[this.dateObj.attributes.week]}&nbsp;&nbsp;【${this.dateObj.attributes.festival}】</div>`;
    }
    else{
      this.content.innerHTML += `<div class="date-head">${this.dateObj.attributes.year} 年 ${this.dateObj.attributes.month} 月
          &nbsp;&nbsp;${week_dic[this.dateObj.attributes.week]}</div>`;
    }

    if (this.dateObj.attributes.jnr != "None") {
      this.content.innerHTML += `<div class="date-content">${this.dateObj.attributes.day}
         <span style="font-size:24px; color:#EB4537">&nbsp;&nbsp;${this.dateObj.attributes.jnr}</span></div>`;
    }
    else{
      this.content.innerHTML += `<div class="date-content">${this.dateObj.attributes.day}
         <span style="font-size:24px;">&nbsp;&nbsp;&nbsp;${this.dateObj.state}</span></div>`;
    }

    if (this.dateObj.attributes.jieqi != "None"){
      this.content.innerHTML += `<div class="date-lunar">${this.dateObj.attributes.lunar}【${this.dateObj.attributes.jieqi}】</div>`;
    }
    else{
        this.content.innerHTML += `<div class="date-lunar">${this.dateObj.attributes.lunar}</div>`;
    }

    this.content.innerHTML += `
      <div class="date-ganzhi">${this.dateObj.attributes.cyclicalYear}【${this.dateObj.attributes.animal}】年 
          ${this.dateObj.attributes.cyclicalMonth}月 ${this.dateObj.attributes.cyclicalDay}日</div>`;

    if (this.config.countdown){
      let strs = this.config.countdown.split("|");
      if (strs.length != 2) {
        throw new Error('countdown parameter error');
      }
      let s1 = new Date(strs[0].replace(/-/g, "/")); //2019-09-01的日期格式转换成2009/09/01
      let s2 = new Date(); //当前时间
      let dd = parseInt((s1-s2)  / (1000 * 60 * 60 * 24)) //计算相隔的天数
      this.content.innerHTML += `<div class="date-countdown">距&nbsp; 
        <span style="font-size:16px; color:#ff7800">${strs[1]}</span> &nbsp;还有 
        <span style="font-size:24px; color:#ff7800">${dd}</span> 天</div>`
    }

  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
  }

  // The height of your card. Home Assistant uses this to automatically
  // distribute all cards over the available columns.
  getCardSize() {
    return 4;
  }
}

customElements.define('date-card', DateCard);