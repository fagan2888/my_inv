# 我的资产分析类定义
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame


def read_data(excel_path):
    balanceRawData = pd.read_excel(excel_path, sheet_name='月度资产明细')
    transactionRawData = pd.read_excel(excel_path, sheet_name='交易明细（不包括固定收益）')
    masterRawData = pd.read_excel(excel_path, sheet_name='主数据')
    return (balanceRawData, transactionRawData, masterRawData)


class MyInvestmentAnalysis:

    def dataTrim(self, balanceRawData, transactionRawData, masterRawData):
        # 数据清理 - 保留所有分类，只显示总额
        allCategory_balance = balanceRawData.loc[:, '期间':'项目名称']
        allCategory_balance.insert(8, '金额', balanceRawData.iloc[:, -1])

        # 数据清理 - 保留交易信息
        allCategory_transcation = transactionRawData

        # 数据清理 - 只保留主数据部分
        masterData = masterRawData.iloc[:, 0:6]
        masterData.rename(columns=masterData.iloc[0], inplace=True)
        masterData.drop(0, inplace=True)
        return (allCategory_balance, allCategory_transcation, masterData)

    # 资产总额曲线: 第二个参数：1-一级分类；2-二级分类；3-三级分类；4-四级分类；5-辅助分类; 0-总额（默认）
    def lineByCategoryTotalAmount(self, allCategory_balance, categoryType=0):
        if categoryType == 1:
            groupByPeriod = allCategory_balance.groupby(['期间', '一级分类']).sum()
            groupByPeriod = groupByPeriod.unstack()
            groupByPeriod.columns = groupByPeriod.columns.levels[1]

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(groupByPeriod, marker='o')
            plt.legend(groupByPeriod.columns)
            plt.title('一级分类资产总额曲线')
            plt.show()
        elif categoryType == 2:
            groupByPeriod = allCategory_balance.groupby(['期间', '二级分类']).sum()
            groupByPeriod = groupByPeriod.unstack()
            groupByPeriod.columns = groupByPeriod.columns.levels[1]

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(groupByPeriod, marker='o')
            plt.legend(groupByPeriod.columns)
            plt.title('二级分类资产总额曲线')
            plt.show()
        elif categoryType == 3:
            groupByPeriod = allCategory_balance.groupby(['期间', '三级分类']).sum()
            groupByPeriod = groupByPeriod.unstack()
            groupByPeriod.columns = groupByPeriod.columns.levels[1]

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(groupByPeriod, marker='o')
            plt.legend(groupByPeriod.columns)
            plt.title('三级分类资产总额曲线')
            plt.show()
        elif categoryType == 4:
            groupByPeriod = allCategory_balance.groupby(['期间', '四级分类']).sum()
            groupByPeriod = groupByPeriod.unstack()
            groupByPeriod.columns = groupByPeriod.columns.levels[1]

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(groupByPeriod, marker='o')
            plt.legend(groupByPeriod.columns)
            plt.title('四级分类资产总额曲线')
            plt.show()
        elif categoryType == 5:
            groupByPeriod = allCategory_balance.groupby(['期间', '辅助分类']).sum()
            groupByPeriod = groupByPeriod.unstack()
            groupByPeriod.columns = groupByPeriod.columns.levels[1]

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(groupByPeriod, marker='o')
            plt.legend(groupByPeriod.columns)
            plt.title('辅助分类资产总额曲线')
            plt.show()
        else:
            groupByPeriod = allCategory_balance.groupby(['期间'])
            df_groupByPeriod_sum = DataFrame(groupByPeriod['金额'].sum())

            fig = plt.figure()
            ax = fig.add_axes([0.1, 0.1, 2, 1])
            plt.plot(df_groupByPeriod_sum, marker='o')
            plt.legend(df_groupByPeriod_sum.columns)
            plt.title('资产总额曲线')
            for index, row in df_groupByPeriod_sum.iterrows():
                plt.text(index, row['金额'], row['金额'], ha='center', va='bottom')
            plt.show()

    # 最近期间的分类饼状图: 第二个参数：1-一级分类；2-二级分类；3-三级分类；4-四级分类；5-辅助分类(默认);
    def pieByCategory(self, allCategory_balance, categoryType=5):
        if categoryType == 1:
            fuzhuCategoryByPeriod_balance = allCategory_balance.groupby(['期间', '一级分类']).sum()
            fuzhuCategoryByPeriod_balance = fuzhuCategoryByPeriod_balance.unstack()
            fuzhuCategoryByPeriod_balance.columns = fuzhuCategoryByPeriod_balance.columns.levels[1]

            result_DF = fuzhuCategoryByPeriod_balance.iloc[-1].dropna()
            fig = plt.figure(figsize=(10, 10))
            plt.title('一级分类饼状图')
            plt.pie(result_DF,
                    labels=result_DF.index,
                    startangle=90,
                    shadow=False,
                    autopct='%1.1f%%')
        elif categoryType == 2:
            fuzhuCategoryByPeriod_balance = allCategory_balance.groupby(['期间', '二级分类']).sum()
            fuzhuCategoryByPeriod_balance = fuzhuCategoryByPeriod_balance.unstack()
            fuzhuCategoryByPeriod_balance.columns = fuzhuCategoryByPeriod_balance.columns.levels[1]

            result_DF = fuzhuCategoryByPeriod_balance.iloc[-1].dropna()

            fig = plt.figure(figsize=(10, 10))
            plt.title('二级分类饼状图')
            plt.pie(result_DF,
                    labels=result_DF.index,
                    startangle=90,
                    shadow=False,
                    autopct='%1.1f%%')
        elif categoryType == 3:
            fuzhuCategoryByPeriod_balance = allCategory_balance.groupby(['期间', '三级分类']).sum()
            fuzhuCategoryByPeriod_balance = fuzhuCategoryByPeriod_balance.unstack()
            fuzhuCategoryByPeriod_balance.columns = fuzhuCategoryByPeriod_balance.columns.levels[1]

            result_DF = fuzhuCategoryByPeriod_balance.iloc[-1].dropna()
            fig = plt.figure(figsize=(10, 10))
            plt.title('三级分类饼状图')
            plt.pie(result_DF,
                    labels=result_DF.index,
                    startangle=90,
                    shadow=False,
                    autopct='%1.1f%%')
        elif categoryType == 4:
            fuzhuCategoryByPeriod_balance = allCategory_balance.groupby(['期间', '四级分类']).sum()
            fuzhuCategoryByPeriod_balance = fuzhuCategoryByPeriod_balance.unstack()
            fuzhuCategoryByPeriod_balance.columns = fuzhuCategoryByPeriod_balance.columns.levels[1]

            result_DF = fuzhuCategoryByPeriod_balance.iloc[-1].dropna()
            fig = plt.figure(figsize=(10, 10))
            plt.title('四级分类饼状图')
            plt.pie(result_DF,
                    labels=result_DF.index,
                    startangle=90,
                    shadow=False,
                    autopct='%1.1f%%')
        else:
            fuzhuCategoryByPeriod_balance = allCategory_balance.groupby(['期间', '辅助分类']).sum()
            fuzhuCategoryByPeriod_balance = fuzhuCategoryByPeriod_balance.unstack()
            fuzhuCategoryByPeriod_balance.columns = fuzhuCategoryByPeriod_balance.columns.levels[1]

            result_DF = fuzhuCategoryByPeriod_balance.iloc[-1].dropna()
            fig = plt.figure(figsize=(10, 10))
            plt.title('辅助分类饼状图')
            plt.pie(result_DF,
                    labels=result_DF.index,
                    startangle=90,
                    shadow=False,
                    autopct='%1.1f%%')

    # 建立利润计算DF - 每次都重新计算
    def buildProfitDF(self, allCategory_balance, allCategory_transcation, masterData):
        # 整理masterData，保留利润有意义的部分四级分类：
        # '可转债基金','A股-大股票指数'，'A股-小股票指数','A股-主题指数','成熟市场指数','主动股票基金',
        profitList = ['可转债基金', 'A股-大股票指数', 'A股-小股票指数',
                      'A股-主题指数', '成熟市场指数', '主动股票基金']
        profitMasterData = masterData.iloc[:, 0:5]
        profitMasterData = profitMasterData.drop_duplicates()

        profitMasterData = profitMasterData.loc[masterData['四级分类'].isin(profitList)]

        target_df = profitMasterData
        periodList = allCategory_balance.loc[:, '期间'].drop_duplicates().tolist()
        profitMasterData.insert(0, '期间', np.nan)

        # 补全期间
        for tempPeriod in periodList:
            profitDF = profitMasterData.fillna(tempPeriod)
            profitMasterData = pd.concat([profitDF, target_df], axis=0)

        profitMasterData.dropna(inplace=True)

        # 填入对应的期初期末金额
        periodCategory_sum = allCategory_balance.groupby(['期间', '四级分类']).sum()

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
        periodCategory_change_sum = allCategory_transcation.groupby(['期间', '四级分类']).sum()
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
                get_price(profit_calculate_stock_dict[index], count=1, end_date=start_date, frequency='daily',
                          fields=['close']).iloc[0, 0]
            row[end_date] = get_price(profit_calculate_stock_dict[index], count=1, end_date=end_date, frequency='daily',
                                      fields=['close']).iloc[0, 0]
            row["Incresment Ratio"] = '{:.2f}%'.format((row[end_date] - row[start_date]) / row[start_date] * 100)
        return df
