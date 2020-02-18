# -*- coding: utf-8 -*-
"""
检测数据正态性
"""

# 导入库
import dautil as dl
import infoClass
import functionClass as fc
import matplotlib.pyplot as plt
from scipy.stats import skew
from scipy.stats import kurtosis
from pandas.tools.plotting import autocorrelation_plot
import numpy as np
from scipy.stats import norm
from IPython.display import HTML
import matplotlib as mpl
from datetime import datetime

zh_font = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
# 计算股票收益
ohlc = dl.data.OHLC()
rets_dict = {}
start = datetime(2018,12,1,0,0,0,0)
end = datetime(2019,5,11,0,0,0,0)

for i, symbol in enumerate(infoClass.STOCKS):
    print(symbol)
    rets = fc.log_rets(fc.get_historical_data(symbol, start=start, end=end)['Adj Close'])
    rets_dict[symbol] = rets

# SHci = fc.log_rets(ohlc.get('000001.ss')['Adj Close'])

# 计算收益的偏度和峰度
skews = [skew(rets_dict[s]) for s in infoClass.STOCKS]
kurts = [kurtosis(rets_dict[s]) for s in infoClass.STOCKS]

std_skews = np.std(skews)
std_kurts = np.std(kurts)
print(std_skews)
print(std_kurts)
#构建输出样式
dfb = dl.report.DFBuilder(cols=['ZH', 'Ticker', 'Skew/std', 'Kurt/std'])

for symbol in infoClass.STOCKS:
    index = infoClass.STOCKS.index(symbol)
    symbol_zh = infoClass.STOCKS_ZH[index]
    skew = skews[infoClass.STOCKS.index(symbol)]/std_skews
    kurt = kurts[infoClass.STOCKS.index(symbol)]/std_kurts
    dfb.row([symbol_zh, symbol, skew, kurt])

df = dfb.build(index=infoClass.STOCKS)
print(df)

# 绘制收益的偏度和峰度
fc.mimic_seaborn()
_, ax = plt.subplots()
ax.scatter(skews, kurts)
fc.plot_text(ax, skews, kurts, zip(infoClass.STOCKS, infoClass.STOCKS_ZH))# zip(infoClass.STOCKS, infoClass.STOCKS_ZH)
ax.set_xlabel('Skew 偏度', fontproperties=zh_font, fontsize=15)
ax.set_ylabel('Kurtosis 峰度', fontproperties=zh_font, fontsize=15)
ax.set_title('收益的偏度和峰度', fontproperties=zh_font, fontsize=15)
fc.find_not_safe_skews_kurts(skews, kurts, infoClass.STOCKS)
plt.show()