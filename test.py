import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('TkAgg')

mpl.rcParams[u'font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

df_result = pd.read_excel("./res/temp.xlsx", index_col=0)

# item_name = df_result['项目名称'].values
# profit = df_result['本期利润'].values
# plt.bar(item_name, profit)
# plt.xticks(rotation=45)

# df_result.plot.bar(x='项目名称', y='本期利润', subplots=True)
axes = df_result.plot.bar(rot=45, subplots=True)




plt.show()
