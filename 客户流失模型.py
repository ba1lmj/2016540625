#导入常用的库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
plt.style.use('ggplot')  #更改设计风格，使用自带的形式进行美化，这是一个r语言的风格
#导入源数据
columns = ['用户ID','购买日期','订单数','订单金额']
df = pd.read_csv("CDNOW_master.txt",names = columns,sep = '\s+')
print(df.head(10))
print(df.describe())
print(df.info())
# 将购买日期列进行数据类型转换
df['购买日期'] = pd.to_datetime(df.购买日期,format = '%Y%m%d') #Y四位数的日期部分，y表示两位数的日期部分
df['月份'] = df.购买日期.values.astype('datetime64[M]')
print(df.head())
print(df.info())
# 解决中文显示参数设置
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 设置图的大小，添加子图
plt.figure(figsize=(15, 12))
# 每月的总销售额
plt.subplot(221)
df.groupby('月份')['订单金额'].sum().plot(fontsize=24)
plt.title('总销售额', fontsize=24)

# 每月的消费次数
plt.subplot(222)
df.groupby('月份')['购买日期'].count().plot(fontsize=24)
plt.title('消费次数', fontsize=24)

# 每月的销量
plt.subplot(223)
df.groupby('月份')['订单数'].sum().plot(fontsize=24)
plt.title('总销量', fontsize=24)

# 每月的消费人数
plt.subplot(224)
df.groupby('月份')['用户ID'].apply(lambda x: len(x.unique())).plot(fontsize=24)
plt.title('消费人数', fontsize=24)
plt.tight_layout()  # 设置子图的间距
plt.show()
# 根据用户id进行分组
group_user = df.groupby('用户ID').sum()
group_user.describe()
#查询条件：订单金额 < 4000
group_user.query('订单金额 < 4000').plot.scatter(x='订单金额',y='订单数')
group_user.订单金额. plot.hist(bins = 20)
#bins = 20,就是分成20块，最高金额是14000，每个项就是700
group_user.query("订单金额< 800")['订单金额'].plot.hist(bins=20)
#每个用户的每次购买时间间隔
order_diff = df.groupby('用户ID').apply(lambda x:x['购买日期'] - x['购买日期'].shift())
order_diff.head(10)
order_diff.describe()
plt.figure(figsize=(15,5))
plt.hist((order_diff / np.timedelta64(1, 'D')).dropna(), bins = 50)
plt.xlabel('消费周期',fontsize=24)
plt.ylabel('频数',fontsize=24)
plt.title('用户消费周期分布图',fontsize=24);
orderdt_min=df.groupby('用户ID').购买日期.min()#第一次消费
orderdt_max=df.groupby('用户ID').购买日期.max()#最后一次消费
(orderdt_max-orderdt_min).head()
(orderdt_max-orderdt_min).mean()
((orderdt_max-orderdt_min)/np.timedelta64(1,'D')).hist(bins=15)
'''因为数据类型是timedelta时间，无法直接作出直方图，所以先换算成数值。换算的方式直接除timedelta函数即可，
np.timedelta64(1, ‘D’)，D表示天，1表示1天，作为单位使用的。因为max-min已经表示为天了，两者相除就是周期'''
#计算所有消费过两次以上的老客的生命周期
life_time = (orderdt_max - orderdt_min).reset_index()
life_time.head()
#用户生命周期分布图
plt.figure(figsize=(10,5))
life_time['life_time'] = life_time.购买日期 / np.timedelta64(1,'D')
life_time[life_time.life_time > 0].life_time.hist(bins = 100, figsize = (12,6))
plt.show()
#去掉0天生命周期的用户之后的用户生命周期的平均值
life_time[life_time.life_time>0].购买日期.mean()
rfm = df.pivot_table(index='用户ID',
                     values=['订单金额', '购买日期', '订单数'],
                     aggfunc={'订单金额': 'sum',
                              '购买日期': 'max',
                              '订单数': 'sum'})
print(rfm.head())

# 日期的最大值与当前日期的差值为R
rfm['R'] = (rfm['购买日期'].max()-rfm['购买日期'])/np.timedelta64(1, 'D')
rfm.rename(columns={'订单金额': 'M','订单数': 'F'},inplace=True)


# 构建rfm模型公式
def get_rfm(x):
    level = x.apply(lambda x: '1' if x >= 0 else '0')
    label = level['R'] + level['F'] + level['M']
    d = {'111': '重要价值客户',
         '011': '重要保持客户',
         '101': '重要挽留客户',
         '001': '重要发展客户',
         '110': '一般价值客户',
         '010': '一般保持客户',
         '100': '一般挽留客户',
         '000': '一般发展客户'}

    result = d[label]
    return result


rfm['label'] = rfm[['R', 'F', 'M']].apply(lambda x: (x - x.mean()) / x.std()).apply(get_rfm, axis=1)
print(rfm.head())
# 求和
rfm.groupby('label').sum()

