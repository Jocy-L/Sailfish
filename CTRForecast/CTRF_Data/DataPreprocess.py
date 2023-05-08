# File content:
# Usage:

#coding=utf-8
import numpy as np
import pandas as pd
from sklearn import preprocessing

path = 'C:/Users/11/Documents/WXWork/1688855519447112/Cache/File/2023-04/关键词427.csv'
# if encoding=’utf-8’ wrong try encoding=GB2312/gbk/ISO-8859-1
df = pd.read_csv(path, low_memory=False, encoding='gbk')
# Cut the columns of data that need to be processed
t = df.iloc[:, 8:]

columns = {
    '展现': 'MM_Manual_show',
    '点击': 'MM_Manual_click',
    '消费': 'MM_Manual_spend',
    '点击率': 'MM_Manual_CTR',
    '平均点击价格': 'MM_Manual_avg_click_price',
    '上方位平均排名': 'MM_Manual_avg_top_No.',
    '上方位展现': 'MM_Manual_show_top',
    '上方位点击': 'MM_Manual_top_click',
    '上方位消费': 'MM_Manual_top_spend',
    '上方展现胜出率': 'MM_Manual_top_win_rate',
    '上方展现胜出率(精确)': 'MM_Manual_top_win_rate_exact',

    0: 'MM_Manual_show',
    1: 'MM_Manual_click',
    2: 'MM_Manual_spend',
    3: 'MM_Manual_CTR',
    4: 'MM_Manual_avg_click_price',
    5: 'MM_Manual_avg_top_No.',
    6: 'MM_Manual_show_top',
    7: 'MM_Manual_top_click',
    8: 'MM_Manual_top_spend',
    9: 'MM_Manual_top_win_rate',
    10: 'MM_Manual_top_win_rate_exact'
}

# Three standardized ways
# ----- min-max -----
MM_Manual = (t - t.min()) / (t.max() - t.min())
MM_Manual.rename(columns=columns, inplace=True)

MM_Auto = preprocessing.minmax_scale(t)
MM_Auto_arry_to_data = pd.DataFrame(MM_Auto)
MM_Auto_arry_to_data.rename(columns=columns, inplace=True)


# ----- Z-score -----
ZS_Manual = (t - t.mean()) / (t.std())
ZS_Auto = preprocessing.scale(t)


# ----- Decimal calibration normalization [-1,1] -----
TT = t / 10 ** np.ceil(np.log10(t.abs().max()))
TT.rename(columns=columns, inplace=True)


# Stitch table data
# mix_data = pd.concat([df, MM_Manual], axis=1)
# mix_data = pd.concat([df, MM_Auto_arry_to_data], axis=1)
# mix_data = pd.concat([df, ZS_Manual], axis=1)
# mix_data = pd.concat([df, ZS_Auto], axis=1)
mix_data = pd.concat([df, TT], axis=1)
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)
print(mix_data)