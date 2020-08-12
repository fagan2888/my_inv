# 我的资产分析类定义
import jqdatasdk as jq
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame


class MyInvestmentAnalysis:
    def __init__(self):
        jq.auth('18500150123', 'YanTeng881128')

    @staticmethod
    def read_data(excel_path):
        balance_raw_data = pd.read_excel(excel_path, sheet_name='月度资产明细')
        transaction_raw_data = pd.read_excel(excel_path, sheet_name='交易明细（不包括固定收益）')
        master_raw_data = pd.read_excel(excel_path, sheet_name='主数据')
        return balance_raw_data, transaction_raw_data, master_raw_data

    @staticmethod
    def data_trim(balance_raw_data, transaction_raw_data, master_raw_data):
        # 数据清理 - 保留所有分类，只显示总额
        all_category_balance = balance_raw_data.loc[:, '期间':'项目名称']
        all_category_balance.insert(8, '金额', balance_raw_data.iloc[:, -1])

        # 数据清理 - 保留交易信息
        all_category_transaction = transaction_raw_data

        # 数据清理 - 只保留主数据部分
        master_data = master_raw_data.iloc[:, 0:6]
        master_data.rename(columns=master_data.iloc[0], inplace=True)
        master_data.drop(0, inplace=True)
        return all_category_balance, all_category_transaction, master_data

    # 资产总额曲线: 第二个参数：1-一级分类；2-二级分类；3-三级分类；4-四级分类；5-辅助分类; 0-总额（默认）
    @staticmethod
    def line_by_category_total_amount(all_category_balance, category_type=0):
        if category_type == 1:
            group_by_period = all_category_balance.groupby(['期间', '一级分类']).sum()
            group_by_period = group_by_period.unstack()
            group_by_period.columns = group_by_period.columns.levels[1]

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(group_by_period, marker='o')
            plt.legend(group_by_period.columns)
            plt.title('一级分类资产总额曲线')
            plt.show()
        elif category_type == 2:
            group_by_period = all_category_balance.groupby(['期间', '二级分类']).sum()
            group_by_period = group_by_period.unstack()
            group_by_period.columns = group_by_period.columns.levels[1]

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(group_by_period, marker='o')
            plt.legend(group_by_period.columns)
            plt.title('二级分类资产总额曲线')
            plt.show()
        elif category_type == 3:
            group_by_period = all_category_balance.groupby(['期间', '三级分类']).sum()
            group_by_period = group_by_period.unstack()
            group_by_period.columns = group_by_period.columns.levels[1]

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(group_by_period, marker='o')
            plt.legend(group_by_period.columns)
            plt.title('三级分类资产总额曲线')
            plt.show()
        elif category_type == 4:
            group_by_period = all_category_balance.groupby(['期间', '四级分类']).sum()
            group_by_period = group_by_period.unstack()
            group_by_period.columns = group_by_period.columns.levels[1]

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(group_by_period, marker='o')
            plt.legend(group_by_period.columns)
            plt.title('四级分类资产总额曲线')
            plt.show()
        elif category_type == 5:
            group_by_period = all_category_balance.groupby(['期间', '辅助分类']).sum()
            group_by_period = group_by_period.unstack()
            group_by_period.columns = group_by_period.columns.levels[1]

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(group_by_period, marker='o')
            plt.legend(group_by_period.columns)
            plt.title('辅助分类资产总额曲线')
            plt.show()
        else:
            group_by_period = all_category_balance.groupby(['期间'])
            df_group_by_period_sum = DataFrame(group_by_period['金额'].sum())

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(df_group_by_period_sum, marker='o')
            plt.legend(df_group_by_period_sum.columns)
            plt.title('资产总额曲线')
            for index, row in df_group_by_period_sum.iterrows():
                plt.text(index, row['金额'], row['金额'], ha='center', va='bottom')
            plt.show()

    # 最近期间的分类饼状图: 第二个参数：1-一级分类；2-二级分类；3-三级分类；4-四级分类；5-辅助分类(默认);
    @staticmethod
    def pie_by_category(all_category_balance, category_type=5):
        if category_type == 1:
            fuzhu_category_by_period_balance = all_category_balance.groupby(['期间', '一级分类']).sum()
            fuzhu_category_by_period_balance = fuzhu_category_by_period_balance.unstack()
            fuzhu_category_by_period_balance.columns = fuzhu_category_by_period_balance.columns.levels[1]

            result_df = fuzhu_category_by_period_balance.iloc[-1].dropna()
            fig = plt.figure(figsize=(10, 10))
            plt.title('一级分类饼状图')
            plt.pie(result_df,
                    labels=result_df.index,
                    startangle=90,
                    shadow=False,
                    autopct='%1.1f%%')
        elif category_type == 2:
            fuzhu_category_by_period_balance = all_category_balance.groupby(['期间', '二级分类']).sum()
            fuzhu_category_by_period_balance = fuzhu_category_by_period_balance.unstack()
            fuzhu_category_by_period_balance.columns = fuzhu_category_by_period_balance.columns.levels[1]

            result_df = fuzhu_category_by_period_balance.iloc[-1].dropna()

            fig = plt.figure(figsize=(10, 10))
            plt.title('二级分类饼状图')
            plt.pie(result_df,
                    labels=result_df.index,
                    startangle=90,
                    shadow=False,
                    autopct='%1.1f%%')
        elif category_type == 3:
            fuzhu_category_by_period_balance = all_category_balance.groupby(['期间', '三级分类']).sum()
            fuzhu_category_by_period_balance = fuzhu_category_by_period_balance.unstack()
            fuzhu_category_by_period_balance.columns = fuzhu_category_by_period_balance.columns.levels[1]

            result_df = fuzhu_category_by_period_balance.iloc[-1].dropna()
            fig = plt.figure(figsize=(10, 10))
            plt.title('三级分类饼状图')
            plt.pie(result_df,
                    labels=result_df.index,
                    startangle=90,
                    shadow=False,
                    autopct='%1.1f%%')
        elif category_type == 4:
            fuzhu_category_by_period_balance = all_category_balance.groupby(['期间', '四级分类']).sum()
            fuzhu_category_by_period_balance = fuzhu_category_by_period_balance.unstack()
            fuzhu_category_by_period_balance.columns = fuzhu_category_by_period_balance.columns.levels[1]

            result_df = fuzhu_category_by_period_balance.iloc[-1].dropna()
            fig = plt.figure(figsize=(10, 10))
            plt.title('四级分类饼状图')
            plt.pie(result_df,
                    labels=result_df.index,
                    startangle=90,
                    shadow=False,
                    autopct='%1.1f%%')
        else:
            fuzhu_category_by_period_balance = all_category_balance.groupby(['期间', '辅助分类']).sum()
            fuzhu_category_by_period_balance = fuzhu_category_by_period_balance.unstack()
            fuzhu_category_by_period_balance.columns = fuzhu_category_by_period_balance.columns.levels[1]

            result_df = fuzhu_category_by_period_balance.iloc[-1].dropna()
            fig = plt.figure(figsize=(10, 10))
            plt.title('辅助分类饼状图')
            plt.pie(result_df,
                    labels=result_df.index,
                    startangle=90,
                    shadow=False,
                    autopct='%1.1f%%')

    # 建立利润计算DF - 每次都重新计算
    @staticmethod
    def build_profit_df(all_category_balance, all_category_transcation, master_data):
        # 整理masterData，保留利润有意义的部分四级分类：
        # '可转债基金','A股-大股票指数'，'A股-小股票指数','A股-主题指数','成熟市场指数','主动股票基金',
        profit_list = ['可转债基金', 'A股-大股票指数', 'A股-小股票指数',
                      'A股-主题指数', '成熟市场指数', '主动股票基金']
        profitMasterData = master_data.iloc[:, 0:5]
        profitMasterData = profitMasterData.drop_duplicates()

        profitMasterData = profitMasterData.loc[master_data['四级分类'].isin(profit_list)]

        target_df = profitMasterData
        periodList = all_category_balance.loc[:, '期间'].drop_duplicates().tolist()
        profitMasterData.insert(0, '期间', np.nan)

        # 补全期间
        for tempPeriod in periodList:
            profitDF = profitMasterData.fillna(tempPeriod)
            profitMasterData = pd.concat([profitDF, target_df], axis=0)

        profitMasterData.dropna(inplace=True)

        # 填入对应的期初期末金额
        periodCategory_sum = all_category_balance.groupby(['期间', '四级分类']).sum()

        # 填入期初，期末金额
        profitMasterData.insert(len(profitMasterData.columns), '期末金额', np.nan)
        profitMasterData.insert(len(profitMasterData.columns) - 1, '期初金额', np.nan)

        currentPeroid = np.nan
        previousPeriod = np.nan
        firstTime = True
        for index, row in periodCategory_sum.iterrows():
            if firstTime == True:
                currentPeroid = index[0]
                firstTime = False
            profitMasterData.loc[(profitMasterData['期间'] == index[0]) &
                                 (profitMasterData['四级分类'] == index[1]), '期末金额'] = row['金额']

            if currentPeroid != index[0]:
                previousPeriod = currentPeroid
                currentPeroid = index[0]
            profitMasterData.loc[(profitMasterData['期间'] == index[0]) &
                                 (profitMasterData['四级分类'] == index[1]), '期初金额'] = profitMasterData.loc[
                (profitMasterData['期间'] == previousPeriod) &
                (profitMasterData['四级分类'] == index[1]), '期末金额']

        # 填入本期变动
        profitMasterData.insert(len(profitMasterData.columns) - 1, '本期变动', np.nan)
        periodCategory_change_sum = all_category_transcation.groupby(['期间', '四级分类']).sum()
        for index, row in periodCategory_change_sum.iterrows():
            profitMasterData.loc[(profitMasterData['期间'] == index[0]) &
                                 (profitMasterData['四级分类'] == index[1]), '本期变动'] = row['买入／卖出金额']

        profitMasterData.fillna(0, inplace=True)

        # 计算利润及利润率
        profitMasterData.insert(len(profitMasterData.columns), '本期利润',
                                (profitMasterData.loc[:, '期末金额'] - profitMasterData.loc[:, '期初金额'] -
                                 profitMasterData.loc[:, '本期变动']))
        profitMasterData.insert(len(profitMasterData.columns), '利润率',
                                (profitMasterData.loc[:, '本期利润'] / profitMasterData.loc[:, '期初金额']))

        # 最终整理数据并返回
        profitMasterData.reset_index(inplace=True, drop=True)
        profitDF = profitMasterData
        return profitDF

    # 分类利润率曲线: 第二个参数：1-一级分类；2-二级分类；3-三级分类；4-四级分类；5-辅助分类; 0-总额（默认）
    def lineProfitByCategory(self, buildProfitDF, categoryType=0):
        if categoryType == 1:
            profitByCategory = buildProfitDF.groupby(['期间', '一级分类']).sum()
            profitByCategory.loc[:, '利润率'] = profitByCategory.loc[:, '本期利润'] / profitByCategory.loc[:, '期初金额']
            profitByCategory = profitByCategory['利润率']
            profitByCategory = profitByCategory.unstack()

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(profitByCategory, marker='o')
            plt.legend(profitByCategory.columns)
            plt.title('一级分类利润率曲线')
            plt.show()
        elif categoryType == 2:
            profitByCategory = buildProfitDF.groupby(['期间', '二级分类']).sum()
            profitByCategory.loc[:, '利润率'] = profitByCategory.loc[:, '本期利润'] / profitByCategory.loc[:, '期初金额']
            profitByCategory = profitByCategory['利润率']
            profitByCategory = profitByCategory.unstack()

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(profitByCategory, marker='o')
            plt.legend(profitByCategory.columns)
            plt.title('二级分类利润率曲线')
            plt.show()
        elif categoryType == 3:
            profitByCategory = buildProfitDF.groupby(['期间', '三级分类']).sum()
            profitByCategory.loc[:, '利润率'] = profitByCategory.loc[:, '本期利润'] / profitByCategory.loc[:, '期初金额']
            profitByCategory = profitByCategory['利润率']
            profitByCategory = profitByCategory.unstack()

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(profitByCategory, marker='o')
            plt.legend(profitByCategory.columns)
            plt.title('三级分类利润率曲线')
            plt.show()
        elif categoryType == 4:
            profitByCategory = buildProfitDF.groupby(['期间', '四级分类']).sum()
            profitByCategory.loc[:, '利润率'] = profitByCategory.loc[:, '本期利润'] / profitByCategory.loc[:, '期初金额']
            profitByCategory = profitByCategory['利润率']
            profitByCategory = profitByCategory.unstack()

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(profitByCategory, marker='o')
            plt.legend(profitByCategory.columns)
            plt.title('四级分类利润率曲线')
            plt.show()
        elif categoryType == 5:
            profitByCategory = buildProfitDF.groupby(['期间', '辅助分类']).sum()
            profitByCategory.loc[:, '利润率'] = profitByCategory.loc[:, '本期利润'] / profitByCategory.loc[:, '期初金额']
            profitByCategory = profitByCategory['利润率']
            profitByCategory = profitByCategory.unstack()

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(profitByCategory, marker='o')
            plt.legend(profitByCategory.columns)
            plt.title('辅助分类利润率曲线')
            plt.show()
        else:
            profitByCategory = buildProfitDF.groupby(['期间']).sum()
            profitByCategory.loc[:, '利润率'] = profitByCategory.loc[:, '本期利润'] / profitByCategory.loc[:, '期初金额']
            profitByCategory = profitByCategory['利润率']

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(profitByCategory, marker='o')
            plt.title('总金额利润率曲线')
            plt.show()

            # 返回选定的项目名称按期间余额

    def buildInvestmentItemDF(self, allCategory_balance, investmentItemList):
        investmentItemDF = allCategory_balance.loc[allCategory_balance.loc[:, '项目名称'].isin(investmentItemList)]
        investmentItemDF.reset_index(inplace=True, drop=True)
        return investmentItemDF

    # 打印选定投资项目范围饼状图
    def pieByGivenInvestmentItem(self, investmentItemDF):
        lastPeriodInvestmentItemDF = investmentItemDF.loc[investmentItemDF.loc[:, '期间']
                                                          == investmentItemDF.iloc[-1].loc['期间']].loc[:, ['项目名称', '金额']]
        lastPeriodInvestmentItemDF.set_index('项目名称', inplace=True)
        lastPeriodInvestmentItemDF.fillna(0)

        fig = plt.figure(figsize=(15, 15))
        plt.title('选定投资项目饼状图 - 选定总金额：' + str(lastPeriodInvestmentItemDF['金额'].sum()))
        plt.pie(lastPeriodInvestmentItemDF,
                labels=lastPeriodInvestmentItemDF.index,
                startangle=90,
                shadow=False,
                autopct='%1.1f%%')

        ##计算比例并添加到DF中
        amountSum = lastPeriodInvestmentItemDF['金额'].sum()
        lastPeriodInvestmentItemDF.insert(len(lastPeriodInvestmentItemDF.columns), '占比',
                                          lastPeriodInvestmentItemDF.loc[:, '金额'] / amountSum)

        lastPeriodInvestmentItemDF['占比'] = lastPeriodInvestmentItemDF['占比'].apply(lambda x: format(x, '.2%'))

        lastPeriodInvestmentItemDF = lastPeriodInvestmentItemDF.sort_values('占比')
        return lastPeriodInvestmentItemDF

    # 打印自给定日期起至当前的指数增长率
    def analyzeProfit(self, profit_calculate_stock_dict, start_date, end_date):
        # 构建结果df
        df = pd.DataFrame(index=profit_calculate_stock_dict.keys(), columns=[start_date, end_date, "Incresment Ratio"])
        for index, row in df.iterrows():
            row[start_date] = \
                jq.get_price(profit_calculate_stock_dict[index], count=1, end_date=start_date, frequency='daily',
                             fields=['close']).iloc[0, 0]
            row[end_date] = \
                jq.get_price(profit_calculate_stock_dict[index], count=1, end_date=end_date, frequency='daily',
                             fields=['close']).iloc[0, 0]
            row["Increment Ratio"] = '{:.2f}%'.format((row[end_date] - row[start_date]) / row[start_date] * 100)
        return df
