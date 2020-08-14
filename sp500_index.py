# 获取美指数据

from datetime import datetime

# 导入库
import pandas as pd
import requests
from bs4 import BeautifulSoup

"""
数据存在于id为datatable的table内
日期为英文日期格式
<table id="datatable">
      <tr>
        <th class="left">Date</th>
        <th class="right">
          <span class="title">
            Value
          </span>
          <span class="value">Value</span>
        </th>
      </tr>


      <tr class="odd">
        <td class="left">Jul 16, 2018</td>
        <td class="right">24.24
          <span class="estimate">estimate</span>
        </td>
      </tr>
      <tr class="even">
        <td class="left">Jul 1, 2018</td>
        <td class="right">23.71
        </td>
      </tr>
      <tr class="odd">
        <td class="left">Jun 1, 2018</td>
        <td class="right">23.86
        </td>
      </tr>
      <tr class="even">
        <td class="left">May 1, 2018</td>
        <td class="right">23.40
        </td>
      </tr>
      <tr class="odd">
        <td class="left">Apr 1, 2018</td>
        <td class="right">22.99
        </td>
      </tr>
      <tr class="even">
        <td class="left">Mar 1, 2018</td>
        <td class="right">23.41
        </td>
...
"""

_data_type_dict = {
    'price':
        {'url': 'http://www.multpl.com/s-p-500-historical-prices/table/',
         'period': {'M': 'by-month', 'Y': 'by-year'},
         'columns': 'close',
         },
    'pe':
        {'url': 'http://www.multpl.com/table?f=',
         'period': {'M': 'm', 'Y': 'y'},
         'columns': 'pe',
         },
    'dyr':
        {'url': 'http://www.multpl.com/s-p-500-dividend-yield/table?f=',
         'period': {'M': 'm', 'Y': 'y'},
         'columns': 'dyr',
         }
}


def convert_date(date_str):
    mon_dict = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
    }
    date_str = date_str.replace(',', '').split(' ')
    return '%s-%s-%s' % (date_str[2], mon_dict[date_str[0]], date_str[1].rjust(2, '0'))


class Spx(object):
    """
    multpl网站sp500数据
    http://www.multpl.com/
    """

    @staticmethod
    def hist_data(data_type, start_date='2000-01-01', end_date=None, period='M'):
        """
        获取历史行情数据，限制开始、结束时间版本
        data_type：数据类别，str，分别为：'price'、'pe'、'dyr'
        start_date：开始日期，str，如：'2018-07-01'
        end_date：结束日期，str，如：'2018-07-31'
        period：数据线级别，str，分别为：'W'、'M'（周、月）
        """

        # 今天日期
        today_str = datetime.now().date().strftime('%Y-%m-%d')

        # 约束开始日期
        if start_date > today_str:
            return None

        # 约束结束日期
        if end_date is None or end_date > today_str:
            # 今天日期
            end_date = today_str

        # url
        url = _data_type_dict[data_type].get('url') + _data_type_dict[data_type].get('period')[period]
        # print
        # url

        # 获取网站数据
        response = requests.get(url)

        # 去除多余信息(换行符、数字中的逗号、百分号)
        content = response.text
        # 解析
        soup = BeautifulSoup(content, 'html.parser')
        table = str(soup.select('#datatable')[0]).replace('<span class="estimate">estimate</span>', '').replace(
            '\n        ', '').replace(',', '').replace('%', '')
        soup = BeautifulSoup(table, 'html.parser')

        date_list = []
        data_list = []
        # 遍历表格
        for date_item, value_item in zip(soup.select('td[class="left"]'),
                                         soup.select('td[class="right"]')):
            # 转换为标准日期格式
            standard_date = convert_date(date_item.get_text())
            # 判断是否在指定日期之内
            if standard_date <= end_date:
                if standard_date < start_date:
                    break
                date_list.append(standard_date)
                data_list.append(value_item.get_text())

        # 无数据返回空列表
        if len(data_list) == 0:
            return None

        # 组织数据
        df = pd.DataFrame(index=date_list, data=data_list, columns=[_data_type_dict[data_type].get('columns')])
        # 格式转换
        df.index = pd.to_datetime(df.index)
        df = df.astype('float')
        # 返回排序后的数据
        return df.sort_index()
