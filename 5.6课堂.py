import pandas_datareader as pdr
import datetime
import numpy as np
import pandas as pd

aapl = pdr.get_data_yahoo('AAPL', start=datetime.datetime(2006, 10, 1), end=datetime.datetime(2012, 1, 1))
print(aapl.head())
# 将aapl数据框中`Adj Close`列已调整收盘价数据赋值给变量`daily_close`
daily_close = aapl[['Adj Close']]#Adj Close已调整收盘价
# 计算每日收益率
daily_pct_change = daily_close.pct_change()
# 用0填补缺失值NA
daily_pct_change.fillna(0, inplace=True)
# 查看每日收益率的前几行
print(daily_pct_change.head())
# 计算每日对数收益率
daily_log_returns = np.log(daily_close.pct_change()+1)
# 查看每日对数收益率的前几行print(daily_log_returns.head())
# 按营业月对 `aapl` 数据进行重采样，取每月最后一项
monthly = aapl.resample('BM').apply(lambda x: x[-1])
# 计算每月的百分比变化，并输出前几行print(monthly.pct_change().head())
# 按季度对`aapl`数据进行重采样，将均值最为每季度的数值
quarter = aapl.resample("3M").mean()
# 计算每季度的百分比变化，并输出前几行print(quarter.pct_change().head())
# 导入 matplotlib
import matplotlib.pyplot as plt
# 绘制直方图
daily_pct_change.hist(bins=50)
# 显示图
plt.show()
# 输出daily_pct_change的统计摘要
print(daily_pct_change.describe())
# 计算累积日收益率
cum_daily_return = (1 + daily_pct_change).cumprod()# 输出 `cum_daily_return` 的前几行
print(cum_daily_return.head())
# 绘制累积日收益率曲线
cum_daily_return.plot(figsize=(12,8))
# 显示绘图
plt.show()