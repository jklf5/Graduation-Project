# -*- coding: utf-8 -*-
"""
提供STOCKS类存放各股票信息
"""
import numpy as np
import pandas as pd
import fundamental_analysis as fa

'''
按照净资产收益率年均>10%,净利润增长率年均>10%,营业收入增长率年均>10%挑选出A股所有符合要求的股票如下:
1.	000418.SZ	小天鹅A
2.	000568.SZ	泸州老窖
3.	002126.SZ	银轮股份
4.	002223.SZ	鱼跃医疗
5.	002372.SZ	伟星新材
6.	002677.SZ	浙江美大
7.	002717.SZ	岭南股份
8.	300003.SZ	乐普医疗
9.	300015.SZ	爱尔眼科
10.	300136.SZ	信维通信
11.	300207.SZ	欣旺达
12.	300244.SZ	迪安诊断
13.	600276.SS	恒瑞医药
14.	600340.SS	华夏幸福
15.	600419.SS	天润乳业
16.	603288.SS	海天味业
17.	603368.SS	柳药股份

'''
STOCKS_static, STOCKS_ZH_static = fa.fundamental_analysis()
STOCKS_static = [each.replace('SH', 'SS') for each in STOCKS_static]

STOCKS = STOCKS_static
STOCKS_ZH = STOCKS_ZH_static
print(STOCKS, STOCKS_ZH)
