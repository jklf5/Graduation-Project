# -*- coding: utf-8 -*-
"""
常用函数:
log_rets:求差分
merge_SHci:合并股票数据
plot_polyfit:绘制拟合线
plot_text:绘制给定坐标的文本标签
find_not_safe:找出不安全的股票
count_save_not_safe:计数并保存不安全的股票
find_not_safe_skews_kurts:找出偏度和峰度过于离群的股票
open_not_safe_txt:读取不安全股票文件
write_not_safe_txt:向不安全股票文件写入
delete_not_safe:删除股票列表中不安全的股票
mimic_seaborn:模仿seaborn风格
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import infoClass
import os
import matplotlib as mpl
from pandas_datareader import data
from datetime import datetime

zh_font = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')

def get_historical_data(symbol, start=None, end=None):
    return data.get_data_yahoo(symbol, start=start, end=end)

def log_rets(close):
    # return np.log(close / close.shift(1))
    return np.diff(np.log(close))  # diff计算沿给定轴的第n个离散差分

def merge_SHci(stock, SHci):
    return pd.merge(left=stock, right=SHci,
                    right_index=True, left_index=True,
                    suffixes=('_stock', '_SHci')).dropna()  # dropna：滤除缺失数据

# def grid_list(arr):
#     ''' Creates a 2D cartesian product grid from an array:

#     >>> from dautil import collect
#     >>>  arr = list(range(2))
#     >>> arr
#     [0, 1]
#     >>> collect.grid_list(arr)
#     [[(0, 0), (0, 1)], [(1, 0), (1, 1)]]


#     :param arr: A 1-d array-like list.

#     :returns: A 2-d list containing tuples as elements.
#     '''
#     dim = len(arr)
#     grid = GridList(dim, dim, 0).grid

#     for i in range(dim):
#         for j in range(dim):
#             grid[i][j] = (arr[i], arr[j])

#     return grid

def plot_polyfit(ax, x, y, degree=1, plot_points=False):
    '''
    绘制一条拟合线
    ax:坐标区域对象
    x:一组x坐标值
    y:一组y坐标值
    degree:自由度
    plot_points:是否绘制图
    poly1d:生成多项式对象
    polyval:计算多项式的函数值
    '''
    poly = np.polyfit(x, y, degree)
    print(np.poly1d(poly))
    ax.plot(x, np.polyval(poly, x), label='Fit')

    if plot_points:
        ax.plot(x, y, 'o')
    return np.poly1d(poly)

def plot_text(ax, xcoords, ycoords, point_labels, add_scatter=False,
              *args, **kwargs):
    '''
    绘制给定坐标的文本标签
    ax:坐标区域对象
    xcoords:类似于数组的X轴坐标
    ycoords:类似于数组的y轴坐标
    point_labels:放在图表上的文本标签
    add_scatter:是否有要插入散点图
    '''
    if add_scatter:
        ax.scatter(xcoords, ycoords)

    for x, y, txt in zip(xcoords, ycoords, point_labels):
        ax.text(x, y, txt, *args, **kwargs, fontproperties=zh_font, fontsize=12.5)


def find_not_safe(x, y, z, stocks):
    '''
    找出不安全的股票
    x:x轴坐标
    y:y轴坐标
    z:拟合线对象
    stocks:股票列表
    '''
    not_safe_find = []
    for each in range(len(x)):
        # print(z(x[each]))
        if(z(x[each])>y[each]):
            not_safe_find.append(stocks[each])
    print("不安全的股票如下：")
    print(not_safe_find)
    count_save_not_safe(not_safe_find)
    

def count_save_not_safe(not_safe_find):
    '''
    计数并保存不安全的股票
    not_safe_find:用find_not_safe函数找出的不安全的股票列表
    '''
    not_safe = open_not_safe_txt()
    if not not_safe:
        for each in not_safe_find:
            temp = []
            temp.append(each)
            temp.append('1')
            not_safe.append(temp)
        write_not_safe_txt(not_safe)
    else:
        for each_not_safe in not_safe_find:
            count = 0
            for each_not_safe_intxt in not_safe: 
                if(each_not_safe in each_not_safe_intxt):
                    count += 1
                    index_intxt = not_safe.index(each_not_safe_intxt)
                    break
            if(count == 0):
                temp = []
                temp.append(each_not_safe)
                temp.append('1')
                not_safe.append(temp)
            else:
                not_safe[index_intxt][1] += '1'
        # print(not_safe)
        write_not_safe_txt(not_safe)

def find_not_safe_skews_kurts(skews, kurts, stocks):
    '''
    找出偏度和峰度过于离群的股票
    skews:偏度值
    kurts:峰度值
    stocks:股票列表
    '''
    not_safe_skews_kurts = []
    std_skews = np.std(skews)
    std_kurts = np.std(kurts)
    for each in range(len(skews)):
        # print(abs(skews[each]/std_skews))
        # print(abs(kurts[each]/std_kurts))
        if(abs(skews[each]/std_skews) > 1.96 or abs(kurts[each]/std_kurts)>1.96):
        # if(abs(float(skews[each])-0) >= 0.15 or abs(float(kurts[each])-0) > 2.5):
            # if(abs(float(kurts[each])-0) > 2.6):
            not_safe_skews_kurts.append(stocks[each])
    print(not_safe_skews_kurts)
    count_save_not_safe(not_safe_skews_kurts)

def open_not_safe_txt():
    '''
    读取不安全股票文件
    '''
    if not os.path.exists('not_safe.txt'):
        temp = open('./not_safe.txt', 'w')
        temp.close()
    with open('./not_safe.txt', 'r') as f:
        lis = []
        for line in f.readlines():
            line = line.strip('\n')
            b = line.split(' ')
            lis.append(b)
    # print(lis)
    return lis

def write_not_safe_txt(not_safe):
    '''
    向不安全股票文件写入
    '''
    with open('./not_safe.txt', 'w') as f:
        for each_row in not_safe:
            for each_col in each_row:
                f.write(str(each_col))
                f.write(' ')
            f.write('\n')

def delete_not_safe(stocks, stocks_zh):
    '''
    删除股票列表中不安全的股票
    stocks:股票列表
    stocks_zh:股票中文列表
    '''
    with open('./not_safe.txt', 'r') as f:
        lis = []
        for line in f.readlines():
            line = line.strip('\n')
            b = line.split(' ')
            lis.append(b)
    # print(lis)
    # for each_not_safe_intxt in lis:
    #     if(each_not_safe_intxt[1] != '1'):
    #         for each_stock in stocks:
    #             if(each_stock in each_not_safe_intxt):
    #                 index_stock = stocks.index(each_stock)
    #                 stocks.remove(each_stock)
    #                 stocks_zh.pop(index_stock)
    #                 break
    for each_not_safe_intxt in lis:
        index_stock = stocks.index(each_not_safe_intxt[0])
        stocks.remove(each_not_safe_intxt[0])
        stocks_zh.pop(index_stock)
        
    print(stocks, stocks_zh)

def mimic_seaborn():
    """ 模仿Seaborn风格 """
    sns_style = {'axes.axisbelow': True,
                 'axes.edgecolor': 'white',
                 'axes.facecolor': '#EAEAF2',
                 'axes.grid': True,
                 'axes.labelcolor': '.15',
                 'axes.linewidth': 0,
                 'font.family': 'Arial',
                 # deviating
                 'grid.color': 'yellow',
                 'grid.linestyle': '-',
                 # deviating
                 'grid.linewidth': 2,
                 'image.cmap': 'Greys',
                 'legend.frameon': False,
                 'legend.numpoints': 1,
                 'legend.scatterpoints': 1,
                 'lines.solid_capstyle': 'round',
                 'pdf.fonttype': 42,
                 'text.color': '.15',
                 'xtick.color': '.15',
                 'xtick.direction': 'out',
                 'xtick.major.size': 0,
                 'xtick.minor.size': 0,
                 'ytick.color': '.15',
                 'ytick.direction': 'out',
                 'ytick.major.size': 0,
                 'ytick.minor.size': 0}
    mpl.rcParams.update(sns_style)