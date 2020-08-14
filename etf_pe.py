# -*- coding: utf-8 -*-
from datetime import timedelta, date
from io import BytesIO

import datetime
import os
import pandas as pd
import requests
import time
from jqdatasdk import *
from numpy import sqrt, mean, NaN
from scipy.stats import mstats


class Dividend(object):
    # 计算股息率
    def __init__(self, statsDate=None):
        if statsDate is None:
            statsDate = datetime.date.today()
        self.statsDate = statsDate
        self.df_div = self.calc_dividend()

    def calc_dividend(self, code_list=[]):
        code_list = list(map(normalize_code, code_list))  # 格式化股票代码
        if len(code_list) == 0:  # 计算所有股票的股息率
            all_stocks = list(get_all_securities(['stock']).index)
            code_list = [item[0:6] for item in all_stocks]  # 格式转换
            df1 = self.__calc_dividend(code_list[0:1500])  # 每次最大只能查询3000条数据
            df2 = self.__calc_dividend(code_list[1501:3000])
            df3 = self.__calc_dividend(code_list[3001:])
            df = pd.concat([df1, df2, df3], axis=0)
        else:  # 计算指定的股票
            df = self.__calc_dividend(code_list)

        bonus_results = []
        code_list = []
        columns = [u'股息', u'分红股本', u'分红金额']
        grouped = df.groupby(df.SecuCode)  # 不同股票一组
        for name, item in grouped:
            grouped_item = item.groupby(item.Year).sum().sort_index(ascending=False)  # 合并同一年度多次分红
            bonus_results.append([grouped_item.iloc[0]['ActualCashDiviRMB'],
                                  grouped_item.iloc[0]['DiviBase'],
                                  grouped_item.iloc[0]['TotalCash']])  # 去最新年份数据
            code_list.append(name)
        df_bonus = pd.DataFrame(data=bonus_results, index=code_list, columns=columns)
        df_cap = self.__get_cap(code_list)
        df_div = pd.concat([df_cap, df_bonus], axis=1, sort=True).fillna(value=0)
        df_div[u'股息率'] = df_div[u'分红金额'] / (df_div[u'市值'] * 1e8) * 100
        return df_div

    def __calc_dividend(self, code_list):
        # 计算指定code_list中的股息率
        secu_category = [1]  # 证券类别:1-A股，SecuMain表中的字段
        code_list = list(map(lambda item: item[0:6], code_list))  # 格式化股票代码
        incode = finance.run_query(query(
            jy.SecuMain.SecuCode,
            jy.SecuMain.InnerCode,
        ).filter(
            jy.SecuMain.SecuCategory.in_(secu_category),
            jy.SecuMain.SecuCode.in_(code_list)
        ))

        start_date = self.statsDate - datetime.timedelta(365 * 2)
        end_date = self.statsDate - datetime.timedelta(1)

        q = query(
            jy.LC_Dividend.InnerCode,  # 证券内部编码
            jy.LC_Dividend.ActualCashDiviRMB,  # 实派(税后/人民币元)
            jy.LC_Dividend.ToAccountDate,
            jy.LC_Dividend.DiviBase
        ).filter(
            jy.LC_Dividend.IfDividend == 1,
            jy.LC_Dividend.ToAccountDate < end_date,
            jy.LC_Dividend.ToAccountDate >= start_date,  # 股息到帐日期/红利发放日
            jy.LC_Dividend.InnerCode.in_(incode['InnerCode'])  # 股票代码
        )
        df = pd.merge(incode, jy.run_query(q).fillna(value=0, method=None, axis=0), on='InnerCode')
        df['Year'] = list(map(lambda v: v.year, df['ToAccountDate']))
        df['SecuCode'] = list(map(normalize_code, df['SecuCode']))  # 格式化股票代码
        df['ActualCashDiviRMB'] = df['ActualCashDiviRMB'] / 10.0  # 每十股分红
        df['TotalCash'] = df['ActualCashDiviRMB'] * df['DiviBase']
        del df['InnerCode']
        return df

    def __get_cap(self, code_list=[]):
        # 获取市值
        if len(code_list) == 0:
            q = query(valuation.code, valuation.market_cap)
        else:
            q = query(valuation.code, valuation.market_cap).filter(valuation.code.in_(code_list))
        df_cap = get_fundamentals(q, date=pd.datetime.today()).fillna(value=0)
        #         df_cap.code = map(lambda code: code[0:6], df_cap.code)
        df_cap.index = df_cap.code
        del df_cap['code']
        df_cap = df_cap.rename(columns={'market_cap': u'市值'})
        return df_cap

    def get_dividend(self, code):
        # 获取个股的股息率
        code = normalize_code(code)
        return self.df_div.loc[code][u'股息率']

    def get_idx_dividend(self, idx):
        # 获取指数的股息率
        code_list = get_idx_components(idx, self.statsDate)
        df_idx = self.df_div[self.df_div.index.isin(code_list)]
        idx_div = df_idx[u'分红金额'].sum() / (df_idx[u'市值'].sum() * 1e8) * 100
        return idx_div


