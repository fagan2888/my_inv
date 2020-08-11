# 2020财务自由分析

from sympy import *


def monthly_payment(total_debt, year_rate, year_duration):
    # 贷款额为a，月利率为i，年利率为I，还款月数为n
    i = year_rate / 12
    n = 12 * year_duration

    return total_debt * i * pow((1 + i), n) / (pow((1 + i), n) - 1)


# setting params
current_stock_value = 680 * 10000  # 当前的股票市值
current_cash = 180 * 10000  # 当前现金
current_shanghai_point = 3300  # 当前上证大盘指数
final_value = 1600 * 10000  # 最终总金额目标
low_risk_investment_return_ratio = 0.08
y1 = 1.5  # 第一阶段年限
y2 = 1.5  # 第二阶段年限

# end of setting params

x = Symbol('x')
y = Symbol('y')

# 计算第二阶段起点市值
result_phase2 = solve([x * (1 + low_risk_investment_return_ratio) ** y2 + 90 * 10000 * y2 - final_value], [x])[x]

# 计算自当前起，还需要上涨的市值（万）
result_real = solve([current_stock_value + y + 90 * 10000 * y1 + current_cash - result_phase2], [y])[y]

print("第一阶段终点股票市值需要增加：" + str(result_real) + "元")
print("第一阶段终点股票还需上涨比例：" + str(result_real / current_stock_value))
print(
    "第一阶段终点按比例上证指数为: " + str(current_shanghai_point * (current_stock_value + result_real) / current_stock_value) + "点")
print("第二阶段起点总持有金额: " + str(result_phase2))

# setting params
total_house_price = 400 * 10000  # 房价总额(RMB)
debt_ratio = 0.65  # 贷款比例
debt_interest_ratio = 0.03  # 贷款年利率
debt_years = 20  # 贷款年限

migration_cost = 100 * 10000
house_other_cost_monthly = 1000 * 5  # 房屋水电气保税（RMB）

car_monthly_cost = 500 * 5
# end of setting params


m_payment = monthly_payment(total_house_price * debt_ratio, debt_interest_ratio, debt_years)

# 贷款买房后，可多出来的投资金额
investment_surplus = final_value - migration_cost - 1000 * 10000 - total_house_price * (1 - debt_ratio)
# 多出来的月度投资收益
inv_return_surplus = investment_surplus * low_risk_investment_return_ratio / 12

print("贷款房子月供：" + str(m_payment) + "；多出来的月度投资收益：" + str(inv_return_surplus))

# 未来加拿大生活年度总收益
total_annual_income = (investment_surplus + 1000 * 10000) * low_risk_investment_return_ratio

cpi_reduse_value = (investment_surplus + 1000 * 10000) * 0.03

total_annual_living_cost_available = total_annual_income - car_monthly_cost * 12 - house_other_cost_monthly * 12\
                                     - m_payment * 12 - cpi_reduse_value

print("未来在加拿大年度可以支付的生活花销：" + str(total_annual_living_cost_available))

# param set history
# 20200731
# ## setting params
# current_stock_value = 680*10000    ## 当前的股票市值
# current_cash = 180*10000    ## 当前现金
# current_shanghai_point = 3300    ## 当前上证大盘指数
# final_value = 1600*10000    ## 最终总金额目标
# low_risk_investment_return_ratio = 0.08
# y1 = 1.5   ## 第一阶段年限
# y2 = 1.5    ## 第二阶段年限

# ## end of setting params
# ## setting params
# total_house_price = 400*10000    ## 房价总额(RMB)
# debt_ratio = 0.65    ## 贷款比例
# debt_interest_ratio = 0.03     ## 贷款年利率
# debt_years = 20    ## 贷款年限

# migration_cost = 100*10000
# house_other_cost_monthly = 1000*5     ## 房屋水电气保税（RMB）

# car_monthly_cost = 500*5
# ## end of setting params
