import datetime
from scipy import optimize


# 函数
def xnpv(rate, cash_flows):
    return sum([cf / (1 + rate) ** ((t - cash_flows[0][0]).days / 365.0) for (t, cf) in cash_flows])


def xirr(cash_flows, guess=0.1):
    try:
        return optimize.newton(lambda r: xnpv(r, cash_flows), guess)
    except:
        print('Calc Wrong')


# 测试
data = [(datetime.date(2006, 1, 24), -39967), (datetime.date(2008, 2, 6), -19866),
        (datetime.date(2010, 10, 18), 245706), (datetime.date(2013, 9, 14), 52142)]
print(xirr(data))