def convert_code(code):
    if code.endswith('XSHG'):
        return 'sh' + code[0:6]
    elif code.endswith('XSHE'):
        return 'sz' + code[0:6]


def init_xueqiu():
    xueqiu_s = requests.session()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    xueqiu_s.headers.update({'User-Agent': user_agent})
    xueqiu_s.headers.update({'X-Requested-With': 'XMLHttpRequest'})
    xueqiu_s.get('https://xueqiu.com/')
    return xueqiu_s


def get_hist(code, begin='', end='', days=0, timeout=5):
    xueqiu_s = init_xueqiu()
    # code: sh000300, begin/end: 20160901, days: 指定最近天数
    # http://xueqiu.com/S/SH000902/historical.csv
    if len(begin) > 0 and days > 0:  # !!!不能同时指定begin和days!!!
        print('begin: %s, days: %d', begin, days)
        return None
    url = 'https://xueqiu.com/stock/forchartk/stocklist.json?symbol=%s&period=1day&type=normal' % (code)
    if len(begin) > 0:
        url = '%s&begin=%d' % (url, int(time.mktime(datetime.strptime(begin, '%Y%m%d').timetuple()) * 1000))
    if len(end) > 0:
        url = '%s&end=%s' % (url, int(time.mktime(datetime.strptime(end, '%Y%m%d').timetuple()) * 1000))
    if days > 0:
        url = '%s&begin=%d' % (url, int(time.mktime((datetime.today() - timedelta(days)).timetuple()) * 1000))
    url = '%s&_=%d' % (url, int(time.time() * 1000))
    #     print url
    r = xueqiu_s.get(url, timeout=timeout)
    org_fmt = "%a %b %d %H:%M:%S +0800 %Y"
    if r.ok is False:
        return None
    ret_data = r.json()
    stock_data = ret_data['chartlist']
    data_list = []
    day_list = []
    # date open close high low vol
    for item in stock_data:
        try:
            date = datetime.strptime(item['time'], org_fmt)
        except:
            date = datetime.strptime(item['time'], "%a %b %d %H:%M:%S +0900 %Y")
        data_list.append(item['close'])
        day_list.append(date)
    return pd.DataFrame(data=data_list, index=day_list, columns=[code])


def pd_read_csv(data_path, flag=False):
    # flag:是否使用read_file函数
    if flag is True:
        file_content = read_file(data_path)
    else:
        file_content = open(data_path, 'rb').read()
    df = pd.read_csv(BytesIO(file_content))
    df.index = pd.to_datetime(df['Unnamed: 0'])
    del df['Unnamed: 0']
    df.index.name = None
    return df


