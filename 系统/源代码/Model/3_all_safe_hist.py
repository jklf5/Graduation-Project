# -*- coding: utf-8 -*-
"""
筛选后的股票的收益直方图以及各股票收益总和条形图
"""

from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas_datareader import data
import functionClass as fc
import infoClass
import matplotlib as mpl
import scipy.stats as scs
import dautil as dl

fc.delete_not_safe(infoClass.STOCKS, infoClass.STOCKS_ZH)
infoClass.STOCKS.append('000001.ss')
zh_font = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')

all_data = pd.DataFrame()
start = datetime(2018, 1, 1, 0, 0, 0, 0)
end = datetime(2019, 5, 11, 0, 0, 0, 0)
for symbol in infoClass.STOCKS:
    print(symbol)
    all_data[symbol] = data.get_data_yahoo(symbol, start=start, end=end)['Adj Close']

all_data.dropna()
# 计算对数收益率
# log_returns = np.log(all_data)
# log_returns = log_returns.diff()
log_returns = np.log(all_data / all_data.shift(1))
# print(log_returns)
# 计算收益总和
all_sum = []
for symbol in infoClass.STOCKS:
    temp = log_returns[symbol].tolist()
    retssum = 0
    temp.pop(0)
    retssum = sum(temp)
    all_sum.append(retssum)
print(all_sum)
# 绘制直方图
dl.options.mimic_seaborn()
plt.xlim(-0.1, 0.1)
log_returns.hist(bins=50, figsize=(9,6))
plt.subplots_adjust(wspace=0.3, hspace=0.6)# 调整小分图之间的间距
plt.show()

# 绘制条形图
ax = plt.figure()
plt.barh(infoClass.STOCKS, all_sum)
plt.title('股票收益率总和对比', fontproperties=zh_font, fontsize=15)
plt.xlabel('收益率总和', fontproperties=zh_font, fontsize=14)
plt.ylabel('证券代码', fontproperties=zh_font, fontsize=14)
plt.show()
