# -*- coding: utf-8 -*-
"""
使用资本资产定价模型（CAPM）找出低于市场安全线的股票
"""

# 导入库
import dautil as dl
import numpy as np
import pandas as pd
import infoClass
import functionClass as fc
import matplotlib.pyplot as plt
import matplotlib as mpl
from pandas_datareader import data
from datetime import datetime

start = datetime(2018,1,1,0,0,0,0)
end = datetime(2019,5,11,0,0,0,0)

def calc_beta(symbol):
    
    # ohlc = dl.data.OHLC()# 生成数据获取对象
    # SHci = ohlc.get('000001.ss')['Adj Close']# 获取市场数据
    # stock = ohlc.get(symbol)['Adj Close']# 获取股票数据
    SHci = data.get_data_yahoo('000001.ss', start=start, end=end)['Adj Close']
    stock = data.get_data_yahoo(symbol, start=start, end=end)['Adj Close']
    df = pd.DataFrame({'SHci': SHci, symbol: stock}).dropna()# 将股票数据与市场数据结合
    SHci_rets = fc.log_rets(df['SHci'])# 计算市场对数收益率
    rets = fc.log_rets(df[symbol])# 计算股票对数收益率
    beta, _ = np.polyfit(SHci_rets, rets, 1)# 拟合beta系数
    print(symbol)
    # annualize & percentify
    return beta, 250 * rets.mean() * 100 # 返回beta系数，年化收益率

# print(data.get_data_yahoo('000001.ss'))

zh_font = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc') # 设置图中输出的字体为中文
# 计算beta和股票的平均收益
betas = []
means = []

for symbol in infoClass.STOCKS:
    beta, ret_mean = calc_beta(symbol)
    betas.append(beta)
    means.append(ret_mean)
#构建输出样式
dfb = dl.report.DFBuilder(cols=['ZH', 'Ticker', 'Beta', 'Mean'])

for symbol in infoClass.STOCKS:
    index = infoClass.STOCKS.index(symbol)
    symbol_zh = infoClass.STOCKS_ZH[index]
    beta = betas[infoClass.STOCKS.index(symbol)]
    mean = means[infoClass.STOCKS.index(symbol)]
    dfb.row([symbol_zh, symbol, beta, mean])

df = dfb.build(index=infoClass.STOCKS)
print(df)

# 绘制结果和市场安全线
# %matplotlib inline
fc.mimic_seaborn()
_, ax = plt.subplots()
z = fc.plot_polyfit(ax, betas, means)
fc.plot_text(ax, betas, means, zip(infoClass.STOCKS, infoClass.STOCKS_ZH), add_scatter=True)# zip(infoClass.STOCKS, infoClass.STOCKS_ZH)
ax.set_title('资本资产定价模型', fontproperties=zh_font, fontsize=15)
ax.set_xlabel('Beta', fontsize=14)
ax.set_ylabel('平均年化收益率（%）', fontproperties=zh_font, fontsize=14)
fc.find_not_safe(betas, means, z, infoClass.STOCKS)
plt.show()