def get_idx_components(idx, day):
    securities_lst = [
        u'000166.XSHE', u'000686.XSHE', u'000712.XSHE', u'000728.XSHE', u'000750.XSHE', u'000776.XSHE',
        u'000783.XSHE', u'000987.XSHE', u'002500.XSHE', u'002670.XSHE', u'002673.XSHE', u'002736.XSHE',
        u'002797.XSHE', u'600030.XSHG', u'600061.XSHG', u'600109.XSHG', u'600369.XSHG', u'600837.XSHG',
        u'600909.XSHG', u'600958.XSHG', u'600999.XSHG', u'601099.XSHG', u'601198.XSHG', u'601211.XSHG',
        u'601375.XSHG', u'601377.XSHG', u'601555.XSHG', u'601688.XSHG', u'601788.XSHG', u'601881.XSHG',
        u'601901.XSHG']
    bank_lst = [
        u'000001.XSHE', u'002142.XSHE', u'002807.XSHE', u'002839.XSHE', u'600000.XSHG', u'600015.XSHG',
        u'600016.XSHG', u'600036.XSHG', u'600919.XSHG', u'600926.XSHG', u'601009.XSHG', u'601166.XSHG',
        u'601169.XSHG', u'601229.XSHG', u'601288.XSHG', u'601328.XSHG', u'601398.XSHG', u'601818.XSHG',
        u'601939.XSHG', u'601988.XSHG', u'601997.XSHG', u'601998.XSHG']
    if type(day) is date:
        day = pd.Timestamp(day)
    if idx in ['399986.XSHE', '399975.XSHE', '000852.XSHG']:
        all_df = get_all_securities(['stock'], day)
        if day > pd.Timestamp("2011-08-02"):
            all_df = all_df[all_df.index.isin(get_index_stocks('000985.XSHG', day))]  # 中证全指过滤
        if idx == '399986.XSHE' and day < pd.Timestamp("2015-05-19"):  # 中证银行
            df = all_df[all_df.index.isin(bank_lst)]
        elif idx == '399975.XSHE' and day < pd.Timestamp("2015-05-19"):  # 中证证券
            df = all_df[all_df.index.isin(securities_lst)]
        elif idx == '000852.XSHG' and day < pd.Timestamp("2014-10-17"):  # 中证1000
            stocks_800 = get_index_stocks('000906.XSHG', day)
            df = all_df[~all_df.index.isin(stocks_800)]  # 剔除中证800
            df = get_fundamentals(query(
                valuation.code, valuation.circulating_market_cap
            ).filter(
                valuation.code.in_(df.index.tolist())
            ).order_by(valuation.circulating_market_cap.desc()).limit(1000)).dropna().set_index('code')
        else:
            return get_index_stocks(idx, day)
        return df.index.tolist()
    return get_index_stocks(idx, day)


def calc_volatility(code, start_date=None, end_date=None):
    # 计算指数点位波动率
    if code in ['hscei', 'hsi']:
        try:
            df = get_hist('HK' + code.upper(), '20050101')
        except Exception as e:
            print(e)
            return 0.0
    else:
        if start_date is None:
            start_date = get_security_info(code).start_date
            if start_date < date(2005, 1, 4):  # 只计算2005年以来的数据
                start_date = date(2005, 1, 4)
        if end_date is None:
            end_date = pd.datetime.today() - timedelta(1)
        df = get_price([code], start_date=start_date, end_date=end_date, frequency='daily', fields=None)['close']
        df.dropna()
    df['diff'] = -df.diff(-1) / df
    df = df.dropna()
    return sqrt(250 * sum(pow(df['diff'] - mean(df['diff']), 2)) / len(df))


# 指定日期的指数PE_PB（等权重）
def get_index_pe_pb_date(code, date):
    stocks = get_idx_components(code, date)
    q = query(valuation).filter(valuation.code.in_(stocks))
    df = get_fundamentals(q, date)
    if len(df) > 0:
        pe = len(df) / sum([1 / p if p > 0 else 0 for p in df.pe_ratio])
        pb = len(df) / sum([1 / p if p > 0 else 0 for p in df.pb_ratio])
        return (round(pe, 2), round(pb, 2))
    else:
        return float('NaN')