#将用户消费数据进行数据透视：
#用户活跃程度分层
#将用户消费数据进行数据透视：
df1 = df.pivot_table(index = "用户ID",columns = "月份",values = '购买日期',aggfunc = 'count').fillna(0)
print(df1.head())
df2 = df1.applymap(lambda x:1 if x>0 else 0)
print(df2.tail())


def active_status(data):
    status = []
    for i in range(18):  # 共18个月

        # 若本月没有消费
        if data[i] == 0:
            if len(status) > 0:  # 前面某月消费过，是老客
                if status[i - 1] == 'unreg':  # 前一个月不是首次消费，不是新客
                    status.append('unreg')  # 则本月也不是新客
                else:
                    status.append('unactive')  # 前一个月是首次消费，属于新客，则本月为不活跃用户
            else:
                status.append('unreg')  # 前面某月没有消费过，则本月也不是新客
        # 若本月消费
        else:
            if len(status) == 0:  # 前面没有消费过
                status.append('new')  # 则为新客
            else:  # 前面消费过
                if status[i - 1] == 'unactive':  # 前一个月没有消费，是不活跃用户
                    status.append('return')  # 本月为回流用户
                elif status[i - 1] == 'unreg':  # 前一个月没有消费，不是新客
                    status.append('new')
                else:  # 前一个月是首次消费
                    status.append('active')  # 本月为活跃用户

    return status
#可得到一张不同用户在不同月份的不同状态（new=新、active=活跃、return=回流、unactive=流失）,unreg相当于未注册，指这个用户在这个月及以前从未购买过产品，主要为了统计起来更加方便而加进去。
indexs=df['月份'].sort_values().astype('str').unique()
df3=df2.apply(lambda x:pd.Series(active_status(x),index=indexs),axis=1)
print(df3.head())
#把unreg替换成NaN，再用fillna(0)把空值填为0。然后转置，把月份作为索引行，状态作为列，得到如下的表
df4=df3.replace('unreg',np.NaN).apply(lambda x:pd.value_counts(x)).fillna(0).T
df4
#作出非堆积效果图：
u =df4.reset_index()
labels = u[['active','new','return','unactive']].columns
plt.figure(figsize=(15,5))
plt.stackplot(u['index'].astype(str).apply(lambda x:x[:-3]), u['active'],u['new'],u['return'],u['unactive'], labels=labels)
plt.xlabel('月份')
plt.ylabel('消费人数')
plt.title('每月的消费人数')
plt.legend(loc = 'upper left')
plt.show()
df5=df4.apply(lambda x:x/x.sum(),axis=1)#每一层用户占总用户的比例
print(df5)
a = df.groupby('用户ID')['购买日期'].agg(['min','max']).reset_index()
new_old = (a['min'] == a['max']).value_counts().values
print(new_old)
plt.pie(x = new_old,
       autopct = '%.1f%%',
       shadow = True,
       explode = [0.08,0],
       textprops = {'fontsize' : 11})
plt.axis('equal')
plt.legend(['仅消费一次','多次消费'])
plt.show()
#每个用户在每月的订单数
pivoted_df=df.pivot_table(index='用户ID',columns='月份',values='购买日期',#pivot_table透视表
                       aggfunc='count').fillna(0)#某些用户在某月没有消费过，用nan表示，这里用0填充

print(pivoted_df.head())
#转换：消费2次以上记为1，消费1次记为0，消费0次记为NAN
#applymap针对dataframe所有数据
pivoted_df_transf=pivoted_df.applymap(lambda x: 1 if x>1 else np.nan if x==0 else 0)
pivoted_df_transf.head()
#count统计所有非空数据个数表示总消费用户数，sum计算非0数据的和表示消费两次以上的用户数
df_duplicate =pd.DataFrame(pivoted_df_transf.sum()/pivoted_df_transf.count()).reset_index()
df_duplicate.columns = ['Date', 'DuplicatedRate']
df_duplicate['Date'] = df_duplicate.Date.astype(str).apply(lambda x:x[:-3])

plt.figure(figsize = (15,6))
plt.plot(df_duplicate.Date, df_duplicate.DuplicatedRate)
plt.xlabel('时间', fontsize=24)
plt.ylabel('复购率',fontsize=24)
# plt.ylim(0,1)
plt.title('复购率的变化',fontsize=24)
plt.show()
#回购率
#每个用户每个月平均消费金额
pivoted_money=df.pivot_table(index='用户ID',columns='月份',values='订单金额',
                             aggfunc='mean').fillna(0)

columns_month=df.月份.sort_values().astype('str').unique()
pivoted_money.columns=columns_month
print(pivoted_money.head())
pivoted_purchase=pivoted_money.applymap(lambda x:1 if x>0 else 0)
print(pivoted_purchase.head())
#如果本月进行消费，下月也进行消费，则记为1；如果下月没有消费，则记为0，若本月没有记为消费，则记为nan
def purchase_return(data):
    status=[]
    for i in range(17):#循环17个月
        if data[i]==1:#若本月消费
            if data[i+1]==1:#下个月也消费
                status.append(1)#就记为1
            if data[i+1]==0:#下个月不消费，就记为0
                status.append(0)
        else:
            status.append(np.nan)
    status.append(np.nan)
    return pd.Series(status, index=columns_month)
