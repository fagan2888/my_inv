import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('TkAgg')

df_result = pd.read_excel("./res/sp500_index_price_pe.xlsx", index_col=[0])
df_result.plot()
plt.show()