# 指数历史PE_PB
def get_index_pe_pb(code, start_date=None, end_date=None):
    if start_date is None:
        start_date = get_security_info(code).start_date
        if start_date < date(2005, 1, 4):  # 只计算2005年以来的数据
            start_date = date(2005, 1, 4)
    if end_date is None:
        end_date = pd.datetime.today() - timedelta(1)
    x = get_price(code, start_date=start_date, end_date=end_date, frequency='daily', fields='close')
    date_list = x.index.tolist()
    #     print date_list
    pe_list = []
    pb_list = []
    for d in date_list:  # 交易日
        pe_pb = get_index_pe_pb_date(code, d)
        pe_list.append(pe_pb[0])
        pb_list.append(pe_pb[1])
    df = pd.DataFrame({'PE': pd.Series(pe_list, index=date_list),
                       'PB': pd.Series(pb_list, index=date_list)})
    return df


def get_index_list_pe_pb_date(code_list, date):
    '''指定日期的指数PE_PB'''
    ret_dict = {}
    df_all = get_fundamentals(query(valuation), date)  # 某日所有股票
    for code in code_list:
        stocks = get_idx_components(code, date)
        df = df_all[df_all['code'].isin(stocks)]  # 某个指数
        if len(df) > 0:
            # 整体法，市值加权
            df = df[df.pb_ratio != 0]  # 去除0
            df = df[df.pe_ratio != 0]  # 去除0
            pe1 = sum(df.market_cap) / sum(df.market_cap / df.pe_ratio)
            pb1 = sum(df.market_cap) / sum(df.market_cap / df.pb_ratio)
            # 等权，亏损置零
            pe2 = len(df) / sum(1 / df.pe_ratio[df.pe_ratio > 0])
            pb2 = len(df) / sum(1 / df.pb_ratio[df.pb_ratio > 0])
            # 中位数，无需预处理
            pe3 = df.pe_ratio.median()
            pb3 = df.pb_ratio.median()
            # 算数平均，取分位数95%置信区间
            pe4 = mean(mstats.winsorize(df.pe_ratio, limits=0.025))
            pb4 = mean(mstats.winsorize(df.pb_ratio, limits=0.025))

            ret_dict[code] = {'pe1': round(pe1, 2), 'pb1': round(pb1, 2),
                              'pe2': round(pe2, 2), 'pb2': round(pb2, 2),
                              'pe3': round(pe3, 2), 'pb3': round(pb3, 2),
                              'pe4': round(pe4, 2), 'pb4': round(pb4, 2), }
    return ret_dict


def get_index_list_pe_pb(code_list, start_date=None, end_date=None):
    # 返回字典，key为code，value为dataframe
    # code_list中成立最久的放在最前面
    if start_date is None:
        start_date = date(2005, 1, 4)
    if end_date is None:
        end_date = pd.datetime.today() - timedelta(1)
    x = get_price(code_list[0], start_date=start_date, end_date=end_date, frequency='daily', fields='close')
    date_list = x.index.tolist()
    index_list_dict = {}
    for code in code_list:
        index_list_dict[code] = pd.DataFrame(index=date_list, data=NaN,
                                             columns=['pe1', 'pb1', 'pe2', 'pb2', 'pe3', 'pb3', 'pe4', 'pb4'])
    for d in date_list:  # 交易日
        ret_dict = get_index_list_pe_pb_date(code_list, d)
        for key in ret_dict:
            index_list_dict[key].loc[d]['pe1'] = ret_dict[key]['pe1']
            index_list_dict[key].loc[d]['pb1'] = ret_dict[key]['pb1']
            index_list_dict[key].loc[d]['pe2'] = ret_dict[key]['pe2']
            index_list_dict[key].loc[d]['pb2'] = ret_dict[key]['pb2']
            index_list_dict[key].loc[d]['pe3'] = ret_dict[key]['pe3']
            index_list_dict[key].loc[d]['pb3'] = ret_dict[key]['pb3']
            index_list_dict[key].loc[d]['pe4'] = ret_dict[key]['pe4']
            index_list_dict[key].loc[d]['pb4'] = ret_dict[key]['pb4']
    return index_list_dict


def get_idx_name(idx):
    all_index = get_all_securities(['index'])
    idx_name_map = {'hscei': u'恒生国企', 'hsi': u'恒生指数', u'中证全指证券公司指数(四级行业)': u'证券公司', u'红利指数': u'上证红利',
                    u'中证1000指数': u'中证1000', u'中证银行指数': u'中证银行'}
    if idx in idx_name_map:
        return idx_name_map[idx]
    else:
        name = all_index.loc[idx].display_name
        if name in idx_name_map:
            return idx_name_map[name]
        else:
            return name


