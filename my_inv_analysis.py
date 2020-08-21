# 运行我的资产分析

import my_inv
import datetime
import jqdatasdk as jq

# 数据准备
excelPath = './res/资产明细表_202007.xlsx'
my_investment_analysis = my_inv.MyInvestmentAnalysis()
my_investment_analysis.data_preparation(excelPath)


# # 分析目前比较基准已经有的涨幅
# jq.auth('18500150123', 'YanTeng881128')
# profit_calculate_stock_dict = {'沪深300': '000300.XSHG',
#                                '中证500': '000905.XSHG',
#                                '上证50': '000016.XSHG',
#                                '中证红利': '000922.XSHG',
#                                '创业板指': '399006.XSHE',
#                                '中证养老': '399812.XSHE',
#                                '全指医药': '000933.XSHG',
#                                '全指消费': '000990.XSHG',
#                                '中证传媒': '399971.XSHE',
#                                '中证环保': '000827.XSHG',
#                                '证券公司': '399975.XSHE',
#                                '全指金融': '000992.XSHG'
#                                }
#
# profit_df = my_investment_analysis.analyze_profit(profit_calculate_stock_dict, datetime.date(2019, 3, 1),
#                                                   datetime.date(2020, 8, 17))
# print(profit_df)

# 给定期间内，投资项目利润、利润率柱状图
# my_investment_analysis.calculate_inv_profit_ratio('2019-07', '2019-10')

# # 股票占比分析
# investment_item_list = ['50ETF-510050', 'H股ETF-510900', '中欧价值发现混合-166005',
#                         '传媒ETF-512980', '兴全可转债混合-340001', '创业板100-159915',
#                         '富国中证红利-100032', '广发中证全指金融地产-001469', '广发中证养老-000968',
#                         '广发中证医药-001180', '广发中证环保-001064',
#                         '建信/富国中证500指数增强/天弘500增强私募 - 000478/161017', '招商股票+现金',
#                         '易方达安心回报债券A-110027', '易方达消费行业股票-110022', '易方达证券公司指数分级-502010',
#                         '汇添富价值精选混合-519069', '申万沪深300增强-310318', '华宝油气-162411']
#
# df_result = my_investment_analysis.pie_by_given_investment_item(investment_item_list)
# print(df_result)

# 运行我的资产report
for x in range(0, 6):
    my_investment_analysis.line_by_category_total_amount(x)
    my_investment_analysis.line_profit_by_category(x)

for x in range(1, 6):
    my_investment_analysis.pie_by_category(x)



