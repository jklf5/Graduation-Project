# -*- coding: utf-8 -*-
"""
绘制筛选后各股票与上证指数的对数收益率的对比图
"""
import matplotlib.pyplot as plt
from datetime import datetime
import functionClass as fc
import infoClass
from pandas_datareader import data
import matplotlib as mpl
import numpy as np
import pandas as pd
import dautil as dl

start = datetime(2018, 1, 1, 0, 0, 0, 0)
end = datetime(2019, 5, 11, 0, 0, 0, 0)

fc.delete_not_safe(infoClass.STOCKS, infoClass.STOCKS_ZH)
zh_font = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
SHci = data.get_data_yahoo('000001.ss', start=start, end=end)['Adj Close']

fc.mimic_seaborn()
# dl.options.mimic_seaborn()
for i in range(len(infoClass.STOCKS)):
    print(infoClass.STOCKS[i])
    length = len(infoClass.STOCKS)
    plt.subplot(length/2, 2, i+1)# 子图的个数，注意筛选后股票的个数
    get_temp = data.get_data_yahoo(infoClass.STOCKS[i], start=start, end=end)['Adj Close']
    plt.plot(SHci.index[1:], np.diff(np.log(get_temp)), label=infoClass.STOCKS[i])
    plt.plot(SHci.index[1:], np.diff(np.log(SHci)), label='000001')
    plt.title(infoClass.STOCKS[i])
    plt.xlabel('Date')
    plt.ylabel('Return')
    plt.legend(loc='best')

# plt.legend()
plt.subplots_adjust(wspace=0.5,hspace=1)# 调整小分图之间的间距
plt.show()