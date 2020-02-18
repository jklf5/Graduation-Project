# -*- coding: utf-8 -*-
"""
基本面分析筛选
"""
import pandas as pd
import numpy as np
from datetime import datetime

def fundamental_analysis():
        data = pd.read_excel('stocks_fundamental.xlsx')
        df = pd.DataFrame(data)
        # NPGR：净利润同比增长率
        # ROE：净资产收益率
        # OIGR：营业收入增长率
        select = df.loc[(df.ROE2015_1>0) & (df.ROE2015_2>0) & (df.ROE2015_3>0) & (df.ROE2015_4>10)
                & (df.ROE2016_1>0) & (df.ROE2016_2>0) & (df.ROE2016_3>0) & (df.ROE2016_4>10)
                & (df.ROE2017_1>0) & (df.ROE2017_2>0) & (df.ROE2017_3>0) & (df.ROE2017_4>10)
                & (df.ROE2018_1>0) & (df.ROE2018_2>0) & (df.ROE2018_3>0) & (df.ROE2018_4>10)
                & (df.NPGR2015_1>0) & (df.NPGR2015_2>0) & (df.NPGR2015_3>0) & (df.NPGR2015_4>10)
                & (df.NPGR2016_1>0) & (df.NPGR2016_2>0) & (df.NPGR2016_3>0) & (df.NPGR2016_4>10)
                & (df.NPGR2017_1>0) & (df.NPGR2017_2>0) & (df.NPGR2017_3>0) & (df.NPGR2017_4>10)
                & (df.NPGR2018_1>0) & (df.NPGR2018_2>0) & (df.NPGR2018_3>0) & (df.NPGR2018_4>10)
                & (df.OIGR2015_1>0) & (df.OIGR2015_2>0) & (df.OIGR2015_3>0) & (df.OIGR2015_4>10)
                & (df.OIGR2016_1>0) & (df.OIGR2016_2>0) & (df.OIGR2016_3>0) & (df.OIGR2016_4>10)
                & (df.OIGR2017_1>0) & (df.OIGR2017_2>0) & (df.OIGR2017_3>0) & (df.OIGR2017_4>10)
                & (df.OIGR2018_1>0) & (df.OIGR2018_2>0) & (df.OIGR2018_3>0) & (df.OIGR2018_4>10)
                & (df.ListingDate<datetime(2015,1,1)) & (df.ROE_CV<0.5)]
        return select['SecuritiesCode'].tolist(), select['SecuritiesShortName'].tolist()
