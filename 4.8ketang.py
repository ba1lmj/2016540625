import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tushare as ts
from pylab import  mpl

stocks={'上证指数':'sh','深证指数':'sz','沪深300':'hs300','上证50':'sz50','中小指数':'zxb','创业板':'cyb'}

def return_risk(stocks,startdate='2006-1-1'):#算股票风险
    close=pd.DataFrame()
    for stock in stocks.values():
        close[stock]=ts.get_k_data(stock,ktype='D',autype='qfq',start=startdate)['close']#新建一列stock存放每个股票的收盘价close
    tech_rets=close.pct_change()[1:]   #算收益
    rets=tech_rets.dropna()#去掉空值 数据清洗，避免存在空值，使计算结果不准确
    ret_mean=rets.mean()*100#算平均值
    ret_std=rets.std()*100#算标准差
    return  ret_mean,ret_std

def plot_return_risk():#风险可视化
    ret,vol=return_risk(stocks)
    color=np.array([0.18,0.96,0.75,0.3,0.9,0.5])   #自定义的颜色
    plt.scatter(ret,vol,marker='o',c=color,s=500,cmap=plt.get_cmap('Spectral'))
    plt.xlabel('日收益率均值%')
    plt.ylabel('标准差%')
    for label,x,y in zip(stocks.keys(),ret,vol):
        plt.annotate(label,xy=(x,y),xytext=(20,20),textcoords='offset points',ha='right',va="bottom",bbox=dict(boxstyle=
        'round,pad=0.5',fc='yellow',alpha=0.5),arrowprops=dict(arrowstyle="->",connectionstyle='arc3,rad=0'))#在图里面标注注释
stocks = {'上证指数': 'sh', '深证指数': 'sz', '沪深300': 'hs300', '上证50': 'sz50', '中小指数': 'zxb', '创业板': 'cyb'}
plot_return_risk()

stocks={'中国平安':"601318",'格力空调':"000651","徐工机械":"000425","招商银行":"600036","恒生电子":"600570","贵州茅台":"600519"}
startdate="2018-1-1"
plot_return_risk()
