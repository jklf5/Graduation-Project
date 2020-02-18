# -*- coding: utf-8 -*-
"""
使用最小方差为指标构建投资组合模型
"""
import dautil as dl
import infoClass
import functionClass as fc
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf
import matplotlib as mpl
from pandas_datareader import data
from datetime import datetime

start = datetime(2018,1,1,0,0,0,0)
end = datetime(2019,5,11,0,0,0,0)

# 定义函数计算投资组合收益的方差
def variance_return(stocka, stockb, stds):
    ohlc = dl.data.OHLC()
    dfa = data.get_data_yahoo(stockb, start=start, end=end)
    dfb = data.get_data_yahoo(stockb, start=start, end=end)
    #dfa = ohlc.get(stocka)
    #dfb = ohlc.get(stockb)
    merged = pd.merge(left=dfa, right=dfb,
                      right_index=True, left_index=True,
                      suffixes=('_A', '_B')).dropna()
    retsa = fc.log_rets(merged['Adj Close_A'])
    retsb = fc.log_rets(merged['Adj Close_B'])
    corr = np.corrcoef(retsa, retsb)[0][1]
    return 0.25 * (stds[stocka] ** 2 + stds[stockb] ** 2 +
                   2 * stds[stocka] * stds[stockb] * corr)

# 定义函数计算方差
def calc_combination_std(stocka, stockb, stds, ratios):
    if stocka == stockb:
        # return 0
        return np.nan

    key = stocka + '_' + stockb
    ratio = ratios.get(key, None)

    if ratio:
        return ratio

    var = variance_return(stocka, stockb, stds)
    ratios[key] = var
    return var

fc.delete_not_safe(infoClass.STOCKS, infoClass.STOCKS_ZH)
zh_font = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
# 为每一只股票计算平均收益和标准偏差
stds = {}

ohlc = dl.data.OHLC()

for stock in infoClass.STOCKS:
    print(stock)
    close = data.get_data_yahoo(stock, start=start, end=end)['Adj Close']
    # close = ohlc.get(stock)['Adj Close']
    rets = fc.log_rets(close)
    stds[stock] = rets.std()
# 计算所有股票的所有组合的网格比率
pairs = dl.collect.grid_list(infoClass.STOCKS)
sorted_pairs = [[sorted(row[i]) for row in pairs]
                for i in range(len(infoClass.STOCKS))]
ratios = {}

# grid = []
# for i in range(len(infoClass.STOCKS)):
#     temp = []
#     for row in sorted_pairs:
#         ratio = calc_ratio(row[i][0], row[i][1], means, stds, ratios)
#         temp.append(ratio)
#     grid.append(temp)

grid = [[calc_combination_std(row[i][0], row[i][1], stds, ratios)
         for row in sorted_pairs] for i in range(len(infoClass.STOCKS))]
print(grid)

# 使用tensorflow求最大值及每行最大值索引
with tf.Session() as sess:
    grid_tensor = tf.convert_to_tensor(grid)
    print(sess.run(grid_tensor))
    minmun = tf.reduce_min(grid_tensor)
    # minnum = tf.reduce_min(grid_tensor)
    print(sess.run(minmun))
    min_index_tensor = tf.argmin(grid_tensor)
    print(sess.run(min_index_tensor))
    # min_index_tensor = tf.argmin(grid_tensor)
    min_index = min_index_tensor.eval()

min_num = grid[0][1]
min_index_x = 0
min_index_y = 1
for i in range(len(grid)):
    for j in min_index:
        if(min_num > grid[i][j]):
            min_num = grid[i][j]
            min_index_x = i
            min_index_y = j
print(infoClass.STOCKS[min_index_x], infoClass.STOCKS_ZH[min_index_x])
print(infoClass.STOCKS[min_index_y], infoClass.STOCKS_ZH[min_index_y])

# 在热图中绘制网格
# %matplotlib inline
plt.title('等权重双资产投资组合（最小方差）', fontproperties=zh_font, fontsize=15)
sns.heatmap(grid, annot=True, cmap='YlGnBu', linewidths=0.3, annot_kws={"size":10}, xticklabels=infoClass.STOCKS, yticklabels=infoClass.STOCKS)
plt.show()