pivoted_purchase_return = pivoted_purchase.apply(purchase_return,axis=1)#axis=1表示计算方向在行的方向上，左右运算
pivoted_purchase_return.head()
df_purchase = (pivoted_purchase_return.sum() / pivoted_purchase_return.count()).reset_index()
df_purchase.columns = ['Date', 'PurchaseRate']
df_purchase['Date'] = df_purchase.Date.astype(str).apply(lambda x:x[:-3])

plt.figure(figsize = (15,5))
plt.plot(df_purchase.Date, df_purchase.PurchaseRate)
plt.xlabel('时间', fontsize=24)
plt.ylabel('回购率', fontsize=24)
plt.title('回购率的变化', fontsize=24)
plt.show()
#分析留存率
#新建一个对象，并增加用户第一次消费时间的列,merge将两个dataframe合并
data_t=df[['用户ID','购买日期','订单数','订单金额']]
user_purchase_retention=pd.merge(left=data_t,right=orderdt_min.reset_index(),how='inner',on='用户ID',suffixes=('','_min'))
print(user_purchase_retention.head(5))
#axis=1表示计算方向在行的方向上，左右运算
pivoted_purchase_return=pivoted_purchase.apply(purchase_return,axis=1)
pivoted_purchase_return.head()
df_purchase = (pivoted_purchase_return.sum() / pivoted_purchase_return.count()).reset_index()
df_purchase.columns = ['Date', 'PurchaseRate']
df_purchase['Date'] = df_purchase.Date.astype(str).apply(lambda x:x[:-3])

plt.figure(figsize = (15,5))
plt.plot(df_purchase.Date, df_purchase.PurchaseRate)
plt.xlabel('时间', fontsize=24)
plt.ylabel('回购率', fontsize=24)
plt.title('回购率的变化', fontsize=24)
plt.show()
#分析留存率
#新建一个对象，并增加用户第一次消费时间的列,merge将两个dataframe合并
data_t=df[['用户ID','购买日期','订单数','订单金额']]
user_purchase_retention=pd.merge(left=data_t,right=orderdt_min.reset_index(), how='inner',on='用户ID',suffixes=('','_min'))
print(user_purchase_retention.head(5))
#每一次消费时间与第一次消费时间间隔
user_purchase_retention['order_date_diff']=user_purchase_retention['购买日期']-user_purchase_retention['购买日期_min']
#将timedelta转换为数值型
user_purchase_retention['date_diff']=user_purchase_retention.order_date_diff.apply(lambda x:x/np.timedelta64(1,'D'))
user_purchase_retention.head(5)
#将时间间隔分桶（0-3）（3-7）等
bin=[0,3,7,15,30,60,90,180,365]
user_purchase_retention['date_diff_bin']=pd.cut(user_purchase_retention.date_diff,bins=bin)
user_purchase_retention.head(10)
#用户第一次消费之后，后续各时间段的消费总额
pivoted_retention=user_purchase_retention.pivot_table(index='用户ID',
columns='date_diff_bin',values='订单金额',aggfunc=sum,dropna=False)
pivoted_retention.head()
#1代表有消费，0代表没有
pivoted_retention_trans=pivoted_retention.applymap(lambda x:1 if x>0 else 0)
print(pivoted_retention_trans)
#每笔订单离第一笔订单的时间间隔
(pivoted_retention_trans.sum()/pivoted_retention_trans.count()).plot.bar(figsize=(10,5))
plt.xlabel('消费时间间隔')
plt.title('留存率')
plt.show()
#先将用户消费金额按升序排列，逐行计算用户累计金额，最后一行是总消费金额
user_money=df.groupby('用户ID').订单金额.sum().sort_values().reset_index()
user_money['money_cumsum']=user_money.订单金额.cumsum()
money_total=user_money.money_cumsum.max()
#转行成百分比
user_money['prop']=user_money.apply(lambda x:x.money_cumsum/money_total,axis=1)#apply用在每个行上
user_money.tail()
user_money.prop.plot()
plt.xlabel('用户ID', fontsize=24)
plt.ylabel('比率', fontsize=24)
plt.title('用户累计销售额贡献比', fontsize=24)
plt.show()
#先将用户销量按升序排列，逐行计算用户累计销量，最后一行是总销量
user_productsSum=df.groupby('用户ID').订单数.sum().sort_values().reset_index()
user_productsSum['products_cumsum']=user_productsSum.订单数.cumsum()
productsSum_total=user_productsSum.products_cumsum.max()
#转行成百分比
user_productsSum['prop']=user_productsSum.apply(lambda x:x.products_cumsum/productsSum_total,axis=1)#apply用在每个行
print(user_productsSum)