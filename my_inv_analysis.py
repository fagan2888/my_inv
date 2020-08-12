# 运行我的资产分析
import datetime

import my_inv

# 数据准备
excelPath = './res/资产明细表_202007.xlsx'
my_investment_analysis = my_inv.MyInvestmentAnalysis()
(balance_raw_data, transaction_raw_data, master_raw_data) = my_investment_analysis.read_data(excelPath)
(all_category_balance, all_category_transaction, master_data) = my_investment_analysis.data_trim(balance_raw_data,
                                                                                                 transaction_raw_data,
                                                                                                 master_raw_data)
df_profit = my_investment_analysis.build_profit_df(all_category_balance, all_category_transaction, master_data)

# 分析目前比较基准已经有的涨幅
profit_calculate_stock_dict = {'沪深300': '000300.XSHG',
                               '中证500': '000905.XSHG',
                               '上证50': '000016.XSHG',
                               '中证红利': '000922.XSHG',
                               '创业板指': '399006.XSHE',
                               '中证养老': '399812.XSHE',
                               '全指医药': '000933.XSHG',
                               '全指消费': '000990.XSHG',
                               '中证传媒': '399971.XSHE',
                               '中证环保': '000827.XSHG',
                               '证券公司': '399975.XSHE',
                               '全指金融': '000992.XSHG'
                               }

profit_df = my_investment_analysis.analyze_profit(profit_calculate_stock_dict, datetime.date(2019, 3, 1),
                                                  datetime.date(2020, 8, 11))