def ffloat(data_in):
    return '%.2f' % (data_in)


def get_hk_lixinger(idx='hsi'):
    # 如需要使用理性人的数据，请各位自己申请
    idx_map = {'hsi': '10001', 'hscei': '10002'}
    lixinger = requests.Session()
    url = 'https://open.lixinger.com/api/h/indice/fundamental'
    payload = {'token': 'xxxxxx',  # 各位自己申请
               "date": "latest",
               "metrics": ["pe_ttm.y_10.equalAvg", "pb.y_10.equalAvg", "dyr.weightedAvg"],
               "stockCodes": [idx_map[idx]]}
    try:
        r = lixinger.post(url, json=payload)
        data_dict = r.json()
    except:
        return None
    if 'code' in data_dict and data_dict['code'] == 0:
        if 'data' in data_dict:
            return data_dict['data'][0]
    else:
        return None
    return data_dict


def idx_analysis(idx_dict, data_root='./'):
    '''新版指数估值分析'''
    index_list = idx_dict.keys()
    pe_results = []
    pe_code_list = []
    pb_results = []
    pb_code_list = []
    # 沪深
    PE = 'pe2'
    PB = 'pb2'
    div_obj = Dividend()
    for code in index_list:
        data_path = '%s%s_pe_pb.csv' % (data_root, convert_code(code))
        index_name = get_idx_name(code)
        df_pe_pb = pd_read_csv(data_path)
        df_pe_pb = df_pe_pb[df_pe_pb.iloc[-1].name.date() - timedelta(365 * 10):]  # 最长十年的数据
        if len(df_pe_pb) < 250 * 3:  # 每年250个交易日,小于3年不具有参考价值
            #                 print code, 'samples:', len(df_pe_pb), index_name
            continue
        pe_ratio = round(len(df_pe_pb[PE][df_pe_pb[PE] < df_pe_pb.iloc[-1][PE]]) / float(len(df_pe_pb[PE])) * 100, 2)
        pb_ratio = round(len(df_pe_pb[PB][df_pe_pb[PB] < df_pe_pb.iloc[-1][PB]]) / float(len(df_pe_pb[PB])) * 100, 2)
        score, state = calc_idx_state(code, df_pe_pb.iloc[-1][PE], pe_ratio, df_pe_pb.iloc[-1][PB], pb_ratio)
        pe_results.append([index_name, ffloat(df_pe_pb.iloc[-1][PE]), pe_ratio, ffloat(df_pe_pb.iloc[-1][PB]), pb_ratio,
                           score, state,
                           df_pe_pb.iloc[0].name.date().strftime('%Y')])

        pb_results.append([index_name, ffloat(1 / df_pe_pb.iloc[-1][PE] * 100),
                           ffloat(df_pe_pb['pb1'][-1] / df_pe_pb['pe1'][-1] * 100),
                           ffloat(div_obj.get_idx_dividend(code)), ffloat(calc_volatility(code) * 100),
                           idx_dict[code][0], idx_dict[code][1], score])

        pe_code_list.append(code)
        pb_code_list.append(code)
    #     港股
    hk_dict = {'hsi': ['159920', '000071'], 'hscei': ['510900', '110031']}
    for code in hk_dict:
        hk_data = get_hk_lixinger(code)
        if hk_data is None:
            continue
        if hk_data['dyr'][u'weightedAvg'] is None:
            dividend_r = 0.0
        else:
            dividend_r = hk_data['dyr'][u'weightedAvg']
        index_name = get_idx_name(code)
        pe = hk_data[u'pe_ttm']['y_10'][u'equalAvg'][u'latestVal']
        pb = hk_data[u'pb']['y_10'][u'equalAvg'][u'latestVal']
        pe_pos = hk_data[u'pe_ttm']['y_10'][u'equalAvg'][u'latestValPos'] * 100
        pb_pos = hk_data[u'pb']['y_10'][u'equalAvg'][u'latestValPos'] * 100
        score, state = calc_idx_state(code, pe, pe_pos, pb, pb_pos)
        pe_results.append([index_name, ffloat(pe), round(pe_pos, 2),
                           ffloat(pb), ffloat(pb_pos), score, state,
                           str(int(hk_data['date'][:4]) - 10)])
        pb_results.append([index_name, ffloat(1 / pe * 100), ffloat(pb / pe * 100),
                           ffloat(dividend_r * 100),
                           ffloat(calc_volatility(code) * 100),
                           hk_dict[code][0], hk_dict[code][1], score])
        pe_code_list.append(code.upper())
        pb_code_list.append(code.upper())

    date_str = df_pe_pb.iloc[-1].name.date().strftime('%Y%m%d')
    pe_columns = [u'名称', u'市盈率', u'百分位', u'市净率', u'PB百分位', u'sort', u'综合估值', u'起始']
    pe_df = pd.DataFrame(data=pe_results, index=pe_code_list, columns=pe_columns)
    pe_df.index = pe_df[u'名称']
    del pe_df[u'名称']
    pe_df.index.name = date_str

    pb_columns = [u'名称', u'收益率', u'ROE', u'股息率', u'波动率', u'场内基金', u'场外基金', u'sort']
    pb_df = pd.DataFrame(data=pb_results, index=pb_code_list, columns=pb_columns)
    pb_df.index = pb_df[u'名称']
    del pb_df[u'名称']
    pb_df.index.name = date_str

    # 先排序，然后删除排序标识
    pe_df = pe_df.sort_values(['sort'], ascending=True)
    pb_df = pb_df.sort_values(['sort'], ascending=True)
    del pe_df['sort']
    del pb_df['sort']

    return (pe_df, pb_df)


