import tushare as ts
import matplotlib.pyplot as plt
import seaborn as sns
df_st = ts.get_h_data('002337')
print(df_st)
df_st.to_csv('d:/123.csv', encoding='utf-8-sig')
stock1 = ts.get_k_data()
