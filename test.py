import time

import pandas as pd


# jq.auth('18500150123', 'YanTeng881128')
#
# result = jq.get_all_securities(types=['index'], date=None)
# print(result)

def get_timestamp_from_format_time(format_time):
    struct_time = time.strptime(format_time, '%Y-%m-%d')
    return time.mktime(struct_time)


df = pd.read_excel('./res/sp500_index_price_pe.xlsx', index_col=0)

result = df.index[0]
result = get_timestamp_from_format_time(result)
print(result == datatime('1900-01-01'))
pass