def calc_idx_state(idx, pe, pe_ratio, pb, pb_ratio):
    # 计算指数的估值状态
    idx_dict = {
        #     '000300.XSHG':[0.5,0.5],'000905.XSHG':[0.5,0.5],'000852.XSHG':[0.5,0.5],
        #     '399006.XSHE':[0.5,0.5],'399005.XSHE':[0.5,0.5],#宽指数
        #     '000985.XSHG':[0.5,0.5],#中证全指
        #     '000015.XSHG':[0.2,0.8],'000922.XSHG':[0.8,0.2],'000827.XSHG':[0.8,0.2],#策略指数
        #     '000990.XSHG':[0.8,0.2],'000991.XSHG':[0.8,0.2],'000993.XSHG':[0.8,0.2],#全指消费、医药、信息
        #     '399986.XSHE':[0.2,0.8],'399975.XSHE':[0.2,0.8], #银行、证券
        #     '399330.XSHE':[0.8,0.2],#深证100
        #     '000925.XSHG':[0.2,0.8],#基本面50

        ##Add By Laye
        ## 宽基指数
        '000985.XSHG': [0.5, 0.5],  # 中证全指
        '000300.XSHG': [0.5, 0.5],  # 沪深300
        '000905.XSHG': [0.5, 0.5],  # 中证500
        '000852.XSHG': [0.5, 0.5],  # 中证1000
        ##
        ## 大盘指数
        '000016.XSHG': [0.5, 0.5],  # 上证50
        '000922.XSHG': [0.5, 0.5],  # 中证红利
        ##
        ## 小盘指数
        '399006.XSHE': [0.8, 0.2],  # 创业板指
        '399005.XSHE': [0.8, 0.2],  # 中小板指
        ##
        ## 主题指数
        '399812.XSHE': [0.8, 0.2],  # 中证养老
        '000933.XSHG': [0.8, 0.2],  # 中证医药
        '000990.XSHG': [0.8, 0.2],  # 全指消费
        '000993.XSHG': [0.8, 0.2],  # 全指信息
        '399971.XSHE': [0.8, 0.2],  # 中证传媒
        '000827.XSHG': [0.8, 0.2],  # 中证环保
        '399975.XSHE': [0.5, 0.5],  # 证券公司
    }

    def calc_state(score):
        # 根据score计算估值
        if score < 10.0:
            return u'极度低估'
        elif 10 <= score and score < 20:
            return u'低估'
        elif 20 <= score and score < 40:
            return u'正常偏低'
        elif 40 <= score and score < 60:
            return u'正常'
        elif 60 <= score and score < 80:
            return u'正常偏高'
        elif 80 <= score and score < 90:
            return u'高估'
        elif 90 <= score:
            return u'极度高估'

    if idx in idx_dict:
        weight = idx_dict[idx]
    else:
        weight = [0.5, 0.5]
    score = weight[0] * pe_ratio + weight[1] * pb_ratio
    #     print weight, score, weight[0]*pe_ratio, weight[1]*pb_ratio
    return [score, calc_state(score)]


