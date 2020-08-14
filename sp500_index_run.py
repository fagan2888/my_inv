from sp500_index import *

# get price; default start date is 2010-01-01
df_price = Spx.hist_data('price', start_date='1990-01-01')

# get pe; default start date is 2010-01-01
df_pe = Spx.hist_data('pe', start_date='1990-01-01')

# get Dividend Yield by Year
# df_dyy = Spx.hist_data('dyr')

result_df = df_price.join(df_pe)

writer = pd.ExcelWriter('./res/sp500_index_price_pe.xlsx')
result_df.to_excel(writer)
writer.save()

pass