def update_hs_data(idx_dict, data_root='./'):
    index_list = list(idx_dict.keys())
    data_path = '%s%s_pe_pb.csv' % (data_root, convert_code(index_list[0]))
    if os.path.exists(data_path):  # 增量更新,只判断列表中第一个
        df = pd_read_csv(data_path)
        start_date = df.iloc[-1].name + timedelta(1)
        df_pe_pb = get_index_list_pe_pb(index_list, start_date)
        for key in df_pe_pb:
            df = pd_read_csv('%s%s_pe_pb.csv' % (data_root, convert_code(key)))
            delta_df = df_pe_pb[key][df.iloc[-1].name + timedelta(1):]  # 多个指数数据有可能不同步
            if len(delta_df) > 0:
                df_pe_pb[key] = pd.concat([df, delta_df])
            else:
                df_pe_pb[key] = df
    else:
        print('init')
        df_pe_pb = get_index_list_pe_pb(index_list)

    for key in df_pe_pb:
        data_path = '%s%s_pe_pb.csv' % (data_root, convert_code(key))
        df_pe_pb[key].dropna().to_csv(data_path)


idx_dict = {
    #     '000300.XSHG':['510300','160706'],'000905.XSHG':['510500','160119'],'000852.XSHG':['512100','004194'],
    #     '399006.XSHE':['159915','110026'],'399005.XSHE':['159902','163111'],#宽指数
    #     '000985.XSHG':['-','-'],#中证全指
    #     '000015.XSHG':['510880','-'],'000922.XSHG':['-','100032'],'000827.XSHG':['512580','0001064'],#策略指数
    #     '000990.XSHG':['159946','001458'],'000991.XSHG':['159938','001180'],'000993.XSHG':['159939','002974'],#全指消费、医药、信息
    #     '399986.XSHE':['512800','001594'],'399975.XSHE':['512880','-'], #银行、证券
    #     '399330.XSHE':['159901','161227'],#深证100
    #     '000925.XSHG':['160716','160716'],#基本面50

    ##Add By Laye
    ## 宽基指数
    '000985.XSHG': ['-', '-'],  # 中证全指
    '000300.XSHG': ['510300', '160706'],  # 沪深300
    '000905.XSHG': ['510500', '160119'],  # 中证500
    '000852.XSHG': ['512100', '004194'],  # 中证1000
    ##
    ## 大盘指数
    '000016.XSHG': ['510050', '-'],  # 上证50
    '000922.XSHG': ['-', '100032'],  # 中证红利
    ##
    ## 小盘指数
    '399006.XSHE': ['159915', '110026'],  # 创业板指
    '399005.XSHE': ['159902', '163111'],  # 中小板指
    ##
    ## 主题指数
    '399812.XSHE': ['-', '000968'],  # 中证养老
    '000933.XSHG': ['-', '001180'],  # 中证医药
    '000990.XSHG': ['159946', '001458'],  # 全指消费
    '000993.XSHG': ['159939', '002974'],  # 全指信息
    '399971.XSHE': ['512980', '-'],  # 中证传媒
    '000827.XSHG': ['512580', '001064'],  # 中证环保
    '399975.XSHE': ['512880', '-'],  # 证券公司
}

update_hs_data(idx_dict)
(value_df, fund_df) = idx_analysis(idx_dict)
